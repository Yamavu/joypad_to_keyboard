import asyncio
from typing import Optional

import evdev
from evdev import ecodes

from config.sn30pro import BTN_MAPPING, ABS_HAT_MAPPING, DEVICE_NAME, PRODUCT_ID, VENDOR_ID


class Mapper:
    def __init__(self):
        self.ui = evdev.UInput()
        self.btn_mapping = BTN_MAPPING
        self.abs_mapping = ABS_HAT_MAPPING

    def send_keystroke(self, btn_code, value=None):
        if btn_code in self.btn_mapping:
            mapped_events = self.btn_mapping[btn_code]
        elif btn_code in self.abs_mapping and value in self.abs_mapping[btn_code]:
            mapped_events = self.abs_mapping[btn_code][value]
        else:
            mapped_events = []
        if mapped_events:
            print(f"sending {mapped_events} to uinput")
        else:
            return
        if isinstance(mapped_events, int):
            mapped_events = [mapped_events]
        for event in mapped_events:
            self.ui.write(ecodes.EV_KEY, event, 1)  # KEY_A down
        for event in reversed(mapped_events):
            self.ui.write(ecodes.EV_KEY, event, 0)  # KEY_A up
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


async def main():
    mapper = Mapper()
    try:
        input_device = find_device(PRODUCT_ID, VENDOR_ID, DEVICE_NAME)
        if input_device is None:
            print( f"Device {DEVICE_NAME!r} not found")
            return
        async for event in input_device.async_read_loop():
            event: evdev.InputEvent = event
            if event.type == ecodes.EV_KEY and event.value == 1:
                print(evdev.categorize(event), repr(event))
                mapper.send_keystroke(event.code)
            elif event.type == ecodes.EV_ABS:
                print(evdev.categorize(event), repr(event))
                mapper.send_keystroke(event.code, event.value)
    except PermissionError:
        print ("no permission for /dev/input")
    finally:
        mapper.close()


if __name__ == "__main__":
    asyncio.run(main())
