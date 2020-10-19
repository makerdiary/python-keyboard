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

# fmt: off
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
    2, 22, 42, 102, 162, 182, 202, 222,
    123, 82
))

leds_y = bytearray((
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
    32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32,
    48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48,
    64, 64, 64, 64, 64, 64, 64, 64,
    64, 64
))

angle = bytearray((
    180, 178, 176, 173, 168, 160, 146, 128, 109, 96, 87, 82, 79, 76,
    69, 71, 72, 75, 79, 87, 109, 146, 168, 176, 180, 183, 184, 186,
    170, 170, 170, 170, 170, 170, 170, 64, 64, 64, 64, 64, 64,
    57, 54, 51, 46, 36, 9, 229, 213, 206, 202, 200, 198,
    203, 205, 209, 243, 40, 46, 50, 52,
    13, 225
))

distance = bytearray((
    116, 101, 86, 71, 57, 45, 35, 32, 35, 45, 57, 71, 86, 108, 109, 89, 73,
    58, 43, 28, 17, 17, 28, 43, 58, 73, 89, 109, 106, 85, 69, 53, 37, 21, 5,
    11, 27, 43, 59, 75, 102, 99, 69, 54, 39, 25, 16, 20, 32, 46, 62, 77, 103,
    114, 95, 76, 33, 59, 76, 95, 114,
    33, 43
))
# fmt: on


def hsv_to_rgb(h, s, v):
    i = (h * 6) >> 8
    f = (h * 6) & 0xFF

    p = (v * (256 - s)) >> 8
    q = (v * (65536 - s * f)) >> 16
    t = (v * (65536 - s * (256 - f))) >> 16

    if i == 0:
        return (v, t, p)
    if i == 1:
        return (q, v, p)
    if i == 2:
        return (p, v, t)
    if i == 3:
        return (p, q, v)
    if i == 4:
        return (t, p, v)
    return (v, p, q)


def wheel(h):
    i = (h * 3) >> 8
    a = (h * 3) & 0xFF
    b = 255 - a

    if i == 0:
        return (b, a, 0)
    if i == 1:
        return (0, b, a)

    return (a, 0, b)


def wheel2(h, v):
    i = (h * 3) >> 8
    a = (h * 3) & 0xFF
    b = 255 - a

    a = a * v // 255
    b = b * v // 255

    if i == 0:
        return (b, a, 0)
    if i == 1:
        return (0, b, a)

    return (a, 0, b)


