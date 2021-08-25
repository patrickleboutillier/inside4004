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
        self.sp = 0
        self.stack = [0, 0, 0, 0]

        self.timing = timing

        @A11 
        def _():
            if self.cpu.inst.fin() and self.cpu.inst.dcff:
                self.scratch.enableReg1()
            else:
                self.data.v = self.stack[self.sp] & 0xF

        @A21
        def _():
            if self.cpu.inst.fin() and self.cpu.inst.dcff:
                self.scratch.enableReg0()
            else:
                self.data.v = (self.stack[self.sp] >> 4) & 0xF

        @A31
        def _():
            self.data.v = self.stack[self.sp] >> 8

        @A3clk1
        def _():
            self.cm_rom.v = 1

        @A3clk2
        def _():
            if self.cpu.inst.fin() and self.cpu.inst.dcff:
                return
            self.incPC()

        @M1clk1
        def _():
            self.cm_rom.v = 0
            if self.cpu.inst.jms() and self.cpu.inst.dcff:
                self.incSP()


    def setPH(self):
        self.stack[self.sp] = (self.stack[self.sp] & 0x0FF) | self.data.v << 8

    def setPM(self):
        self.stack[self.sp] = (self.stack[self.sp] & 0xF0F) | self.data.v << 4

    def setPL(self):
        self.stack[self.sp] = (self.stack[self.sp] & 0xFF0) | self.data.v

    def incPC(self):
        self.stack[self.sp] += 1

    def incSP(self):
        self.sp = (self.sp + 1) & 0b11

    def decSP(self):
        self.sp = (self.sp - 1) & 0b11


    def dump(self):
        print("SP/PC:{:02b}/{:<4}".format(self.sp, self.stack[self.sp]), end = '')  