# Keyboard Configuration

M60 is not just a USB HID device, but also a USB storage device. Python code can be saved and executed in the keyboard. When the keyboard powers on, it will run the Python file `code.py` in its USB storage.
In `code.py`, we can modify its keymap, add a macro and add a new feature to keyboard.

![](https://gitee.com/makerdiary/python-keyboard/raw/resource/img/CIRCUITPY.png)

The default content of `code.py` is:

```python

from PYKB import *


keyboard = Keyboard()

___ = TRANSPARENT
BOOT = BOOTLOADER
L1 = LAYER_TAP(1)
L2D = LAYER_TAP(2, D)
L3B = LAYER_TAP(3, B)
LSFT4 = LAYER_MODS(4, MODS(LSHIFT))
RSFT4 = LAYER_MODS(4, MODS(RSHIFT))

# Semicolon & Ctrl
SCC = MODS_TAP(MODS(RCTRL), ';')

keyboard.keymap = (
    # layer 0
    (
        ESC,   1,   2,   3,   4,   5,   6,   7,   8,   9,   0, '-', '=', BACKSPACE,
        TAB,   Q,   W,   E,   R,   T,   Y,   U,   I,   O,   P, '[', ']', '|',
        CAPS,  A,   S, L2D,   F,   G,   H,   J,   K,   L, SCC, '"',    ENTER,
        LSFT4, Z,   X,   C,   V, L3B,   N,   M, ',', '.', '/',         RSFT4,
        LCTRL, LGUI, LALT,          SPACE,            RALT, MENU,  L1, RCTRL
    ),

    # layer 1
    (
        '`',  F1,  F2,  F3,  F4,  F5,  F6,  F7,  F8,  F9, F10, F11, F12, DEL,
        ___, ___,  UP, ___, ___, ___, ___, ___, ___, ___,SUSPEND,___,___,___,
        ___,LEFT,DOWN,RIGHT,___, ___, ___, ___, ___, ___, ___, ___,      ___,
        ___, ___, ___, ___, ___,BOOT, ___,MACRO(0), ___, ___, ___,       ___,
        ___, ___, ___,                ___,               ___, ___, ___,  ___
    ),

    # layer 2
    (
        '`',  F1,  F2,  F3,  F4,  F5,  F6,  F7,  F8,  F9, F10, F11, F12, DEL,
        ___, ___, ___, ___, ___, ___, ___,PGUP, ___, ___, ___,AUDIO_VOL_DOWN,AUDIO_VOL_UP,AUDIO_MUTE,
        ___, ___, ___, ___, ___, ___,LEFT,DOWN, UP,RIGHT, ___, ___,      ___,
        ___, ___, ___, ___, ___, ___,PGDN, ___, ___, ___, ___,           ___,
        ___, ___, ___,                ___,               ___, ___, ___,  ___
    ),

    # layer 3
    (
        BT_TOGGLE,BT1,BT2, BT3,BT4,BT5,BT6,BT7, BT8, BT9, BT0, ___, ___, ___,
        ___, ___, ___, ___, ___, ___,___,USB_TOGGLE,___,___,___,___,___, ___,
        ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___,      ___,
        ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___,           ___,
        ___, ___, ___,                ___,               ___, ___, ___,  ___
    ),

    # layer 4
    (
        '`', ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___,
        ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___,
        ___, ___, ___,   D, ___, ___, ___, ___, ___, ___, ';', ___,      ___,
        ___, ___, ___, ___, ___,   B, ___, ___, ___, ___, ___,           ___,
        ___, ___, ___,                ___,               ___, ___, ___,  ___
    ),
)


def macro_handler(dev, n, is_down):
    if is_down:
        dev.send_text('You pressed macro #{}\n'.format(n))
    else:
        dev.send_text('You released macro #{}\n'.format(n))

def pairs_handler(dev, n):
    dev.send_text('You just triggered pair keys #{}\n'.format(n))


keyboard.macro_handler = macro_handler
keyboard.pairs_handler = pairs_handler

# Pairs: J & K, U & I
keyboard.pairs = [{35, 36}, {20, 19}]

