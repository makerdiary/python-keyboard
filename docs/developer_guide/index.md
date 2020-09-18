# Dive Into Keyboard

Normally, you only need to change `code.py` to configure the keyboard.
If you are very good at Python and have a new idea which can not be implemented in `code.py`,
you can modify [the `keyboard` library](https://github.com/makerdiary/python-keyboard/tree/main/keyboard).


!!! Note
    When you modify the `keyboard` library, the keyboard may stop working if there is any syntax error or other error in the code. You will need another keyboard to fix it. If you get a fatal error, you can always do a [factory reset](../factory_reset.md).

By default, The CircuitPython firmware of M60 has two frozen modules - [`adafruit_ble`](https://github.com/adafruit/Adafruit_CircuitPython_BLE) and `PYKB`. `PYKB` is a frozen version of the `keyboard` library.

## Use latest `keyboard` library
1. Copy `keyboard` folder of [python-keyboard](https://github.com/makerdiary/python-keyboard/tree/main/keyboard) to the `lib` directory of the `CIRCUITPY` USB drive.
2. Replace `from PYKB import *` to `from keyboard import *` in `code.py` of the USB drive.


## Develop with C/C++, Rust, JerryScript, TinyGo
The M60 keybaord also supports C/C++, Rust, JerryScript and TinyGo. To create your own firmware, read [the hardware information](hardware.md) to get started.