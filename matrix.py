
from board import *
import digitalio


ROWS = (P27, P13, P30, P20, P3)
COLS = (P26, P31, P29, P28, P5, P4, P24, P25, P23, P22, P14, P15, P16, P17)


def LAYOUT(*args):
    REMAP = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,
        14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
        28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,  0, 40,
        41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51,  0, 52,  0,
        53, 55, 54,  0,  0, 56,  0,  0, 57, 58, 59, 60)

    f = lambda c: str(c) if type(c) is int else c

    return ''.join(( f(args[c]) for c in REMAP))


class Matrix:

    def __init__(self, rows=ROWS, cols=COLS, row2col=True):
        self.rows = []
        for pin in rows:
            io = digitalio.DigitalInOut(pin)
            io.direction = digitalio.Direction.OUTPUT
            io.drive_mode = digitalio.DriveMode.PUSH_PULL
            io.value = 0
            self.rows.append(io)
            
        self.cols = []
        for pin in cols:
            io = digitalio.DigitalInOut(pin)
            io.direction = digitalio.Direction.INPUT
            io.pull = digitalio.Pull.DOWN if row2col else digitalio.Pull.UP
            self.cols.append(io)

        self.selected_value = bool(row2col)
        self.pressed_keys = []
    
    def scan(self):
        new_keys = []
        pressed_keys = []
        released_keys = self.pressed_keys
        for r in range(len(self.rows)):
            self.rows[r].value = self.selected_value
            for c in range(len(self.cols)):
                if self.cols[c].value == self.selected_value:
                    key = r * len(self.cols) + c
                    pressed_keys.append(key)
                    if key in released_keys:
                        released_keys.remove(key)
                    else:
                        new_keys.append(key)
            self.rows[r].value = not self.selected_value
        self.pressed_keys = pressed_keys
        return pressed_keys, released_keys, new_keys
