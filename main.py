import asyncio
from typing import Set, Dict, Sequence
from typing import Optional
from collections import defaultdict

import evdev
from evdev import ecodes

from config.sn30 import BTN_MAPPING, ABS_HAT_MAPPING, DEVICE_NAME, VENDOR_ID, PRODUCT_ID, INVALID_HAT_VALUE

def map_value_to_name(value: int | Sequence[int]) -> str:
    """
    Maps an integer evdev event code or a sequence of codes to their symbolic names.
    """
    if isinstance(value, int):
        value = [value] # Ensure it's always a list for consistent processing

    mapped_names = []
    for code in value:
        # Iterate through all ecodes.items() to find the name corresponding to the code
        found_name = None
        for name, code_value in ecodes.ecodes.items():
            if not (name.startswith("KEY") or name.startswith("BTN")):
                continue
            if code == code_value :
                found_name = name
                break # Found the name, exit inner loop
        if found_name:
            mapped_names.append(found_name)
        else:
            mapped_names.append(f"UNKNOWN_CODE({code})") # Handle unknown codes

    return "+".join(mapped_names)


def collect_target_events():
    mapped_events: Set[int] = set()
    def collect(e_list):
        mapped_events = set()
        if isinstance(e_list, int):
            e_list = [e_list]
        for e in e_list:
            mapped_events.add(e)
        return mapped_events
    for e_list in BTN_MAPPING.values():
        mapped_events.union(collect(e_list))
    for e_list_list in ABS_HAT_MAPPING.values():
        for e_list in e_list_list.values():
            mapped_events.union(collect(e_list))
    return list(mapped_events)

class Mapper:
    def __init__(self):
        events: Dict[int,Sequence[int]] = {
            ecodes.EV_KEY: collect_target_events()
        }
        self.ui = evdev.UInput(
            events=events,
            name='virtual-keyboard',
            vendor=0x1234,  # Example vendor ID
            product=0x5678, # Example product ID
            version=0x0001)
        self.ui = evdev.UInput()
        self.btn_mapping = BTN_MAPPING
        self.abs_mapping = ABS_HAT_MAPPING
        self.abs_hat_pos = dict(zip(
            ABS_HAT_MAPPING.keys(), 
            [INVALID_HAT_VALUE] * len(ABS_HAT_MAPPING.keys())
        ))


    def send_keystroke(self, btn_code, value:int, active=True):
        if btn_code in self.btn_mapping:
            mapped_events: int | Sequence[int] = self.btn_mapping[btn_code]
        elif btn_code in self.abs_mapping:
            if value not in self.abs_mapping[btn_code] and self.abs_hat_pos[btn_code] != INVALID_HAT_VALUE:
                value = self.abs_hat_pos[btn_code]
                active = False
            else:
                self.abs_hat_pos[btn_code] = value
            mapped_events: int | Sequence[int] = self.abs_mapping[btn_code][value]
        else:
            mapped_events = []
        if mapped_events:
            print(f"{'sending' if active else 'releasing'} {map_value_to_name(mapped_events)} to uinput")
        if isinstance(mapped_events, int):
            mapped_events = [mapped_events]
        assert len(mapped_events) < 5, f"as a safety check len(mapped_events) < 5"
        if active:
            for event in mapped_events:
                self.ui.write(ecodes.EV_KEY, event, 1)  # key down
        else:
            for event in reversed(mapped_events):
                self.ui.write(ecodes.EV_KEY, event, 0)  # key up
        self.ui.syn()
    def close(self):
        self.ui.close()

def find_device(product_id, vendor_id, name) -> Optional[evdev.InputDevice]:
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        eq = [
            device.info.vendor == vendor_id,
            device.info.product == product_id,
            device.name == name
        ]
        if all(eq):
            return device
    print(f"Device {DEVICE_NAME!r} not found")
    for device in devices:
        print(device.path, device.name, device.info.vendor, device.info.product)

def map_button_press(event, mapper):
    print(evdev.categorize(event), repr(event))
    _active = event.value == 1
    mapper.send_keystroke(event.code, event.value, active=_active)

def map_hat_movement(event, mapper):
    mapper.send_keystroke(event.code, event.value)

async def main():
    mapper = Mapper()
    try:
        input_device = find_device(PRODUCT_ID, VENDOR_ID, DEVICE_NAME)
        if input_device is None:
            print( f"Device {DEVICE_NAME!r} not found")
            return
        async for event in input_device.async_read_loop():
            event: evdev.InputEvent = event
            if event.type == ecodes.EV_KEY:
                map_button_press(event, mapper)
            elif event.type == ecodes.EV_ABS:
                print(evdev.categorize(event), repr(event))
                map_hat_movement(event, mapper)
    except PermissionError:
        print ("no permission for /dev/input")
    finally:
        mapper.close()

if __name__ == "__main__":
    asyncio.run(main())
