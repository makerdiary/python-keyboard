# Backlight

The keboard has 64 programmable RGB LEDs. We are still working on the backlight. Before we get it done,
you are able to customize the backlight in the `macro_handler`.
For example, we set <kbd>9</kbd> to red color when a macro key pressed, and turn into green color
when the macro key is released:

```python
def macro_handler(dev, n, is_down):
    if is_down:
        dev.backlight.pixel(9, 0xff, 0, 0)
    else:
        dev.backlight.pixel(9, 0, 0xff, 0)
    dev.backlight.update()
```

`dev.backlight` provides some basic fucntions to control the RGB LEDs

## Backlight APIs
+ `update()` synchronizes with its buffer.
+ `pixel(i, r, g, b)` sets the bufffer of the LED `i`
+ `set_brightness(value)` sets the global brightness of all LEDs (from 0 to 255)

## Index of RGB LED
You can find the index of an LED here.
```
# ESC(0)    1(1)   2(2)   3(3)   4(4)   5(5)   6(6)   7(7)   8(8)   9(9)   0(10)  -(11)  =(12)  BACKSPACE(13)
# TAB(27)   Q(26)  W(25)  E(24)  R(23)  T(22)  Y(21)  U(20)  I(19)  O(18)  P(17)  [(16)  ](15)   \(14)
# CAPS(28)  A(29)  S(30)  D(31)  F(32)  G(33)  H(34)  J(35)  K(36)  L(37)  ;(38)  "(39)      ENTER(40)
#LSHIFT(52) Z(51)  X(50)  C(49)  V(48)  B(47)  N(46)  M(45)  ,(44)  .(43)  /(42)            RSHIFT(41)
# LCTRL(53)  LGUI(54)  LALT(55)               SPACE(56)          RALT(57)  MENU(58)  Fn(59)  RCTRL(60)
```

No.61 and No.62 are under the space key. No.63 is at the back of keyboard.

