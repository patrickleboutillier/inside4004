from asm import *


def test_ld(a, b):
    FIM(p5, a) ; FIM(p7, b)
    LD(r11)
    XCH(r14)
    JMS('assert:r14_eq_r15')

def test_ldm(a, b):
    FIM(p7, b)
    LDM(a)
    XCH(r14)
    JMS('assert:r14_eq_r15')

for a in range(16):
    test_ld(a, a)

for a in range(16):
    test_ldm(a, a)
HLT()


from test import *
