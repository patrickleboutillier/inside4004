from asm import *

FIM(p0, 100)
FIN(p1)         # Place data at ROM address 100 in p1
JIN(p1)         # Jump to the address contained in p1 (50)
ERR()

PC(50)
LABEL('dest')
HLT()

PC(100)
BYTE(50)


