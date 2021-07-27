from asm import *

FIM(p7, 0)
CLC()
TCC()
XCH(r14)
JMS('assert:r14_eq_r15')

FIM(p7, 1)
STC()
TCC()
XCH(r14)
JMS('assert:r14_eq_r15')

HLT()

from tests import *