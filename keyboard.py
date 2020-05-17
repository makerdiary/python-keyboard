
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
        ___,LEFT,DOWN,RIGHT,___, ___, ___, ___, ___, ___, ___, ___,      ___,
        ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___,           ___,
        ___, ___, ___,                ___,               ___, ___, ___,  ___
    ),
    
    # layer 2
    (
        '`', F1, F2, F3, F4, F5, F6, F7, F8, F9, F10, F11, F12, DEL,
        ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___,
        ___, ___, ___, ___, ___, ___,LEFT, UP,DOWN,RIGHT, ___, ___,      ___, 
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
        self.pressed_keys = []
        self.layers = 1
        self.pressed_mask = 0
        self.queue = Queue(128)
        self.t = 0
        self.pair_keys = {}

    def setup(self):
        n = len(self.rows) * len(self.cols)
        self.t_keydown = [0] * n
        self.keys = [0] * n
        
        def f(x):
            if type(x) is int:
                return chr(x) if x > 9 else ASCII_TO_KEYCODE[ord(str(x))]
            if type(x) is str and len(x) == 1:
                return ASCII_TO_KEYCODE[ord(str(x))]
            raise ValueError('Invalid keycode or keyname {}'.format(x))

        convert = lambda *args: ''.join((f(x) for x in args))

        self._keymap = tuple(convert(*layer) for layer in self.keymap)
        
        self.pair_keys_code = list(map(lambda x: ord(f(x)), self.pair_keys.keys()))
        
        get_coord = lambda x: self.coords[self.keymap[0].index(x)]
        def get_mask(x):
            keys = self.pair_keys[x]
            return 1 << get_coord(keys[0]) | 1 << get_coord(keys[1])

        self.pair_keys_mask = list(map(get_mask, self.pair_keys))
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
        self.t = time.monotonic_ns()
        pressed_mask = 0
        n_pressed_keys = 0
        for r, o in enumerate(self.ro):
            o.value = self.selected_value           # select row
            for c, i in enumerate(self.ci):
                key_index = r * len(self.ci) + c
                key_mask = 1 << key_index
                if i.value == self.selected_value:
                    pressed_mask |= key_mask
                    n_pressed_keys += 1
                    if not (self.pressed_mask & (1 << key_index)):
                        self.t_keydown[key_index] = self.t
                        self.queue.put(key_index)
                elif self.pressed_mask & (1 << key_index):
                    self.queue.put(0x80 | key_index)
                
            o.value = not self.selected_value
        self.pressed_mask = pressed_mask
        return n_pressed_keys

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

        pair_keys_state = 0
        # pending_key = 0xFF
        while True:
            n_pressed_keys = self.scan()
            n_events = len(self.queue)
            if not n_events:
                continue

            # detecting pair keys
            if n_pressed_keys == 1 and n_events == 1:
                if pair_keys_state == 0:
                    for mask in self.pair_keys_mask:
                        if self.pressed_mask & mask == self.pressed_mask:
                            pair_keys_state = 1
                            break
                    else:
                        pair_keys_state = -1
                
                
                if pair_keys_state > 0:
                    event = self.queue.preview()
                    dt = time.monotonic_ns() - self.t_keydown[event & 0x7F]
                    if  dt < 25000000:
                        # wait for a more event
                        continue
            elif n_pressed_keys == 2 and n_events == 2:
                if self.pressed_mask in self.pair_keys_mask:
                    multi_hit_index = self.pair_keys_mask.index(self.pressed_mask)
                    keycode = self.pair_keys_code[multi_hit_index]
                    print('multi hit {}'.format(multi_hit_index))
                    key = self.queue.get()
                    self.keys[key] = keycode
                    
                    # only one action
                    key = self.queue.get()
                    self.keys[key] = 0
                    
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
            
            pair_keys_state = 0
            while len(self.queue):
                event = self.queue.get()
                key = event & 0x7F
                if event & 0x80:
                    print('{} \\'.format(key))
                    keycode = self.keys[key]
                    dt = (self.t - self.t_keydown[key]) // 1000000
                    print('dt({}) = {}'.format(key, dt))
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
                else:
                    print('/ {}'.format(key))
                    keycode = self.keycode(key)
                    self.keys[key] = keycode
                    print('keycode {}'.format(keycode))
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

            if not ble.connected and not ble.advertising:
                ble.start_advertising(advertisement)
                ble.advertising = True

            # time.sleep(0.01)


def main():
    kbd = Keyboard()
    kbd.pair_keys = { L2: (S, D), L1: (J, K) }
    kbd.run()


if __name__ == '__main__':
    main()
