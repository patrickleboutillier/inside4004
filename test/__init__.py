from asm import *


# A minimalist library to perform unit testing on the MCS-4
# It uses r14 as a temp space and requires data to be placed in r15.


# Asserts that the carry is clear
LABEL('assert:cy_clear')
JCN(0b1010, PC() + 3)
ERR()
BBL(0)


# Asserts that the carry is set
LABEL('assert:cy_set')
JCN(0b0010, PC() + 3)
ERR()
BBL(0)


# Assert that the contents of the accumulator is equal to the value in r15
# Carry is preserved
LABEL('assert:acc_eq_r15')
XCH(r14)    # Save ACC to r14
TCC()       # Carry is in accumulator
XCH(r14)    # Accumulator restored, carry in r14
SUB(r15)    # Subtract r15 from the accumulator, result should be 0.
CLC()
JCN(0b0100, PC() + 3)
ERR()
XCH(r14)    # Carry is now in accumulator
RAR()       # Send cary to accumulator
BBL(0)


# Assert that the contents of r14t is equal to the value in r15
# Carry is NOT preserved
LABEL('assert:r14_eq_r15')
XCH(r14)
CLC()
SUB(r15)    # Subtract r15 from the accumulator, result should be 0.
CLC()
JCN(0b0100, PC() + 3)
ERR()
BBL(0)