keyboard.verbose = False

keyboard.run()

```

`keymap` contains multiple layers of keycodes. `macro_handler` is used to handle all macros. `pairs_handler` is used to handle any pair-keys.

**When `code.py` is saved, the keyboard will reload it. If `code.py` has a syntax error, the keyboard will stop working. But, don't worry, it wouldn't damage the hardware. Fix the error and save it, then the keyboard will recover**

If you know how Python works, configuring the keyboard would be very easy. If not, we have some examples to get started.

1.  To swap the positions of <kbd>Caps</kbd> and <kbd>LCtrl</kbd>, just swap `CAPS` and `LCTRL` in `layer 0` of `keymap`:

    ```python
        # layer 0
        (
            ESC,   1,   2,   3,   4,   5,   6,   7,   8,   9,   0, '-', '=', BACKSPACE,
            TAB,   Q,   W,   E,   R,   T,   Y,   U,   I,   O,   P, '[', ']', '|',
            LCTRL,  A,   S, L2D,   F,   G,   H,   J,   K,   L, SCC, '"',    ENTER,
            LSFT4, Z,   X,   C,   V, L3B,   N,   M, ',', '.', '/',         RSFT4,
            CAPS, LGUI, LALT,          SPACE,            RALT, MENU,  L1, RCTRL
        ),
    ```

2.  Instead of <kbd>D</kbd>, use <kbd>Caps</kbd> as a Tap-key to activate navigation functions. Only need to change `layer 0` to:

    ```python
        # layer 0
        (
            ESC,   1,   2,   3,   4,   5,   6,   7,   8,   9,   0, '-', '=', BACKSPACE,
            TAB,   Q,   W,   E,   R,   T,   Y,   U,   I,   O,   P, '[', ']', '|',
            LAYER_TAP(2, CAPS),  A,   S,  D,   F,   G,   H,   J,   K,   L, SCC, '"',    ENTER,
            LSFT4, Z,   X,   C,   V, L3B,   N,   M, ',', '.', '/',         RSFT4,
            LCTRL, LGUI, LALT,          SPACE,            RALT, MENU,  L1, RCTRL
        ),
    ```

2.  Add a new macro. Use <kbd>Fn</kbd> and <kbd>Enter</kbd> to trigger No.1 macro. Just add `MACRO(1)` to `layer 1`:

    ```python
        # layer 1
        (
            '`',  F1,  F2,  F3,  F4,  F5,  F6,  F7,  F8,  F9, F10, F11, F12, DEL,
            ___, ___,  UP, ___, ___, ___, ___, ___, ___, ___,SUSPEND,___,___,___,
            ___,LEFT,DOWN,RIGHT,___, ___, ___, ___, ___, ___, ___, ___,    MACRO(1),
            ___, ___, ___, ___, ___,BOOT, ___,MACRO(0), ___, ___, ___,       ___,
            ___, ___, ___,                ___,               ___, ___, ___,  ___
        ),
    ```

    To define the function of the macro, please follow [the macro guide](macro.md)

4.  Use <kbd>RShift</kbd>, <kbd>RGUI</kbd>, <kbd>Fn</kbd> and <kbd>RCtrl</kbd> as Tap-keys. Tapping them outputs arrows keys (press & release quickly). Just change `layer 0` to:

    ```python
        # layer 0
        (
            ESC,   1,   2,   3,   4,   5,   6,   7,   8,   9,   0, '-', '=', BACKSPACE,
            TAB,   Q,   W,   E,   R,   T,   Y,   U,   I,   O,   P, '[', ']', '|',
            CAPS,  A,   S, L2D,   F,   G,   H,   J,   K,   L, SCC, '"',    ENTER,
            LSFT4, Z,   X,   C,   V, L3B,   N,   M, ',', '.', '/',   MODS_TAP(MODS(RSHIFT), UP),
            LCTRL, LGUI, LALT,          SPACE,     RALT, MODS_TAP(MODS(RGUI), LEFT), LAYER_TAP(1, DOWN), MODS_TAP(MODS(RCTRL), RIGHT)
        ),
    ```
