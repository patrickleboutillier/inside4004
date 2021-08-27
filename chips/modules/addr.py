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
        self.row_h = 0
        self.row_l = 0
        self.row_m = 0
        self.sp = 0
        self.row_num = 0
        self.stack = [{'h':0, 'm':0, 'l':0}, {'h':0, 'm':0, 'l':0}, {'h':0, 'm':0, 'l':0}, {'h':0, 'm':0, 'l':0}]

        self.timing = timing

        @A11 
        def _():
            if self.cpu.inst.fin() and self.cpu.inst.sc:
                self.scratch.enableRegPairL()
            else:
                self.data.v = self.stack[self.sp]['l']

        @A21
        def _():
            if self.cpu.inst.fin() and not self.cpu.inst.sc:
                self.scratch.enableRegPairH()
            else:
                self.data.v = self.stack[self.sp]['m']

        @A31
        def _():
            self.data.v = self.stack[self.sp]['h']

        @A32clk1
        def _():
            self.cm_rom.v = 1

        @A32clk2
        def _():
            if self.cpu.inst.fin() and not self.cpu.inst.sc:
                return
            self.incPC()

        @M12clk1
        def _():
            self.cm_rom.v = 0
            if self.cpu.inst.jms() and not self.cpu.inst.sc:
                self.incSP()


    def isPC(self, addr):
        pc = self.stack[self.sp]['h'] << 8 | self.stack[self.sp]['m'] << 4 | self.stack[self.sp]['l']
        return pc == addr

    def setPH(self):
        self.stack[self.sp]['h'] = self.data.v

    def setPM(self):
        self.stack[self.sp]['m'] = self.data.v

    def setPL(self):
        self.stack[self.sp]['l'] = self.data.v

    def incPC(self):
        pc = self.stack[self.sp]['h'] << 8 | self.stack[self.sp]['m'] << 4 | self.stack[self.sp]['l']
        pc = pc + 1
        self.stack[self.sp]['h'] = pc >> 8
        self.stack[self.sp]['m'] = pc >> 4 & 0xF
        self.stack[self.sp]['l'] = pc & 0xF

    def incSP(self):
        self.sp = (self.sp + 1) & 0b11

    def decSP(self):
        self.sp = (self.sp - 1) & 0b11


    def dump(self):
        print("SP/PC:{:02b}/{:<4}".format(self.sp, self.stack[self.sp]), end = '')  