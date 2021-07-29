from asm import *


def test_add(a, b, ci, c, co):
    if ci:
        STC()
    else:
        CLC()
    FIM(p6, a << 4 | b) ; FIM(p7, c)
    LD(r12)
    ADD(r13)
    XCH(r14)    # Save ACC to r14 
    if co:
        JMS('assert:cy_set')
    else:
        JMS('assert:cy_clear')
    JMS('assert:r14_eq_r15')


test_add(5, 7, 0, 12, 0)
test_add(4, 8, 1, 13, 0)
test_add(7, 9, 0, 0, 1)
test_add(9, 10, 1, 4, 1)
HLT()


from test import *
