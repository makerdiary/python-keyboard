
import digitalio
import time
import usb_hid
from board import *

import adafruit_ble
from adafruit_ble.advertising import Advertisement
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.hid import HIDService
from adafruit_hid.keyboard import Keyboard as _Keyboard

from keycodes import *


___ = TRANSPARENT
L1 = LAYER_TAP(1)
L2 = LAYER_TAP(2)


KEYMAP = (
    # layer 0
    (
        ESC,  1,  2,  3,  4,  5,  6,  7,  8,  9,  0, '-', '=', BACKSPACE,
        TAB,  Q,  W,  E,  R,  T,  Y,  U,  I,  O,  P, '[', ']', '|',
        CAPS,  A,  S,  D,  F,  G,  H,  J,  K,  L, ';', '"',        ENTER,
        LSHIFT,  Z,  X,  C,  V,  B,  N,  M, ',', '.', '/',        RSHIFT,
        LCTRL, LGUI, LALT,        SPACE,          RALT, MENU,  L1, RCTRL
    ),

    # layer 1
    (
        '`', F1, F2, F3, F4, F5, F6, F7, F8, F9, F10, F11, F12, DEL,
        ___, ___,  UP, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___,
        ___, LEFT, DOWN, RIGHT, ___, ___, ___, ___, ___, ___, ___, ___,      ___,
        ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___,           ___,
        ___, ___, ___,                ___,               ___, ___, ___,  ___
    ),

    # layer 2
    (
        '`', F1, F2, F3, F4, F5, F6, F7, F8, F9, F10, F11, F12, DEL,
        ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___,
        ___, ___, ___, ___, ___, ___, LEFT, UP, DOWN, RIGHT, ___, ___,      ___,
        ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___,           ___,
        ___, ___, ___,                ___,               ___, ___, ___,  ___
    ),
)


ROWS = (P27, P13, P30, P20, P3)
COLS = (P26, P31, P29, P28, P5, P4, P24, P25, P23, P22, P14, P15, P16, P17)


COORDS = bytearray((
    0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13,
    14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
    28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,  0, 40,
    41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51,  0, 52,  0,
    53, 55, 54,  0,  0, 56,  0,  0, 57, 58, 59, 60,  0,  0
))


class Queue:
    def __init__(self, size):
        self.size = size
        self.queue = bytearray(size)

        self.head = 0
        self.tail = 0

    def put(self, data):
        self.queue[self.head] = data
        self.head += 1
        if self.head >= self.size:
            self.head = 0

    def get(self):
        data = self.queue[self.tail]
        self.tail += 1
        if self.tail >= self.size:
            self.tail = 0

        return data

    def preview(self, n=0):
        return self.queue[(self.tail + n) % self.size]

    def __len__(self):
        length = self.head - self.tail
        return length if length >= 0 else length + self.size


