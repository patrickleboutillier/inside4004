from asm import *


def test_kbp(a, b):
    LDM(a)
    FIM(p7, b)
    KBP()
    XCH(r14)    # Save ACC to r14
    JMS('assert:r14_eq_r15')


for a in range(16):
    b = a
    if a == 4:
        b = 3
    elif a == 8:
        b = 4
    elif a > 2:
        b = 15
    test_kbp(a, b)
HLT()


from test import *