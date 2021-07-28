from asm import *


def test_sub(a, b, ci, c, co):
    if ci:
        STC()
    else:
        CLC()
    FIM(p6, a << 4 | b) ; FIM(p7, c)
    LD(r12)
    SUB(r13)
    XCH(r14)    # Save ACC to r14 
    if co:
        JMS('assert:cy_set')
    else:
        JMS('assert:cy_clear')
    JMS('assert:r14_eq_r15')


test_sub(7, 5, 0, 2, 1)
test_sub(7, 5, 1, 1, 1)
test_sub(6, 6, 0, 0, 1)
test_sub(6, 6, 1, 15, 0)
test_sub(3, 6, 0, 13, 0)
HLT()


from test import *
