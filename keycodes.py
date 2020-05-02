# -*- coding: utf-8 -*-

NA = '\x00'
TRANSPARENT = '\x01'
TAB = '\t'
ENTER = '\n'
BACKSPACE = '\b'
BACKSLASH = '\\'
GRAVE_ACCENT = '`'
APPLICATION = chr(0x0F)
LEFT_CTRL   = chr(0x10)
LEFT_SHIFT  = chr(0x11)
LEFT_ALT    = chr(0x12)
LEFT_GUI    = chr(0x13)
RIGHT_CTRL  = chr(0x14)
RIGHT_SHIFT = chr(0x15)
RIGHT_ALT   = chr(0x16)
RIGHT_GUI   = chr(0x17)

ESCAPE      = chr(0x1B)

SPACE       = ' '

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

CAPSLOCK    = '@'
F1          = 'A'
F2          = 'B'
F3          = 'C'
F4          = 'D'
F5          = 'E'
F6          = 'F'
F7          = 'G'
F8          = 'H'
F9          = 'I'
F10         = 'J'
F11         = 'K'
F12         = 'L'
PRINTSCREEN = 'M'
SCROLLLOCK	= 'N'
PAUSE		= 'O'
INSERT		= 'P'
HOME		= 'Q'
PAGEUP		= 'R'
DELETE		= 'S'
END		    = 'T'
PAGEDOWN	= 'U'
RIGHT		= 'V'
LEFT		= 'W'
DOWN		= 'X'
UP		    = 'Y'
NUMLOCK		= 'Z'
DELETE      = chr(127)

GRAVE   = GRAVE_ACCENT
MENU    = APPLICATION
LCTRL   = LEFT_CTRL
LSHIFT  = LEFT_SHIFT 
LALT    = LEFT_ALT
LGUI    = LEFT_GUI
RCTRL   = RIGHT_CTRL
RSHIFT  = RIGHT_SHIFT
RALT    = RIGHT_ALT
RGUI    = RIGHT_GUI
CAPS    = CAPSLOCK
ESC     = ESCAPE
DEL     = DELETE


_fix_digit = lambda x: str(x) if type(x) is int else x


LAYER_OR    = lambda mask: chr(0xF0000 | mask)
LAYER_AND   = lambda mask: chr(0xE0000 | mask)
LAYER_ON    = lambda n: chr(0xF0000 | (1 << n))
LAYER_OFF   = lambda n: chr(0xE0000 | (0xFFFF & ~(1 << n)))
LAYER_TOGGLE = lambda n: chr(0xD0000 | (1 << n))
LAYER_TAP   = lambda n, key='\x00': chr(0xF000 | (n << 8) | ord(_fix_digit(key)))
LAYER_MODS  = lambda n, mods: chr(0xE000 | (n << 8) | mods)
MODS_TAP    = lambda mods, key: chr(0xD000 | (mods << 8) | ord(_fix_digit(key)))
MODS_KEY    = lambda mods, key: chr(0xC000 | (mods << 8) | ord(_fix_digit(key)))


NAME_TO_KEYCODE = (
    '\x00'  # NUL
    '\x00'  # SOH
    '\x00'  # STX
    '\x00'  # ETX
    '\x00'  # EOT
    '\x00'  # ENQ
    '\x00'  # ACK
    '\x00'  # BEL \a
    '\x2a'  # BS BACKSPACE \b (called DELETE in the usb.org document)
    '\x2b'  # TAB \t
    '\x28'  # LF \n (called Return or ENTER in the usb.org document)
    '\x00'  # VT \v
    '\x00'  # FF \f
    '\x28'  # CR \r as Return
    '\x00'  # SO
    '\x65'  # SI as APPLICATION / MENU
    '\xE0'  # DLE as LEFT CTRL
    '\xE1'  # DC1 as LEFT SHIFT
    '\xE2'  # DC2 as LEFT ALT
    '\xE3'  # DC3 as LEFT GUI
    '\xE4'  # DC4 as RIGHT CTRL
    '\xE5'  # NAK as RIGHT SHIFT
    '\xE6'  # SYN as RIGHT ALT
    '\xE7'  # ETB as RIGHT GUI
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
    '\x39'  # @ as Capslock
    '\x3a'  # A as F1
    '\x3b'  # B as F2
    '\x3c'  # C as F3
    '\x3d'  # D as F4
    '\x3e'  # E as F5
    '\x3f'  # F as F6
    '\x40'  # G as F7
    '\x41'  # H as F8
    '\x42'  # I as F9
    '\x43'  # J as F10
    '\x44'  # K as F11
    '\x45'  # L as F12
    '\x46'  # M as PRINTSCREEN
    '\x47'  # N as SCROLLLOCK
    '\x48'  # O as PAUSE
    '\x49'  # P as INSERT
    '\x4a'  # Q as HOME
    '\x4b'  # R as PAGEUP
    '\x4c'  # S as DELETE
    '\x4d'  # T as END
    '\x4e'  # U as PAGEDOWN
    '\x4f'  # V as RIGHT
    '\x50'  # W as LEFT
    '\x51'  # X as DOWN
    '\x52'  # Y as UP
    '\x53'  # Z as NUMLOCK
    '\x2f'  # [
    '\x31'  # \ backslash
    '\x30'  # ]
    '\x00'  # ^
    '\x2c'  # _ as space
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
    '\x4c'  # DEL DELETE (called Forward Delete in usb.org document)
)

KEYCODE = lambda name: ord(NAME_TO_KEYCODE[name])
