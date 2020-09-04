# Upgrade Firmware

The keyboard has a built-in bootloader to upgrade its firmware.

## Check Current Firmware Version

To check the information of the firmware, just open the `boot_out.txt` file in the USB storage of the keyboard. The file contains the version and the compiled date of the firmware:

```
Adafruit CircuitPython 6.0.0-alpha.1-110-g121d78ec9 on 2020-08-27; Makerdiary M60 Keyboard with nRF52840
```

If you find a newer firmware (file with `.uf2` extension) in [python-keyboard / firmware](https://github.com/makerdiary/python-keyboard/tree/zh-cn/firmware), you could do an upgrade.


## Enter Bootloader

There are 4 ways to run into the bootloader:

1.  When USB is connected, press <kbd>Fn</kbd> + <kbd>b</kbd> to enter the bootloader

2.  When USB is connected, hold the ON/OFF button for 3 seconds to enter the bootloader

3.  When in Python REPL mode, run:

    ```python
    import microcontroller as mcu
    mcu.on_next_reset(mcu.RunMode.BOOTLOADER)
    mcu.reset()
    ```

4.  When battery is not attached, hold the ON/OFF button and power on the keyboard with USB.

## Upgrade

When the bootloader is running, a USB drive named `M60Keyboard` will appear in your computer.
Download the latest `.uf2` firmware, drag-n-drop the firmware into the USB drive, then wait until a new USB drive named `CIRCUITPY` appears.
