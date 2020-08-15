
try:
    # using built-in matrix if it is available
    from matrix import Matrix
except ImportError:
    from ..matrix import Matrix
    from board import *

    Matrix.ROWS = (R1, R2, R3, R4, R5, R6, R7, R8)
    Matrix.COLS = (C1, C2, C3, C4, C5, C6, C7, C8)
    Matrix.ROW2COL = False


# ESC   1   2   3   4   5   6   7   8   9   0   -   =  BACKSPACE
# TAB   Q   W   E   R   T   Y   U   I   O   P   [   ]   |
# CAPS  A   S   D   F   G   H   J   K   L   ;   "      ENTER
#LSHIFT Z   X   C   V   B   N   M   ,   .   /         RSHIFT
# LCTRL LGUI LALT          SPACE         RALT MENU  L1 RCTRL
COORDS = (
    0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13,
    27,26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14,
    28,29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,     40,
    52,51, 50, 49, 48, 47, 46, 45, 44, 43, 42,         41,
    53,  54, 55,             56,           57, 58, 59, 60
)
