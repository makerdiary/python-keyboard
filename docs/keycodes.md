| Name          | Description                      |
| ------------- | -------------------------------- |
| `NO`          | Do nothing                       |
| `TRANSPARENT` | Use the key of next active layer |

## Bluetooth

| Name          | Description                      |
| ------------- | -------------------------------- |
| `BT0` ~ `BT9` | Switch to Bluetooth ID n (0 - 9) |
| `BT_TOGGLE`   | Toggle Bluetooth                 |

## USB

| Name         | Description |
| ------------ | ----------- |
| `USB_TOGGLE` | Toggle USB  |

**Note: When connecting the keyboard to a computer via USB, USB will be enabled automatically. When both USB and Bluetooth are enabled, USB will be used.**

## System

| Name         | Description                                          |
| ------------ | ---------------------------------------------------- |
| `BOOTLOADER` | Enter the bootloader of the keyboard                 |
| `HEATMAP`    | Generate heatmap (todo)                              |
| `SUSPEND`    | Suspend. To wake up keyboard, just press any key     |
| `SHUTDOWN`   | Shutdown. Use ON/OFF button to power on the keyboard |

## Layer & Modifier

- `MODS_KEY(mods, key)` sends one or more modifier(s) + a normal key. `MODS()` is used to wrap modifiers.

  `MODS_KEY(MODS(LCTRL), C)`, `MODS_KEY(MODS(LCTRL, LSHIFT), C)`, `MODS_KEY(MODS(LCTRL, LSHIFT, LALT), C)`

- `LAYER_TOGGLE(n)` toggles layer `n`

- `MACRO(n)` creates macro `n`

### TAP-Key

A `TAP-Key` has 2 modes - tap (press and release quickly) and hold (long press)

- `LAYER_TAP(n, key)` tap - outputs `key`, hold - turns on layer n momentary

- `LAYER_TAP_TOGGLE(n)` tap - toggles layer n, hold - turns on layer n momentary

- `LAYER_MODS(n, mods)` tap - outputs specified modifier(s), hold - turns on layer n momentary

  `LAYER_MODS(1, MODS(LCTRL))`, `LAYER_MODS(1, MODS(LCTRL, LSHIFT))`

- `MODS_TAP(mods, key)` tap - outputs `key`, hold - outputs specified modifier(s)

  `MODS_TAP(MODS(LCTRL), ';')`, `MODS_TAP(MODS(LCTRL, LALT), LEFT)`

## APP & Media

```
AUDIO_MUTE
AUDIO_VOL_UP
AUDIO_VOL_DOWN
TRANSPORT_NEXT_TRACK
TRANSPORT_PREV_TRACK
TRANSPORT_STOP
TRANSPORT_STOP_EJECT
TRANSPORT_PLAY_PAUSE
# application launch
APPLAUNCH_CC_CONFIG
APPLAUNCH_EMAIL
APPLAUNCH_CALCULATOR
APPLAUNCH_LOCAL_BROWSER
# application control
APPCONTROL_SEARCH
APPCONTROL_HOME
APPCONTROL_BACK
APPCONTROL_FORWARD
APPCONTROL_STOP
APPCONTROL_REFRESH
APPCONTROL_BOOKMARKS
# supplement for Bluegiga iWRAP HID(not supported by Windows?)
APPLAUNCH_LOCK
TRANSPORT_RECORD
TRANSPORT_FAST_FORWARD
TRANSPORT_REWIND
TRANSPORT_EJECT
APPCONTROL_MINIMIZE
# https://docs.microsoft.com/en-us/windows-hardware/drivers/hid/display-brightness-control
DISPLAY_BRIGHTNESS_UP
DISPLAY_BRIGHTNESS_DOWN
```

## Nomal keys

```
A
B
C
D
E
F
G
H
I
J
K
L
M
N
O
P
Q
R
S
T
U
V
W
X
Y
Z

1
2
3
4
5
6
7
8
9
0

ENTER
ESCAPE
ESC
BACKSPACE
TAB
SPACE
MINUS
EQUAL
LEFTBRACE
RIGHTBRACE
BACKSLASH
HASHTILDE
SEMICOLON
APOSTROPHE
QUOTE
GRAVE
COMMA
DOT
SLASH
CAPSLOCK
CAPS

F1
F2
F3
F4
F5
F6
F7
F8
F9
F10
F11
F12

PRINTSCREEN
PRTSCN
SCROLLLOCK
PAUSE
INSERT
HOME
PAGEUP
PGUP
DELETE
DEL
END
PAGEDOWN
PGDN
RIGHT
LEFT
DOWN
UP

NUMLOCK
KPSLASH
KPASTERISK
KPMINUS
KPPLUS
KPENTER
KP1
KP2
KP3
KP4
KP5
KP6
KP7
KP8
KP9
KP0
KPDOT

# 102ND
APPLICATION
MENU
POWER
KPEQUAL

F13
F14
F15
F16
F17
F18
F19
F20
F21
F22
F23
F24

OPEN
HELP
# PROPS
SELECT
STOP
AGAIN
UNDO
CUT
COPY
PASTE
FIND
MUTE
KPCOMMA

INT1
INT2
INT3
INT4
INT5
INT6
INT7
INT8
INT9

RO
KATAKANAHIRAGANA
YEN
HENKAN
MUHENKAN
KPJPCOMMA

LANG1
LANG2
LANG3
LANG4
LANG5
LANG6
LANG7
LANG8
LANG9

HANGEUL
HANJA
KATAKANA
HIRAGANA
ZENKAKUHANKAKU

KPLEFTPAREN
KPRIGHTPAREN

LEFT_CTRL
LEFT_SHIFT
LEFT_ALT
LEFT_GUI
RIGHT_CTRL
RIGHT_SHIFT
RIGHT_ALT
RIGHT_GUI

LCTRL
LSHIFT
LALT
LGUI
RCTRL
RSHIFT
RALT
RGUI

CTRL
SHIFT
ALT
GUI
```
