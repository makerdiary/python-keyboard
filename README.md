Python Keyboard
===============

  中文 | [English][1]
------|--------------

这是一个手焊的 USB 和蓝牙双模键盘，还是一个里面跑 Python 的键盘


![](img/python-inside-keyboard.png)

![](img/colorful-keycaps.jpg)


## 自己动手造键盘
1.  [手焊键盘](hardware.md)
2.  参考 [Pitaya Go 下载教程](https://wiki.makerdiary.com/pitaya-go/programming/) 更新 [CircuitPython 固件](circuitpython-5.3.0-for-pitaya-go.hex)，固件更新之后，Pitaya Go 会在电脑端模拟出一个名为 `CIRCUITPY` 的 U 盘和一个串口
3.  下载两个 CircuitPython 库 - [adafruit-ble](https://github.com/adafruit/Adafruit_CircuitPython_BLE) & [adafruit-hid](https://github.com/adafruit/Adafruit_CircuitPython_HID)，然后它们放在 `CIRCUITPY` U 盘的 `lib` 目录，U 盘内容结构，如下：

    ```
    CIRCUITPY
    ├───code.py
    └───lib
        ├───adafruit_ble
        └───adafruit_hid
    ```

4.  把以下 Python 代码拷贝到 `code.py`，保存之后 `code.py` 会被重新加载运行，这时你就得到了一个 USB + 蓝牙的双模键盘


    ```python
    import time
    from board import *
    import digitalio
    import usb_hid

    import adafruit_ble
    from adafruit_ble.advertising import Advertisement
    from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
    from adafruit_ble.services.standard.hid import HIDService
    from adafruit_hid.keyboard import Keyboard
    from adafruit_hid.keycode import Keycode as _

    ROWS = (P27, P13, P30, P20, P3)
    COLS = (P26, P31, P29, P28, P5, P4, P24, P25, P23, P22, P14, P15, P16, P17)

    KEYMAP = (_.ESCAPE, _.ONE, _.TWO, _.THREE, _.FOUR, _.FIVE, _.SIX, _.SEVEN, _.EIGHT, _.NINE, _.ZERO, _.MINUS, _.EQUALS, _.BACKSPACE,
            _.TAB, _.Q, _.W, _.E, _.R, _.T, _.Y, _.U, _.I, _.O, _.P, _.LEFT_BRACKET, _.RIGHT_BRACKET, _.BACKSLASH,
            _.CAPS_LOCK, _.A, _.S, _.D, _.F, _.G, _.H, _.J, _.K, _.L, _.SEMICOLON, _.QUOTE, None, _.ENTER,
            _.LEFT_SHIFT, _.Z, _.X, _.C, _.V, _.B, _.N, _.M, _.COMMA, _.PERIOD, _.FORWARD_SLASH, None, _.RIGHT_SHIFT, None,
            _.LEFT_CONTROL, _.LEFT_ALT, _.LEFT_GUI, None, None, _.SPACE, None, None, _.RIGHT_ALT, _.RIGHT_GUI, _.APPLICATION, _.RIGHT_CONTROL, None, None)

    class Matrix:
        def __init__(self, rows=ROWS, cols=COLS):
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
                io.pull = digitalio.Pull.DOWN
                self.cols.append(io)
            self.pressed_keys = []

        def scan(self):
            new_keys = []
            pressed_keys = []
            released_keys = self.pressed_keys
            for r in range(len(self.rows)):
                self.rows[r].value = 1
                for c in range(len(self.cols)):
                    if self.cols[c].value:
                        key = r * len(self.cols) + c
                        pressed_keys.append(key)
                        if key in released_keys:
                            released_keys.remove(key)
                        else:
                            new_keys.append(key)
                self.rows[r].value = 0
            self.pressed_keys = pressed_keys
            return pressed_keys, released_keys, new_keys

    def main():
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

        while True:
            pressed_keys, released_keys, new_keys = matrix.scan()
            if released_keys:
                released_keycodes = list(map(lambda i: KEYMAP[i], released_keys))
                print('released keys {}'.format(released_keycodes))

                usb_keyboard.release(*released_keycodes)
                if ble.connected:
                    advertising = False
                    ble_keyboard.release(*released_keycodes)
            if new_keys:
                new_keycodes = list(map(lambda i: KEYMAP[i], new_keys))
                print('new keys {}'.format(new_keycodes))
                usb_keyboard.press(*new_keycodes)
                if ble.connected:
                    advertising = False
                    ble_keyboard.press(*new_keycodes)

            if not ble.connected and not advertising:
                ble.start_advertising(advertisement)
                advertising = True

            time.sleep(0.001)

    if __name__ == '__main__':
        main()
    ```

    如果你的键盘矩阵连接到 Pitaya Go 的 IO 有所不同， 你需要要更改代码中 `ROWS` 和 `COLS`


## 更进一步——让键盘更具生产力
这是一个 60% 键盘，缺少了包括 F1~F12、 方向键、小键盘等键位。

但通过引入[ TMK ](https://github.com/tmk/tmk_keyboard/blob/master/tmk_core/doc/keymap.md)中的层级切换和组合按键功能，并融入 [Toward a more useful keyboard](https://github.com/jasonrudolph/keyboard) 中把手指尽量停留在 <kbd>A</kbd>、<kbd>S</kbd>、<kbd>D</kbd>、<kbd>F</kbd> 和 <kbd>J</kbd>、<kbd>K</kbd>、<kbd>L</kbd>、<kbd>;</kbd> 等起始键位的理念，我们可以让这个小键盘更具生产力。

这里引入 Tap-key 功能，即按某个按键不放激活另外的功能。

比如把 <kbd>d</kbd> 用作 Tap-key，即短按 <kbd>d</kbd> 输出 <kbd>d</kbd>， 按住 <kbd>d</kbd> 不放则激活移动光标功能，<kbd>H</kbd>、<kbd>J</kbd>、<kbd>K</kbd>、<kbd>L</kbd>被映射为方向键，而 <kbd>U</kbd> 和 <kbd>N</kbd> 则为 <kbb>PgUp</kbd> 和 <kbd>PgDn</kbd>。

![](img/d-for-navigation.png)

+ <kbd>d</kbd> + <kbd>h</kbd> → <kbd>←</kbd>
+ <kbd>d</kbd> + <kbd>j</kbd> → <kbd>↓</kbd>
+ <kbd>d</kbd> + <kbd>k</kbd> → <kbd>↑</kbd>
+ <kbd>d</kbd> + <kbd>l</kbd> → <kbd>→</kbd>
+ <kbd>d</kbd> + <kbd>u</kbd> → <kbd>PgUp</kbd>
+ <kbd>d</kbd> + <kbd>n</kbd> → <kbd>PgDn</kbd>

要实现这个功能，把 `keyboard.py` 和 `action_code.py` 复制到 `CIRCUITPY` U 盘中，然后将 `code.py` 修改为：

```python
# code.py

from keyboard import main

main()
```

另外，这个 Python 键盘还支持了同时按下两个按键 (间隔不超过25ms) 激活特殊功能，也计划支持长按 <kbd>;</kbd> 用作 <kbd>Ctrl</kbd>，用 <kbd>;</kbd> + <kbd>c</kbd> 替代 <kbd>Ctrl</kbd> + <kbd>c</kbd>，在 VS Code 中使用很方便。

## Todo
+ 长按 <kbd>;</kbd> 用作 <kbd>Ctrl</kbd>
+ 宏功能
+ 优化速度


[1]: https://github.com/makerdiary/python-keyboard
