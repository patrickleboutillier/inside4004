import chips.i4001 as i4001, chips.i4002 as i4002, chips.i4003 as i4003, chips.i4004 as i4004
import MCS4
from hdl import *


MCS4 = MCS4.MCS4()

# Create 5 ROMs
PROM = [i4001.i4001(0, 0b0000), i4001.i4001(1, 0b1111), i4001.i4001(2, 0b1111), i4001.i4001(3, 0b0000), i4001.i4001(4, 0b0000)]
for r in PROM:
    MCS4.addROM(r)

# Create 2 RAMS
RAM = [i4002.i4002(0, 0), i4002.i4002(0, 1)]
for r in RAM:
    MCS4.addRAM(0, r)

# Create keyboard 4003
kbd = i4003.i4003("KB")
kbd.clock().connect(PROM[0].io().wire(0))
kbd.data_in().connect(PROM[0].io().wire(1))
kbd.enable().v(1)
MCS4.addSR(kbd)

MCS4.program()
MCS4.run()