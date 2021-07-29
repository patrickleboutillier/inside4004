from asm import *

LDM(0)
DCL()               # Select RAM bank 0
FIM(p0, 0b00000000) # RAM chip 0
SRC(p0)
FIM(p7, 0b00001010)
LD(r15)
WMP()               # Write 0b1010 to the output of RAM0/0
CLB()
FIM(p0, 0x00)       # ROM chip 0
SRC(p0)
RDR()               # Read input of ROM0 in acc. Should be connected to output of RAM0/0
XCH(r14)            # Save ACC to r14
JMS('assert:r14_eq_r15')

LDM(0)
DCL()               # Select RAM bank 0
FIM(p0, 0b01000000) # RAM chip 1
SRC(p0)
FIM(p7, 0b00000101)
LD(r15)
WMP()               # Write 0b0101 to the output of RAM0/1
CLB()
FIM(p0, 0x10)       # ROM chip 1
SRC(p0)
RDR()               # Read input of ROM1 in acc. Should be connected to output of RAM0/1
XCH(r14)            # Save ACC to r14
JMS('assert:r14_eq_r15')

LDM(0)
FIM(p0, 0x20) # ROM chip 2
SRC(p0)
FIM(p7, 0b00000110)
LD(r15)
WRR()               # Write 0b0110 to the output of RAM0/1
CLB()
FIM(p0, 0x30)       # ROM chip 3
SRC(p0)
RDR()               # Read input of ROM3 in acc. Should be connected to output of ROM2
XCH(r14)            # Save ACC to r14
JMS('assert:r14_eq_r15')

HLT()


from test import *