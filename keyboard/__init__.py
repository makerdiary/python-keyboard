import array
import time
import struct

import _bleio
import microcontroller
import usb_hid

import adafruit_ble
from adafruit_ble.advertising import Advertisement
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard import BatteryService
from adafruit_ble.services.standard.hid import HIDService

from .hid import HID
from .model import Matrix, COORDS, Backlight, battery_level
from .action_code import *


# fmt: off
KEY_NAME =  (
    'ESC', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'BACKSPACE',
    '|', ']', '[', 'P', 'O', 'I', 'U', 'Y', 'T', 'R', 'E', 'W', 'Q', 'TAB', 'CAPS',
    'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', '"', 'ENTER',
    'RSHIFT', '/', '.', ',', 'M', 'N', 'B', 'V', 'C', 'X', 'Z', 'LSHIFT',
    'LCTRL', 'LGUI', 'LALT', 'SPACE', 'RALT', 'MENU', 'FN', 'RCTRL'
)
# fmt: on


@micropython.asm_thumb
def mem(r0):
    """Read memory from the address"""
    ldr(r0, [r0, 0])


def usb_is_connected():
    return mem(0x40000438) == 0x3


def reset_into_bootloader():
    microcontroller.on_next_reset(microcontroller.RunMode.BOOTLOADER)
    microcontroller.reset()


