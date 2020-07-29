
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.mouse import Mouse


class HID:
    def __init__(self, devices):
        self.keyboard = Keyboard(devices)
        self.consumer_control = ConsumerControl(devices)
        # self.mouse = Mouse(devices)

        self.send = self.keyboard.send
        self.press = self.keyboard.press
        self.release = self.keyboard.release

        self.send_consumer = self.consumer_control.send
