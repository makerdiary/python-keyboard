class Backlight:
    def __init__(self):
        self.hue = 0
        self.sat = 255
        self.val = 255

    def on(self, r=0xFF, g=0xFF, b=0xFF):
        pass

    def off(self):
        pass

    def set_brightness(self, v):
        pass

    def pixel(self, i, r, g, b):
        pass

    def set_hid_leds(self, v):
        pass

    def set_bt_led(self, v):
        pass

    def update(self):
        pass

    def check(self):
        return False

    def next(self):
        pass

    def handle_key(self, key, pressed):
        pass

    def toggle(self):
        pass

    def set_mode(self, mode):
        pass
