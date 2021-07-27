from asm import *


def test_rar(ci, a, b, co):
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
    ci = n & 0x10
    co = n& 0x1
    a = n & 0xF
    b = n >> 1
    test_rar(ci, a, b, co)
HLT()


from test import *


LABEL('do_test_co_0')
RAR()
XCH(r14)    # Save ACC to r14
JMS('assert:cy_clear')
JMS('assert:r14_eq_r15')
BBL(0)

LABEL('do_test_co_1')
RAR()
XCH(r14)    # Save ACC to r14
JMS('assert:cy_set')
JMS('assert:r14_eq_r15')
BBL(0)