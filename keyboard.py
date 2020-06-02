
import array
import digitalio
import time
import usb_hid
from board import *

import adafruit_ble
from adafruit_ble.advertising import Advertisement
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.hid import HIDService
from adafruit_hid.keyboard import Keyboard as _Keyboard

from action_code import *


___ = TRANSPARENT
BOOT = BOOTLOADER
L1 = LAYER_TAP(1)
L2 = LAYER_TAP(2)
L2D = LAYER_TAP(2, D)
L3 = LAYER_TAP(3)
T3 = LAYER_TAP_TOGGLE(3)


KEYMAP = (
    # layer 0
    (
        ESC, 1,  2,  3,  4,  5,  6,  7,  8,  9,  0, '-', '=', BACKSPACE,
        TAB,  Q,  W,  E,  R,  T,  Y,  U,  I,  O,  P, '[', ']', '|',
        CAPS,  A, S, L2D,  F,  G,  H,  J,  K,  L, ';', '"',       ENTER,
        LSHIFT,  Z,  X,  C,  V,  B,  N,  M, ',', '.', '/',       RSHIFT,
        LCTRL, LGUI, LALT,        SPACE,         RALT, MENU,  L1, RCTRL
    ),

    # layer 1
    (
        '`',  F1,  F2,  F3,  F4,  F5,  F6,  F7,  F8,  F9, F10, F11, F12, DEL,
        ___, ___,  UP, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___,
        ___,LEFT,DOWN,RIGHT,___, ___, ___, ___, ___, ___, ___, ___,      ___,
        ___, ___, ___, ___, ___,BOOT, ___, ___, ___, ___, ___,           ___,
        ___, ___, ___,                ___,               ___, ___, ___,  ___
    ),

    # layer 2
    (
        '`',  F1,  F2,  F3,  F4,  F5,  F6,  F7,  F8,  F9, F10, F11, F12, DEL,
        ___, ___, ___, ___, ___, ___, ___,PGUP, ___, ___, ___, ___, ___, ___,
        ___, ___, ___, ___, ___, ___,LEFT, UP,DOWN,RIGHT, ___, ___,      ___,
        ___, ___, ___, ___, ___, ___,PGDN, ___, ___, ___, ___,           ___,
        ___, ___, ___,                ___,               ___, ___, ___,  ___
    ),

    # layer 3
    (
        ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___,
        ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___,
        ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___,      ___,
        ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___,     UP,
        ___, ___, ___,                ___,               ___,LEFT,DOWN,RIGHT
    ),
)


ROWS = (P27, P13, P30, P20, P3)
COLS = (P26, P31, P29, P28, P5, P4, P24, P25, P23, P22, P14, P15, P16, P17)


COORDS = (
    0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13,
    14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
    28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,  0, 40,
    41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51,  0, 52,  0,
    53, 55, 54,  0,  0, 56,  0,  0, 57, 58, 59, 60,  0,  0
)


