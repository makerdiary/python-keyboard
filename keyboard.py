import time
import usb_hid

import adafruit_ble
from adafruit_ble.advertising import Advertisement
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.hid import HIDService
from adafruit_hid.keyboard import keyboard

from keycodes import *
from matrix import Matrix, LAYOUT


___ = TRANSPARENT
L1  = LAYER_TAP(1)
L2D = LAYER_TAP(2, D)
PGUP = PAGEUP
PGDN = PAGEDOWN

KEYMAP = (
    # layer 0
    LAYOUT(
        ESC,  1,  2,  3,  4,  5,  6,  7,  8,  9,  0, '-', '=', BACKSPACE,
         TAB,  Q,  W,  E,  R,  T,  Y,  U,  I,  O,  P, '[', ']', '|',
         CAPS,  A,  S,L2D,  F,  G,  H,  J,  K,  L,';', '"',   ENTER,
        LSHIFT,  Z,  X,  C,  V,  B,  N,  M,',','.','/',      RSHIFT,
        LCTRL, LGUI, LALT,     SPACE,      RALT, MENU,  L1, RCTRL
    ),

    # layer 1
    LAYOUT(
        '`', F1, F2, F3, F4, F5, F6, F7, F8, F9, F10, F11, F12, DEL,
        ___,___,  UP,___,___,___,___,___,___,___,___, ___, ___, ___,
         ___,LEFT,DOWN,RIGHT,___,___,___,___,___,___,___,___,   ___,
          ___,___,___,___,___,___,___,___,___,___,___, ___,     ___,
        ___,___,___,           ___,             ___, ___, ___,  ___
    ),

    # layer 2
    LAYOUT(
        '`', F1, F2, F3, F4, F5, F6, F7, F8, F9, F10, F11, F12, DEL,
        ___,___,___,___,___,___,___,PGUP,___,___,___, ___, ___, ___,
         ___,___,___,___,___,___,LEFT,DOWN,UP,RIGHT,___,___,   ___,
          ___,___,___,___,___,___,PGDN,___,___,___,___, ___,    ___,
        ___,___,___,          ___,             ___, ___, ___,  ___
    )
)


class Kbd:
    keymap = KEYMAP

    def __init__(self):
        self.layers = 1

    def keycode(self, key):
        for layer in range(len(self.keymap) - 1, -1, -1):
            if (self.layers >> layer) & 1:
                id = ord(self.keymap[layer][key])
                if id == ord(TRANSPARENT):
                    continue
                return KEYCODE(id) if id < 128 else id
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
        advertising = True
        ble_keyboard = Keyboard(hid.devices)
        
        matrix = Matrix()
        usb_keyboard = Keyboard(usb_hid.devices)

        keys = {}
        pending_keys = []
        while True:
            _, released_keys, new_keys = matrix.scan()
            t = time.monotonic_ns()
            if released_keys:
                print('< {}'.format(released_keys))
                for key in released_keys:
                    keycode = keys[key][0]
                    dt = (t - keys[key][1]) // 1000000
                    print('dt({}) = {}'.format(key, dt))
                    if 0 < keycode and keycode < 0xE8:
                        usb_keyboard.release(keycode)
                        if ble.connected:
                            advertising = False
                            ble_keyboard.release(keycode)
                    elif keycode & 0xF000 == 0xF000:
                        if key in pending_keys:
                            pending_keys.remove(key)
                            key = keycode & 0xFF
                            code = KEYCODE(key)
                            if dt < 500 and code:
                                usb_keyboard.press(code)
                                usb_keyboard.release(code)
                                if ble.connected:
                                    advertising = False
                                    ble_keyboard.press(code)
                                    ble_keyboard.release(code)
                                
                        else:
                            self.layers &= ~(1 << ((keycode >> 8) & 0xF))
                            print('layers {}'.format(self.layers))
            if new_keys:
                print('> {}'.format(new_keys))
                for key in new_keys:
                    while pending_keys:
                        pending_key = pending_keys.pop(0)
                        pending_keycode = keys[pending_key][0]
                        if pending_keycode & 0xF000 == 0xF000:
                            self.layers |= 1 << ((pending_keycode >> 8) & 0xF)
                            print('layers {}'.format(self.layers))

                    keycode = self.keycode(key)
                    keys[key] = (keycode, t)
                    print('keycode {}'.format(keycode))

                    if 0 < keycode and keycode < 0xFF:
                        usb_keyboard.press(keycode)
                        if ble.connected:
                            advertising = False
                            ble_keyboard.press(keycode)
                    elif keycode & 0xF000 == 0xF000:
                        # LAYER_TAP
                        pending_keys.append(key)
                    elif keycode & 0xF000 == 0xE000:
                        # LAYER_MODS
                        pass
                    elif keycode & 0xF000 == 0xD000:
                        # MODS_TAP
                        pass
                
            if not ble.connected and not advertising:
                ble.start_advertising(advertisement)
                advertising = True

            time.sleep(0.01)


def main():
    kbd = Kbd()
    kbd.run()


if __name__ == '__main__':
    main()
