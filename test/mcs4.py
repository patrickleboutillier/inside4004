import chips.i4001 as i4001, chips.i4002 as i4002, chips.i4004 as i4004
import MCS4
from hdl import *


MCS4 = MCS4.MCS4()

# Create 4 ROMs
PROM = [i4001.i4001(0, 0b1111), i4001.i4001(1, 0b1111), i4001.i4001(2, 0b0000), i4001.i4001(3, 0b1111)]
for r in PROM:
    MCS4.addROM(r)

# Create 2 RAMS
RAM = [i4002.i4002(0, 0), i4002.i4002(0, 1)]
for r in RAM:
    MCS4.addRAM(0, r)

# Connect input and outputs for our test cases
for i in range(4):
    RAM[0].output().wire(i).connect(PROM[0].io().wire(i))
    RAM[1].output().wire(i).connect(PROM[1].io().wire(i))       
    PROM[2].io().wire(i).connect(PROM[3].io().wire(i))


MCS4.program()
MCS4.run()