class Device:
    def __init__(self, kbd):
        self.kbd = kbd
        self.backlight = kbd.backlight
        self.send_consumer = kbd.send_consumer
        self.wait = kbd.matrix.wait
        self.scan = kbd.matrix.scan
        self.suspend = kbd.matrix.suspend

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
    def __init__(self, keymap=(), pairs=(), verbose=True):
        self.keymap = keymap
        self.profiles = {}
        self.pairs = pairs
        self.verbose = verbose
        self.pairs_handler = lambda dev, n: None
        self.pair_keys = set()
        self.macro_handler = lambda dev, key, pressed: None
        self.layer_mask = 1
        self.matrix = Matrix()
        self.backlight = Backlight()
        self.uid = microcontroller.cpu.uid * 2
        self.usb_status = 0
        self.leds = None
        self.tap_delay = 500
        self.fast_type_thresh = 200
        self.pair_delay = 10

        self._connection = ""

        self.data = array.array("L", microcontroller.nvm[:272])
        if self.data[0] != 0x424B5950:
            self.data[0] = 0x424B5950
            self.data[1] = 1
            for i in range(4, 68):
                self.data[i] = 0
        self.ble_id = self.data[1]
        self.heatmap = memoryview(self.data)[4:]

        ble_hid = HIDService()
        self.battery = BatteryService()
        self.battery.level = battery_level()
        self.battery_update_time = time.time() + 360
        self.advertisement = ProvideServicesAdvertisement(ble_hid, self.battery)
        self.advertisement.appearance = 961
        self.ble = adafruit_ble.BLERadio()
        self.change_bt(self.ble_id)
        self.ble_hid = HID(ble_hid.devices)
        self.usb_hid = HID(usb_hid.devices)

    def update_connection(self):
        if usb_is_connected() and self.usb_status == 3:
            conn = "USB"
        else:
            conn = "BT%d" % self.ble_id
        if conn != self._connection:
            self._connection = conn
            if conn in self.action_maps:
                self.current_keymap = self.action_maps[self._connection]
            else:
                self.current_keymap = self.actonmap
            print("Connection changed to %s" % self._connection)

            # reset `layer_mask` when keymap is changed
            self.layer_mask = 1

    def check(self):
        if self.adv_timeout:
            if self.ble.connected:
                self.adv_timeout = 0
                self.backlight.set_bt_led(None)
                for c in self.ble.connections:
                    try:
                        # 11.25 ms is the min connection interval for most systems
                        c.connection_interval = 11.25
                    except Exception:
                        print("Failed to set ble connection interval")
                    # Avoid getting connection_interval, as it may block forever
                    # self.log('ble connection interval {}'.format(c.connection_interval))
            elif time.time() > self.adv_timeout:
                self.stop_advertising()

        leds = None
        if usb_is_connected():
            if self.usb_status == 0:
                self.usb_status = 3
            elif self.usb_status == 3:
                leds = self.usb_hid.leds
        elif self.usb_status > 0:
            self.usb_status = 0
            if not self.ble._adapter.advertising:
                self.start_advertising()

        if leds is None:
            leds = self.ble_hid.leds if self.ble.connected else 0
        if leds != self.leds:
            self.leds = leds
            self.backlight.set_hid_leds(leds)
            self.log("keyboard leds {}".format(bin(leds)))
        self.update_connection()

        # update battery level
        if time.time() > self.battery_update_time:
            self.battery_update_time = time.time() + 360
            self.battery.level = battery_level()

    def setup(self):
        convert = lambda a: array.array("H", (get_action_code(k) for k in a))
        self.actonmap = tuple(convert(layer) for layer in self.keymap)

        self.action_maps = {}
        for key in self.profiles:
            self.action_maps[key] = tuple(
                convert(layer) for layer in self.profiles[key]
            )

        for pair in self.pairs:
            for key in pair:
                self.pair_keys.add(key)
        self.update_connection()

    def start_advertising(self):
        self.ble.start_advertising(self.advertisement)
        self.backlight.set_bt_led(self.ble_id)
        self.adv_timeout = time.time() + 60

    def stop_advertising(self):
        try:
            self.backlight.set_bt_led(None)
            self.adv_timeout = 0
            self.ble.stop_advertising()
        except Exception as e:
            print(e)

    def get_key_sequence_info(self, start, end):
        """Get the info from a sequence of key events"""
        matrix = self.matrix
        event = matrix.view(start - 1)
        key = event & 0x7F
        desc = KEY_NAME[key]
        if event < 0x80:
            desc += " \\ "
            t0 = matrix.get_keydown_time(key)
        else:
            desc += " / "
            t0 = matrix.get_keyup_time(key)

        t = []
        for i in range(start, end):
            event = matrix.view(i)
            key = event & 0x7F
            desc += KEY_NAME[key]
            if event < 0x80:
                desc += " \\ "
                t1 = matrix.get_keydown_time(key)
            else:
                desc += " / "
                t1 = matrix.get_keyup_time(key)
            dt = matrix.ms(t1 - t0)
            t0 = t1
            t.append(dt)

        return desc, t

    def is_tapping_key(self, key):
        """Check if the key is tapped (press & release quickly)"""
        matrix = self.matrix
        n = len(matrix)
        if n == 0:
            n = matrix.wait(
                self.tap_delay - matrix.ms(matrix.time() - matrix.get_keydown_time(key))
            )
        target = key | 0x80
        if n >= 1:
            new_key = matrix.view(0)
            if new_key == target:
                return True
            if new_key >= 0x80:
                # Fast Typing - B is a tap-key
                #   A↓      B↓      A↑      B↑
                # --+-------+-------+-------+------> t
                #           |  dt1  |
                #         dt1 < tap_delay
                if self.verbose:
                    desc, t = self.get_key_sequence_info(-1, n)
                    print(desc)
                    print(t)
                return True

            if n == 1:
                n = matrix.wait(
                    self.fast_type_thresh
                    - matrix.ms(matrix.time() - matrix.get_keydown_time(new_key))
                )
        if n < 2:
            return False

        if target == matrix.view(1):
            # Fast Typing - B is a tap-key
            #   B↓      C↓      B↑      C↑
            # --+-------+-------+-------+------> t
            #   |  dt1  |  dt2  |
            # dt1 < tap_delay && dt2 < fast_type_thresh
            if self.verbose:
                desc, t = self.get_key_sequence_info(-1, n)
                print(desc)
                print(t)
            return True

        if self.verbose:
            desc, t = self.get_key_sequence_info(-1, n)
            print(desc)
            print(t)

        return False

    def change_bt(self, n):
        if self.ble.connected:
            for c in self.ble.connections:
                c.disconnect()
        if self.ble._adapter.advertising:
            self.ble.stop_advertising()

        if 0 > n or n > 9:
            return

        uid = self.uid[n : n + 6]
        uid[-1] = uid[-1] | 0xC0
        address = _bleio.Address(uid, _bleio.Address.RANDOM_STATIC)
        try:
            self.ble._adapter.address = address
            name = "PYKB {}".format(n)
            self.advertisement.complete_name = name
            self.ble.name = name
            self.ble_id = n
            if self.data[1] != n:
                self.data[1] = n
                microcontroller.nvm[:272] = struct.pack("68L", *self.data)
        except Exception as e:
            print(e)
        self.log(self.ble._adapter.address)
        self.start_advertising()

    def toggle_bt(self):
        if self.ble.connected:
            for c in self.ble.connections:
                c.disconnect()
        elif self.ble._adapter.advertising:
            self.stop_advertising()
        else:
            self.start_advertising()
        self.update_connection()

    def toggle_usb(self):
        if usb_is_connected():
            if self.usb_status == 1:
                self.usb_status = 3
            else:
                self.usb_status = 1
        self.update_connection()

    def action_code(self, position):
        position = COORDS[position]
        layer_mask = self.layer_mask
        for layer in range(len(self.current_keymap) - 1, -1, -1):
            if (layer_mask >> layer) & 1:
                code = self.current_keymap[layer][position]
                if code == 1:  # TRANSPARENT
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
        try:
            if self.usb_status == 0x3 and usb_is_connected():
                self.usb_hid.press(*keycodes)
                return
        except Exception as e:
            print(e)

        try:
            if self.ble.connected:
                self.ble_hid.press(*keycodes)
            elif not self.ble._adapter.advertising:
                self.start_advertising()
        except Exception as e:
            print(e)

    def release(self, *keycodes):
        try:
            if self.usb_status == 0x3 and usb_is_connected():
                self.usb_hid.release(*keycodes)
                return
        except Exception as e:
            print(e)

        try:
            if self.ble.connected:
                self.ble_hid.release(*keycodes)
        except Exception as e:
            print(e)

    def send_consumer(self, keycode):
        try:
            if self.usb_status == 0x3 and usb_is_connected():
                self.usb_hid.send_consumer(keycode)
                return
        except Exception as e:
            print(e)

        try:
            if self.ble.connected:
                self.ble_hid.send_consumer(keycode)
        except Exception as e:
            print(e)

    def get(self):
        event = self.matrix.get()
        key = event & 0x7F
        pressed = event < 0x80
        if pressed:
            self.heatmap[key] += 1
        self.backlight.handle_key(key, pressed)
        return event

    def run(self):
        self.setup()
        log = self.log
        matrix = self.matrix
        dev = Device(self)
        keys = [0] * matrix.keys
        ms = matrix.ms
        last_time = 0
        while True:
            t = 20 if self.backlight.check() else 1000
            n = matrix.wait(t)
            self.check()
            if n == 0:
                continue

            # detecting pair keys
            if n == 1:
                key = matrix.view(0)
                if key < 0x80 and key in self.pair_keys:
                    n = matrix.wait(
                        self.pair_delay
                        - ms(matrix.time() - matrix.get_keydown_time(key))
                    )

            if n >= 2:
                pair = {matrix.view(0), matrix.view(1)}
                if pair in self.pairs:
                    pair_index = self.pairs.index(pair)
                    key1 = self.get()
                    key2 = self.get()

                    dt = ms(
                        matrix.get_keydown_time(key2) - matrix.get_keydown_time(key1)
                    )
                    log("pair keys {} {}, dt = {}".format(pair_index, pair, dt))
                    try:
                        self.pairs_handler(dev, pair_index)
                    except Exception as e:
                        print(e)

            while len(matrix):
                event = self.get()
                key = event & 0x7F
                if event & 0x80 == 0:
                    action_code = self.action_code(key)
                    keys[key] = action_code
                    if action_code < 0xFF:
                        self.press(action_code)
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
                            if self.is_tapping_key(key):
                                log("TAP")
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
                            layer = (action_code >> 8) & 0x1F
                            mask = 1 << layer
                            if action_code & 0xE0 == 0xC0:
                                log("LAYER_MODS")
                                mods = action_code & 0x1F
                                keycodes = mods_to_keycodes(mods)
                                self.press(*keycodes)
                                self.layer_mask |= mask
                            elif self.is_tapping_key(key):
                                log("TAP")
                                keycode = action_code & 0xFF
                                if keycode == OP_TAP_TOGGLE:
                                    log("TOGGLE {}".format(layer))
                                    self.layer_mask = (self.layer_mask & ~mask) | (
                                        mask & ~self.layer_mask
                                    )
                                    keys[key] = 0
                                else:
                                    keys[key] = keycode
                                    self.press(keycode)
                            else:
                                self.layer_mask |= mask

                            log("layers {}".format(self.layer_mask))
                        elif kind == ACT_MACRO:
                            if callable(self.macro_handler):
                                i = action_code & 0xFFF
                                try:
                                    self.macro_handler(dev, i, True)
                                except Exception as e:
                                    print(e)
                        elif kind == ACT_BACKLIGHT:
                            if action_code == RGB_MOD:
                                self.backlight.next()
                        elif kind == ACT_COMMAND:
                            if action_code == BOOTLOADER:
                                reset_into_bootloader()
                            elif action_code == SUSPEND:
                                matrix.suspend()
                            elif action_code == SHUTDOWN:
                                microcontroller.reset()
                            elif action_code == HEATMAP:
                                microcontroller.nvm[:272] = struct.pack(
                                    "68L", *self.data
                                )
                                if usb_is_connected():
                                    microcontroller.reset()
                            elif action_code == USB_TOGGLE:
                                self.toggle_usb()
                            elif action_code == BT_TOGGLE:
                                self.toggle_bt()
                            elif BT(0) <= action_code and action_code <= BT(9):
                                i = action_code - BT(0)
                                log("switch to bt {}".format(i))
                                self.change_bt(i)

                    if self.verbose:
                        keydown_time = matrix.get_keydown_time(key)
                        dt = ms(matrix.time() - keydown_time)
                        dt2 = ms(keydown_time - last_time)
                        last_time = keydown_time
                        print(
                            "{} {} \\ {} latency {} | {}".format(
                                key, KEY_NAME[key], hex(action_code), dt, dt2
                            )
                        )
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
                            layer = (action_code >> 8) & 0x1F
                            keycode = action_code & 0xFF
                            if keycode & 0xE0 == 0xC0:
                                log("LAYER_MODS")
                                mods = keycode & 0x1F
                                keycodes = mods_to_keycodes(mods)
                                self.release(*keycodes)
                            self.layer_mask &= ~(1 << layer)
                            log("layers {}".format(self.layer_mask))
                        elif kind == ACT_MACRO:
                            i = action_code & 0xFFF
                            try:
                                self.macro_handler(dev, i, False)
                            except Exception as e:
                                print(e)

                    if self.verbose:
                        keyup_time = matrix.get_keyup_time(key)
                        dt = ms(matrix.time() - keyup_time)
                        dt2 = ms(keyup_time - last_time)
                        last_time = keyup_time
                        print(
                            "{} {} / {} latency {} | {}".format(
                                key, KEY_NAME[key], hex(action_code), dt, dt2
                            )
                        )
