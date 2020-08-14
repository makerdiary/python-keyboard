
import _bleio
import array
import time
import microcontroller
import usb_hid

import adafruit_ble
from adafruit_ble.advertising import Advertisement
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.hid import HIDService

from .hid import HID
from .model import Matrix, COORDS
from .action_code import *


___ = TRANSPARENT
BOOT = BOOTLOADER
L1 = LAYER_TAP(1)
L2D = LAYER_TAP(2, D)
L3B = LAYER_TAP(3, B)

# Semicolon & Ctrl
SCC = MODS_TAP(MODS(RCTRL), ';')


KEYMAP = (
    # layer 0
    (
        ESC,   1,   2,   3,   4,   5,   6,   7,   8,   9,   0, '-', '=', BACKSPACE,
        TAB,   Q,   W,   E,   R,   T,   Y,   U,   I,   O,   P, '[', ']', '|',
        CAPS,  A,   S, L2D,   F,   G,   H,   J,   K,   L, SCC, '"',    ENTER,
        LSHIFT,Z,   X,   C,   V, L3B,   N,   M, ',', '.', '/',        RSHIFT,
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
        BT_TOGGLE,BT1,BT2, BT3,BT4,BT5,BT6,BT7, BT8, BT9, BT0, ___, ___, ___,
        ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___,
        ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___,      ___,
        ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___,           ___,
        ___, ___, ___,                ___,               ___, ___, ___,  ___
    ),
)

@micropython.asm_thumb
def mem(r0):
    ldr(r0, [r0, 0])

def usb_is_connected():
    return mem(0x40000438) == 0x3

def reset_into_bootloader():
    microcontroller.on_next_reset(microcontroller.RunMode.BOOTLOADER)
    microcontroller.reset()


def is_tapped(matrix, key):
    n = len(matrix)
    if n == 0:
        n = matrix.wait(500 - matrix.ms(matrix.time() - matrix.get_keydown_time(key)))
    target = key | 0x80
    if n == 1:
        if target == matrix.view(0):
            return True
        else:
            n = matrix.wait(200 - matrix.ms(matrix.time() - matrix.get_keydown_time(key)))
    if n == 2 and target == matrix.view(1):
        return True

    return False


class Device:
    def __init__(self, kbd):
        self.kbd = kbd
        self.send_consumer = kbd.send_consumer
        self.wait = kbd.matrix.wait

    def send(self, *names):
        keycodes = tuple(map(lambda n: get_action_code(n), names))
        self.kbd.send(*keycodes)

    def press(self, *names):
        keycodes = map(lambda n: get_action_code(n), names)
        self.kbd.press(*keycodes)

    def release(self, *names):
        keycodes = map(lambda n: get_action_code(n), names)
        self.kbd.release(*keycodes)

    def send_text(self, text):
        shift = False
        for c in text:
            keycode = ASCII_TO_KEYCODE[ord(c)]
            if keycode & 0x80:
                keycode = keycode & 0x7F
                if not shift:
                    shift = True
                    self.kbd.press(SHIFT)
            elif shift:
                self.kbd.release(SHIFT)
                shift = False

            self.kbd.send(keycode)

        if shift:
            self.kbd.release(SHIFT)


