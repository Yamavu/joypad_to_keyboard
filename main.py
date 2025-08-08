import asyncio
from pathlib import Path
from pprint import pp

import evdev
from evdev import ecodes

from config import BTN_MAPPING, ABS_HAT_MAPPING, DEVICE_ID


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
        if isinstance(mapped_events, int):
            mapped_events = [mapped_events]
        for event in mapped_events:
            self.ui.write(ecodes.EV_KEY, event, 1)  # KEY_A down
        for event in reversed(mapped_events):
            self.ui.write(ecodes.EV_KEY, event, 0)  # KEY_A up
        self.ui.syn()

    def close(self):
        self.ui.close()


async def main():
    input_device_path = Path("/dev/input") / f"event{DEVICE_ID:d}"
    mapper = Mapper()
    try:
        input_device = evdev.InputDevice(input_device_path)
        async for event in input_device.async_read_loop():
            event: evdev.InputEvent = event
            if event.type == ecodes.EV_KEY and event.value == 1:
                print(evdev.categorize(event), event.value)
                mapper.send_keystroke(event.code)
            elif event.type == ecodes.EV_ABS:
                print(evdev.categorize(event), event.value)
                mapper.send_keystroke(event.code, event.value)
    except FileNotFoundError as e:
        print(f"Device {DEVICE_ID} not found")
    finally:
        mapper.close()


if __name__ == "__main__":
    asyncio.run(main())
