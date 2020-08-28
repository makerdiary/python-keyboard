# Get started with M60 Keyboard

M60 is a compact keyboard. It has a keymap composed of multiple layers, which is [similar to TMK Keyboard](https://github.com/tmk/tmk_keyboard/blob/master/tmk_core/doc/keymap.md). By default, No.0 layer is used:

![](https://gitee.com/makerdiary/python-keyboard/raw/resource/img/layer0.svg)

As the 60% keyboard lacks a lot of keys such as F1~F12 and arrow keys, <kbd>Fn</kbd> is used to activate a new layer.
When holding <kbd>Fn</kbd> down, the following keys are activated.

![](https://gitee.com/makerdiary/python-keyboard/raw/resource/img/layer1.svg)

+ <kbd>Fn</kbd> + <kbd>M</kbd> triggers No.0 macro
+ <kbd>Fn</kbd> + <kbd>P</kbd> suspends the keyboard when only powered by battery.
+ <kbd>Fn</kbd> + <kbd>B</kbd> enters its bootloader (only for upgrade)

Except <kbd>Fn</kbd>, a normal key can be used as a Tap-key,  which is holding a key down to activate an alternate function.

## Using <kbd>B</kbd> to configure Bluetooth and USB

<kbd>B</kbd> is used as a Tap-key to configure Bluetooth and USB. Taping <kbd>B</kbd> outputs `b` (press & release quickly). Holding <kbd>B</kbd> down activates another new layer. With the layer, the following functions are available:

+ <kbd>B</kbd> + <kbd>Esc</kbd> toggles Bluetooth
+ <kbd>B</kbd> + <kbd>0</kbd> ~ <kbd>9</kbd> changes Bluetooth ID to switch between multiple computers and phones
+ <kbd>B</kbd> + <kbd>U</kbd> toggles USB

### Using <kbd>D</kbd> for Navigation

<kbd>D</kbd> is also used as a Tap key for navigation functions.

![](https://gitee.com/makerdiary/python-keyboard/raw/master/img/d-for-navigation.png)

+ <kbd>D</kbd> + <kbd>H</kbd> → <kbd>←</kbd>
+ <kbd>D</kbd> + <kbd>J</kbd> → <kbd>↓</kbd>
+ <kbd>D</kbd> + <kbd>K</kbd> → <kbd>↑</kbd>
+ <kbd>D</kbd> + <kbd>L</kbd> → <kbd>→</kbd>
+ <kbd>D</kbd> + <kbd>U</kbd> → <kbd>PgUp</kbd>
+ <kbd>D</kbd> + <kbd>N</kbd> → <kbd>PgDn</kbd>

## Using <kbd>;</kbd> as <kbd>Ctrl</kbd>

<kbd>;</kbd> is another type of Tap-key. Taping <kbd>;</kbd> outputs `;`. However, holding <kbd>;</kbd> down outputs `Ctrl` instead of activating a layer.

![](https://github.com/xiongyihui/keyboard/raw/master/img/semicolon_as_ctrl.png)

+ <kbd>;</kbd> + <kbd>c</kbd> = <kbd>Ctrl</kbd> + <kbd>c</kbd>
+ <kbd>;</kbd> + <kbd>v</kbd> = <kbd>Ctrl</kbd> + <kbd>v</kbd>
+ <kbd>;</kbd> + <kbd>x</kbd> = <kbd>Ctrl</kbd> + <kbd>x</kbd>
+ <kbd>;</kbd> + <kbd>a</kbd> = <kbd>Ctrl</kbd> + <kbd>a</kbd>


### Using Pair-keys

Simultaneously pressing two keys (interval less than 10ms) activates an alternate function.
By default, <kbd>J</kbd> <kbd>K</kbd> are used as a pair-keys. When simultaneously pressing <kbd>J</kbd> and <kbd>K</kbd> in a text editor, it will output a pre-defined string.

## Setup Bluetooth

First, we press <kbd>B</kbd> + <kbd>1</kbd> to start Bluetooth advertising, and then we will see the blue LED under <kbd>1</kbd> is in breathing mode：

![](https://gitee.com/makerdiary/python-keyboard/raw/resource/img/ble_broadcast.gif)

### On Windows

Open `Settings` / `Device` and then click `Add Bluetooth or other device`:

![](https://gitee.com/makerdiary/python-keyboard/raw/resource/img/windows-devices-en.png)

<img src="https://gitee.com/makerdiary/python-keyboard/raw/resource/img/windows-add-device-en.png" width="400">

Choose `Bluetooth` in the `Add a device` dialog, then you will see the device `PYKB 1`. Click `PYKB 1` to connect the keyboard.

<img src="https://gitee.com/makerdiary/python-keyboard/raw/resource/img/windows-add-bluetooth-device-en.png" width="400">

When to connect the keyboard to a second computer, just use <kbd>B</kbd> + <kbd>2</kbd> to start connecting. From <kbd>0</kbd> to <kbd>9</kbd>, the keyboard can connect to 10 bluetooth devices.

## Go further

We hope M60 brings you an idea to make a keyboard more productive. You may have your own thoughts of configuring a keyboard. Follow [the configuring guide](configuration.md) to find what works best for you.
