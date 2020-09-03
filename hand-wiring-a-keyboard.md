Hand-wiring a Keyboard
======================

这里介绍怎么手焊一个键盘，并用100多行Python代码实现USB蓝牙双模键盘。

![](img/python-inside-keyboard.png)

## 准备材料
+ 黄铜线5米+（直径0.8mm），也可以用普通导线，但黄铜更酷一些
+ 定位板，选了60%的，因为选择多，键还少~ （比如睫毛外设的铝合金卫星轴定位板）
+ 平衡杆或卫星轴，因为不用PCB，只能选定位板类型的
+ 轴61个，为了办公室炫耀（挨打），当然选清脆（扰人）的青轴啦
+ 二极管61个，这是防多按键冲突（Anti-ghost），如果很少用3及以上键同时按的组合键（比如 ctrl + shift + c），这个可以省掉（立创商城购买挺方便）
+ 还需要个带蓝牙和USB的主控 [Pitaya Go](https://github.com/makerdiary/pitaya-go)，后面Python就跑在这个开发板里面


## 工具
+ 烙铁、焊锡
+ 钳子，用来剪黄铜线
+ 镊子
+ 万用表，如果眼力足够好，这也可以省掉~

## 手焊键盘
1.  安装卫星轴

    把卫星轴安装在定位板上，可以用润滑脂把润滑一下，可以减少按键的噪声，润滑脂是半固体状的，不是润滑油。也可也用平衡杆替代卫星轴。

    ![](https://gitee.com/makerdiary/python-keyboard/raw/master/img/grease.jpg)

2.  安装键轴

    把键轴安装在定位板上

    ![](https://gitee.com/makerdiary/python-keyboard/raw/master/img/switch.jpg)

3.  焊接矩阵键盘

    矩阵键盘分行、列，先把用二极管把轴的一个脚跟行线连接，并焊接好，二极管的方向可以行到列，也可以是列到行，但整个矩阵要保持二极管的方向一致。

    
    ![](img/rows2.jpg)

    ![](img/rows.jpg)

    把焊好一条行线后，可以用万用表测一下二极管的方向是否都是一致的，或者是否有虚焊。这里用的是黑色贴片二极管，因为小，肉眼分辨方向相当考验眼力，特别是焊接之后还有焊迹。也可以选用插件的二极管，焊接更简单一些。

    ![](img/rows-cols.jpg)

4.  将行、列线连接到主控 Pitaya Go 的IO口

    ![](img/pitaya-go.jpg)

    这里矩阵键盘有5行、14列，Pitaya Go有20个可用的IO，剩下的1个IO还可以接个灯。矩阵键盘和主控焊接完成后，最好用万用表检测一下各行各列是否短接，至少目测一下。

## 键盘里跑Python

1.  参考 [Pitaya Go 下载教程](https://wiki.makerdiary.com/pitaya-go/programming/) 更新 [CircuitPython 固件](https://gitee.com/makerdiary/python-keyboard/raw/master/circuitpython-5.3.0-for-pitaya-go.hex)，固件更新之后，Pitaya Go 会在电脑端模拟出一个名为 `CIRCUITPY` 的 U 盘和一个串口
2.  下载两个 CircuitPython 库 - [adafruit-ble](https://github.com/adafruit/Adafruit_CircuitPython_BLE) & [adafruit-hid](https://github.com/adafruit/Adafruit_CircuitPython_HID)，然后它们放在 `CIRCUITPY` U 盘的 `lib` 目录，U 盘内容结构，如下：

    ```
    CIRCUITPY
    ├───code.py
    └───lib
        ├───adafruit_ble
        └───adafruit_hid
    ```

3.  把以下 Python 代码拷贝到 `code.py`，保存之后 `code.py` 会被重新加载运行，这时你就得到了一个 USB + 蓝牙的双模键盘


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

    main()
    ```

    如果你的键盘矩阵连接到 Pitaya Go 的 IO 有所不同， 你需要要更改代码中 `ROWS` 和 `COLS`


![](img/colorful-keyboard.jpg)
