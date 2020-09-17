# Macro

To set up a macro, add a macro to the keymap and define its function. By default, <kbd>Fn</kbd> is configured as macro number 0:

```python
# code.py
from keyboard import *

keyboard = Keyboard()
keyboard.keymap = (
    (
        ESC,   1,   2,   3,   4,   5,   6,   7,   8,   9,   0, '-', '=', BACKSPACE,
        TAB,   Q,   W,   E,   R,   T,   Y,   U,   I,   O,   P, '[', ']', '|',
        CAPS,  A,   S,  D,   F,   G,   H,   J,   K,   L, ';', '"',    ENTER,
        LSHIFT,Z,   X,   C,   V,   B,   N,   M, ',', '.', '/',         RSHIFT,
        LCTRL, LGUI, LALT,          SPACE,        RALT, MENU,  MACRO(0), RCTRL
    ),
)

def macro_handler(dev, n, is_down):
    if is_down:
        dev.send_text('You pressed macro #{}\n'.format(n))
    else:
        dev.send_text('You released macro #{}\n'.format(n))

keyboard.macro_handler = macro_handler
keyboard.run()
```

## Examples

### Use a macro to launch the Calculator application on Windows

Replace the function `macro_handler` with the following code to launch the Calculator with a single keystroke:

```python
def macro_handler(dev, n, is_down):
    if is_down and n == 0:
        dev.send(GUI, R)
        time.sleep(0.1)
        dev.send_text('calc\n')
```

### Automatic typing

Read a file in the keyboard's USB storage and type its content automatically.

```python
def macro_handler(dev, n, is_down):
    if is_down and n == 0:
        with open('code.py', 'r') as f:
            for line in f:
                dev.send_text(line)
```

### Repeated key strokes

Use a macro to trigger a repeated sequence of key presses until a new key is pressed.

```python
def macro_handler(dev, n, is_down):
    if n == 0 and not is_down:
        t = time.time()
        dt = 0.01                   # seconds
        while dev.scan() < 2:
            if time.time() > t:
                dev.send_text('hello, world\n')
                t += dt
```
