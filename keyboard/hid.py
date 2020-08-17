
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.mouse import Mouse


class HID:
    def __init__(self, devices):
        self.keyboard = Keyboard(devices)
        self.consumer_control = ConsumerControl(devices)
        # self.mouse = Mouse(devices)

        for device in devices:
            if hasattr(device, '_characteristic') and device.usage_page == 0x1 and device.usage == 0x6:
                self._leds = device._characteristic
                break
        else:
            self._leds = None

        self.send = self.keyboard.send
        self.press = self.keyboard.press
        self.release = self.keyboard.release

        self.send_consumer = self.consumer_control.send

    @property
    def leds(self):
        if self._leds:
            return self._leds.value[0]
        return 0
