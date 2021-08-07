import sys
import chips.i4001 as i4001, chips.i4002 as i4002, chips.i4003 as i4003, chips.i4004 as i4004
import chips.keyboard as keyboard, chips.printer as printer
import MCS4
from hdl import *


MCS4 = MCS4.MCS4()
data = MCS4.data()
cm_rom = MCS4.cm_rom()
cm_ram = MCS4.cm_ram()
test = MCS4.test()

# Create 5 ROMs
PROM = [i4001.i4001(0, 0, data, cm_rom), i4001.i4001(1, 1, data, cm_rom), i4001.i4001(2, 0, data, cm_rom), 
    i4001.i4001(3, 0, data, cm_rom), i4001.i4001(4, 0, data, cm_rom)]
for r in PROM:
    MCS4.addROM(r)

# Create 2 RAMS
RAM = [i4002.i4002(0, 0, data, cm_ram.wire(0)), i4002.i4002(0, 1, data, cm_ram.wire(0))]
for r in RAM:
    MCS4.addRAM(0, r)

# Create keyboard 4003
kbdsr = i4003.i4003(name="KB", clock=PROM[0].io().wire(0), data_in=PROM[0].io().wire(1), enable=wire(1))
MCS4.addSR(kbdsr)

# Keyboard
keyboard = keyboard.keyboard(kbdsr.parallel_out())
for i in range(4):
    buf(keyboard.output().wire(i), PROM[1].io().wire(i))

# Create keyboard 4003s
# Order important here to void race conditions
psr2 = i4003.i4003(name="P2", clock=PROM[0].io().wire(2), data_in=PROM[0].io().wire(1), enable=wire(1))
psr1 = i4003.i4003(name="P1", clock=PROM[0].io().wire(2), data_in=psr2.serial_out(), enable=wire(1))
MCS4.addSR(psr1)
MCS4.addSR(psr2)

# Printer
printer = printer.printer(fire=RAM[0].output().wire(1), advance=RAM[0].output().wire(3), color=RAM[0].output().wire(0))
for i in range(10):
    buf(psr2.parallel_out().wire(i), printer.input().wire(i))
    buf(psr1.parallel_out().wire(i), printer.input().wire(10+i))
buf(printer.sector(), test)
buf(printer.index(), PROM[2].io().wire(0))

# Load the program
MCS4.program()


step = False
dump = False
fire_hammers = 0x272
key_found = 0x2a
advance = 0x24d
wait_for_start_sector_pulse = [0x001, 0x22c, 0x23f, 0x24b]
wait_for_end_sector_pulse = [0x0fd, 0x26e]
CPU = MCS4._CPU


def callback(nb):
    global step
    if CPU.addr.getPC() in wait_for_start_sector_pulse and test.v() == 0:
        printer.endSectorPeriod()
        printer.startSectorPulse()
    elif CPU.addr.getPC() in wait_for_end_sector_pulse and test.v() == 1:
        printer.endSectorPulse()
    else:
        printer.cycle()

    if (CPU.addr.getPC() == 0x0bd) and (RAM[0]._status[0][3] == 0) and (CPU.index_reg[14] == 0) and (CPU.index_reg[15] == 0): # Before keyboard scanning
        # MCS4.dump(nb)
        # step = True
        k = keyboard.readKey()
        if k == 'q':
            sys.exit()

    #if CPU.addr.getPC() in [advance]: # , 0x292
    #    MCS4.dump(nb)
    #    step = True

    if step:
        MCS4.dump(nb)
        s = input()
        if s == 'c':

            # pass
            step = False
    elif dump:
       MCS4.dump(nb)


# Run the system
MCS4.run(callback)