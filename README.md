PYKB - Python Keyboard
======================

 English | [中文][1]
---------|----------

Create a hand-wired keyboard, run Python on it, turn it into production.

![](img/python-inside-keyboard.png)

## Hand-wiring a keyboard
Follow [the guide - hand-wiring-a-keyboard.md](hand-wiring-a-keyboard.md) to rapidly make a keyboard with 100 lines of Python code.

![](img/colorful-keycaps.jpg)

## From prototype to production <sup><kbd>in progress</kbd></sup>
With putting more time into the Python keyboard, we find it more and more interesting. We think a Python keyboard can make a big difference, so we decide to design a new keyboard for everyone. Check out [the M60 mechanical keyboard](https://makerdiary.com/m60).

[![](img/m60.jpg)](https://makerdiary.com/m60)

## To be a productive keyboard
As the 60% keyboard lacks a lot of keys (F1~F12, arrow keys and etc). We can use
[features like TMK's layers and composite keys](https://github.com/tmk/tmk_keyboard/blob/master/tmk_core/doc/keymap.md) to make the small keyboard much more powerful.
With the idea from [Toward a more useful keyboard](https://github.com/jasonrudolph/keyboard) to keep our fingers at the home row, we can optimize the keyboard to make us more productive.

Adding the Tap-key feature, which is holding a key down to activate an alternate function, can make a big difference.

### Using <kbd>D</kbd> for Navigation

Taping <kbd>d</kbd> outputs <kbd>d</kbd> (press & release quickly), holding <kbd>d</kbd> down activates navigation functions.

![](img/d-for-navigation.png)

+ <kbd>d</kbd> + <kbd>h</kbd> as <kbd>←</kbd>
+ <kbd>d</kbd> + <kbd>j</kbd> as <kbd>↓</kbd>
+ <kbd>d</kbd> + <kbd>k</kbd> as <kbd>↑</kbd>
+ <kbd>d</kbd> + <kbd>l</kbd> as <kbd>→</kbd>
+ <kbd>d</kbd> + <kbd>u</kbd> as <kbd>PageUp</kbd>
+ <kbd>d</kbd> + <kbd>n</kbd> as <kbd>PageDown</kbd>


### Using <kbd>;</kbd> as <kbd>Ctrl</kbd>
Use <kbd>;</kbd> as a MODS_TAP key, taping <kbd>;</kbd> outputs <kbd>;</kbd>, holding <kbd>;</kbd> down outputs <kbd>Ctrl</kbd>.

![](https://github.com/xiongyihui/keyboard/raw/master/img/semicolon_as_ctrl.png)


### Using Pair-keys
Simultaneously pressing two keys (interval less than 10ms) activates an alternate function.

### Optimizing with C modules<sup><kbd>in progress</kbd></sup>

A C module `matrix` of keyboard matrix is written to reduce latency and power consumption. The module has the same function as [`keyboard/matrix.py`](keyboard/matrix.py).


## Todo
- [ ] add system keys
- [ ] add mouse keys


## Credits
+ [MicroPython](https://github.com/micropython/micropython)
+ [CircuitPython](https://github.com/adafruit/circuitpython)
+ [TMK](https://github.com/tmk/tmk_keyboard)
+ [Toward a more useful keyboard](https://github.com/jasonrudolph/keyboard)


[1]: https://gitee.com/makerdiary/python-keyboard
