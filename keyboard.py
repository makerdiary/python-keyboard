
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
# from matrix import Matrix as CMatrix


___ = TRANSPARENT
BOOT = BOOTLOADER
L1 = LAYER_TAP(1)
L2 = LAYER_TAP(2)
L2D = LAYER_TAP(2, D)
L3 = LAYER_TAP(3)
T3 = LAYER_TAP_TOGGLE(3)

# Semicolon & Ctrl
SCC = MODS_TAP(MODS(RCTRL), ';')


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
        ___, ___, ___, ___, ___, ___,LEFT,DOWN, UP,RIGHT, ___, ___,      ___,
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
        self.keys = len(self.ROWS) * len(self.COLS)
        self.queue = bytearray(self.keys)
        self.head = 0
        self.tail = 0
        self.length = 0

        self.rows = []                                # row as output
        for pin in self.ROWS:
            io = digitalio.DigitalInOut(pin)
            io.direction = digitalio.Direction.OUTPUT
            io.drive_mode = digitalio.DriveMode.PUSH_PULL
            io.value = 0
            self.rows.append(io)

        self.cols = []                                # col as input
        for pin in self.COLS:
            io = digitalio.DigitalInOut(pin)
            io.direction = digitalio.Direction.INPUT
            io.pull = digitalio.Pull.DOWN if self.ROW2COL else digitalio.Pull.UP
            self.cols.append(io)

        # row selected value depends on diodes' direction
        self.pressed = bool(self.ROW2COL)
        self.t0 = [0] * self.keys                   # key pressed time
        self.t1 = [0] * self.keys                   # key released time
        self.mask = 0
        self.count = 0

    def scan(self):
        t = time.monotonic_ns()

        # use local variables to speed up
        pressed = self.pressed
        last_mask = self.mask
        cols = self.cols

        mask = 0
        count = 0
        key_index = -1
        for row in self.rows:
            row.value = pressed           # select row
            for col in cols:
                key_index += 1
                if col.value == pressed:
                    key_mask = 1 << key_index
                    if not (last_mask & key_mask):
                        if t - self.t1[key_index] < 20000000:
                            print('debonce')
                            continue
                            
                        self.t0[key_index] = t
                        self.put(key_index)
                        
                    mask |= key_mask
                    count += 1
                elif last_mask and (last_mask & (1 << key_index)):
                    if t - self.t0[key_index] < 20000000:
                        print('debonce')
                        mask |= 1 << key_index
                        continue
                        
                    self.t1[key_index] = t
                    self.put(0x80 | key_index)

            row.value = not pressed
        self.mask = mask
        self.count = count
        
        return self.length

    def wait(self, timeout=0):
        last = self.length 
        if timeout:
            end_time = time.monotonic_ns() + timeout * 1000000
            while True:
                n = self.scan()
                if n > last or time.monotonic_ns() > end_time:
                    return n
        else:
            while True:
                n = self.scan()
                if n > last:
                    return n

    def put(self, data):
        self.queue[self.head] = data
        self.head += 1
        if self.head >= self.keys:
            self.head = 0
        self.length += 1

    def get(self):
        data = self.queue[self.tail]
        self.tail += 1
        if self.tail >= self.keys:
            self.tail = 0
        self.length -= 1
        return data

    def view(self, n):
        return self.queue[(self.tail + n) % self.keys]

    def __getitem__(self, n):
        return self.queue[(self.tail + n) % self.keys]

    def __len__(self):
        return self.length

    def get_keydown_time(self, key):
        return self.t0[key]

    def get_keyup_time(self, key):
        return self.t1[key]

    def time(self):
        return time.monotonic_ns()

    def ms(self, t):
        return t // 1000000

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
        # matrix = CMatrix()      # keyboard matrix C module
        keys = [0] * matrix.keys
        while True:
            n = matrix.scan()
            if n == 0:
                continue

            # detecting pair keys
            if n == 1:
                key = matrix.view(0)
                if key < 0x80 and key in self.pair_keys:
                    n = matrix.wait(10 - matrix.ms(matrix.time() - matrix.get_keydown_time(key)))

            if n >= 2:
                pair = {matrix.view(0), matrix.view(1)}
                if pair in self.pairs:
                    pair_index = self.pairs.index(pair)
                    key1 = matrix.get()
                    key2 = matrix.get()
                        
                    dt = matrix.get_keydown_time(key2) - matrix.get_keydown_time(key1)
                    print('pair keys {} {}, dt = {}'.format(pair_index, pair, dt))
                    # todo
                    for c in b'pair keys':
                        send(ASCII_TO_KEYCODE[c])

            while len(matrix):
                event = matrix.get()
                key = event & 0x7F
                if event & 0x80 == 0:
                    action_code = self.action_code(key)
                    keys[key] = action_code
                    if action_code < 0xFF:
                        press(action_code)
                        dt = matrix.ms(matrix.time() - matrix.get_keydown_time(key))
                        print('{} \\ {} latency {}'.format(key, hex(action_code), dt))
                    else:
                        kind = action_code >> 12
                        if kind < ACT_MODS_TAP:
                            # MODS
                            mods = (action_code >> 8) & 0x1F
                            keycodes = mods_to_keycodes(mods)
                            keycodes.append(action_code & 0xFF)
                            press(*keycodes)
                        elif kind < ACT_USAGE:
                            # MODS_TAP
                            if len(matrix) == 0:
                                matrix.wait(500 - matrix.ms(matrix.time() - matrix.get_keydown_time(key)))
                            if len(matrix) > 0 and matrix.view(0) == (key | 0x80):
                                print('press & release quickly')
                                keycode = action_code & 0xFF
                                keys[key] = keycode
                                press(keycode)
                                matrix.get()
                                release(keycode)
                            else:
                                mods = (action_code >> 8) & 0x1F
                                keycodes = mods_to_keycodes(mods)
                                press(*keycodes)
                        elif kind == ACT_LAYER_TAP:
                            layer = ((action_code >> 8) & 0xF)
                            mask = 1 << layer
                            keycode = action_code & 0xFF
                            if keycode != OP_TAP_TOGGLE:
                                if len(matrix) == 0:
                                    matrix.wait(500 - matrix.ms(matrix.time() - matrix.get_keydown_time(key)))
                                if len(matrix) > 0 and matrix.view(0) == (key | 0x80):
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
                    
                        dt = matrix.ms(matrix.time() - matrix.get_keydown_time(key))
                        print('{} \\ {} latency {}'.format(key, hex(action_code), dt))
                else:
                    action_code = keys[key]
                    if action_code < 0xFF:
                        release(action_code)
                    else:
                        kind = action_code >> 12
                        if kind < ACT_MODS_TAP:
                            # MODS
                            mods = (action_code >> 8) & 0x1F
                            keycodes = mods_to_keycodes(mods)
                            keycodes.append(action_code & 0xFF)
                            release(*keycodes)
                        elif kind < ACT_USAGE:
                            # MODS_TAP
                            mods = (action_code >> 8) & 0x1F
                            keycodes = mods_to_keycodes(mods)
                            release(*keycodes)
                        elif kind == ACT_LAYER_TAP:
                            layer = ((action_code >> 8) & 0xF)
                            keycode = action_code & 0xFF
                            if keycode != OP_TAP_TOGGLE:
                                self.layer_mask &= ~(1 << layer)
                                print('layers {}'.format(self.layer_mask))
                    
                    dt = matrix.ms(matrix.time() - matrix.get_keyup_time(key))
                    print('{} / {} latency {}'.format(key, hex(action_code), dt))

            if not ble.connected and not ble.advertising:
                ble.start_advertising(advertisement)
                ble.advertising = True


def main():
    kbd = Keyboard()
    # pair key {J, K}
    kbd.pairs = [{35, 36}]
    kbd.run()
