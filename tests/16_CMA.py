from asm import *


def test_cma(a, b):
    CLC()
    LDM(a)
    FIM(p7, b)
    CMA()
    XCH(r14)    # Save ACC to r14
    JMS('assert:cy_clear')
    JMS('assert:r14_eq_r15')

for a in range(16):
    test_cma(a, ~a & 0xF)
HLT()


from tests import *