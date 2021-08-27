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
        self.row_num = 0            # The working row number
        self.row_even = 0           # The even register in the working row
        self.row_odd = 0            # The odd register in the working row
        self.data_in = 0            # Data in from the bus

        self.timing = timing

        @M12
        @M22
        @A12clk1
        @A22clk1
        @A32clk1
        @X12clk1
        @X22clk1
        @X32clk1    # Sample data from the bus at these times.
        def _():
            self.data_in = self.data.v

        @A32clk2
        @X12clk2    # Set working row from the register array. There is a 0 override for FIN during X12.
        def _():
            if self.inst.sc:
                row_num = self.row_num
                if self.timing.x1():
                    if self.inst.fin():
                        row_num = 0  
                self.row_even = self.index_reg[row_num * 2]
                self.row_odd = self.index_reg[(row_num * 2) + 1]

        @A12clk2
        @M12clk2
        def _():    #  Save working row to the register array
            if self.inst.sc:
                self.index_reg[self.row_num * 2] = self.row_even
                self.index_reg[(self.row_num * 2) + 1] = self.row_odd

        @M12clk2
        def _():
            if (self.inst.fim() or self.inst.fin()) and not self.inst.sc:
                self.setRegPairH()

        @M22clk2    # Read OPA from the data bus and set the working row. Also, save 
        def _():
            if self.inst.sc:
                self.row_num = self.data.v >> 1
            if (self.inst.fim() or self.inst.fin()) and not self.inst.sc:
                self.setRegPairL()


    # Enable the working register (according to whether OPA is even or odd) to the bus.
    def enableReg(self):
        self.data.v = self.row_even if self.inst.opa_even() else self.row_odd

    # Enable the even working register to the bus.
    def enableRegPairH(self):
        self.data.v = self.row_even

    # Enable the odd working register to the bus.
    def enableRegPairL(self):
        self.data.v = self.row_odd

    # Set the proper working register value from data_in.
    def setReg(self):
        if self.inst.opa_even():
            self.row_even = self.data_in
        else:
            self.row_odd = self.data_in

    # Set the even (high) working register from data_in
    def setRegPairH(self):
        self.row_even = self.data_in

    # Set the odd (low) working register from data_in
    def setRegPairL(self):
        self.row_odd = self.data_in


    def dump(self):
        print("INDEX:{}".format("".join(["{:x}".format(x) for x in self.index_reg])), end='')

    