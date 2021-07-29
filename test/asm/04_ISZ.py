from asm import *

LDM(6)              
XCH(r0)             # Start r0 at 6

LABEL('loop')
INC(r3)
ISZ(r0, 'loop')
JIN(p1)             # Loop should stop after 10 iterations, so jump to 10
ERR()

PC(10)
HLT()