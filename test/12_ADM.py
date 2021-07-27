from asm import *


def test_add(a, b, ci, c, co):
    LDM(b)
    WRM()
    FIM(p7, c)
    LDM(a)
    if ci:
        STC()
    else:
        CLC()
    ADM()
    XCH(r14)    # Save ACC to r14 
    if co:
        JMS('assert:cy_set')
    else:
        JMS('assert:cy_clear')
    JMS('assert:r14_eq_r15')

# Choose a random RAM cell
FIM(p0, 0b00010111)
SRC(p0)
test_add(5, 7, 0, 12, 0)
test_add(4, 8, 1, 13, 0)
test_add(7, 9, 0, 0, 1)
test_add(9, 10, 1, 4, 1)
HLT()


from test import *
