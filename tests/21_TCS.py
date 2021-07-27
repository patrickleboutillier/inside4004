from asm import *

FIM(p7, 9)
CLC()
TCS()
XCH(r14)
JMS('assert:r14_eq_r15')

FIM(p7, 10)
STC()
TCS()
XCH(r14)
JMS('assert:r14_eq_r15')

HLT()

from tests import *