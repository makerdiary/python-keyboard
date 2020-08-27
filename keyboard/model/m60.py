
from .is32fl3733 import IS31FL3733

try:
    # using built-in matrix if it is available
    from matrix import Matrix
except ImportError:
    from ..matrix import Matrix
    from board import R1, R2, R3, R4, R5, R6, R7, R8, C1, C2, C3, C4, C5, C6, C7, C8

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


class Backlight:
    def __init__(self):
        self.dev = IS31FL3733()
        self._hid_leds = 0
        self._bt_led = None
        self.pixel = self.dev.pixel

    def on(self, r=0xFF, g=0xFF, b=0xFF):
        for i in range(64):
            self.pixel(i, r, g, b)
        self.update()

    def off(self):
        for i in range(64):
            self.pixel(i, 0, 0, 0)
        self.update()

    def set_brightness(self, v):
        self.dev.set_brightness(v)

    def set_hid_leds(self, v):
        self._hid_leds = v
        if self._hid_leds & 2:
            # capslock
            self.dev.update_pixel(28, 0, 0x80, 0)
        else:
            self.dev.update_pixel(28, 0, 0, 0)
            if self._bt_led is None and not self.dev.any():
                self.dev.power.value = 0

    def set_bt_led(self, v):
        if self._bt_led is not None:
            self.dev.breathing_pixel(self._bt_led, 0)
        if v == 0:
            v = 10
        self._bt_led = v
        if v is not None:
            self.dev.breathing_pixel(v, 2)
        elif (self._hid_leds & 2) == 0:
            self.dev.power.value = 0

    def update(self):
        in_use = False
        if self._hid_leds & 2:
            self.pixel(28, 0, 0x80, 0)
            in_use = True
        if self._bt_led:
            self.pixel(self._bt_led, 0, 0, 0)
            in_use = True
        self.pixel(63, 0, 0, 0)
        self.dev.update()
        if not in_use and not self.dev.any():
            self.dev.power.value = 0
