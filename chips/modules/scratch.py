from chips.modules.timing import *
from hdl import *


# This class implements the 16-register "scratch pad" of the CPU.
# It uses the data bus exclusively for input and output, but it has a direct connection to the OPA output
# that is used as the index inside the register (with possible alterations, i.e. set the last bit to 0 or 1)


class scratch:
    def __init__(self, timing, data):
        self.data = data            # The data bus
        self.inst = None            # Must be set after initialisation
        self.index_reg = [0] * 16   # The actual registers
        self.row_num = 0
        self.row_even = 0 
        self.row_odd = 0
        self.data_in = 0
        self.data_out = 0

        self.timing = timing

        @A32clk2
        def _():
            if self.inst.sc:
                self.row_even = self.index_reg[self.row_num * 2]
                self.row_odd = self.index_reg[(self.row_num * 2) + 1]

        @X12clk2
        def _():
            if self.inst.sc:
                row_num = self.row_num
                if self.inst.fin():
                    row_num = 0                  
                self.row_even = self.index_reg[row_num * 2]
                self.row_odd = self.index_reg[(row_num * 2) + 1]

        @A12clk2
        @M12clk2
        def _():
            if self.inst.sc:
                self.index_reg[self.row_num * 2] = self.row_even
                self.index_reg[(self.row_num * 2) + 1] = self.row_odd

        @M22clk2
        def _():
            if self.inst.sc:
                self.row_num = self.data.v >> 1

        @M12
        @M22
        @A12clk1
        @A22clk1
        @A32clk1
        @X12clk1
        @X22clk1
        @X32clk1
        def _():
            self.data_in = self.data.v


    def enableReg(self):
        self.data.v = self.row_even if self.inst.opa_even() else self.row_odd

    def enableRegPairH(self):
        self.data.v = self.row_even

    def enableRegPairL(self):
        self.data.v = self.row_odd

    def setReg(self):
        if self.inst.opa_even():
            self.row_even = self.data_in
        else:
            self.row_odd = self.data_in

    def setRegPairH(self):
        self.row_even = self.data.v

    def setRegPairL(self):
        self.row_odd = self.data.v


    def dump(self):
        print("INDEX:{}".format("".join(["{:x}".format(x) for x in self.index_reg])), end='')

    