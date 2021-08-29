from chips.modules.timing import *
from hdl import *


# This class implements the instruction processing part of the CPU. It contains the DC (double cycle) flip-flop, the condition register.
# as well as the OPA and OPR register, which are populated via the data bus.
# It is also responsible for everything that happens during M1 and M2 in the CPU.


class io:
    def __init__(self, inst, test, cm_rom, cm_ram):
        self.inst = inst
        self.inst.ioc = self
        self.test = test
        self.cm_rom = cm_rom
        self.cm_ram = cm_ram
        self.ram_bank = 1

        @M22clk1
        def _():
            # This signal turned off at X12clk1 below
            if self.inst.io():
                self.inst.cm_ram.v(self.inst.ram_bank)

        @X12clk1
        def _():
            if self.inst.io():
                self.inst.cm_ram.v(0) 


    def testZero(self):
        return 1 if self.test.v == 0 else 0