# Pair-Keys

They keyboard can be configured to activate a pre-defined function when two keys are pressed simultaneously (_i.e._, within an interval less than 10ms).

Like a macro, activating pair-keys triggers an immediate event. Unlike a macro, pair-keys do not have a released (key-up) event.

By default, the keyboard uses <kbd>J</kbd> <kbd>K</kbd> and <kbd>U</kbd> <kbd>I</kbd> as pair-keys to trigger an example function (_e.g._, typing "You just triggered pair keys #0").

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
        LCTRL, LGUI, LALT,          SPACE,        RALT, MENU, RGUI, RCTRL
    ),
)


# ESC(0)    1(1)   2(2)   3(3)   4(4)   5(5)   6(6)   7(7)   8(8)   9(9)   0(10)  -(11)  =(12)  BACKSPACE(13)
# TAB(27)   Q(26)  W(25)  E(24)  R(23)  T(22)  Y(21)  U(20)  I(19)  O(18)  P(17)  [(16)  ](15)   \(14)
# CAPS(28)  A(29)  S(30)  D(31)  F(32)  G(33)  H(34)  J(35)  K(36)  L(37)  ;(38)  "(39)      ENTER(40)
#LSHIFT(52) Z(51)  X(50)  C(49)  V(48)  B(47)  N(46)  M(45)  ,(44)  .(43)  /(42)            RSHIFT(41)
# LCTRL(53)  LGUI(54)  LALT(55)               SPACE(56)          RALT(57)  MENU(58)  Fn(59)  RCTRL(60)

# Indexes of Pairs: J & K, U & I
keyboard.pairs = [{35, 36}, {20, 19}]

def pairs_handler(dev, n):
    dev.send_text('You just triggered pair keys #{}\n'.format(n))

keyboard.pairs_handler = pairs_handler

keyboard.run()
```
