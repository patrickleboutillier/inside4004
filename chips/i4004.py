import chips.modules.timing as timing
import chips.modules.addr as addr, chips.modules.inst as inst, chips.modules.scratch as scratch
import chips.modules.alu as alu, chips.modules.control as control, chips.modules.io as io
from hdl import *


class i4004:
    def __init__(self, clk, data, cm_rom, cm_ram, test):
        self.timing = timing.timing(clk, None)
        self.sync = self.timing.sync
        self.data = data
        self.test = test
        self.inst = inst.inst(self.data)
        self.alu = alu.alu(self.inst, data)
        self.scratch = scratch.scratch(self.inst, self.timing, data)
        self.addr = addr.addr(self.inst, self.timing, self.data)
        self.io = io.io(self.inst, test, cm_rom, cm_ram)
        self.control = control.control(self.inst)



    def dump(self, cycle):
        print("\nCYCLE #{}".format(cycle))
        self.addr.dump() ; print("  ", end='')
        self.inst.dump() ; print("  ", end='')
        self.scratch.dump() ; print("  ", end='')
        print("TEST:{:b}  ACC/CY:{:04b}/{}".format(self.test.v, self.alu.acc, self.alu.cy))
