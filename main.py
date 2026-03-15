# import asyncio
import time
from typing import Optional

import evdev
from evdev import ecodes as e

from mapper import Mapper
from config.sn30 import (
    BTN_MAPPING,
    ABS_HAT_MAPPING,
    INITIAL_HAT_VALUE,
    DEVICE_NAME,
    VENDOR_ID,
    PRODUCT_ID,
)

VIRTUAL_DEVICE = {
    "name": "joypad2keyboard",
    "vendor": 0x04A8,  # Example vendor ID
    "product": 0x0002,  # Example product ID
    "version": 0x0001,
}


def print_devices():
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        print(device.path, device.name, device.info.vendor, device.info.product)


def wait_for_device(product_id, vendor_id, name) -> evdev.InputDevice:
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

    waiting = False
    while True:
        input_device: Optional[evdev.InputDevice] = find_device(
            product_id, vendor_id, name
        )
        if input_device is None:
            if not waiting:
                print(f"Waiting for device: {DEVICE_NAME}")
                waiting = True
            time.sleep(2)
            continue
        print(f"Device {DEVICE_NAME!r} found ... starting event loop.")
        return input_device


def main():
    try:
        input_device = wait_for_device(PRODUCT_ID, VENDOR_ID, DEVICE_NAME)
        key_events = Mapper.collect_target_events(BTN_MAPPING, ABS_HAT_MAPPING)
        print(key_events)
        output_device = evdev.UInput(events={e.EV_KEY: key_events}, **VIRTUAL_DEVICE)
        mapper = Mapper(output_device, BTN_MAPPING, ABS_HAT_MAPPING, INITIAL_HAT_VALUE)
        mapper.map_input(input_device)
    except PermissionError:
        print("no permission for /dev/input")


if __name__ == "__main__":
    # asyncio.run(main())
    main()
