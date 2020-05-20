# -*- coding: utf-8 -*-
#
# reference:
#   + https://gist.github.com/MightyPork/6da26e382a7ad91b5496ee55fdc73db2
#

NO = '\x00'
TRANSPARENT = '\x01'

# NONE = 0x00  # No key pressed
# Keyboard Error Roll Over - used for all slots if too many keys are pressed ("Phantom key")
# ROLLOVER = 0x01
# 0x02 #  Keyboard POST Fail
# 0x03 #  Keyboard Error Undefined

# A = 0x04  # Keyboard a and A
# B = 0x05  # Keyboard b and B
# C = 0x06  # Keyboard c and C
# D = 0x07  # Keyboard d and D
# E = 0x08  # Keyboard e and E
# F = 0x09  # Keyboard f and F
# G = 0x0a  # Keyboard g and G
# H = 0x0b  # Keyboard h and H
# I = 0x0c  # Keyboard i and I
# J = 0x0d  # Keyboard j and J
# K = 0x0e  # Keyboard k and K
# L = 0x0f  # Keyboard l and L
# M = 0x10  # Keyboard m and M
# N = 0x11  # Keyboard n and N
# O = 0x12  # Keyboard o and O
# P = 0x13  # Keyboard p and P
# Q = 0x14  # Keyboard q and Q
# R = 0x15  # Keyboard r and R
# S = 0x16  # Keyboard s and S
# T = 0x17  # Keyboard t and T
# U = 0x18  # Keyboard u and U
# V = 0x19  # Keyboard v and V
# W = 0x1a  # Keyboard w and W
# X = 0x1b  # Keyboard x and X
# Y = 0x1c  # Keyboard y and Y
# Z = 0x1d  # Keyboard z and Z

A = 'a'
B = 'b'
C = 'c'
D = 'd'
E = 'e'
F = 'f'
G = 'g'
H = 'h'
I = 'i'
J = 'j'
K = 'k'
L = 'l'
M = 'm'
N = 'n'
O = 'o'
P = 'p'
Q = 'q'
R = 'r'
S = 's'
T = 't'
U = 'u'
V = 'v'
W = 'w'
X = 'x'
Y = 'y'
Z = 'z'

# 1 = 0x1e # Keyboard 1 and !
# 2 = 0x1f # Keyboard 2 and @
# 3 = 0x20 # Keyboard 3 and #
# 4 = 0x21 # Keyboard 4 and $
# 5 = 0x22 # Keyboard 5 and %
# 6 = 0x23 # Keyboard 6 and ^
# 7 = 0x24 # Keyboard 7 and &
# 8 = 0x25 # Keyboard 8 and *
# 9 = 0x26 # Keyboard 9 and (
# 0 = 0x27 # Keyboard 0 and )

ENTER = 0x28  # Keyboard Return (ENTER)
ESCAPE = 0x29 # Keyboard ESCAPE
ESC = ESCAPE
BACKSPACE = 0x2a  # Keyboard DELETE (Backspace)
TAB = 0x2b  # Keyboard Tab
SPACE = 0x2c  # Keyboard Spacebar
MINUS = 0x2d  # Keyboard - and _
EQUAL = 0x2e  # Keyboard = and +
LEFTBRACE = 0x2f  # Keyboard [ and {
RIGHTBRACE = 0x30  # Keyboard ] and }
BACKSLASH = 0x31  # Keyboard \ and |
HASHTILDE = 0x32  # Keyboard Non-US # and ~
SEMICOLON = 0x33  # Keyboard ; and :
APOSTROPHE = 0x34  # Keyboard ' and "
QUOTE = 0x34
GRAVE = 0x35  # Keyboard ` and ~
COMMA = 0x36  # Keyboard , and <
DOT = 0x37  # Keyboard . and >
SLASH = 0x38  # Keyboard / and ?
CAPSLOCK = 0x39  # Keyboard Caps Lock
CAPS = CAPSLOCK

