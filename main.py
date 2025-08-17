# import asyncio
import time
from typing import Set, Dict, Sequence, List
from typing import Optional
from collections import defaultdict

import evdev
from evdev import ecodes

from config.sn30 import (
    BTN_MAPPING,
    ABS_HAT_MAPPING,
    DEVICE_NAME,
    VENDOR_ID,
    PRODUCT_ID,
    INVALID_HAT_VALUE,
)

MAX_LEN = 5  # maximum number of concurrent key events for a single button press


def collect_target_events() -> List[int]:
    mapped_events: Set[int] = set()

    def collect(e_list)->Set[int]:
        _mapped_events = set()
        if isinstance(e_list, int):
            e_list = [e_list]
        for e in e_list:
            _mapped_events.add(e)
        return _mapped_events

    for e_list in BTN_MAPPING.values():
        mapped_events.union(collect(e_list))
    for e_list_list in ABS_HAT_MAPPING.values():
        for e_list in e_list_list.values():
            mapped_events.union(collect(e_list))
    return list(mapped_events)


TARGET_EVENTS = collect_target_events()


def map_value_to_name(value: int | Sequence[int]) -> str:
    """
    Maps an integer evdev event code or a sequence of codes to their symbolic names.
    """
    if isinstance(value, int):
        value = [value]  # Ensure it's always a list for consistent processing

    mapped_names = []
    for code in value:
        # Iterate through all ecodes.items() to find the name corresponding to the code
        found_name = None
        for name, code_value in ecodes.ecodes.items():
            if not name.startswith("KEY") and not name.startswith("BTN"):
                continue
            if code == code_value:
                found_name = name
                break  # Found the name, exit inner loop
        if found_name is not None:
            mapped_names.append(found_name)
        else:
            mapped_names.append(f"UNKNOWN_CODE({code})")  # Handle unknown codes
    return "+".join(mapped_names)


class Mapper:
    def __init__(self):
        self.btn_mapping = BTN_MAPPING
        self.abs_mapping = ABS_HAT_MAPPING
        self.abs_hat_pos = dict(
            zip(
                ABS_HAT_MAPPING.keys(),
                [INVALID_HAT_VALUE] * len(ABS_HAT_MAPPING.keys()),
            )
        )

    def __enter__(self):
        events: Dict[int, Sequence[int]] = {ecodes.EV_KEY: TARGET_EVENTS}
        self.ui = evdev.UInput(
            events=events,
            name="virtual-keyboard",
            vendor=0x1234,  # Example vendor ID
            product=0x5678,  # Example product ID
            version=0x0001,
        )
        return self

    def send_keystroke(self, btn_code, value: int, active=True):
        if btn_code in self.btn_mapping:
            mapped_events: int | Sequence[int] = self.btn_mapping[btn_code]
        elif btn_code in self.abs_mapping:
            if all(
                [
                    value not in self.abs_mapping[btn_code],
                    self.abs_hat_pos[btn_code] != INVALID_HAT_VALUE,
                ]
            ):
                value = self.abs_hat_pos[btn_code]
                active = False
            else:
                self.abs_hat_pos[btn_code] = value
            mapped_events: int | Sequence[int] = self.abs_mapping[btn_code][value]
        else:
            mapped_events = []
        if mapped_events:
            print(
                f"{'sending' if active else 'releasing'} {map_value_to_name(mapped_events)} to uinput"
            )
        if isinstance(mapped_events, int):
            mapped_events = [mapped_events]
        assert len(mapped_events) < MAX_LEN, (
            f"as a safety check len(mapped_events) < {MAX_LEN}"
        )
        if active:
            for event in mapped_events:
                self.ui.write(ecodes.EV_KEY, event, 1)  # key down
        else:
            for event in reversed(mapped_events):
                self.ui.write(ecodes.EV_KEY, event, 0)  # key up
        self.ui.syn()

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.ui.close()


def print_devices():
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        print(device.path, device.name, device.info.vendor, device.info.product)


def find_device(product_id, vendor_id, name) -> Optional[evdev.InputDevice]:
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        if all(
            [
                device.info.vendor == vendor_id,
                device.info.product == product_id,
                device.name == name,
            ]
        ):
            return device
    print(f"Device {DEVICE_NAME!r} not found")


def map_input(input_device: evdev.InputDevice):
    try:
        with input_device.grab_context(), Mapper() as mapper:
            for event in input_device.read_loop():
                if event.type == ecodes.EV_KEY:
                    _active = event.value == 1
                    mapper.send_keystroke(event.code, event.value, active=_active)
                elif event.type == ecodes.EV_ABS:
                    # print(evdev.categorize(event), repr(event))
                    mapper.send_keystroke(event.code, event.value)
    except Exception as e:
        print(e)


def main():
    try:
        waiting = False
        while True:
            input_device: Optional[evdev.InputDevice] = find_device(
                PRODUCT_ID, VENDOR_ID, DEVICE_NAME
            )
            if input_device is None:
                if not waiting:
                    print(f"Waiting for device: {DEVICE_NAME}")
                    waiting = True
                time.sleep(2)
            else:
                print(f"Device {DEVICE_NAME!r} found ... starting event loop.")
                break
        map_input(input_device)
    except PermissionError:
        print("no permission for /dev/input")


if __name__ == "__main__":
    # asyncio.run(main())
    main()
