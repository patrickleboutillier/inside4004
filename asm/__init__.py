import atexit
import sys

from .asm import *

def ehook(type, value, traceback):
    asm._err = True
    return sys.__excepthook__(type, value, traceback)

sys.excepthook = ehook
atexit.register(asm._done)