F1 = 0x3a  # Keyboard F1
F2 = 0x3b  # Keyboard F2
F3 = 0x3c  # Keyboard F3
F4 = 0x3d  # Keyboard F4
F5 = 0x3e  # Keyboard F5
F6 = 0x3f  # Keyboard F6
F7 = 0x40  # Keyboard F7
F8 = 0x41  # Keyboard F8
F9 = 0x42  # Keyboard F9
F10 = 0x43  # Keyboard F10
F11 = 0x44  # Keyboard F11
F12 = 0x45  # Keyboard F12

PRINTSCREEN = 0x46  # Keyboard Print Screen
PRTSCN = PRINTSCREEN
SCROLLLOCK = 0x47  # Keyboard Scroll Lock
PAUSE = 0x48  # Keyboard Pause
INSERT = 0x49  # Keyboard Insert
HOME = 0x4a  # Keyboard Home
PAGEUP = 0x4b  # Keyboard Page Up
PGUP = PAGEUP
DELETE = 0x4c  # Keyboard Delete Forward
DEL = DELETE
END = 0x4d  # Keyboard End
PAGEDOWN = 0x4e  # Keyboard Page Down
PGDN = PAGEUP
RIGHT = 0x4f  # Keyboard Right Arrow
LEFT = 0x50  # Keyboard Left Arrow
DOWN = 0x51  # Keyboard Down Arrow
UP = 0x52  # Keyboard Up Arrow

NUMLOCK = 0x53  # Keyboard Num Lock and Clear
KPSLASH = 0x54  # Keypad /
KPASTERISK = 0x55  # Keypad *
KPMINUS = 0x56  # Keypad -
KPPLUS = 0x57  # Keypad +
KPENTER = 0x58  # Keypad ENTER
KP1 = 0x59  # Keypad 1 and End
KP2 = 0x5a  # Keypad 2 and Down Arrow
KP3 = 0x5b  # Keypad 3 and PageDn
KP4 = 0x5c  # Keypad 4 and Left Arrow
KP5 = 0x5d  # Keypad 5
KP6 = 0x5e  # Keypad 6 and Right Arrow
KP7 = 0x5f  # Keypad 7 and Home
KP8 = 0x60  # Keypad 8 and Up Arrow
KP9 = 0x61  # Keypad 9 and Page Up
KP0 = 0x62  # Keypad 0 and Insert
KPDOT = 0x63  # Keypad . and Delete

# 102ND = 0x64 # Keyboard Non-US \ and |
APPLICATION = 0x65  # Keyboard Application
MENU = APPLICATION
POWER = 0x66  # Keyboard Power
KPEQUAL = 0x67  # Keypad =

F13 = 0x68  # Keyboard F13
F14 = 0x69  # Keyboard F14
F15 = 0x6a  # Keyboard F15
F16 = 0x6b  # Keyboard F16
F17 = 0x6c  # Keyboard F17
F18 = 0x6d  # Keyboard F18
F19 = 0x6e  # Keyboard F19
F20 = 0x6f  # Keyboard F20
F21 = 0x70  # Keyboard F21
F22 = 0x71  # Keyboard F22
F23 = 0x72  # Keyboard F23
F24 = 0x73  # Keyboard F24

OPEN = 0x74  # Keyboard Execute
HELP = 0x75  # Keyboard Help
# PROPS = 0x76  # Keyboard Menu
SELECT = 0x77  # Keyboard Select
STOP = 0x78  # Keyboard Stop
AGAIN = 0x79  # Keyboard Again
UNDO = 0x7a  # Keyboard Undo
CUT = 0x7b  # Keyboard Cut
COPY = 0x7c  # Keyboard Copy
PASTE = 0x7d  # Keyboard Paste
FIND = 0x7e  # Keyboard Find
MUTE = 0x7f  # Keyboard Mute
# VOLUMEUP = 0x80  # Keyboard Volume Up
# VOLUMEDOWN = 0x81  # Keyboard Volume Down
# 0x82  Keyboard Locking Caps Lock
# 0x83  Keyboard Locking Num Lock
# 0x84  Keyboard Locking Scroll Lock
KPCOMMA = 0x85  # Keypad Comma
# 0x86  Keypad Equal Sign

