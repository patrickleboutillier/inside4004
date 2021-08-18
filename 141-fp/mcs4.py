import os
import chips.i4001 as i4001, chips.i4002 as i4002, chips.i4003 as i4003, chips.i4004 as i4004
import chips.keyboard as keyboard, chips.printer as printer, chips.lights as lights
import MCS4
from hdl import *


MCS4 = MCS4.MCS4()
ph1 = MCS4.clock.ph1
ph2 = MCS4.clock.ph2
data = MCS4.data
cm_rom = MCS4.cm_rom
cm_ram = MCS4.cm_ram
test = MCS4.test
CPU = MCS4.CPU
sync = CPU.sync

# Create 5 ROMs
PROM = [i4001.i4001(0, 0, ph1, ph2, sync, data, cm_rom), i4001.i4001(1, 1, ph1, ph2, sync, data, cm_rom), i4001.i4001(2, 0, ph1, ph2, sync, data, cm_rom), 
    i4001.i4001(3, 0, ph1, ph2, sync, data, cm_rom), i4001.i4001(4, 0, ph1, ph2, sync, data, cm_rom)]
for r in PROM:
    MCS4.addROM(r)

# Create 2 RAMS
RAM = [i4002.i4002(0, 0, ph1, ph2, sync, data, cm_ram.wire(0)), i4002.i4002(0, 1, ph1, ph2, sync, data, cm_ram.wire(0))]
for r in RAM:
    MCS4.addRAM(0, r)

# Lights
lights = lights.lights(memory=RAM[1].output.wire(0), overflow=RAM[1].output.wire(1), negative=RAM[1].output.wire(2))

# Create keyboard 4003
kbdsr = i4003.i4003(name="KB", clock=PROM[0].io.wire(0), data_in=PROM[0].io.wire(1), enable=wire(1))
MCS4.addSR(kbdsr)

# Keyboard
keyboard = keyboard.keyboard(kbdsr.parallel_out, lights)
for i in range(4):
    buf(keyboard.output().wire(i), PROM[1].io.wire(i))
buf(keyboard.advance(), PROM[2].io.wire(3))
kb = os.environ.get('KEY_BUFFER')
if kb is not None:
    keyboard.setKeyBuffer(kb)


# Create printer 4003s
# Order important here to void race conditions
psr2 = i4003.i4003(name="P2", clock=PROM[0].io.wire(2), data_in=PROM[0].io.wire(1), enable=wire(1))
psr1 = i4003.i4003(name="P1", clock=PROM[0].io.wire(2), data_in=psr2.serial_out, enable=wire(1))
MCS4.addSR(psr1)
MCS4.addSR(psr2)

# Printer
printer = printer.printer(fire=RAM[0].output.wire(1), advance=RAM[0].output.wire(3), color=RAM[0].output.wire(0))
for i in range(10):
    buf(psr2.parallel_out.wire(i), printer.input().wire(i))
    buf(psr1.parallel_out.wire(i), printer.input().wire(10+i))
buf(printer.sector(), test)
buf(printer.index(), PROM[2].io.wire(0))


# Load the program
MCS4.program()


# TODO: Use argparse to handle these options
step = False
dump = False
wait_for_start_sector_pulse = [0x001, 0x22c, 0x23f, 0x24b]
wait_for_end_sector_pulse = [0x0fd, 0x26e]
kb_toggle = False
optimize = False


def callback(nb):
    global step, kb_toggle, optimize
    # Save some time by not waiting for nothing...
    if optimize:
        if CPU.addr.getPC() in wait_for_start_sector_pulse and test.v() == 0:
            printer.endSectorPeriod()
            printer.startSectorPulse()
        elif CPU.addr.getPC() in wait_for_end_sector_pulse and test.v() == 1:
            printer.endSectorPulse()
        else:
            printer.cycle()
    else:
        printer.cycle()

    if (CPU.addr.stack[CPU.addr.sp] == 0x003) and (RAM[0].status[0][3] == 0): # Before keyboard scanning in main loop, and a button is not currently held down)
        keyboard.clearAdvance() # In case we "pressed" the paper advance button
        kb_toggle = not kb_toggle
        if not kb_toggle:
            keyboard.readKey()

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