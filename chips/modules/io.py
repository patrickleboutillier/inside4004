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

        @A32clk1    # Turn on cm-rom for the 4001 chips that are listening.
        def _():
            self.cm_rom.v = 1

        @M12clk1    # Turn off cm-rom for the 4001 chips that are listening.
        def _():
            self.cm_rom.v = 0

        @M22clk1
        def _():
            if self.inst.io():
                self.cm_ram.v(self.ram_bank)

        @X12clk1
        def _():
            if self.inst.io():
                self.cm_ram.v(0) 


    def testZero(self):
        return 1 if self.test.v == 0 else 0

    def setRAMBank(self):
        acc_out = self.inst.alu.acc_out
        if acc_out & 0b0111 == 0:
            self.ram_bank = 1
        elif acc_out & 0b0111 == 1:
            self.ram_bank = 2
        elif acc_out & 0b0111 == 2:
            self.ram_bank = 4
        elif acc_out & 0b0111 == 3:
            self.ram_bank = 3
        elif acc_out & 0b0111 == 4:
            self.ram_bank = 8
        elif acc_out & 0b0111 == 5:
            self.ram_bank = 10
        elif acc_out & 0b0111 == 6:
            self.ram_bank = 12
        elif acc_out & 0b0111 == 7:
            self.ram_bank = 14