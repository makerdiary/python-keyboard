Upgrade Firmware
================

The keyboard has a built-in bootloader to upgrade its firmware.

## Enter Bootloader
There are several ways to run into the bootloader:

1. When USB is connected, press <kbd>Fn</kbd> + <kbd>b</kbd> to enter the bootloader
2. When USB is connected, hold the ON/OFF button for 3 seconds to enter the bootloader
3. When in Python REPL mode, run:

   ```
   import microcontroller as mcu
   mcu.on_next_reset(mcu.RunMode.BOOTLOADER)
   mcu.reset()
   ```

4. When battery is not attached, hold the ON/OFF button and power on the keyboard with USB.

When the bootloader is running, a USB drive named `M60Keyboard` will appear in your computer. Drag-n-drop a new `.UF` firmware into the USB drive.
