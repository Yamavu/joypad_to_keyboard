from evdev import ecodes

DEVICE_ID = 20
DEVICE_NAME = "8Bitdo SFC30 GamePad"
VENDOR_ID = 11720
PRODUCT_ID = 10288

BTN_MAPPING = {
    ecodes.BTN_X: ecodes.KEY_F,
    ecodes.BTN_A: [ecodes.KEY_LEFTCTRL, ecodes.KEY_S],
    ecodes.BTN_B: ecodes.KEY_B,
    ecodes.BTN_Y: ecodes.KEY_M,
    ecodes.BTN_TL: [ecodes.KEY_LEFTCTRL, ecodes.KEY_Y],
    ecodes.BTN_TR: [ecodes.KEY_LEFTCTRL, ecodes.KEY_LEFTSHIFT, ecodes.KEY_Y],
    ecodes.BTN_SELECT: [ecodes.KEY_LEFTCTRL, ecodes.KEY_LEFTSHIFT, ecodes.KEY_U],
    ecodes.BTN_START: ecodes.KEY_LEFTALT,
}

INVALID_HAT_VALUE = -1
ABS_HAT_MAPPING = {
    ecodes.ABS_X: {
        0: [ecodes.KEY_LEFTCTRL],
        255: [ecodes.KEY_E],
    },
    ecodes.ABS_Y: {
        0: [ecodes.KEY_LEFTCTRL, ecodes.KEY_LEFTSHIFT, ecodes.KEY_K],
        255: [ecodes.KEY_LEFTCTRL, ecodes.KEY_LEFTSHIFT, ecodes.KEY_L],
    }
}
