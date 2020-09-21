# fmt: off

import analogio
import microcontroller
from .is32fl3733 import IS31FL3733

try:
    # usebuilt-in matrix if it is available
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


BATTERY_LIMIT = 3100  # Cutoff voltage [mV].
BATTERY_FULLLIMIT = 4190  # Full charge definition [mV].
BATTERY_DELTA = 10  # mV between each element in the SoC vector.

BATTERY_VOLTAGE = (
    0,  0,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  2,
    2,  2,  2,  2,  2,  2,  2,  2,  3,  3,  3,  3,  3,  3,  3,  4,  4,  4,  4,  4,
    4,  5,  5,  5,  6,  6,  7,  7,  8,  8,  9,  9, 10, 11, 12, 13, 13, 14, 15, 16,
    18, 19, 22, 25, 28, 32, 36, 40, 44, 47, 51, 53, 56, 58, 60, 62, 64, 66, 67, 69,
    71, 72, 74, 76, 77, 79, 81, 82, 84, 85, 85, 86, 86, 86, 87, 88, 88, 89, 90, 91,
    91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 100
)

battery_in = analogio.AnalogIn(microcontroller.pin.P0_02)


def battery_level():
    # (3300 * 2 * battery.value) >> 16
    voltage = (3300 * battery_in.value) >> 15
    i = (voltage - BATTERY_LIMIT) // BATTERY_DELTA
    if i >= len(BATTERY_VOLTAGE):
        i = len(BATTERY_VOLTAGE) - 1
    elif i < 0:
        i = 0
    return BATTERY_VOLTAGE[i]


leds_x = bytearray((
    0, 16, 32, 48, 64, 80, 96, 112, 128, 144, 160, 176, 192, 216,
    220,200, 184, 168, 152, 136, 120, 104, 88, 72, 56, 40, 24, 4,
    6, 27, 43, 59, 75, 91, 107, 123, 139, 155, 171, 187, 214,
    210, 180, 164, 148, 132, 116, 100, 84, 68, 52, 36, 10,
    2, 22, 42, 102, 162, 182, 202, 222, 123, 82
))

leds_y = bytearray((
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
    32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32,
    48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48,
    64, 64, 64, 64, 64, 64, 64, 64, 64, 64
))

 
def to_rgb(h, s, v):
    i = (h * 3) >> 8
    o = (h * 3) & 0xFF

    f = v * (255 - s) // 255
    a = f + ((v - f) * o) >> 8
    b = f + ((v - f) * (256 - o)) >> 8

    if i == 0: return (b, a, f)
    if i == 1: return (f, b, a)

    return (a, f, b)


class Backlight:
    def __init__(self):
        self.dev = IS31FL3733()
        self._hid_leds = 0
        self._bt_led = None
        self.pixel = self.dev.pixel

        self.hsv = [0, 255, 255]
        self.keys = {}
        self.n = 0

        self.modes = (self.off, self.mono, self.gradient, self.spectrum, self.spectrum_x, self.spectrum_y, self.elapse)
        self.mode = 6
        self.mode_function = self.modes[self.mode]
        self.dynamic = True

    def on(self, r=0xFF, g=0xFF, b=0xFF):
        for i in range(63):
            self.pixel(i, r, g, b)
        self.update()

    def off(self):
        for i in range(64):
            self.pixel(i, 0, 0, 0)
        self.update()

    def mono(self):
        self.on(*to_rgb(*self.hsv))

    def gradient(self):
        h0, s0, v0 = self.hsv
        for i in range(63):
            h = (leds_y[i] + h0) & 0xFF
            self.pixel(i, *to_rgb(h, s0, v0))
        self.update()

    def spectrum(self, offset=0):
        self.n = (self.n + 1) & 0xFF
        r, g, b = to_rgb(self.n, 255, 255)
        for i in range(63):
            self.pixel(i, r, g, b)
        self.update()
        return True

    def spectrum_x(self):
        n = self.n
        for i in range(63):
            h = (leds_x[i] + n) & 0xFF
            self.pixel(i, *to_rgb(h, 255, 255))
        self.update()
        self.n = (n + 1) & 0xFF
        return True
        
    def spectrum_y(self):
        n = self.n
        for i in range(63):
            h = (leds_y[i] + n) & 0xFF
            self.pixel(i, *to_rgb(h, 255, 255))
        self.update()
        self.n = (n + 1) & 0xFF
        return True
        
    def handle_key(self, key, pressed):
        if self.mode == 6:
            self.keys[key] = 255
        
    def elapse(self):
        if 0 == len(self.keys):
            return False
        for i in self.keys.keys():
            t = self.keys[i]
            self.pixel(i, *to_rgb(255 - t, 255, t))
            t -= 1
            if t < 0:
                self.keys.pop(i)
            else:
                self.keys[i] = t
        self.update()
        return True

    def set_brightness(self, v):
        self.dev.set_brightness(v)

    def set_hid_leds(self, v):
        self._hid_leds = v
        if self._hid_leds & 2:
            # capslock
            self.dev.update_pixel(28, 0, 0x80, 0)
        else:
            self.dev.update_pixel(28, 0, 0, 0)
            self.mode_function()

    def set_bt_led(self, v):
        if self._bt_led is not None:
            self.dev.breathing_pixel(self._bt_led, 0)
        if v == 0:
            v = 10
        self._bt_led = v
        if v is not None:
            self.dev.breathing_pixel(v, 2)
        elif (self._hid_leds & 2) == 0 and not self.dev.any():
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

    def check(self):
        if self.dynamic:
            return self.mode_function()
        return False

    def next(self):
        for i in range(63):
            self.pixel(i, 0, 0, 0)
        self.mode += 1
        if self.mode >= len(self.modes):
            self.mode = 0
        self.mode_function = self.modes[self.mode]
        if self.mode == 6:
            self.keys.clear()
        if self.mode >= 3:
            self.dynamic = True 
        else:
            self.dynamic = False
            self.mode_function()
