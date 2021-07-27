from asm import *


def test_ral(ci, a, b, co):
    if ci:
        STC()
    else:
        CLC()
    LDM(a)
    FIM(p7, b)
    if co:
        JMS('do_test_co_1')
    else:
        JMS('do_test_co_0')


for n in range(32):
    ci = n & 0x1
    co = n & 0x10
    a = n >> 1
    b = n & 0xF
    test_ral(ci, a, b, co)
HLT()


from tests import *


LABEL('do_test_co_0')
RAL()
XCH(r14)    # Save ACC to r14
JMS('assert:cy_clear')
JMS('assert:r14_eq_r15')
BBL(0)

LABEL('do_test_co_1')
RAL()
XCH(r14)    # Save ACC to r14
JMS('assert:cy_set')
JMS('assert:r14_eq_r15')
BBL(0)