from asm import *


def test_inc(a, b):
    CLC()
    FIM(p2, a << 4) ; FIM(p7, b)
    INC(r4)
    XCH(r4)
    XCH(r14)    # Save ACC to r14 
    JMS('assert:cy_clear')
    JMS('assert:r14_eq_r15')

for a in range(16):
    test_inc(a, (a + 1) & 0xF)
HLT()


from tests import *
