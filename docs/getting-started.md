# Get started with M60 Keyboard

M60 is a compact keyboard. It has a keymap composed of multiple layers, [similar to TMK Keyboard](https://github.com/tmk/tmk_keyboard/blob/master/tmk_core/doc/keymap.md). By default, layer number 0 is used, which includes a normal key map:

![](https://gitee.com/makerdiary/python-keyboard/raw/resource/img/layer0.svg)

## Keymap

As the 60% keyboard lacks a lot of keys such as F1~F12 and arrow keys, <kbd>Fn</kbd> is used to activate a second layer, layer number 1.

By default, holding <kbd>Fn</kbd> down activates the following functions:

![](https://gitee.com/makerdiary/python-keyboard/raw/resource/img/layer1.svg)

- <kbd>Fn</kbd> + <kbd>M</kbd> triggers No.0 macro
- <kbd>Fn</kbd> + <kbd>P</kbd> suspends the keyboard when only powered by battery.
- <kbd>Fn</kbd> + <kbd>B</kbd> enters its bootloader (only for used for firmware upgrades)

Except for <kbd>Fn</kbd>, any normal key can be used as a Tap-key. A Tap-key is a key that can be used as an ordinary key when tapped, or can be held down to activate alternate functions.

All of the default Tap-keys, including <kbd>D</kbd>, <kbd>B</kbd>, and <kbd>;</kbd> can be [re-configured](configuration.md).

### Using <kbd>D</kbd> for Navigation

<kbd>D</kbd> is the default Tap-key to activate the navigation functions. Holding it activates layer number 2, which includes navigation keys:

![](https://gitee.com/makerdiary/python-keyboard/raw/master/img/d-for-navigation.png)

- <kbd>D</kbd> + <kbd>H</kbd> → <kbd>←</kbd>
- <kbd>D</kbd> + <kbd>J</kbd> → <kbd>↓</kbd>
- <kbd>D</kbd> + <kbd>K</kbd> → <kbd>↑</kbd>
- <kbd>D</kbd> + <kbd>L</kbd> → <kbd>→</kbd>
- <kbd>D</kbd> + <kbd>U</kbd> → <kbd>PgUp</kbd>
- <kbd>D</kbd> + <kbd>N</kbd> → <kbd>PgDn</kbd>

### Using <kbd>B</kbd> to Configure Bluetooth and USB

<kbd>B</kbd> is the default Tap-key to configure Bluetooth and USB. Tapping <kbd>B</kbd> (i.e., pressing & releasing it quickly) outputs `b`. Holding <kbd>B</kbd> down activates another the Bluetooth keyboard layer, layer number 3. When the Bluetooth layer is active, the following functions are available:

- <kbd>B</kbd> + <kbd>Esc</kbd> toggles Bluetooth
- <kbd>B</kbd> + <kbd>0</kbd> ~ <kbd>9</kbd> changes Bluetooth ID to switch between multiple computers and phones
- <kbd>B</kbd> + <kbd>U</kbd> toggles USB

### Using <kbd>;</kbd> as <kbd>Ctrl</kbd>

<kbd>;</kbd> is a different type of Tap-key. Tapping <kbd>;</kbd> outputs `;`. However, holding <kbd>;</kbd> down outputs `Ctrl` instead of activating a layer.

![](https://github.com/xiongyihui/keyboard/raw/master/img/semicolon_as_ctrl.png)

- <kbd>;</kbd> + <kbd>c</kbd> = <kbd>Ctrl</kbd> + <kbd>c</kbd>
- <kbd>;</kbd> + <kbd>v</kbd> = <kbd>Ctrl</kbd> + <kbd>v</kbd>
- <kbd>;</kbd> + <kbd>x</kbd> = <kbd>Ctrl</kbd> + <kbd>x</kbd>
- <kbd>;</kbd> + <kbd>a</kbd> = <kbd>Ctrl</kbd> + <kbd>a</kbd>

## Using Pair-keys

Simultaneously pressing two keys (i.e., pressing them in an interval of less than 10ms) activates an alternate function.

Two sets of pair-keys are configured by default, to illustrate how to setup these keys. These include <kbd>J</kbd> <kbd>K</kbd> and <kbd>U</kbd> <kbd>I</kbd>. As shipped, simultaneously pressing <kbd>J</kbd> and <kbd>K</kbd> or <kbd>U</kbd> and <kbd>I</kbd> in a text editor will output a pre-defined string (_e.g._, "You just triggered pair keys #0").

## How to Setup Bluetooth

First, press <kbd>B</kbd> + <kbd>1</kbd> to start Bluetooth advertising. You will then see the blue LED under <kbd>1</kbd> enter in "breathing" mode and flash slowly：

![](https://gitee.com/makerdiary/python-keyboard/raw/resource/img/ble_broadcast.gif)

### On Windows

Open `Settings` / `Device` and then click `Add Bluetooth or other device`:

![](https://gitee.com/makerdiary/python-keyboard/raw/resource/img/windows-devices-en.png)

<img src="https://gitee.com/makerdiary/python-keyboard/raw/resource/img/windows-add-device-en.png" width="400">

Choose `Bluetooth` in the `Add a device` dialog, then you will see the device `PYKB 1`. Click `PYKB 1` to connect the keyboard.

<img src="https://gitee.com/makerdiary/python-keyboard/raw/resource/img/windows-add-bluetooth-device-en.png" width="400">

In order to connect the keyboard to a second computer, just use <kbd>B</kbd> + <kbd>2</kbd> to start connecting. From <kbd>0</kbd> to <kbd>9</kbd>, the keyboard can connect to 10 bluetooth devices.

## Go Further

We hope M60 keyboard incites ideas to make a keyboard more productive, all without having to install any third-party software or drivers on your computer.

If you have your own thoughts on how to best configure the keyboard, just follow [the configuration guide](configuration.md) to find what works best for you.