class Keyboard:
    def __init__(self, keymap=KEYMAP, rows=ROWS, cols=COLS, coords=COORDS, row2col=True):
        self.keymap = keymap
        self.rows = rows
        self.cols = cols
        self.coords = coords
        self.row2col = row2col
        self.layers = 1
        self.scan_time = 0
        self.pair_keys = {}
        self.pressed_mask = 0
        self.pressed_count = 0
        self.queue = Queue(128)

    def setup(self):
        n = len(self.rows) * len(self.cols)
        self.pressed_time = [0] * n
        self.keys = [0] * n

        # convert pykey to pycode (unicode string)
        def pykeycode(x):
            if type(x) is int:
                return chr(x) if x > 9 else ASCII_TO_KEYCODE[ord(str(x))]
            if type(x) is str and len(x) == 1:
                return ASCII_TO_KEYCODE[ord(str(x))]
            raise ValueError('Invalid keycode or keyname {}'.format(x))

        concat = lambda *a: ''.join((pykeycode(x) for x in a))

        self._keymap = tuple(concat(*layer) for layer in self.keymap)

        self.pair_keys_code = tuple(
            map(lambda x: ord(pykeycode(x)), self.pair_keys.keys()))

        def get_coord(x): return self.coords[self.keymap[0].index(x)]

        def get_mask(x):
            keys = self.pair_keys[x]
            return 1 << get_coord(keys[0]) | 1 << get_coord(keys[1])

        self.pair_keys_mask = tuple(map(get_mask, self.pair_keys))
        # print([hex(x) for x in self.pair_keys_mask])

        self.ro = []                                # row as output
        for pin in self.rows:
            io = digitalio.DigitalInOut(pin)
            io.direction = digitalio.Direction.OUTPUT
            io.drive_mode = digitalio.DriveMode.PUSH_PULL
            io.value = 0
            self.ro.append(io)

        self.ci = []                                # col as input
        for pin in self.cols:
            io = digitalio.DigitalInOut(pin)
            io.direction = digitalio.Direction.INPUT
            io.pull = digitalio.Pull.DOWN if self.row2col else digitalio.Pull.UP
            self.ci.append(io)

        # row selected value depends on diodes' direction
        self.selected_value = bool(self.row2col)

    def scan(self):
        self.scan_time = time.monotonic_ns()
        pressed_mask = 0
        n_pressed = 0
        for r, o in enumerate(self.ro):
            o.value = self.selected_value           # select row
            for c, i in enumerate(self.ci):
                key_index = r * len(self.ci) + c
                key_mask = 1 << key_index
                if i.value == self.selected_value:
                    pressed_mask |= key_mask
                    n_pressed += 1
                    if not (self.pressed_mask & (1 << key_index)):
                        self.pressed_time[key_index] = self.scan_time
                        self.queue.put(key_index)
                elif self.pressed_mask & (1 << key_index):
                    self.queue.put(0x80 | key_index)

            o.value = not self.selected_value
        self.pressed_mask = pressed_mask
        self.pressed_count = n_pressed

        return len(self.queue)

    def wait(self, n_events=1, until=None):
        while True:
            n = len(self.queue)
            if n >= n_events or (until and self.scan_time > until):
                return n

            self.scan()

    def keycode(self, position):
        position = self.coords[position]

        for layer in range(len(self._keymap) - 1, -1, -1):
            if (self.layers >> layer) & 1:
                code = self._keymap[layer][position]
                if code == TRANSPARENT:
                    continue
                return ord(code)
        return 0

    def run(self):
        hid = HIDService()
        advertisement = ProvideServicesAdvertisement(hid)
        advertisement.appearance = 961
        ble = adafruit_ble.BLERadio()
        if ble.connected:
            for c in ble.connections:
                c.disconnect()
        ble.start_advertising(advertisement)
        ble.advertising = True
        ble_keyboard = _Keyboard(hid.devices)
        usb_keyboard = _Keyboard(usb_hid.devices)

        def send(code):
            usb_keyboard.press(code)
            usb_keyboard.release(code)
            if ble.connected:
                ble.advertising = False
                ble_keyboard.press(code)
                ble_keyboard.release(code)

        def press(code):
            usb_keyboard.press(code)
            if ble.connected:
                ble.advertising = False
                ble_keyboard.press(code)

        def release(code):
            usb_keyboard.release(code)
            if ble.connected:
                ble.advertising = False
                ble_keyboard.release(code)

        self.setup()
        while True:
            n_events = self.scan()
            if n_events == 0:
                continue

            # detecting pair keys
            if n_events == 1 and self.pressed_count == 1:
                for mask in self.pair_keys_mask:
                    if self.pressed_mask & mask == self.pressed_mask:
                        n_events = self.wait(2, self.scan_time + 25000000)
                        break

            if n_events >= 2:
                mask = 1 << self.queue.preview(0) | 1 << self.queue.preview(1)
                if mask in self.pair_keys_mask:
                    pair_keys_index = self.pair_keys_mask.index(mask)
                    keycode = self.pair_keys_code[pair_keys_index]
                    key1 = self.queue.get()
                    key2 = self.queue.get()
                    dt = self.pressed_time[key2] - self.pressed_time[key1]
                    print('pair keys {} ({}, {}), dt = {}'.format(
                        pair_keys_index,
                        key1,
                        key2,
                        dt // 1000000))

                    # only one action
                    self.keys[key1] = keycode
                    self.keys[key2] = 0

                    if keycode < 2:
                        pass
                    elif keycode < 0xFF:
                        press(keycode)
                    else:
                        kind = keycode >> 12
                        layer = ((keycode >> 8) & 0xF)
                        if kind < (ACT_MODS_TAP + 1):
                            # todo
                            mods = (keycode >> 8) & 0x1F
                        elif kind == ACT_LAYER_TAP:
                            self.layers |= 1 << layer
                            print('layers {}'.format(self.layers))

            while len(self.queue):
                event = self.queue.get()
                key = event & 0x7F
                if event & 0x80 == 0:
                    keycode = self.keycode(key)
                    self.keys[key] = keycode
                    print('{} / keycode = {}'.format(key, keycode))
                    if keycode < 2:
                        pass
                    elif keycode < 0xFF:
                        press(keycode)
                    else:
                        kind = keycode >> 12
                        layer = ((keycode >> 8) & 0xF)
                        if kind == ACT_LAYER_TAP:
                            self.layers |= 1 << layer
                            print('layers {}'.format(self.layers))
                else:
                    keycode = self.keys[key]
                    dt = (self.scan_time - self.pressed_time[key]) // 1000000
                    print('{} \\ keycode = {}, dt = {}'.format(key, keycode, dt))
                    if keycode < 2:
                        pass
                    if keycode < 0xFF:
                        release(keycode)
                    else:
                        kind = keycode >> 12
                        layer = ((keycode >> 8) & 0xF)
                        if kind == ACT_LAYER_TAP:
                            self.layers &= ~(1 << layer)
                            print('layers {}'.format(self.layers))
                            code = keycode & 0xFF
                            if dt < 500 and code:
                                send(code)

            if not ble.connected and not ble.advertising:
                ble.start_advertising(advertisement)
                ble.advertising = True

            # time.sleep(0.01)


def main():
    kbd = Keyboard()
    kbd.pair_keys = {L2: (S, D), L1: (J, K)}
    kbd.run()


if __name__ == '__main__':
    main()
