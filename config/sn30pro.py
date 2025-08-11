from evdev import ecodes

#DEVICE_ID = 22
DEVICE_NAME = "8Bitdo SF30 Pro"
VENDOR_ID = 1118
PRODUCT_ID = 736

BTN_MAPPING = {
    ecodes.BTN_NORTH: [ecodes.KEY_LEFTCTRL, ecodes.KEY_LEFTSHIFT, ecodes.KEY_O],
    ecodes.BTN_SOUTH: [ecodes.KEY_LEFTCTRL, ecodes.KEY_LEFTSHIFT, ecodes.KEY_P],
    ecodes.BTN_EAST: [ecodes.KEY_F1],
    ecodes.BTN_C: ecodes.KEY_Z,
    ecodes.BTN_Y: ecodes.KEY_L,
    ecodes.BTN_Z: ecodes.KEY_R,
    ecodes.BTN_TL: ecodes.KEY_S,
    ecodes.BTN_TR: ecodes.KEY_T,
}

ABS_HAT_MAPPING = {
    ecodes.ABS_HAT0X: {
        -1: [ecodes.KEY_LEFTCTRL, ecodes.KEY_MINUS],
        1: [ecodes.KEY_LEFTCTRL, ecodes.KEY_LEFTSHIFT, ecodes.KEY_0],
    },
    ecodes.ABS_HAT0Y: {-1: [ecodes.KEY_LEFT], 1: [ecodes.KEY_RIGHT]},
}
