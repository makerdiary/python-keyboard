
import array
import digitalio
import time
import usb_hid
from microcontroller.pin import *

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

SCC = MODS_TAP(MODS(LCTRL), ';')


KEYMAP = (
    # layer 0
    (
        ESC,   1,   2,   3,   4,   5,   6,   7,   8,   9,   0, '-', '=', BACKSPACE,
        TAB,   Q,   W,   E,   R,   T,   Y,   U,   I,   O,   P, '[', ']', '|',
        CAPS,  A,   S, L2D,   F,   G,   H,   J,   K,   L, SCC, '"',    ENTER,
        LSHIFT,Z,   X,   C,   V,   B,   N,   M, ',', '.', '/',        RSHIFT,
        LCTRL, LGUI, LALT,          SPACE,            RALT, MENU,  L1, RCTRL
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


def reset_into_bootloader():
    import microcontroller

    microcontroller.on_next_reset(microcontroller.RunMode.BOOTLOADER)
    microcontroller.reset()


class Matrix:
    ROWS = (P0_05, P0_06, P0_07, P0_08, P1_09, P1_08, P0_12, P0_11)
    COLS = (P0_19, P0_20, P0_21, P0_22, P0_23, P0_24, P0_25, P0_26)
    ROW2COL = False

    def __init__(self):
        self.size = len(self.ROWS) * len(self.COLS)
        self.queue = bytearray(self.size)
        self.head = 0
        self.tail = 0
        self.length = 0

        self.rows_io = []                                # row as output
        for pin in self.ROWS:
            io = digitalio.DigitalInOut(pin)
            io.direction = digitalio.Direction.OUTPUT
            io.drive_mode = digitalio.DriveMode.PUSH_PULL
            io.value = 0
            self.rows_io.append(io)

        self.cols_io = []                                # col as input
        for pin in self.COLS:
            io = digitalio.DigitalInOut(pin)
            io.direction = digitalio.Direction.INPUT
            io.pull = digitalio.Pull.DOWN if self.ROW2COL else digitalio.Pull.UP
            self.cols_io.append(io)

        # row selected value depends on diodes' direction
        self.selected_value = bool(self.ROW2COL)
        self.scan_time = 0
        self.pressed_mask = 0
        self.pressed_count = 0
        self.pressed_t = [0] * self.size
        self.released_t = [0] * self.size

    def scan(self):
        self.scan_time = time.monotonic_ns()

        # use local variables to speed up
        selected_value = self.selected_value
        last_pressed_mask = self.pressed_mask
        cols_io = self.cols_io

        pressed_mask = 0
        n_pressed = 0
        key_index = -1
        for row_io in self.rows_io:
            row_io.value = selected_value           # select row
            for col_io in cols_io:
                key_index += 1
                if col_io.value == selected_value:
                    key_mask = 1 << key_index
                    if not (last_pressed_mask & key_mask):
                        if self.scan_time - self.released_t[key_index] < 20000000:
                            print('debonce')
                            continue
                            
                        self.pressed_t[key_index] = self.scan_time
                        self.put(key_index)
                        
                    pressed_mask |= key_mask
                    n_pressed += 1
                elif last_pressed_mask and (last_pressed_mask & (1 << key_index)):
                    if self.scan_time - self.pressed_t[key_index] < 20000000:
                        print('debonce')
                        pressed_mask |= 1 << key_index
                        continue
                        
                    self.released_t[key_index] = self.scan_time
                    self.put(0x80 | key_index)

            row_io.value = not selected_value
        self.pressed_mask = pressed_mask
        self.pressed_count = n_pressed
        
        return self.length

    def wait(self, end_time):
        n_events = self.length 
        while True:
            n = self.scan()
            if n > n_events or self.scan_time > end_time:
                return n

    def put(self, data):
        self.queue[self.head] = data
        self.head += 1
        if self.head >= self.size:
            self.head = 0
        self.length += 1

    def get(self):
        data = self.queue[self.tail]
        self.tail += 1
        if self.tail >= self.size:
            self.tail = 0
        self.length -= 1
        return data

    def __getitem__(self, n):
        return self.queue[(self.tail + n) % self.size]

    def __len__(self):
        return self.length

class Keyboard:
    def __init__(self, keymap=KEYMAP, coords=COORDS):
        self.keymap = keymap
        self.coords = coords
        self.layer_mask = 1

    def setup(self):
        convert = lambda a: array.array('H', (get_action_code(k) for k in a))
        self.actonmap = tuple(convert(layer) for layer in self.keymap)

        self.pair_keys = set()
        for pair in self.pairs:
            for key in pair:
                self.pair_keys.add(key)

    def action_code(self, position):
        position = self.coords[position]
        layer_mask = self.layer_mask
        for layer in range(len(self.actonmap) - 1, -1, -1):
            if (layer_mask >> layer) & 1:
                code = self.actonmap[layer][position]
                if code == 1:   # TRANSPARENT
                    continue
                return code
        return 0

    def run(self):
        hid = HIDService()
        advertisement = ProvideServicesAdvertisement(hid)
        advertisement.appearance = 961
        ble = adafruit_ble.BLERadio()
        ble.name = 'Python Keyboard'
        if ble.connected:
            for c in ble.connections:
                c.disconnect()
        ble.start_advertising(advertisement)
        ble.advertising = True
        ble_keyboard = _Keyboard(hid.devices)
        usb_keyboard = _Keyboard(usb_hid.devices)

        def send(*code):
            usb_keyboard.press(*code)
            usb_keyboard.release(*code)
            if ble.connected:
                ble.advertising = False
                ble_keyboard.press(*code)
                ble_keyboard.release(*code)

        def press(*code):
            usb_keyboard.press(*code)
            if ble.connected:
                ble.advertising = False
                ble_keyboard.press(*code)

        def release(*code):
            usb_keyboard.release(*code)
            if ble.connected:
                ble.advertising = False
                ble_keyboard.release(*code)

        self.setup()
        matrix = Matrix()
        keys = [0] * matrix.size
        while True:
            n_events = matrix.scan()
            if n_events == 0:
                # print((time.monotonic_ns() - matrix.scan_time) // 1000000)
                continue

            # detecting pair keys
            if n_events == 1 and matrix[0] in self.pair_keys:
                    n_events = matrix.wait(matrix.scan_time + 10000000)

            if n_events >= 2:
                pair = {matrix[0], matrix[1]}
                if pair in self.pairs:
                    pair_index = self.pairs.index(pair)
                    key1 = matrix.get()
                    key2 = matrix.get()
                        
                    dt = matrix.pressed_t[key2] - matrix.pressed_t[key1]
                    print('pair keys {} {}, dt = {}'.format(
                        pair_index,
                        pair,
                        dt // 1000000))
                    # todo
                    for c in b'pair keys':
                        send(ASCII_TO_KEYCODE[c])

            while len(matrix):
                event = matrix.get()
                key = event & 0x7F
                if event & 0x80 == 0:
                    action_code = self.action_code(key)
                    keys[key] = action_code
                    print('{} \\ action_code = {}'.format(key, hex(action_code)))
                    if action_code < 0xFF:
                        press(action_code)
                    else:
                        kind = action_code >> 12
                        kind = action_code >> 12
                        if kind == ACT_MODS:
                            mods = (action_code >> 8) & 0xF
                            keycodes = mods_to_keycodes(mods)
                            keycodes.append(action_code & 0xFF)
                            press(*keycodes)
                        elif kind == ACT_MODS_TAP:
                            if matrix.length == 0:
                                matrix.wait(matrix.pressed_t[key] + 500000000)
                            if matrix.length > 0 and matrix[0] == (key | 0x80):
                                print('press & release quickly')
                                keycode = action_code & 0xFF
                                keys[key] = keycode
                                press(keycode)
                                matrix.get()
                                release(keycode)
                            else:
                                mods = (action_code >> 8) & 0xF
                                keycodes = mods_to_keycodes(mods)
                                print(keycodes)
                                press(*keycodes)
                        elif kind == ACT_LAYER_TAP:
                            layer = ((action_code >> 8) & 0xF)
                            mask = 1 << layer
                            keycode = action_code & 0xFF
                            if keycode != OP_TAP_TOGGLE:
                                if matrix.length == 0:
                                    matrix.wait(matrix.pressed_t[key] + 500000000)
                                if matrix.length > 0 and matrix[0] == (key | 0x80):
                                    print('press & release quickly')
                                    keys[key] = keycode
                                    press(keycode)
                                    matrix.get()
                                    release(keycode)
                                else:
                                    self.layer_mask |= mask
                            else:
                                print('toggle {}'.format(self.layer_mask))
                                self.layer_mask = (self.layer_mask & ~mask) | (mask & ~self.layer_mask)
                            
                            print('layers {}'.format(self.layer_mask))
                        elif action_code == BOOTLOADER:
                            reset_into_bootloader()
                else:
                    action_code = keys[key]
                    dt = (matrix.scan_time - matrix.pressed_t[key]) // 1000000
                    print('{} / action_code = {}, dt = {}'.format(key, action_code, dt))
                    if action_code < 0xFF:
                        release(action_code)
                    else:
                        kind = action_code >> 12
                        if kind == ACT_MODS:
                            mods = (action_code >> 8) & 0xF
                            keycodes = mods_to_keycodes(mods)
                            keycodes.append(action_code & 0xFF)
                            release(*keycodes)
                        elif kind == ACT_MODS_TAP:
                            mods = (action_code >> 8) & 0xF
                            keycodes = mods_to_keycodes(mods)
                            release(*keycodes)
                        elif kind == ACT_LAYER_TAP:
                            layer = ((action_code >> 8) & 0xF)
                            keycode = action_code & 0xFF
                            if keycode != OP_TAP_TOGGLE:
                                self.layer_mask &= ~(1 << layer)
                                print('layers {}'.format(self.layer_mask))
                            # if dt < 500 and keycode:
                                # send(keycode)

            if not ble.connected and not ble.advertising:
                ble.start_advertising(advertisement)
                ble.advertising = True

            print((time.monotonic_ns() - matrix.scan_time) // 1000000)


def main():
    kbd = Keyboard()
    # pair key {J, K}
    kbd.pairs = [{35, 36}]
    kbd.run()
