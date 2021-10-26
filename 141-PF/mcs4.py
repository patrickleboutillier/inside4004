import os, time
import chips.i4001 as i4001, chips.i4002 as i4002, chips.i4003 as i4003, chips.i4004 as i4004
import chips.keyboard as keyboard, chips.printer as printer, chips.lights as lights
import MCS4
from hdl import *


MCS4 = MCS4.MCS4()
clk1 = MCS4.clock.clk1
clk2 = MCS4.clock.clk2
data = MCS4.data
cm_rom = MCS4.cm_rom
cm_ram = MCS4.cm_ram
test = MCS4.test
CPU = MCS4.CPU
sync = CPU.sync


# Create 5 ROMs
# PROM = [i4001.i4001(0, 0, clk1, clk2, sync, data, cm_rom), i4001.i4001(1, 1, clk1, clk2, sync, data, cm_rom)]
    # i4001.i4001(2, 0, clk1, clk2, sync, data, cm_rom)] 
    # i4001.i4001(3, 0, clk1, clk2, sync, data, cm_rom), i4001.i4001(4, 0, clk1, clk2, sync, data, cm_rom)]
# for r in PROM:
    # MCS4.addROM(r)

# Create 2 RAMS
# RAM = [i4002.i4002(0, 0, clk1, clk2, sync, data, cm_ram)] #, i4002.i4002(0, 1, clk1, clk2, sync, data, cm_ram)]
# for r in RAM:
    # MCS4.addRAM(0, r)

# Lights
# lights = lights.lights(memory=RAM[1].output.pwire(0), overflow=RAM[1].output.pwire(1), negative=RAM[1].output.pwire(2))

# Create keyboard 4003
# kbdsr = i4003.i4003(name="KB", clock=PROM[0].io.pwire(0), data_in=PROM[0].io.pwire(1), enable=pwire(1))
# MCS4.addSR(kbdsr)

# Keyboard
# keyboard = keyboard.keyboard(kbdsr.parallel_out, lights)
# for i in range(4):
    # pbuf(keyboard.output.pwire(i), PROM[1].io.pwire(i))
# pbuf(keyboard.advance, PROM[2].io.pwire(3))
# kb = os.environ.get('KEY_BUFFER')
# if kb is not None:
    # keyboard.appendKeyBuffer(kb)
# kb = MCS4.args.key_buffer
# if kb is not None:
    # keyboard.appendKeyBuffer(kb)

# Create printer 4003s
# Order important here to void race conditions
# psr2 = i4003.i4003(name="P2", clock=PROM[0].io.pwire(2), data_in=PROM[0].io.pwire(1), enable=pwire(1))
# psr1 = i4003.i4003(name="P1", clock=PROM[0].io.pwire(2), data_in=psr2.serial_out, enable=pwire(1))
# MCS4.addSR(psr1)
# MCS4.addSR(psr2)

# Printer
# printer = printer.printer(fire=RAM[0].output.pwire(1), advance=RAM[0].output.pwire(3), color=RAM[0].output.pwire(0))
# for i in range(10):
#     pbuf(psr2.parallel_out.pwire(i), printer.input.pwire(i))
#     pbuf(psr1.parallel_out.pwire(i), printer.input.pwire(10+i))
# pbuf(printer.sector, test)
# pbuf(printer.index, PROM[2].io.pwire(0))


# Load the program
# MCS4.program()


# TODO: Use argparse to handle these options
step = False

# kb_toggle = False
# send_key = wire(0, 0b0110)


def callback(nb):
    global step, kb_toggle, MCS4
    # printer.doCycle()

    # CPU.addr.sendKey() 
    # send_key.v = 0 
    # if CPU.addr.isPCin([0x003]):                      # Before keyboard scanning in main loop, and a button is not currently held down)
    #     # keyboard.clearAdvance()                     # In case we "pressed" the paper advance button
    #     kb_toggle = not kb_toggle
    #     if not kb_toggle:
    #         # print(nb, "readKey")
    #         # keyboard.readKey()
    #         print(time.localtime() ,"send_key")
    #         send_key.v = 1

    if step:
        MCS4.dump(nb)
        s = input()
        if s == 'c':
            # pass
            step = False


# Run the system
MCS4.run(None)