INT1 = 0x87
INT2 = 0x88
INT3 = 0x89
INT4 = 0x8a
INT5 = 0x8b
INT6 = 0x8c
INT7 = 0x8d
INT8 = 0x8e
INT9 = 0x8f

RO = 0x87  # Keyboard International1
KATAKANAHIRAGANA = 0x88  # Keyboard International2
YEN = 0x89  # Keyboard International3
HENKAN = 0x8a  # Keyboard International4
MUHENKAN = 0x8b  # Keyboard International5
KPJPCOMMA = 0x8c  # Keyboard International6
# 0x8d  Keyboard International7
# 0x8e  Keyboard International8
# 0x8f  Keyboard International9

LANG1 = 0x90
LANG2 = 0x91
LANG3 = 0x92
LANG4 = 0x93
LANG5 = 0x94
LANG6 = 0x95
LANG7 = 0x96
LANG8 = 0x97
LANG9 = 0x98

HANGEUL = 0x90  # Keyboard LANG1
HANJA = 0x91  # Keyboard LANG2
KATAKANA = 0x92  # Keyboard LANG3
HIRAGANA = 0x93  # Keyboard LANG4
ZENKAKUHANKAKU = 0x94  # Keyboard LANG5
# 0x95  Keyboard LANG6
# 0x96  Keyboard LANG7
# 0x97  Keyboard LANG8
# 0x98  Keyboard LANG9

# 0x99  Keyboard Alternate Erase
# 0x9a  Keyboard SysReq/Attention
# 0x9b  Keyboard Cancel
# 0x9c  Keyboard Clear
# 0x9d  Keyboard Prior
# 0x9e  Keyboard Return
# 0x9f  Keyboard Separator
# 0xa0  Keyboard Out
# 0xa1  Keyboard Oper
# 0xa2  Keyboard Clear/Again
# 0xa3  Keyboard CrSel/Props
# 0xa4  Keyboard ExSel

# 0xb0  Keypad 00
# 0xb1  Keypad 000
# 0xb2  Thousands Separator
# 0xb3  Decimal Separator
# 0xb4  Currency Unit
# 0xb5  Currency Sub-unit
KPLEFTPAREN = 0xb6  # Keypad (
KPRIGHTPAREN = 0xb7  # Keypad )
# 0xb8  Keypad {
# 0xb9  Keypad }
# 0xba  Keypad Tab
# 0xbb  Keypad Backspace
# 0xbc  Keypad A
# 0xbd  Keypad B
# 0xbe  Keypad C
# 0xbf  Keypad D
# 0xc0  Keypad E
# 0xc1  Keypad F
# 0xc2  Keypad XOR
# 0xc3  Keypad ^
# 0xc4  Keypad %
# 0xc5  Keypad <
# 0xc6  Keypad >
# 0xc7  Keypad &
# 0xc8  Keypad &&
# 0xc9  Keypad |
# 0xca  Keypad ||
# 0xcb  Keypad :
# 0xcc  Keypad #
# 0xcd  Keypad Space
# 0xce  Keypad @
# 0xcf  Keypad !
# 0xd0  Keypad Memory Store
# 0xd1  Keypad Memory Recall
# 0xd2  Keypad Memory Clear
# 0xd3  Keypad Memory Add
# 0xd4  Keypad Memory Subtract
# 0xd5  Keypad Memory Multiply
# 0xd6  Keypad Memory Divide
# 0xd7  Keypad +/-
# 0xd8  Keypad Clear
# 0xd9  Keypad Clear Entry
# 0xda  Keypad Binary
# 0xdb  Keypad Octal
# 0xdc  Keypad Decimal
# 0xdd  Keypad Hexadecimal

