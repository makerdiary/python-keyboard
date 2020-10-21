# -*- coding: utf-8 -*-
#
# reference:
#   + https://gist.github.com/MightyPork/6da26e382a7ad91b5496ee55fdc73db2
#
# fmt: off

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
PGDN = PAGEDOWN
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
    b'\x00'  # NUL
    b'\x01'  # SOH as TRANSPARENT
    b'\x00'  # STX
    b'\x00'  # ETX
    b'\x00'  # EOT
    b'\x00'  # ENQ
    b'\x00'  # ACK
    b'\x00'  # BEL \a
    b'\x2a'  # BS BACKSPACE \b
    b'\x2b'  # TAB \t
    b'\x28'  # LF \n RETURN / ENTER
    b'\x00'  # VT \v
    b'\x00'  # FF \f
    b'\x28'  # CR \r as RETURN
    b'\x00'  # SO
    b'\x00'  # SI
    b'\x00'  # DLE
    b'\x00'  # DC1
    b'\x00'  # DC2
    b'\x00'  # DC3
    b'\x00'  # DC4
    b'\x00'  # NAK
    b'\x00'  # SYN
    b'\x00'  # ETB
    b'\x00'  # CAN
    b'\x00'  # EM
    b'\x00'  # SUB
    b'\x29'  # ESC
    b'\x00'  # FS
    b'\x00'  # GS
    b'\x00'  # RS
    b'\x00'  # US
    b'\x2c'  # SPACE
    b'\x9e'  # ! (shift 1)
    b'\xb4'  # ' (shift ')
    b'\xa0'  # # (shift 3)
    b'\xa1'  # $ (shift 4)
    b'\xa2'  # % (shift 5)
    b'\xa4'  # & (shift 7)
    b'\x34'  # '
    b'\xa6'  # ( (shift 9)
    b'\xa7'  # ) (shift 0)
    b'\xa5'  # * (shift 8)
    b'\xae'  # + (shift =)
    b'\x36'  # ,
    b'\x2d'  # -
    b'\x37'  # .
    b'\x38'  # /
    b'\x27'  # 0
    b'\x1e'  # 1
    b'\x1f'  # 2
    b'\x20'  # 3
    b'\x21'  # 4
    b'\x22'  # 5
    b'\x23'  # 6
    b'\x24'  # 7
    b'\x25'  # 8
    b'\x26'  # 9
    b'\xb3'  # : (shift ;)
    b'\x33'  # ;
    b'\xb6'  # < (shift ,)
    b'\x2e'  # =
    b'\xb7'  # > (shift .)
    b'\xb8'  # ? (shift /)
    b'\x9f'  # @ (shift 2)
    b'\x84'  # A
    b'\x85'  # B
    b'\x86'  # C
    b'\x87'  # D
    b'\x88'  # E
    b'\x89'  # F
    b'\x8a'  # G
    b'\x8b'  # H
    b'\x8c'  # I
    b'\x8d'  # J
    b'\x8e'  # K
    b'\x8f'  # L
    b'\x90'  # M
    b'\x91'  # N
    b'\x92'  # O
    b'\x93'  # P
    b'\x94'  # Q
    b'\x95'  # R
    b'\x96'  # S
    b'\x97'  # T
    b'\x98'  # U
    b'\x99'  # V
    b'\x9a'  # W
    b'\x9b'  # X
    b'\x9c'  # Y
    b'\x9d'  # Z
    b'\x2f'  # [
    b'\x31'  # \ backslash
    b'\x30'  # ]
    b'\xa3'  # ^ (shift 6)
    b'\xad'  # _ (shift -)
    b'\x35'  # `
    b'\x04'  # a
    b'\x05'  # b
    b'\x06'  # c
    b'\x07'  # d
    b'\x08'  # e
    b'\x09'  # f
    b'\x0a'  # g
    b'\x0b'  # h
    b'\x0c'  # i
    b'\x0d'  # j
    b'\x0e'  # k
    b'\x0f'  # l
    b'\x10'  # m
    b'\x11'  # n
    b'\x12'  # o
    b'\x13'  # p
    b'\x14'  # q
    b'\x15'  # r
    b'\x16'  # s
    b'\x17'  # t
    b'\x18'  # u
    b'\x19'  # v
    b'\x1a'  # w
    b'\x1b'  # x
    b'\x1c'  # y
    b'\x1d'  # z
    b'\xaf'  # { (shift [)
    b'\xb1'  # | (shift \)
    b'\xb0'  # } (shift ])
    b'\xb5'  # ~ (shift `)
    b'\x4c'  # DEL DELETE Forward
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


