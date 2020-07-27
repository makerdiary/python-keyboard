import os

machine = os.uname().machine

if machine.find('M60 Keyboard') >= 0:
    from .m60 import *
elif machine.find('Pitaya Go') >= 0:
    from .pitaya_go import *
