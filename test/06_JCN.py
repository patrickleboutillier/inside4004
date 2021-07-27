from asm import *

# zero =  0b0100
# carry = 0b0010

# Initially, acc = 0 and carry = 0
JCN(0b0100, 's2')
ERR()

LABEL('s2')
STC()
JCN(0b0010, 's3')
ERR()

LABEL('s3')
JCN(0b0110, 's4')
ERR()

LABEL('s4')
LDM(1)
JCN(0b1100, 's5')
ERR()

LABEL('s5')
CLC()
JCN(0b1010, 's6')

LABEL('s6')
JCN(0b1110, 's7')
ERR()

LABEL('s7')
JCN(0b0000, 'bad_jump')
LDM(1)
CLC()
JCN(0b0110, 'bad_jump')
LDM(0)
STC()
JCN(0b1110, 'bad_jump')
HLT()

LABEL('bad_jump')
ERR()