OP_BIT_AND = 0
OP_BIT_OR  = 1
OP_BIT_XOR = 2
OP_BIT_SET = 3

ON_PRESS    = 1
ON_RELEASE  = 2
ON_BOTH     = 3


OP_TAP_TOGGLE = 0xF0



# convert keyname to action code
def get_action_code(x):
    if type(x) is int:
        return x if x > 9 else ASCII_TO_KEYCODE[ord(str(x))]
    if type(x) is str and len(x) == 1:
        return ASCII_TO_KEYCODE[ord(x)] & 0x7F
    if x is None:
        return 0
    raise ValueError('Invalid keyname {}'.format(x))

def MODS(*args):
    MAP = { LCTRL: 1, LSHIFT: 2, LALT: 4, LGUI: 8, RCTRL: 0x11, RSHIFT: 0x12, RALT: 0x14, RGUI: 0x18 }
    mods = 0
    for m in args:
        if m not in MAP:
            raise ValueError('Invalid modifier {}'.format(m))
        mods |= MAP[m]
    return mods

def mods_to_keycodes(mods):
    # if mods & 0x10:
    #     all_mods = (RCTRL, RSHIFT, RALT, RGUI)
    # else:
    #     all_mods = (LCTRL, LSHIFT, LALT, LGUI)
    # return list(filter(lambda k: mods & (1 << (k & 0x3)), all_mods))

    b = RCTRL if mods & 0x10 else LCTRL
    o = []
    for i in range(4):
        if (mods >> i) & 1:
            o.append(b + i)
    return o

ACTION = lambda kind, param: (kind << 12) | param

MODS_KEY = lambda mods, key: ACTION(ACT_MODS, (mods << 8) | get_action_code(key))
MODS_TAP = lambda mods, key: ACTION(ACT_MODS_TAP, (mods << 8) | get_action_code(key))
MOUSEKEY = lambda key: ACTION(ACT_MOUSEKEY, key)

LAYER_BITOP = lambda op, part, bits, on: ACTION(ACT_LAYER, op<<10|on<<8|part<<5|(bits&0x1f))
LAYER_BIT_XOR = lambda part, bits, on: LAYER_BITOP(OP_BIT_XOR, part, bits, on)
LAYER_INVERT = lambda layer, on: LAYER_BIT_XOR(layer/4,   1<<(layer%4),  on)
LAYER_TOGGLE = lambda layer: LAYER_INVERT(layer, ON_RELEASE)

LAYER_TAP = lambda layer, key=NO: ACTION(ACT_LAYER_TAP, (layer << 8) | get_action_code(key))
LAYER_TAP_TOGGLE = lambda layer: LAYER_TAP(layer, OP_TAP_TOGGLE)
LAYER_MODS = lambda layer, mods: LAYER_TAP(layer, 0xC0 | mods)

ACTION_USAGE_SYSTEM = lambda n: ACTION(ACT_USAGE, n)
ACTION_USAGE_CONSUMER = lambda n: ACTION(ACT_USAGE, 1 << 10 | (n))
ACTION_MOUSEKEY = lambda key: ACTION(ACT_MOUSEKEY, key)


MS_BTN1 = MOUSEKEY(1 << 0)
MS_BTN2 = MOUSEKEY(1 << 1)
MS_BTN3 = MOUSEKEY(1 << 2)
MS_BTN4 = MOUSEKEY(1 << 3)
MS_BTN5 = MOUSEKEY(1 << 4)
MS_UP   = MOUSEKEY(1 << 8)
MS_DN = MOUSEKEY(2 << 8)
MS_LT = MOUSEKEY(3 << 8)
MS_RT = MOUSEKEY(4 << 8)
MS_UL = MOUSEKEY(5 << 8)
MS_UR = MOUSEKEY(6 << 8)
MS_DL = MOUSEKEY(7 << 8)
MS_DR = MOUSEKEY(8 << 8)
MS_W_UP = MOUSEKEY(9 << 8)
MS_W_DN = MOUSEKEY(10 << 8)

MS_MOVEMENT = (
    (0, 0, 0),
    (0, -2, 0), (0, 2, 0), (-2, 0, 0), (2, 0, 0),
    (-1, -1, 0), (1, -1, 0), (-1, 1, 0), (1, 1, 0),
    (0, 0, 1), (0, 0, -1)
)

