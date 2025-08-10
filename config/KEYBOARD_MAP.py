from evdev import ecodes as e

"""Layout map for german keyboards"""

LAYOUT_MAP = {
    # Standard alphanumeric keys (mostly same physical position)
    'A': e.KEY_A, 'B': e.KEY_B, 'C': e.KEY_C, 'D': e.KEY_D,
    'E': e.KEY_E, 'F': e.KEY_F, 'G': e.KEY_G, 'H': e.KEY_H,
    'I': e.KEY_I, 'J': e.KEY_J, 'K': e.KEY_K, 'L': e.KEY_L,
    'M': e.KEY_M, 'N': e.KEY_N, 'O': e.KEY_O, 'P': e.KEY_P,
    'Q': e.KEY_Q, 'R': e.KEY_R, 'S': e.KEY_S, 'T': e.KEY_T,
    'U': e.KEY_U, 'V': e.KEY_V, 'W': e.KEY_W, 'X': e.KEY_X,
    # Swapped Z and Y
    'Z': e.KEY_Y, # To get a US 'Z' on a German layout, send physical KEY_Y
    'Y': e.KEY_Z, # To get a US 'Y' on a German layout, send physical KEY_Z

    # Numbers
    '1': e.KEY_1, '2': e.KEY_2, '3': e.KEY_3, '4': e.KEY_4,
    '5': e.KEY_5, '6': e.KEY_6, '7': e.KEY_7, '8': e.KEY_8,
    '9': e.KEY_9, '0': e.KEY_0,

    # US-style Special Characters (requiring AltGr on German layout)
    # These return a tuple (modifier_key, base_key)
    '[': (e.KEY_RIGHTALT, e.KEY_8), # AltGr+8 for [
    ']': (e.KEY_RIGHTALT, e.KEY_9), # AltGr+9 for ]
    '{': (e.KEY_RIGHTALT, e.KEY_7), # AltGr+7 for {
    '}': (e.KEY_RIGHTALT, e.KEY_0), # AltGr+0 for }
    '@': (e.KEY_RIGHTALT, e.KEY_Q), # AltGr+Q for @
    '€': (e.KEY_RIGHTALT, e.KEY_E), # AltGr+E for €
    '\\': (e.KEY_RIGHTALT, e.KEY_MINUS), # AltGr+ß (physical minus key) for \
    '|': (e.KEY_RIGHTALT, e.KEY_7), # AltGr+7 on some German layouts for | (might vary)
                                   # More commonly, AltGr + < (less than) key

    # Other common symbols
    '/': (e.KEY_LEFTSHIFT, e.KEY_7), # Shift+7 for /
    '_': (e.KEY_LEFTSHIFT, e.KEY_MINUS), # Shift+Minus for _
    '-': e.KEY_SLASH, # Physical key to the right of 0
    '.': e.KEY_DOT,
    ',': e.KEY_COMMA,
    ';': (e.KEY_LEFTSHIFT, e.KEY_COMMA), # Shift+, for ;
    ':': (e.KEY_LEFTSHIFT, e.KEY_DOT),   # Shift+. for :
    '=': e.KEY_EQUAL,
    '+': (e.KEY_LEFTSHIFT, e.KEY_EQUAL), # Shift+= for +
    '*': (e.KEY_LEFTSHIFT, e.KEY_APOSTROPHE), # Shift+' (on physical 'Ä' key) for *
    '#': (e.KEY_LEFTSHIFT, e.KEY_3), # Shift+3 for #

    # Common modifiers
    'CTRL_L': e.KEY_LEFTCTRL,
    'CTRL_R': e.KEY_RIGHTCTRL,
    'ALT': e.KEY_LEFTALT,
    'ALT_GR': e.KEY_RIGHTALT, # Often AltGr
    'SHIFT_L': e.KEY_LEFTSHIFT,
    'SHIFT_R': e.KEY_RIGHTSHIFT,
    'ENTER': e.KEY_ENTER,
    'SPACE': e.KEY_SPACE,
    'ESC': e.KEY_ESC,
    'TAB': e.KEY_TAB,
    'BACKSPACE': e.KEY_BACKSPACE,
    'DELETE': e.KEY_DELETE,
    'UP': e.KEY_UP, 'DOWN': e.KEY_DOWN,
    'LEFT': e.KEY_LEFT, 'RIGHT': e.KEY_RIGHT,
    
}