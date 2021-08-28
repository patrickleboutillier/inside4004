from chips.modules.timing import *
from hdl import *


# This class implements the addressing part of the CPU. It contains the stack and the stack pointer
# It uses the data bus exclusively for input and output.
# It is also responsible for everything that happens during A1, A2 and A3 in the CPU.


class addr:
    def __init__(self, cpu, scratch, timing, data, cm_rom):
        self.cpu = cpu
        self.scratch = scratch
        self.data = data 
        self.cm_rom = cm_rom
        self.incr_in = 0
        self.data_in = 0
        self.row_h = 0
        self.row_l = 0
        self.row_m = 0
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
            self.data.v = self.row_l

        @A21
        def _():
            self.data.v = self.row_m

        @A31
        def _():
            self.data.v = self.row_h

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
            if self.cpu.inst.jms() and not self.cpu.inst.sc:
                self.incSP()

        @M12clk2    # TODO: Move to instructions
        def _():
            if (self.cpu.inst.jun() or self.cpu.inst.jms()) and not self.cpu.inst.sc:
                self.setPM()
            elif (self.cpu.inst.jcn() or self.cpu.inst.isz()) and not self.cpu.inst.sc:
                if self.cpu.inst.cond:
                    self.setPM()

        @M22clk2    # TODO: Move to instructions
        def _():
            if (self.cpu.inst.jun() or self.cpu.inst.jms()) and not self.cpu.inst.sc:
                self.setPL()
            elif (self.cpu.inst.jcn() or self.cpu.inst.isz()) and not self.cpu.inst.sc:
                if self.cpu.inst.cond:
                    self.setPL()

        @X12clk2
        @X32clk2
        def _():
            if not self.cpu.inst.inh():
                self.row_h = self.stack[self.row_num]['h']
                self.row_m = self.stack[self.row_num]['m']
                self.row_l = self.stack[self.row_num]['l']
                #print("restored", self.row_h << 8 | self.row_m << 4 | self.row_l)

        @M12clk1
        @X22clk1
        def _():
            if self.timing.x2() and self.cpu.inst.inh:
                return
            if not (self.cpu.inst.fin() and not self.cpu.inst.sc):
                #print("commit", self.timing.slave, self.row_h << 8 | self.row_m << 4 | self.row_l)
                self.stack[self.row_num]['h'] = self.row_h
                self.stack[self.row_num]['m'] = self.row_m
                self.stack[self.row_num]['l'] = self.row_l

        @X32
        def _():
            self.row_num = self.sp


    def isPC(self, addr):
        pc = self.row_h << 8 | self.row_m << 4 | self.row_l
        return pc == addr

    def setPH(self):
        self.row_h = self.data.v

    def setPM(self):
        self.row_m = self.data.v

    def setPL(self):
        self.row_l = self.data.v

    def incPC(self):
        pc = self.row_h << 8 | self.row_m << 4 | self.row_l
        pc = pc + 1
        self.row_h = pc >> 8 & 0xF
        self.row_m = pc >> 4 & 0xF
        self.row_l = pc & 0xF

    def incSP(self):
        self.sp = (self.sp + 1) & 0b11


    def dump(self):
        print("SP/PC:{:02b}/{:<4}".format(self.sp, self.row_h << 8 | self.row_m << 4 | self.row_l), end = '')  