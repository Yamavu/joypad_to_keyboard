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
from mapper import Mapper

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
