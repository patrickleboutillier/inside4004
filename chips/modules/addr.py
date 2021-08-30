from chips.modules.timing import *
from hdl import *


# This class implements the addressing part of the CPU. It contains the stack and the stack pointer
# It uses the data bus exclusively for input and output.
# It is also responsible for everything that happens during A1, A2 and A3 in the CPU.


class addr:
    def __init__(self, inst, timing, data):
        self.data = data            # The data bus 
        self.inst = inst
        self.inst.addr = self
        self.incr_in = 0            # The input to the address incrementer
        self.cy = 0                 # The carry (in) for the address incrementer
        self_cy_out = 0             # The carry (out) for the address incrementer
        self.ph = 0                 # The high nibble of the program counter 
        self.pl = 0                 # The middle nibble of the program counter
        self.pm = 0                 # The low nibble of the program counter
        self.sp = 0                 # The stack pointer
        self.row_num = 0            # The working row in the stack
        self.stack = [{'h':0, 'm':0, 'l':0}, {'h':0, 'm':0, 'l':0}, {'h':0, 'm':0, 'l':0}, {'h':0, 'm':0, 'l':0}]

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
            self.incr_in = self.data.v

        @A11        # Output pl to the data bus.
        def _():
            self.data.v = self.pl

        @A21        # Output pm to the data bus.
        def _():
            self.data.v = self.pm

        @A31        # Output ph to the data bus.
        def _():
            self.data.v = self.ph

        @A12clk2    # Increment pl
        def _():
            sum = self.pl + 1
            self.cy_out = sum >> 4
            self.pl = sum & 0xF

        @A22clk1
        @A32clk1
        def _():
            self.cy = self.cy_out

        @A22clk2    # Increment pm
        def _():
            sum = self.pm + self.cy
            self.cy_out = sum >> 4
            self.pm = sum & 0xF

        @A32clk2    # Increment ph
        def _():
            sum = self.ph + self.cy
            self.cy_out = sum >> 4
            self.ph = sum & 0xF

        @X12clk2
        @X32clk2       # Update the program counter with the contents of the stack.
        def _():
            if not self.inst.inh():
                self.ph = self.stack[self.row_num]['h']
                self.pm = self.stack[self.row_num]['m']
                self.pl = self.stack[self.row_num]['l']
                #print("restored", self.ph << 8 | self.pm << 4 | self.pl)

        @M12clk1
        @X22clk1        # Update the stack with the contents of the program counter. 
        def _():
            if self.timing.x2() and self.inst.inh:
                return
            if not (self.inst.fin() and not self.inst.sc):
                #print("commit", self.timing.slave, self.ph << 8 | self.pm << 4 | self.pl)
                self.stack[self.row_num]['h'] = self.ph
                self.stack[self.row_num]['m'] = self.pm
                self.stack[self.row_num]['l'] = self.pl

        @X32            # Commit the stack pointer to row_num
        def _():
            self.row_num = self.sp

    # Used in the calculator simulator to check the value of the program counter. 
    def isPCin(self, addrs):
        pc = self.ph << 8 | self.pm << 4 | self.pl
        for addr in addrs:
            if pc == addr:
                return True
        return False

    def setPH(self):
        self.ph = self.incr_in

    def setPM(self):
        self.pm = self.incr_in

    def setPL(self):
        self.pl = self.incr_in

    # TODO: Do it properly... Increment the program counter
    def incPC(self):
        pc = self.ph << 8 | self.pm << 4 | self.pl
        pc = pc + 1
        self.ph = pc >> 8 & 0xF
        self.pm = pc >> 4 & 0xF
        self.pl = pc & 0xF

    # Increment the stack pointer
    def decSP(self):
        self.sp = (self.sp - 1) & 0b11


    def dump(self):
        print("SP/PC:{:02b}/{:<4}".format(self.sp, self.ph << 8 | self.pm << 4 | self.pl), end = '')  
