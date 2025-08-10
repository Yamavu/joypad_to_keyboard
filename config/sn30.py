from evdev import ecodes

DEVICE_ID = 20
DEVICE_NAME = "8Bitdo SFC30 GamePad"

BTN_MAPPING = {
    ecodes.BTN_X: ecodes.KEY_F,
    ecodes.BTN_A: [ecodes.KEY_LEFTCTRL, ecodes.KEY_S],
    ecodes.BTN_B: ecodes.KEY_B,
    ecodes.BTN_Y: ecodes.KEY,
    ecodes.BTN_TL: [ecodes.KEY_LEFTCTRL, ecodes.KEY_Z],
    ecodes.BTN_TR: [ecodes.KEY_LEFTCTRL, ecodes.KEY_LEFTSHIFT, ecodes.KEY_Z],
    ecodes.BTN_SELECT: ecodes.KEY_LEFTCTRL,
    ecodes.BTN_START: ecodes.KEY_LEFTALT,
}

ABS_HAT_MAPPING = {
    ecodes.ABS_X: {
        0: [ecodes.KEY_LEFTCTRL, ecodes.KEY_Z],
        255: [ecodes.KEY_LEFTCTRL, ecodes.KEY_LEFTSHIFT, ecodes.KEY_Z],
    },
    ecodes.ABS_Y: {
        0: [ecodes.KEY_LEFTCTRL, ecodes.KEY_LEFTBRACE],
        255: [ecodes.KEY_LEFTCTRL, ecodes.KEY_RIGHTBRACE],
    }
}