def reset_into_bootloader():
    import microcontroller

    microcontroller.on_next_reset(microcontroller.RunMode.BOOTLOADER)
    microcontroller.reset()


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

    def __getitem__(self, n):
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

        convert = lambda a: array.array('H', (get_action_code(k) for k in a))
        self.actonmap = tuple(convert(layer) for layer in self.keymap)

        self.pair_keys_code = tuple(
            map(lambda x: get_action_code(x), self.pair_keys.keys()))

        def get_coord(x): return self.coords.index(self.keymap[0].index(x))

        def get_mask(x):
            keys = self.pair_keys[x]
            mask = 0
            for key in keys:
                mask |= 1 << get_coord(key)
            return mask

        self.pair_keys_mask = tuple(map(get_mask, self.pair_keys))
        # print([hex(x) for x in self.pair_keys_mask])

        self.rows_io = []                                # row as output
        for pin in self.rows:
            io = digitalio.DigitalInOut(pin)
            io.direction = digitalio.Direction.OUTPUT
            io.drive_mode = digitalio.DriveMode.PUSH_PULL
            io.value = 0
            self.rows_io.append(io)

        self.cols_io = []                                # col as input
        for pin in self.cols:
            io = digitalio.DigitalInOut(pin)
            io.direction = digitalio.Direction.INPUT
            io.pull = digitalio.Pull.DOWN if self.row2col else digitalio.Pull.UP
            self.cols_io.append(io)

        # row selected value depends on diodes' direction
        self.selected_value = bool(self.row2col)

    def scan(self):
        self.scan_time = time.monotonic_ns()
        selected_value = self.selected_value
        last_pressed_mask = self.pressed_mask
        pressed_mask = 0
        n_pressed = 0
        key_index = 0
        for row_io in self.rows_io:
            row_io.value = selected_value           # select row
            for col_io in self.cols_io:
                if col_io.value == selected_value:
                    key_mask = 1 << key_index
                    pressed_mask |= key_mask
                    n_pressed += 1
                    if not (last_pressed_mask & key_mask):
                        self.pressed_time[key_index] = self.scan_time
                        self.queue.put(key_index)
                elif last_pressed_mask and (last_pressed_mask & (1 << key_index)):
                    self.queue.put(0x80 | key_index)
                
                key_index += 1
            row_io.value = not selected_value
        self.pressed_mask = pressed_mask
        self.pressed_count = n_pressed

        return len(self.queue)

    def wait(self, n_events=1, end_time=None):
        while True:
            n = self.scan()
            if n >= n_events or (end_time and self.scan_time > end_time):
                return n

    def wait_for_mask(self, mask, end_time=None):
        while True:
            n = self.scan()
            if mask == self.pressed_mask or (self.pressed_mask & mask != self.pressed_mask) or (end_time and self.scan_time > end_time):
                return n

    def action_code(self, position):
        position = self.coords[position]

        for layer in range(len(self.actonmap) - 1, -1, -1):
            if (self.layers >> layer) & 1:
                code = self.actonmap[layer][position]
                if code == get_action_code(TRANSPARENT):
                    continue
                return code
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
                        n_events = self.wait_for_mask(mask, self.scan_time + 30000000)
                        break

            if n_events >= 2 and n_events == self.pressed_count:
                mask = 0
                for i in range(n_events):
                    mask |= 1 << self.queue.preview(i)
                if mask in self.pair_keys_mask:
                    pair_keys_index = self.pair_keys_mask.index(mask)
                    action_code = self.pair_keys_code[pair_keys_index]
                    keys = []
                    for _ in range(n_events):
                        key = self.queue.get()
                        self.keys[key] = 0
                        keys.append(key)
                        
                    dt = self.pressed_time[keys[-1]] - self.pressed_time[keys[0]]
                    print('pair keys {} {}, dt = {}'.format(
                        pair_keys_index,
                        keys,
                        dt // 1000000))
                        
                    self.keys[keys[0]] = action_code

                    if action_code < 2:
                        pass
                    elif action_code < 0xFF:
                        press(action_code)
                    else:
                        kind = action_code >> 12
                        if kind == ACT_LAYER_TAP:
                            layer = ((action_code >> 8) & 0xF)
                            mask = 1 << layer
                            keycode = action_code & 0xFF
                            print((keycode, OP_TAP_TOGGLE))
                            if keycode != OP_TAP_TOGGLE:
                                n_events = self.wait(1, self.pressed_time[key] + 500000000)
                                if n_events > 0 and self.queue.preview() == (key | 0x80):
                                    print('press & release quickly')
                                    self.keys[key] = keycode
                                    press(keycode)
                                else:
                                    self.layers |= mask
                            else:
                                print('toggle {}'.format(self.layers))
                                self.layers = (self.layers & ~mask) | (mask & ~self.layers)
                            
                            print('layers {}'.format(self.layers))

            while len(self.queue):
                event = self.queue.get()
                key = event & 0x7F
                if event & 0x80 == 0:
                    action_code = self.action_code(key)
                    self.keys[key] = action_code
                    print('{} / action_code = {}'.format(key, action_code))
                    if action_code < 2:
                        pass
                    elif action_code < 0xFF:
                        press(action_code)
                    else:
                        kind = action_code >> 12
                        if kind == ACT_LAYER_TAP:
                            layer = ((action_code >> 8) & 0xF)
                            mask = 1 << layer
                            keycode = action_code & 0xFF
                            if keycode != OP_TAP_TOGGLE:
                                n_events = self.wait(1, self.pressed_time[key] + 500000000)
                                if n_events > 0 and self.queue.preview() == (key | 0x80):
                                    print('press & release quickly')
                                    self.keys[key] = keycode
                                    press(keycode)
                                else:
                                    self.layers |= mask
                            else:
                                print('toggle {}'.format(self.layers))
                                self.layers = (self.layers & ~mask) | (mask & ~self.layers)
                            
                            print('layers {}'.format(self.layers))
                        elif action_code == BOOTLOADER:
                            reset_into_bootloader()
                else:
                    action_code = self.keys[key]
                    dt = (self.scan_time - self.pressed_time[key]) // 1000000
                    print('{} \\ action_code = {}, dt = {}'.format(key, action_code, dt))
                    if action_code < 2:
                        pass
                    elif action_code < 0xFF:
                        release(action_code)
                    else:
                        kind = action_code >> 12
                        if kind == ACT_LAYER_TAP:
                            layer = ((action_code >> 8) & 0xF)
                            keycode = action_code & 0xFF
                            if keycode != OP_TAP_TOGGLE:
                                self.layers &= ~(1 << layer)
                                print('layers {}'.format(self.layers))
                            # if dt < 500 and keycode:
                                # send(keycode)

            if not ble.connected and not ble.advertising:
                ble.start_advertising(advertisement)
                ble.advertising = True

            print((time.monotonic_ns() - self.scan_time) // 1000000)


def main():
    kbd = Keyboard()
    kbd.pair_keys = {T3: (L1, RCTRL)}
    kbd.run()


if __name__ == '__main__':
    main()
