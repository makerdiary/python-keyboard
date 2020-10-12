# fmt: off

from board import P27, P13, P30, P20, P3, P26, P31, P29, P28, P5, P4, P24, P25, P23, P22, P14, P15, P16, P17
from .backlight import Backlight
from ..matrix import Matrix

Matrix.ROWS = (P27, P13, P30, P20, P3)
Matrix.COLS = (P26, P31, P29, P28, P5, P4, P24, P25, P23, P22, P14, P15, P16, P17)
Matrix.ROW2COL = True

# ESC   1   2   3   4   5   6   7   8   9   0   -   =  BACKSPACE
# TAB   Q   W   E   R   T   Y   U   I   O   P   [   ]   |
# CAPS  A   S   D   F   G   H   J   K   L   ;   "      ENTER
#LSHIFT Z   X   C   V   B   N   M   ,   .   /         RSHIFT
# LCTRL LGUI LALT          SPACE         RALT MENU  L1 RCTRL
COORDS = (
    0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13,
    14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
    28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,  0, 40,
    41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51,  0, 52,  0,
    53, 55, 54,  0,  0, 56,  0,  0, 57, 58, 59, 60,  0,  0
)

def battery_level():
    return 100
