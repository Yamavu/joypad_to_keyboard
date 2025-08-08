from evdev import ecodes

DEVICE_ID = 22

BTN_MAPPING = {
    ecodes.BTN_X: ecodes.KEY_X, 
    ecodes.BTN_A: ecodes.KEY_A,
    ecodes.BTN_B: ecodes.KEY_B,
    ecodes.BTN_C: ecodes.KEY_Z,
    ecodes.BTN_Y: ecodes.KEY_L,
    ecodes.BTN_Z: ecodes.KEY_R,
    ecodes.BTN_TL: ecodes.KEY_S,
    ecodes.BTN_TR: ecodes.KEY_T
}

ABS_HAT_MAPPING = {
    ecodes.ABS_HAT0X: {
        -1: [ecodes.KEY_LEFTCTRL, ecodes.KEY_LEFTBRACE],
        1: [ecodes.KEY_LEFTCTRL, ecodes.KEY_RIGHTBRACE]
    },
    ecodes.ABS_HAT0Y: {
        -1: [ecodes.KEY_LEFT],
        1: [ecodes.KEY_RIGHT]
    }
}