
from keyboard import *
import my_keymap

keyboard = Keyboard()

___ = TRANSPARENT
BOOT = BOOTLOADER
L1 = LAYER_TAP(1)
L2D = LAYER_TAP(2, D)
L3B = LAYER_TAP(3, B)
LSFT4 = LAYER_MODS(4, MODS(LSHIFT))
RSFT4 = LAYER_MODS(4, MODS(RSHIFT))
L5S = LAYER_TAP(5, S)

# Semicolon & Ctrl
SCC = MODS_TAP(MODS(RCTRL), ';')
SINS = MODS_KEY(MODS(SHIFT), INSERT)

if my_keymap.custom_keymap and len(my_keymap.custom_keymap) > 0:
    keyboard.keymap = my_keymap.custom_keymap

else:
    keyboard.keymap = (
        # layer 0
        (
            ESC,   1,   2,   3,   4,   5,   6,   7,   8,   9,   0, '-', '=', BACKSPACE,
            TAB,   Q,   W,   E,   R,   T,   Y,   U,   I,   O,   P, '[', ']', '|',
            CAPS,  A,   S, L2D,   F,   G,   H,   J,   K,   L, SCC, '"',    ENTER,
            LSFT4, Z,   X,   C,   V, L3B,   N,   M, ',', '.', '/',         RSFT4,
            LCTRL, LGUI, LALT,          SPACE,            RALT, MENU,  L1, RCTRL
        ),

        # layer 1
        (
            '`',  F1,  F2,  F3,  F4,  F5,  F6,  F7,  F8,  F9, F10, F11, F12, DEL,
            ___, ___,  UP, ___, ___, ___, ___, ___, ___, ___,SUSPEND,___,___,___,
            ___,LEFT,DOWN,RIGHT,___, ___, ___, ___, ___, ___, ___, ___,      ___,
            ___, ___, ___, ___, ___,BOOT, ___,MACRO(0), ___, ___, ___,       ___,
            ___, ___, ___,                ___,               ___, ___, ___,  ___
        ),

        # layer 2
        (
            '`',  F1,  F2,  F3,  F4,  F5,  F6,  F7,  F8,  F9, F10, F11, F12, DEL,
            ___, ___, ___, ___, ___, ___,HOME,PGUP, ___, ___,SINS,AUDIO_VOL_DOWN,AUDIO_VOL_UP,AUDIO_MUTE,
            ___, ___, ___, ___, ___, ___,LEFT,DOWN, UP,RIGHT, ___, ___,      ___,
            ___, ___, ___, ___, ___, ___,PGDN,END, ___, ___, ___,           ___,
            ___, ___, ___,                ___,               ___, ___, ___,  ___
        ),

        # layer 3
        (
            BT_TOGGLE,BT1,BT2, BT3,BT4,BT5,BT6,BT7, BT8, BT9, BT0, ___, ___, ___,
            RGB_MOD, ___, ___, ___, ___, ___,___,USB_TOGGLE,___,___,___,___,___, ___,
            RGB_TOGGLE,HUE_RGB,RGB_HUE,SAT_RGB,RGB_SAT,___,___,___,___,___,___,___,      ___,
            ___, ___, ___, ___, ___, ___, ___, ___,VAL_RGB,RGB_VAL, ___,           ___,
            ___, ___, ___,                ___,               ___, ___, ___,  ___
        ),

        # layer 4
        (
            '`', ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___,
            ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___,
            ___, ___, ___,   D, ___, ___, ___, ___, ___, ___, ';', ___,      ___,
            ___, ___, ___, ___, ___,   B, ___, ___, ___, ___, ___,           ___,
            ___, ___, ___,                ___,               ___, ___, ___,  ___
        ),

        # layer 5
        (
            ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___,
            ___, ___, ___, ___, ___, ___,MS_W_UP,MS_UL,MS_UP,MS_UR, ___, ___, ___, ___,
            ___, ___, ___, ___, ___, ___,MS_BTN1,MS_LT,MS_DN,MS_RT,MS_BTN2, ___,      ___,
            ___, ___, ___, ___, ___, ___,MS_W_DN,MS_DL,MS_DN,MS_DR, ___,           ___,
            ___, ___, ___,                ___,               ___, ___, ___,  ___
        ),
    )


# Use different keymaps on different connections
# Valid keys are "USB" and "BT0"-"BT9"
# Connection not in this map will use default keymap defined above.
if my_keymap.profiles and len(my_keymap.profiles) > 0:
    keyboard.profiles = my_keymap.profiles
else:    
    keyboard.profiles = {
        # For example, BT8 is connected to a Mac
        "BT8": (
            # layer 0
            (
                ESC,   1,   2,   3,   4,   5,   6,   7,   8,   9,   0, '-', '=', BACKSPACE,
                TAB,   Q,   W,   E,   R,   T,   Y,   U,   I,   O,   P, '[', ']', '|',
                CAPS,  A,   S,   D,   F,   G,   H,   J,   K,   L, SCC, '"',    ENTER,
                LSHIFT,Z,   X,   C,   V,   B,   N,   M, ',', '.', '/',        RSHIFT,
                LCTRL, LALT, LGUI,          SPACE,            MENU, RALT,  L1, RCTRL
            ),

            # layer 1
            (
                '`',  F1,  F2,  F3,  F4,  F5,  F6,  F7,  F8,  F9, F10, F11, F12, DEL,
                ___, ___,  UP, ___, ___, ___, ___, ___, ___, ___,SUSPEND,___,___,___,
                ___,LEFT,DOWN,RIGHT,___, ___, ___, ___, ___, ___, ___, ___,      ___,
                ___, ___, ___, ___, ___,BOOT, ___,MACRO(1), ___, ___, ___,       ___,
                ___, ___, ___,                ___,               ___, ___, ___,  ___
            ),
        )
    }


# add default keymap to profiles
default_keymap_count = len(keyboard.keymap)
for i in keyboard.profiles.keys():
    profile_key_maps = keyboard.profiles.get(i)
    profile_layer_count = len(profile_key_maps)

    # insert default
    keymap_profile = list(profile_key_maps)
    for x in range(profile_layer_count, default_keymap_count):
        default_keymap = keyboard.keymap[x]
        keymap_profile.append(default_keymap)

    keyboard.profiles[i] = tuple(keymap_profile)    


#print(keyboard.profiles)
print('keyboard.keymap = #{}'.format(len(keyboard.keymap)))
print('keyboard.profiles = #{}'.format(len(keyboard.profiles)))

def macro_handler(dev, n, is_down):
    if is_down:
        dev.send_text('You pressed macro #{}\n'.format(n))
    else:
        dev.send_text('You released macro #{}\n'.format(n))

def pairs_handler(dev, n):
    dev.send_text('You just triggered pair keys #{}\n'.format(n))



if my_keymap.macro_handler:
    keyboard.macro_handler = my_keymap.macro_handler
else:    
    keyboard.macro_handler = macro_handler

if my_keymap.pairs_handler:
    keyboard.pairs_handler = my_keymap.pairs_handler    
else:
    keyboard.pairs_handler = pairs_handler

# Pairs: J & K, U & I
if my_keymap.pairs is None:
    keyboard.pairs = [{35, 36}, {20, 19}]
else:
    keyboard.pairs = my_keymap.pairs

# keyboard.verbose = False
print('keyboard.pairs = #{}'.format(len(keyboard.pairs)))

keyboard.run()
