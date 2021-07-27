from asm import *


def test_sub(a, b, ci, c, co):
    LDM(b)
    WRM()
    FIM(p7, c)
    LDM(a)
    if ci:
        STC()
    else:
        CLC()
    SBM()
    XCH(r14)    # Save ACC to r14 
    if co:
        JMS('assert:cy_set')
    else:
        JMS('assert:cy_clear')
    JMS('assert:r14_eq_r15')


# Choose a random RAM cell
FIM(p0, 0b00111101)
SRC(p0)
test_sub(7, 5, 0, 2, 1)
test_sub(7, 5, 1, 1, 1)
test_sub(6, 6, 0, 0, 1)
test_sub(6, 6, 1, 15, 0)
test_sub(3, 6, 0, 13, 0)
HLT()


from test import *
