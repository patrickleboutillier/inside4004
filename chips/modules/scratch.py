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

        @A3clk2
        def _():
            if self.inst.sc:
                self.row_even = self.index_reg[self.row_num * 2]
                self.row_odd = self.index_reg[(self.row_num * 2) + 1]

        @X1clk2
        def _():
            if self.inst.sc:
                row_num = self.row_num
                if self.inst.fin():
                    row_num = 0                  
                self.row_even = self.index_reg[row_num * 2]
                self.row_odd = self.index_reg[(row_num * 2) + 1]

        #@A1clk2
        #@M1clk2
        #def _():
        #    if self.inst.sc:
        #        self.index_reg[self.row_num * 2] = self.row_even
        #        self.index_reg[(self.row_num * 2) + 1] = self.row_odd

        @M2clk2
        def _():
            if self.inst.sc:
                self.row_num = self.data.v >> 1


    def enableReg(self):
        self.data.v = self.index_reg[self.inst.opa]

    def enableReg0(self):
        self.data.v = self.index_reg[0]

    def enableReg1(self):
        self.data.v = self.index_reg[1]

    def enableRegPairH(self):
        self.data.v = self.index_reg[self.inst.opa & 0b1110]

    def enableRegPairL(self):
        self.data.v = self.index_reg[self.inst.opa | 0b0001]

    def setReg(self):
        self.index_reg[self.inst.opa] = self.data.v

    def setRegPairH(self):
        self.index_reg[self.inst.opa & 0b1110] = self.data.v

    def setRegPairL(self):
        self.index_reg[self.inst.opa | 0b0001] = self.data.v

    def regZero(self):
        return 1 if self.index_reg[self.inst.opa] == 0 else 0


    def dump(self):
        print("INDEX:{}".format("".join(["{:x}".format(x) for x in self.index_reg])), end='')

    