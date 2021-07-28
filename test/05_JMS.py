from asm import *

JMS('sub')
# 4 is in acc
ADD(r1)
# 10 is in acc
XCH(r1)
JIN(p0)
ERR()

PC(10)
HLT()

PC(20)
LABEL('sub')
FIM(p0, 6)
BBL(4)
ERR()