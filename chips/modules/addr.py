from chips.modules.timing import *
from hdl import *


# This class implements the addressing part of the CPU. It contains the stack and the stack pointer
# It uses the data bus exclusively for input and output.
# It is also responsible for everything that happens during A1, A2 and A3 in the CPU.


class addr:
    def __init__(self, inst, timing, data, cm_rom):
        self.data = data 
        self.inst = inst
        self.cm_rom = cm_rom
        self.incr_in = 0
        self.data_in = 0
        self.ph = 0
        self.pl = 0
        self.pm = 0
        self.sp = 0
        self.row_num = 0
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

        @A11 
        def _():
            self.data.v = self.pl

        @A21
        def _():
            self.data.v = self.pm

        @A31
        def _():
            self.data.v = self.ph

        @A32clk1
        def _():
            self.cm_rom.v = 1

        @A32clk2
        def _():
            self.incPC()

        @M12clk1
        def _():
            self.cm_rom.v = 0

        @M22clk2    # TODO: Move to instructions
        def _():
            if self.inst.jms() and not self.inst.sc:
                self.incSP()

        @M12clk2    # TODO: Move to instructions
        def _():
            if (self.inst.jun() or self.inst.jms()) and not self.inst.sc:
                self.setPM()
            elif (self.inst.jcn() or self.inst.isz()) and not self.inst.sc:
                if self.inst.cond:
                    self.setPM()

        @M22clk2    # TODO: Move to instructions
        def _():
            if (self.inst.jun() or self.inst.jms()) and not self.inst.sc:
                self.setPL()
            elif (self.inst.jcn() or self.inst.isz()) and not self.inst.sc:
                if self.inst.cond:
                    self.setPL()

        @X12clk2
        @X32clk2
        def _():
            if not self.inst.inh():
                self.ph = self.stack[self.row_num]['h']
                self.pm = self.stack[self.row_num]['m']
                self.pl = self.stack[self.row_num]['l']
                #print("restored", self.ph << 8 | self.pm << 4 | self.pl)

        @M12clk1
        @X22clk1
        def _():
            if self.timing.x2() and self.inst.inh:
                return
            if not (self.inst.fin() and not self.inst.sc):
                #print("commit", self.timing.slave, self.ph << 8 | self.pm << 4 | self.pl)
                self.stack[self.row_num]['h'] = self.ph
                self.stack[self.row_num]['m'] = self.pm
                self.stack[self.row_num]['l'] = self.pl

        @X32
        def _():
            self.row_num = self.sp


    def isPC(self, addr):
        pc = self.ph << 8 | self.pm << 4 | self.pl
        return pc == addr

    def setPH(self):
        self.ph = self.data.v

    def setPM(self):
        self.pm = self.data.v

    def setPL(self):
        self.pl = self.data.v

    def incPC(self):
        pc = self.ph << 8 | self.pm << 4 | self.pl
        pc = pc + 1
        self.ph = pc >> 8 & 0xF
        self.pm = pc >> 4 & 0xF
        self.pl = pc & 0xF

    def incSP(self):
        self.sp = (self.sp + 1) & 0b11


    def dump(self):
        print("SP/PC:{:02b}/{:<4}".format(self.sp, self.ph << 8 | self.pm << 4 | self.pl), end = '')  