LEFT_CTRL = 0xe0  # Keyboard Left Control
LEFT_SHIFT = 0xe1  # Keyboard Left Shift
LEFT_ALT = 0xe2  # Keyboard Left Alt
LEFT_GUI = 0xe3  # Keyboard Left GUI
RIGHT_CTRL = 0xe4  # Keyboard Right Control
RIGHT_SHIFT = 0xe5  # Keyboard Right Shift
RIGHT_ALT = 0xe6  # Keyboard Right Alt
RIGHT_GUI = 0xe7  # Keyboard Right GUI

LCTRL = LEFT_CTRL
LSHIFT = LEFT_SHIFT
LALT = LEFT_ALT
LGUI = LEFT_GUI
RCTRL = RIGHT_CTRL
RSHIFT = RIGHT_SHIFT
RALT = RIGHT_ALT
RGUI = RIGHT_GUI

CTRL = LEFT_CTRL
SHIFT = LEFT_SHIFT
ALT = LEFT_ALT
GUI = LEFT_GUI


ASCII_TO_KEYCODE = (
    '\x00'  # NUL
    '\x01'  # SOH as TRANSPARENT
    '\x00'  # STX
    '\x00'  # ETX
    '\x00'  # EOT
    '\x00'  # ENQ
    '\x00'  # ACK
    '\x00'  # BEL \a
    '\x2a'  # BS BACKSPACE \b
    '\x2b'  # TAB \t
    '\x28'  # LF \n RETURN / ENTER
    '\x00'  # VT \v
    '\x00'  # FF \f
    '\x28'  # CR \r as RETURN
    '\x00'  # SO
    '\x00'  # SI
    '\x00'  # DLE
    '\x00'  # DC1
    '\x00'  # DC2
    '\x00'  # DC3
    '\x00'  # DC4
    '\x00'  # NAK
    '\x00'  # SYN
    '\x00'  # ETB
    '\x00'  # CAN
    '\x00'  # EM
    '\x00'  # SUB
    '\x29'  # ESC
    '\x00'  # FS
    '\x00'  # GS
    '\x00'  # RS
    '\x00'  # US
    '\x2c'  # SPACE
    '\x1e'  # ! (shift 1)
    '\x34'  # ' (shift ')
    '\x20'  # # (shift 3)
    '\x21'  # $ (shift 4)
    '\x22'  # % (shift 5)
    '\x24'  # & (shift 7)
    '\x34'  # '
    '\x26'  # ( (shift 9)
    '\x27'  # ) (shift 0)
    '\x25'  # * (shift 8)
    '\x2e'  # + (shift =)
    '\x36'  # ,
    '\x2d'  # -
    '\x37'  # .
    '\x38'  # /
    '\x27'  # 0
    '\x1e'  # 1
    '\x1f'  # 2
    '\x20'  # 3
    '\x21'  # 4
    '\x22'  # 5
    '\x23'  # 6
    '\x24'  # 7
    '\x25'  # 8
    '\x26'  # 9
    '\x33'  # : (shift ;)
    '\x33'  # ;
    '\x36'  # < (shift ,)
    '\x2e'  # =
    '\x37'  # > (shift .)
    '\x38'  # ? (shift /)
    '\x1f'  # @ (shift 2)
    '\x04'  # A
    '\x05'  # B
    '\x06'  # C
    '\x07'  # D
    '\x08'  # E
    '\x09'  # F
    '\x0a'  # G
    '\x0b'  # H
    '\x0c'  # I
    '\x0d'  # J
    '\x0e'  # K
    '\x0f'  # L
    '\x10'  # M
    '\x11'  # N
    '\x12'  # O
    '\x13'  # P
    '\x14'  # Q
    '\x15'  # R
    '\x16'  # S
    '\x17'  # T
    '\x18'  # U
    '\x19'  # V
    '\x1a'  # W
    '\x1b'  # X
    '\x1c'  # Y
    '\x1d'  # Z
    '\x2f'  # [
    '\x31'  # \ backslash
    '\x30'  # ]
    '\x23'  # ^ (shift 6)
    '\x2d'  # _ (shift -)
    '\x35'  # `
    '\x04'  # a
    '\x05'  # b
    '\x06'  # c
    '\x07'  # d
    '\x08'  # e
    '\x09'  # f
    '\x0a'  # g
    '\x0b'  # h
    '\x0c'  # i
    '\x0d'  # j
    '\x0e'  # k
    '\x0f'  # l
    '\x10'  # m
    '\x11'  # n
    '\x12'  # o
    '\x13'  # p
    '\x14'  # q
    '\x15'  # r
    '\x16'  # s
    '\x17'  # t
    '\x18'  # u
    '\x19'  # v
    '\x1a'  # w
    '\x1b'  # x
    '\x1c'  # y
    '\x1d'  # z
    '\x2f'  # { (shift [)
    '\x31'  # | (shift \)
    '\x30'  # } (shift ])
    '\x35'  # ~ (shift `)
    '\x4c'  # DEL DELETE Forward
)


