from evdev import ecodes as e
from typing import Dict, List

"""
This is a mapping for the 8bitdo SFC30 / SN30 Gamepad
"""

DEVICE_ID = 20
DEVICE_NAME = "8Bitdo SFC30 GamePad"
VENDOR_ID = 11720
PRODUCT_ID = 10288

ABS_HAT_MIN = 0x00
ABS_HAT_MAX = 0xFF
INITIAL_HAT_VALUE= -1

ABS_HAT_MAPPING: Dict[int, Dict[int,int|List[int]]] = {
    e.ABS_X: {
        ABS_HAT_MIN: [e.KEY_LEFTCTRL],
        ABS_HAT_MAX: [e.KEY_E],
    },
    e.ABS_Y: {
        ABS_HAT_MIN: [e.KEY_LEFTCTRL, e.KEY_LEFTSHIFT, e.KEY_K],
        ABS_HAT_MAX: [e.KEY_LEFTCTRL, e.KEY_LEFTSHIFT, e.KEY_L],
    }
}

BTN_MAPPING: Dict[int, int|List[int]] = {
    e.BTN_X: e.KEY_F,
    e.BTN_A: [e.KEY_LEFTCTRL, e.KEY_S],
    e.BTN_B: e.KEY_B,
    e.BTN_Y: e.KEY_M,
    e.BTN_TL: [e.KEY_LEFTCTRL, e.KEY_Y],
    e.BTN_TR: [e.KEY_LEFTCTRL, e.KEY_LEFTSHIFT, e.KEY_Y],
    e.BTN_SELECT: [e.KEY_LEFTCTRL, e.KEY_LEFTSHIFT, e.KEY_U],
    e.BTN_START: e.KEY_LEFTALT,
}
