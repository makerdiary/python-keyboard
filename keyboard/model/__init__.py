import os

machine = os.uname().machine

if machine.find("M60 Keyboard") >= 0:
    from .m60 import Matrix, COORDS, Backlight, battery_level
elif machine.find("Pitaya Go") >= 0:
    from .pitaya_go import Matrix, COORDS, Backlight, battery_level

# fmt: off
KEY_NAME =  (
    'ESC', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'BACKSPACE',
    'TAB', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '[', ']', '|',
    'CAPS', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', '"', 'ENTER',
    'LSHIFT', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/', 'RSHIFT',
    'LCTRL', 'LGUI', 'LALT', 'SPACE', 'RALT', 'MENU', 'FN', 'RCTRL'
)
# fmt: on


def key_name(key):
    return KEY_NAME[COORDS[key]]