class Backlight:
    def __init__(self):
        self.dev = IS31FL3733()
        self._hid_leds = 0
        self._bt_led = None
        self.pixel = self.dev.pixel

        self.enabled = True
        self.hsv = [0, 255, 255]
        self.keys = {}
        self.n = 0

        self.modes = (
            self.off,
            self.mono,
            self.gradient,
            self.spectrum,
            self.spectrum_x,
            self.spectrum_y,
            self.elapse,
            self.broadcast,
            self.blackhole,
            self.pinwheel,
            self.beacon,
            self.beacon2
        )
        self.set_mode(6)
        self.enabled = False

    @property
    def hue(self):
        return self.hsv[0]

    @hue.setter
    def hue(self, h):
        self.hsv[0] = h & 0xFF
        self.refresh()

    @property
    def sat(self):
        return self.hsv[1]

    @sat.setter
    def sat(self, s):
        self.hsv[1] = 0 if s < 0 else (255 if s > 255 else s)
        self.refresh()

    @property
    def val(self):
        return self.dev.brightness

    @val.setter
    def val(self, v):
        self.set_brightness(v)

    def set_brightness(self, v):
        if v <= 0:
            self.enabled = False
            self.off()
        else:
            self.enabled = True
            self.dev.brightness = v if v < 0xFF else 0xFF
            if not self.dynamic:
                self.mode_function()

    def on(self, r=0xFF, g=0xFF, b=0xFF):
        for i in range(63):
            self.pixel(i, r, g, b)
        self.update()

    def off(self):
        self.dev.clear()
        self.update()

    def toggle(self):
        self.enabled = not self.enabled
        if self.enabled:
            self.set_mode(self.mode)
        else:
            self.off()

    def mono(self):
        self.on(*hsv_to_rgb(*self.hsv))

    def gradient(self):
        h0, s0, v0 = self.hsv
        for i in range(63):
            h = (leds_y[i] + h0) & 0xFF
            self.pixel(i, *hsv_to_rgb(h, s0, v0))
        self.update()

    def spectrum(self, offset=0):
        self.n = (self.n + 1) & 0xFF
        r, g, b = wheel(self.n)
        for i in range(63):
            self.pixel(i, r, g, b)
        self.update()
        return True

    def spectrum_x(self):
        n = self.n
        for i in range(63):
            h = (leds_x[i] + n) & 0xFF
            self.pixel(i, *wheel(h))
        self.update()
        self.n = (n + 1) & 0xFF
        return True

    def spectrum_y(self):
        n = self.n
        for i in range(63):
            h = (leds_y[i] + n) & 0xFF
            self.pixel(i, *wheel(h))
        self.update()
        self.n = (n + 1) & 0xFF
        return True

    def broadcast(self):
        n = self.n
        for i in range(63):
            self.pixel(i, *wheel((distance[i] - n) & 0xFF))
        self.update()
        self.n = (n + 2) & 0xFF
        return True

    def blackhole(self):
        n = self.n
        for i in range(63):
            self.pixel(i, *wheel2((distance[i] + n) & 0xFF, distance[i] * 2 - 10))
        self.update()
        self.n = (n + 2) & 0xFF
        return True

    def pinwheel(self):
        n = self.n
        for i in range(63):
            self.pixel(i, *wheel((angle[i] + n) & 0xFF))
        self.update()
        self.n = (n + 2) & 0xFF
        return True

    def beacon(self):
        n = self.n
        for i in range(63):
            offset = (angle[i] + n) & 0xFF
            if offset < 64:
                offset <<= 2
            else:
                offset = 0
            self.pixel(i, *wheel(offset))
        self.update()
        self.n = (n + 2) & 0xFF
        return True

    def beacon2(self):
        n = self.n
        for i in range(63):
            offset = (angle[i] + n) & 0xFF
            if offset < 64:
                offset <<= 2
            elif 128 < offset and offset < 192:
                offset = (offset - 128) << 2
            else:
                offset = 0
            self.pixel(i, *wheel(offset))
        self.update()
        self.n = (n + 2) & 0xFF
        return True

    def handle_key(self, key, pressed):
        if pressed and self.enabled and self.mode == 6:
            self.keys[key] = 255

    def elapse(self):
        if 0 == len(self.keys):
            return False
        for i in self.keys.keys():
            t = self.keys[i]
            self.pixel(i, *wheel2(255 - t, t))
            if t >= 4:
                self.keys[i] = t - 4
            elif t > 0:
                self.keys[i] = t - 1
            else:
                self.keys.pop(i)
        self.update()
        return True

    def set_hid_leds(self, v):
        if self._hid_leds != v:
            self._hid_leds = v
            g = 128 if (self._hid_leds & 2) else 0
            self.dev.update_pixel(28, 0, g, 0)
            self.refresh()

    def set_bt_led(self, v):
        if v == 0:
            v = 10
        if v is not None:
            self.dev.set_mode(v, 2)
        if self._bt_led is not None:
            self.dev.set_mode(self._bt_led, 0)
        self._bt_led = v

    def update(self):
        if self._hid_leds & 2:
            self.pixel(28, 0, 0x80, 0)
        self.dev.update()

    def check(self):
        if self.enabled and self.dynamic:
            return self.mode_function()
        return False

    def refresh(self):
        if self.enabled and not self.dynamic:
            self.mode_function()

    def next(self):
        self.set_mode(self.mode + 1)

    def set_mode(self, mode):
        self.enabled = True
        self.dev.clear()
        self.mode = mode if mode < len(self.modes) else 0
        self.mode_function = self.modes[self.mode]
        if self.mode == 6:
            self.keys.clear()
        if self.mode >= 3:
            self.dynamic = True
        else:
            self.dynamic = False
            self.mode_function()
