# Hardware

## Specs
|                 | M60 Keyboard                                                                                            |
|-----------------|---------------------------------------------------------------------------------------------------------|
| Core Module     | nRF52840, Arm Cortex-M4F, 64MHz, 256KB RAM, 1MB FLASH, 8MB QSPI Flash, M.2 KEY-E                 |
| Wireless        | Bluetooth Low Energy 5.0, NFC                                                                           |
| USB             | Type-C                                                                                                  |
| Layout          | 60% (61 Keys)                                                                                           |
| Hot-Swappable   | Yes                                                                                                     |
| Switch Option   | Cherry MX compatible Switches                                                                           |
| Backlight       | 64 RGB LEDs, IS32FL3733                                                                                 |
|Battery Connector| JST 1.25mm 3-Pin                                                                                        |
| RF Antennas     | 2.4GHz Cabled PCB Antenna, NFC Cabled PCB Antenna                                                       |
| Dimensions      | 285 mm x 94.6 mm                                                                                        |

![](https://github.com/makerdiary/python-keyboard/blob/master/img/hotswappable.jpg?raw=true)

## Keyboard Matrix
The pins of 8x8 keyboard matrix:

|     | 1     | 2     | 3     | 4     | 5     | 6     | 7     | 8     |
|-----|-------|-------|-------|-------|-------|-------|-------|-------|
| ROW | P0_05 | P0_06 | P0_07 | P0_08 | P1_09 | P1_08 | P0_12 | P0_11 |
| COL | P0_19 | P0_20 | P0_21 | P0_22 | P0_23 | P0_24 | P0_25 | P0_26 |

## Power
+ When powered by USB, the keyboard is always on.
+ When powered by a battery, the keyboard is on if the ON/OFF button is pressed or pin `P0_28` outputs `0`.

## Button
The ON/OFF Button is at the back of the keyboard. It is connected to `P0_27`.

## LEDs on M.2
| LEDs           |  Pin  |
|--------------- | ------|
| Red LED        | P0_30 |
| Green LED      | P0_29 |
| Blue LED       | P0_31 |

## RGB LEDs Matrix
The RGB LEDs Matrix has 64 RGB LEDs and is driven by IS32FL3733.

| name           |  Pin   |     note      |
|--------------- | -------| --------------|
| Power          | P1_04  | 1: on, 0: off |
| I2C SDA        | P1_05  |               |
| I2C SCL        | P1_06  |               |
| Interrupt      | P1_07  |               |


## Battery
| name           |  Pin   |     note      |
|--------------- | -------| --------------|
| Charging       | P0_03  | 0: charging   |
| Voltage        | P0_02  | AIN0          |