class Keyboard:
    Matrix = Matrix
    coords = COORDS

    def __init__(self, keymap=KEYMAP, pairs=(), verbose=True):
        self.keymap = KEYMAP
        self.pairs = pairs
        self.verbose = verbose
        self.pairs_handler = None
        self.pair_keys = set()
        self.macro_handler = None
        self.layer_mask = 1
        self.matrix = None
        self.unique_array = microcontroller.cpu.uid * 2

        ble_hid = HIDService()
        advertisement = ProvideServicesAdvertisement(ble_hid)
        advertisement.appearance = 961
        advertisement.complete_name = 'Python Keyboard'
        self.advertisement = advertisement
        ble = adafruit_ble.BLERadio()
        ble.name = 'Python Keyboard'
        self.ble = ble
        self.change_bt_id(1)
        self.ble_hid = HID(ble_hid.devices)
        try:
            self.usb_hid = HID(usb_hid.devices) if usb_is_connected() else None
        except Exception:
            self.usb_hid = None

    def hook(self):
        if usb_is_connected() and not self.usb_hid:
            try:
                self.usb_hid = HID(usb_hid.devices) if usb_is_connected() else None
            except Exception:
                self.usb_hid = None

    def setup(self):
        if not self.matrix:
            self.matrix = self.Matrix()

        convert = lambda a: array.array('H', (get_action_code(k) for k in a))
        self.actonmap = tuple(convert(layer) for layer in self.keymap)

        for pair in self.pairs:
            for key in pair:
                self.pair_keys.add(key)

    def change_bt_id(self, n):
        if self.ble.connected:
            for c in self.ble.connections:
                c.disconnect()
        if self.ble._adapter.advertising:
            self.ble.stop_advertising()

        if 0 > n or n > 9:
            return

        uid = self.unique_array[n:n+6]
        uid[-1] = uid[-1] | 0xC0
        address = _bleio.Address(uid, _bleio.Address.RANDOM_STATIC)
        try:
            self.ble._adapter.address = address
        except Exception:
            print('Not support to change bluetooth mac address. Please upgrade to the lastest firmware')
        print(self.ble._adapter.address)
        self.ble.start_advertising(self.advertisement)

    def toggle_bt(self):
        if self.ble.connected:
            for c in self.ble.connections:
                c.disconnect()
        elif self.ble._adapter.advertising:
            self.ble.stop_advertising()
        else:
            self.ble.start_advertising(self.advertisement)

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

    def send(self, *keycodes):
        self.press(*keycodes)
        self.release(*keycodes)

    def press(self, *keycodes):
        no_usb = True
        try:
            if usb_is_connected():
                if not self.usb_hid:
                    self.usb_hid = HID(usb_hid.devices)
                self.usb_hid.press(*keycodes)
                no_usb = False
        except Exception as e:
            print(e)

        try:
            if self.ble.connected:
                self.ble_hid.press(*keycodes)
            elif no_usb and not self.ble._adapter.advertising:
                self.ble.start_advertising(self.advertisement)
        except Exception as e:
            print(e)

    def release(self, *keycodes):
        try:
            if usb_is_connected():
                self.usb_hid.release(*keycodes)
        except Exception as e:
            print(e)

        try:
            if self.ble.connected:
                self.ble_hid.release(*keycodes)
                # for c in self.ble.connections:
                #     print('ble connect interval {}'.format(c.connection_interval))
        except Exception as e:
            print(e)

    def send_consumer(self, keycode):
        try:
            if usb_is_connected():
                self.usb_hid.send_consumer(keycode)
        except Exception as e:
            print(e)

        try:
            if self.ble.connected:
                self.ble_hid.send_consumer(keycode)
        except Exception as e:
            print(e)

    def run(self):
        self.setup()
        log = self.log
        matrix = self.matrix
        dev = Device(self)
        keys = [0] * matrix.keys
        ms = matrix.ms
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
                    if callable(self.pairs_handler):
                        try:
                            self.pairs_handler(dev, pair_index)
                        except Exception as e:
                            print(e)
                            pass

            while len(matrix):
                event = matrix.get()
                key = event & 0x7F
                if event & 0x80 == 0:
                    action_code = self.action_code(key)
                    keys[key] = action_code
                    if action_code < 0xFF:
                        self.press(action_code)
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
                            self.press(*keycodes)
                        elif kind < ACT_USAGE:
                            # MODS_TAP
                            if is_tapped(matrix, key):
                                log('TAP')
                                keycode = action_code & 0xFF
                                keys[key] = keycode
                                self.press(keycode)
                            else:
                                mods = (action_code >> 8) & 0x1F
                                keycodes = mods_to_keycodes(mods)
                                self.press(*keycodes)
                        elif kind == ACT_USAGE:
                            if action_code & 0x400:
                                self.send_consumer(action_code & 0x3FF)
                        elif kind == ACT_MOUSEKEY:
                            # todo
                            pass
                        elif kind == ACT_LAYER_TAP or kind == ACT_LAYER_TAP_EXT:
                            layer = ((action_code >> 8) & 0x1F)
                            mask = 1 << layer
                            if is_tapped(matrix, key):
                                log('TAP')
                                keycode = action_code & 0xFF
                                if keycode & 0xE0 == 0xC0:
                                    log('LAYER_MODS')
                                    mods = keycode & 0x1F
                                    keycodes = mods_to_keycodes(mods)
                                    self.press(*keycodes)
                                elif keycode != OP_TAP_TOGGLE:
                                    keys[key] = keycode
                                    self.press(keycode)
                                else:
                                    log('toggle {}'.format(self.layer_mask))
                                    self.layer_mask = (self.layer_mask & ~mask) | (mask & ~self.layer_mask)
                            else:
                                if action_code & 0xE0 == 0xC0:
                                    log('LAYER_MODS')
                                    mods = action_code & 0x1F
                                    keycodes = mods_to_keycodes(mods)
                                    self.press(*keycodes)
                                self.layer_mask |= mask

                            log('layers {}'.format(self.layer_mask))
                        elif kind == ACT_MACRO:
                            if callable(self.macro_handler):
                                i = action_code & 0xFFF
                                try:
                                    self.macro_handler(dev, i, True)
                                except Exception as e:
                                    print(e)
                        elif kind == ACT_COMMAND:
                            if action_code == BOOTLOADER:
                                reset_into_bootloader()
                            elif action_code == BT_TOGGLE:
                                self.toggle_bt()
                            elif BT(0) <= action_code and action_code <= BT(9):
                                i = action_code - BT(0)
                                log('switch to bt {}'.format(i))
                                self.change_bt_id(i)

                        dt = ms(matrix.time() - matrix.get_keydown_time(key))
                        log('{} \\ {} latency {}'.format(key, hex(keys[key]), dt))
                else:
                    action_code = keys[key]
                    if action_code < 0xFF:
                        self.release(action_code)
                    else:
                        kind = action_code >> 12
                        if kind < ACT_MODS_TAP:
                            # MODS
                            mods = (action_code >> 8) & 0x1F
                            keycodes = mods_to_keycodes(mods)
                            keycodes.append(action_code & 0xFF)
                            self.release(*keycodes)
                        elif kind < ACT_USAGE:
                            # MODS_TAP
                            mods = (action_code >> 8) & 0x1F
                            keycodes = mods_to_keycodes(mods)
                            self.release(*keycodes)
                        elif kind == ACT_USAGE:
                            if action_code & 0x400:
                                self.send_consumer(0)
                        elif kind == ACT_MOUSEKEY:
                            pass
                        elif kind == ACT_LAYER_TAP or kind == ACT_LAYER_TAP_EXT:
                            layer = ((action_code >> 8) & 0x1F)
                            keycode = action_code & 0xFF
                            if keycode != OP_TAP_TOGGLE:
                                if keycode & 0xE0 == 0xC0:
                                    log('LAYER_MODS')
                                    mods = keycode & 0x1F
                                    keycodes = mods_to_keycodes(mods)
                                    self.release(*keycodes)
                                self.layer_mask &= ~(1 << layer)
                                log('layers {}'.format(self.layer_mask))
                        elif kind == ACT_MACRO:
                            if callable(self.macro_handler):
                                i = action_code & 0xFFF
                                try:
                                    self.macro_handler(dev, i, False)
                                except Exception as e:
                                    print(e)

                    if self.verbose:
                        dt = ms(matrix.time() - matrix.get_keyup_time(key))
                        log('{} / {} latency {}'.format(key, hex(action_code), dt))

