from evdev import ecodes

DEVICE_ID = 20

BTN_MAPPING = {
    ecodes.BTN_X: ecodes.KEY_X,
    ecodes.BTN_A: ecodes.KEY_A,
    ecodes.BTN_B: ecodes.KEY_B,
    ecodes.BTN_Y: ecodes.KEY_Z,
    ecodes.BTN_TL: ecodes.KEY_L,
    ecodes.BTN_TR: ecodes.KEY_R,
    ecodes.BTN_SELECT: ecodes.KEY_S,
    ecodes.BTN_START: ecodes.KEY_T,
}

ABS_HAT_MAPPING = {
    ecodes.ABS_X: {
        0: [ecodes.KEY_LEFTCTRL, ecodes.KEY_LEFTBRACE],
        255: [ecodes.KEY_LEFTCTRL, ecodes.KEY_RIGHTBRACE],
    },
    ecodes.ABS_Y: {0: [ecodes.KEY_LEFT], 255: [ecodes.KEY_RIGHT]},
}
