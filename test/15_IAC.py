from asm import *


def test_iac(a, b, co):
    CLC()
    LDM(a)
    FIM(p7, b)
    IAC()
    XCH(r14)    # Save ACC to r14
    if co: 
        JMS('assert:cy_set')
    else:
        JMS('assert:cy_clear')
    JMS('assert:r14_eq_r15')


for a in range(16):
    b = a + 1 
    test_iac(a, b & 0xF, b & 0x10)
HLT()


from test import *