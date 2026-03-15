from enum import Enum
from evdev import ecodes as e

ABS_HAT_MIN = 0
ABS_HAT_MAX = 255

class ABS_HAT(Enum):
    left = e.ABS_X, ABS_HAT_MIN
    right = e.ABS_X, ABS_HAT_MAX
    up = e.ABS_Y, ABS_HAT_MIN
    down = e.ABS_Y, ABS_HAT_MAX

class BTN(Enum):
    up = e.BTN_X
    right = e.BTN_A
    down = e.BTN_B
    left = e.BTN_Y
    left_shoulder = e.BTN_TL
    right_shoulder = e.BTN_TR
    left_middle = e.BTN_SELECT
    right_middle = e.BTN_START

