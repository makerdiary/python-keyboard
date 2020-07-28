
import array
import time
import supervisor
import usb_hid

import adafruit_ble
from adafruit_ble.advertising import Advertisement
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.hid import HIDService
from adafruit_hid.keyboard import Keyboard as _Keyboard

from .model import Matrix, COORDS
from .action_code import *


___ = TRANSPARENT
BOOT = BOOTLOADER
L1 = LAYER_TAP(1)
L2D = LAYER_TAP(2, D)

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
)

@micropython.asm_thumb
def mem(r0):
    ldr(r0, [r0, 0])

def usb_is_connected():
    return mem(0x40000438) == 0x3

def reset_into_bootloader():
    import microcontroller

    microcontroller.on_next_reset(microcontroller.RunMode.BOOTLOADER)
    microcontroller.reset()


class Keyboard:
    Matrix = Matrix
    coords = COORDS

    def __init__(self, keymap=KEYMAP, pairs=(), verbose=True):
        self.keymap = KEYMAP
        self.pairs = pairs
        self.verbose = verbose
        self.pair_keys = set()
        self.layer_mask = 1

    def setup(self):
        convert = lambda a: array.array('H', (get_action_code(k) for k in a))
        self.actonmap = tuple(convert(layer) for layer in self.keymap)

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

    def log(self, *args):
        if self.verbose:
            print(*args)

    def run(self):
        log = self.log

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
        usb_keyboard = _Keyboard(usb_hid.devices) if usb_is_connected() else None

        def send(*code):
            if usb_keyboard:
                usb_keyboard.press(*code)
                usb_keyboard.release(*code)
            if ble.connected:
                ble.advertising = False
                ble_keyboard.press(*code)
                ble_keyboard.release(*code)

        def press(*code):
            if usb_keyboard:
                usb_keyboard.press(*code)
            if ble.connected:
                ble.advertising = False
                ble_keyboard.press(*code)

        def release(*code):
            if usb_keyboard:
                usb_keyboard.release(*code)
            if ble.connected:
                ble.advertising = False
                ble_keyboard.release(*code)

        self.setup()
        matrix = self.Matrix()
        ms = matrix.ms
        keys = [0] * matrix.keys
        while True:
            n = matrix.wait(10)
            if n == 0:
                continue

            # detecting pair keys
            if n == 1:
                key = matrix.view(0)
                if key < 0x80 and key in self.pair_keys:
                    n = matrix.wait(10 - ms(matrix.time() - matrix.get_keydown_time(key)))

            if n >= 2:
                pair = {matrix.view(0), matrix.view(1)}
                if pair in self.pairs:
                    pair_index = self.pairs.index(pair)
                    key1 = matrix.get()
                    key2 = matrix.get()

                    dt = ms(matrix.get_keydown_time(key2) - matrix.get_keydown_time(key1))
                    log('pair keys {} {}, dt = {}'.format(pair_index, pair, dt))
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
                        if self.verbose:
                            dt = ms(matrix.time() - matrix.get_keydown_time(key))
                            log('{} \\ {} latency {}'.format(key, hex(action_code), dt))
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
                                matrix.wait(500 - ms(matrix.time() - matrix.get_keydown_time(key)))
                            if len(matrix) > 0 and matrix.view(0) == (key | 0x80):
                                log('press & release quickly')
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
                                    matrix.wait(500 - ms(matrix.time() - matrix.get_keydown_time(key)))
                                if len(matrix) > 0 and matrix.view(0) == (key | 0x80):
                                    log('press & release quickly')
                                    keys[key] = keycode
                                    press(keycode)
                                    matrix.get()
                                    release(keycode)
                                else:
                                    self.layer_mask |= mask
                            else:
                                log('toggle {}'.format(self.layer_mask))
                                self.layer_mask = (self.layer_mask & ~mask) | (mask & ~self.layer_mask)

                            log('layers {}'.format(self.layer_mask))
                        elif action_code == BOOTLOADER:
                            reset_into_bootloader()

                        dt = ms(matrix.time() - matrix.get_keydown_time(key))
                        log('{} \\ {} latency {}'.format(key, hex(action_code), dt))
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
                                log('layers {}'.format(self.layer_mask))

                    if self.verbose:
                        dt = ms(matrix.time() - matrix.get_keyup_time(key))
                        log('{} / {} latency {}'.format(key, hex(action_code), dt))

            if not ble.connected and not ble.advertising:
                ble.start_advertising(advertisement)
                ble.advertising = True
