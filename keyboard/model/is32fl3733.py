import board
import busio
import digitalio
import microcontroller


class IS31FL3733:
    def __init__(self, address=0x50):
        self.address = address
        self._page = None
        self._buffer = bytearray(12 * 16 + 1)
        self.pixels = memoryview(self._buffer)[1:]

        self.power = digitalio.DigitalInOut(microcontroller.pin.P1_04)
        self.power.direction = digitalio.Direction.OUTPUT
        self.power.value = 1

        self.i2c = board.I2C()
        self.i2c.try_lock()
        # print(self.i2c.scan())

        self.reset()
        self.setup()
        # print(self.open_pixels())
        # print(self.short_pixels())

    def page(self, n):
        if self._page is n:
            return
        self._page = n
        self.write(0xFE, 0xC5)
        self.write(0xFD, n)

    def reset(self):
        # read reset register (0x11) of page 3 to reset
        self.page(3)
        self.read(0x11)

    def setup(self):
        self.page(3)
        self.write(2, (2 << 5) | (0 << 1))
        self.write(3, (2 << 5) | (3 << 1))
        self.write(4, (0 << 4))

        self.write(6, (2 << 5) | (0 << 1))
        self.write(7, (2 << 5) | (2 << 1))
        self.write(8, (0 << 4))

        self.write(0xA, (1 << 5) | (0 << 1))
        self.write(0xB, (1 << 5) | (1 << 1))
        self.write(0xC, (0 << 4))

        self.write(0, 1)
        self.write(0, 3)
        self.write(0xE, 0)

        self.page(0)
        self.write(0, [255] * 0x18)

        self.set_brightness(255)

    def set_brightness(self, n):
        if not self.power.value:
            self.power.value = 1

        # Global Current Control register (0x01) of page 3
        self.page(3)
        self.write(1, n)

    def pixel(self, i, r, g, b):
        row = i >> 4  # i // 16
        col = i & 15  # i % 16
        self.pixels[row * 48 + col] = g
        self.pixels[row * 48 + 16 + col] = r
        self.pixels[row * 48 + 32 + col] = b

    def update_pixel(self, i, r, g, b):
        row = i >> 4  # i // 16
        col = i & 15  # i % 16
        self.pixels[row * 48 + col] = g
        self.pixels[row * 48 + 16 + col] = r
        self.pixels[row * 48 + 32 + col] = b
        if not self.power.value:
            self.power.value = 1
        self.page(1)
        self.write(row * 48 + col, g)
        self.write(row * 48 + 16 + col, r)
        self.write(row * 48 + 32 + col, b)

    def update(self):
        if not self.power.value:
            self.power.value = 1
        self.page(1)
        self.i2c.writeto(self.address, self._buffer)

    def any(self):
        """Check if any pixel is not zero"""
        for pixel in self.pixels:
            if pixel > 0:
                return True
        return False

    def write(self, register, value):
        if type(value) is int:
            self.i2c.writeto(self.address, bytearray((register, value)))
        else:
            value.insert(0, register)
            buffer = bytearray(value)

            self.i2c.writeto(self.address, buffer)

    def read(self, register):
        buffer = bytearray(1)
        self.i2c.writeto_then_readfrom(self.address, bytearray((register,)), buffer)
        return buffer[0]

    def breathing_pixel(self, i, mode=2):
        if not self.power.value:
            self.power.value = 1
        self.page(2)
        row = i >> 4  # i // 16
        col = i & 15  # i % 16
        self.write(row * 48 + 32 + col, mode)  # blue
        # self.write(row * 48 + col, mode)         # green
        # self.write(row * 48 + 16 + col, mode)    # red

    def open_pixels(self):
        # 18h ~ 2Fh LED Open Register
        self.page(0)
        buffer = bytearray(0x18)
        self.i2c.writeto_then_readfrom(self.address, bytearray((0x18,)), buffer)
        return buffer

    def short_pixels(self):
        # 30h ~ 47h LED Short Register
        self.page(0)
        buffer = bytearray(0x18)
        self.i2c.writeto_then_readfrom(self.address, bytearray((0x30,)), buffer)
        return buffer
