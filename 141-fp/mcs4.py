import chips.i4001 as i4001, chips.i4002 as i4002, chips.i4003 as i4003, chips.i4004 as i4004
import chips.keyboard as keyboard, chips.printer as printer
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
kbdsr = i4003.i4003("KB")
kbdsr.clock().connect(PROM[0].io().wire(0))
kbdsr.data_in().connect(PROM[0].io().wire(1))
kbdsr.enable().v(1)
MCS4.addSR(kbdsr)

# Keyboard
keyboard = keyboard.keyboard()
keyboard.input().connect(kbdsr.parallel_out())
PROM[1].io().connect(keyboard.output())

# Printer
printer = printer.printer()
# TODO: shift register output to input
printer.sector().connect(MCS4.CPU().test())
printer.index().connect(PROM[2].io().wire(0))
printer.fire().connect(RAM[0].output().wire(1))
printer.advance().connect(RAM[0].output().wire(3))

# Load the program
MCS4.program()

step = False
def callback(nb):
    global step
    printer.cycle()
    if (MCS4.CPU().addr.getPC() == 0x029):
        step = True
    #if nb > 920:
        # MCS4.dump(nb)
    if step:
        MCS4.dump(nb)
        s = input()
        if s == 'cont':
            step = False

# Run the system
MCS4.run(callback)