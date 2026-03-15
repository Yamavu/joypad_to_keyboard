from typing import Sequence, List, Set

import evdev
from evdev.ecodes import EV_ABS, EV_KEY, ecodes

MAX_LEN = 5  # maximum number of concurrent key events for a single button press
KEY_DOWN_VALUE = 1
KEY_UP_VALUE = 0


class Mapper:
    def __init__(
        self,
        output_device,
        btn_mapping,
        abs_hat_mapping,
        initial_hat_value,
    ):
        self.output_device = output_device
        self.btn_mapping = btn_mapping
        self.abs_mapping = abs_hat_mapping
        self.abs_hat_pos = dict(
            zip(
                abs_hat_mapping.keys(),
                [initial_hat_value] * len(abs_hat_mapping.keys()),
            )
        )
        self.initial_hat_value = initial_hat_value

    @staticmethod
    def collect_target_events(btn_mapping, abs_hat_mapping) -> List[int]:
        mapped_events: Set[int] = set()

        def collect(e_list) -> Set[int]:
            _mapped_events = set()
            if isinstance(e_list, int):
                e_list = [e_list]
            for e in e_list:
                _mapped_events.add(e)
            return _mapped_events

        for e_list in btn_mapping.values():
            mapped_events = mapped_events.union(collect(e_list))
        for e_list_list in abs_hat_mapping.values():
            for e_list in e_list_list.values():
                mapped_events=mapped_events.union(collect(e_list))
        return list(mapped_events)

    @staticmethod
    def _map_value_to_name(value: int | Sequence[int]) -> str:
        """
        Maps an integer evdev event code or a sequence of codes to their symbolic names.
        """
        if isinstance(value, int):
            value = [value]  # Ensure it's always a list for consistent processing

        mapped_names = []
        for code in value:
            # Iterate through all items() to find the name corresponding to the code
            found_name = None
            for name, code_value in ecodes.items():
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

    def send_keystroke(self, btn_code, value: int, active:bool):
        """
        recieve button code and value 
        """
        if btn_code in self.btn_mapping:
            mapped_events: int | Sequence[int] = self.btn_mapping[btn_code]
        elif btn_code in self.abs_mapping:
            if (
                value not in self.abs_mapping[btn_code]
                and self.abs_hat_pos[btn_code] != self.initial_hat_value
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
                f"{'sending' if active else 'releasing'} {self._map_value_to_name(mapped_events)} to uinput"
            )
        if isinstance(mapped_events, int):
            mapped_events = [mapped_events]
        assert len(mapped_events) < MAX_LEN, (
            f"as a safety check len(mapped_events) < {MAX_LEN}"
        )
        
        _mapped_events = mapped_events
        value = KEY_DOWN_VALUE
        if not active:
            value = KEY_UP_VALUE
            _mapped_events = reversed(mapped_events)
        for event in _mapped_events:
            self.output_device.write(EV_KEY, event, KEY_DOWN_VALUE)  # key down
            self.output_device.syn()
        
    def map_input(self, input_device: evdev.InputDevice):
        assert self.output_device.fd != -1, "Device is closed already."
        try:
            with input_device.grab_context():
                for event in input_device.read_loop():
                    if event.type == EV_KEY:
                        key_pressed = event.value == KEY_DOWN_VALUE
                        self.send_keystroke(event.code, event.value, active=key_pressed)
                    elif event.type == EV_ABS:
                        # EV_ABS don't release, they just send different coordinates
                        self.send_keystroke(event.code, event.value, active=True)
        except Exception as e:
            print(e)
        finally:
            self.output_device.close()