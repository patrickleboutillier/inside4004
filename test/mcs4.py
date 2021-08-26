import chips.i4001 as i4001, chips.i4002 as i4002, chips.i4004 as i4004
import MCS4
from hdl import *


MCS4 = MCS4.MCS4()
clk1 = MCS4.clock.clk1
clk2 = MCS4.clock.clk2
data = MCS4.data
cm_rom = MCS4.cm_rom
cm_ram = MCS4.cm_ram
CPU = MCS4.CPU
sync = CPU.sync

# Create 1 ROM for now
PROM = [i4001.i4001(0, 1, clk1, clk2, sync, data, cm_rom), i4001.i4001(1, 1, clk1, clk2, sync, data, cm_rom), 
    i4001.i4001(2, 0, clk1, clk2, sync, data, cm_rom), i4001.i4001(3, 1, clk1, clk2, sync, data, cm_rom)]
for r in PROM:
    MCS4.addROM(r)

# Create 2 RAMS
RAM = [i4002.i4002(0, 0, clk1, clk2, sync, data, cm_ram.pwire(0)), i4002.i4002(0, 1, clk1, clk2, sync, data, cm_ram.pwire(0))]
for r in RAM:
    MCS4.addRAM(0, r)

# Connect input and outputs for our test cases
for i in range(4):
    pbuf(RAM[0].output.pwire(i), PROM[0].io.pwire(i))
    pbuf(RAM[1].output.pwire(i), PROM[1].io.pwire(i))       
    pbuf(PROM[2].io.pwire(i), PROM[3].io.pwire(i))


MCS4.program()
MCS4.run()