#     /* Key Actions */
#     ACT_MODS            = 0b0000,
#     ACT_LMODS           = 0b0000,
#     ACT_RMODS           = 0b0001,
#     ACT_MODS_TAP        = 0b0010,
#     ACT_LMODS_TAP       = 0b0010,
#     ACT_RMODS_TAP       = 0b0011,
#     /* Other Keys */
#     ACT_USAGE           = 0b0100,
#     ACT_MOUSEKEY        = 0b0101,
#     /* Layer Actions */
#     ACT_LAYER           = 0b1000,
#     ACT_LAYER_TAP       = 0b1010, /* Layer  0-15 */
#     ACT_LAYER_TAP_EXT   = 0b1011, /* Layer 16-31 */
#     /* Extensions */
#     ACT_MACRO           = 0b1100,
#     ACT_BACKLIGHT       = 0b1101,
#     ACT_COMMAND         = 0b1110,
#     ACT_FUNCTION        = 0b1111
# };

ACT_MODS            = 0b0000
ACT_MODS_TAP        = 0b0010
ACT_USAGE           = 0b0100
ACT_MOUSEKEY        = 0b0101
ACT_LAYER           = 0b1000
ACT_LAYER_TAP       = 0b1010    # Layer  0-15
ACT_LAYER_TAP_EXT   = 0b1011    # Layer 16-31
ACT_MACRO           = 0b1100
ACT_BACKLIGHT       = 0b1101
ACT_COMMAND         = 0b1110
ACT_FUNCTION        = 0b1111


def PYCODE(x):
    if type(x) is int:
        return x if x > 9 else ord(ASCII_TO_KEYCODE[ord(str(x))])
    if type(x) is str and len(x) == 1:
        return ord(ASCII_TO_KEYCODE[ord(str(x))])
    raise ValueError('Invalid pycode {}'.format(x))


def MODS(*args):
    MAP = { LCTRL: 1, LSHIFT: 2, LALT: 4, LGUI: 8, RCTRL: 0x11, RSHIFT: 0x12, RALT: 0x14, RGUI: 0x18 }
    mods = 0
    for m in args:
        if m not in MAP:
            raise ValueError('Invalid modifier {}'.format(m))
        mods |= MAP[m]
    return mods


ACTION = lambda kind, param: (kind << 12) | param

MODS_KEY = lambda mods, key: ACTION(ACT_MODS, (mods << 8) | PYCODE(key))
MODS_TAP = lambda mods, key: ACTION(ACT_MODS_TAP, (mods << 8) | PYCODE(key))
MOUSEKEY = lambda key: ACTION(ACT_MOUSEKEY, key)
LAYER_TAP = lambda layer, key=NO: ACTION(ACT_LAYER_TAP, (layer << 8) | PYCODE(key))
LAYER_MODS = lambda layer, mods: LAYER_TAP(layer, 0xC0 | mods)

COMMAND = lambda id, opt: ACTION(ACT_COMMAND,  opt << 8 | id)


BOOTLOADER = COMMAND(0, 0)