MACRO = lambda n: ACTION(ACT_MACRO, n)
BACKLIGHT = lambda n: ACTION(ACT_BACKLIGHT, n)

RGB_TOGGLE = BACKLIGHT(0)
RGB_MOD = BACKLIGHT(1)
MOD_RGB = BACKLIGHT(2)
RGB_HUE = BACKLIGHT(3)
HUE_RGB = BACKLIGHT(4)
RGB_SAT = BACKLIGHT(5)
SAT_RGB = BACKLIGHT(6)
RGB_VAL = BACKLIGHT(7)
VAL_RGB = BACKLIGHT(8)

COMMAND = lambda opt, n: ACTION(ACT_COMMAND,  opt << 8 | n)

BOOTLOADER = COMMAND(0, 0)
HEATMAP = COMMAND(0, 1)
SUSPEND = COMMAND(0, 2)
SHUTDOWN = COMMAND(0, 3)
USB_TOGGLE = COMMAND(0, 4)

BT = lambda n: COMMAND(1, n)
BT0 = BT(0)
BT1 = BT(1)
BT2 = BT(2)
BT3 = BT(3)
BT4 = BT(4)
BT5 = BT(5)
BT6 = BT(6)
BT7 = BT(7)
BT8 = BT(8)
BT9 = BT(9)
BT_TOGGLE = BT(0xFF)
BT_ON = BT(0xFE)
BT_OFF = BT(0xFD)

# Consumer Page(0x0C)
AUDIO_MUTE =                ACTION_USAGE_CONSUMER(0x00E2)
AUDIO_VOL_UP =              ACTION_USAGE_CONSUMER(0x00E9)
AUDIO_VOL_DOWN =            ACTION_USAGE_CONSUMER(0x00EA)
TRANSPORT_NEXT_TRACK =      ACTION_USAGE_CONSUMER(0x00B5)
TRANSPORT_PREV_TRACK =      ACTION_USAGE_CONSUMER(0x00B6)
TRANSPORT_STOP =            ACTION_USAGE_CONSUMER(0x00B7)
TRANSPORT_STOP_EJECT =      ACTION_USAGE_CONSUMER(0x00CC)
TRANSPORT_PLAY_PAUSE =      ACTION_USAGE_CONSUMER(0x00CD)
# application launch
APPLAUNCH_CC_CONFIG =       ACTION_USAGE_CONSUMER(0x0183)
APPLAUNCH_EMAIL =           ACTION_USAGE_CONSUMER(0x018A)
APPLAUNCH_CALCULATOR =      ACTION_USAGE_CONSUMER(0x0192)
APPLAUNCH_LOCAL_BROWSER =   ACTION_USAGE_CONSUMER(0x0194)
# application control
APPCONTROL_SEARCH =         ACTION_USAGE_CONSUMER(0x0221)
APPCONTROL_HOME =           ACTION_USAGE_CONSUMER(0x0223)
APPCONTROL_BACK =           ACTION_USAGE_CONSUMER(0x0224)
APPCONTROL_FORWARD =        ACTION_USAGE_CONSUMER(0x0225)
APPCONTROL_STOP =           ACTION_USAGE_CONSUMER(0x0226)
APPCONTROL_REFRESH =        ACTION_USAGE_CONSUMER(0x0227)
APPCONTROL_BOOKMARKS =      ACTION_USAGE_CONSUMER(0x022A)
# supplement for Bluegiga iWRAP HID(not supported by Windows?)
APPLAUNCH_LOCK =            ACTION_USAGE_CONSUMER(0x019E)
TRANSPORT_RECORD =          ACTION_USAGE_CONSUMER(0x00B2)
TRANSPORT_FAST_FORWARD =    ACTION_USAGE_CONSUMER(0x00B3)
TRANSPORT_REWIND =          ACTION_USAGE_CONSUMER(0x00B4)
TRANSPORT_EJECT =           ACTION_USAGE_CONSUMER(0x00B8)
APPCONTROL_MINIMIZE =       ACTION_USAGE_CONSUMER(0x0206)
# https://docs.microsoft.com/en-us/windows-hardware/drivers/hid/display-brightness-control
DISPLAY_BRIGHTNESS_UP =     ACTION_USAGE_CONSUMER(0x006F)
DISPLAY_BRIGHTNESS_DOWN =   ACTION_USAGE_CONSUMER(0x0070)
