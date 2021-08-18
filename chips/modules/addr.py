from hdl import *


class addr:
    def __init__(self, cpu, scratch, timing, data, cm_rom):
        self.timing = timing
        self.when()
        self.cpu = cpu
        self.scratch = scratch
        self.data = data 
        self.cm_rom = cm_rom
        self.sp = 0
        self.stack = [0, 0, 0, 0]


    def when(self):
        def A1ph1(self):
            if self.cpu.inst.fin() and self.cpu.inst.dc:
                self.scratch.enableReg1()
            else:
                self.data.v(self.stack[self.sp] & 0xF)
        self.timing.whenA1ph1(A1ph1, self)

        def A2ph1(self):
            if self.cpu.inst.fin() and self.cpu.inst.dc:
                self.scratch.enableReg0()
            else:
                self.data.v((self.stack[self.sp] >> 4) & 0xF)
        self.timing.whenA2ph1(A2ph1, self)

        def A3ph1(self):
            # Order not important here
            self.cm_rom.v(1)
            self.data.v(self.stack[self.sp] >> 8)
        self.timing.whenA3ph1(A3ph1, self)

        def A3ph2(self):
            if self.cpu.inst.fin() and self.cpu.inst.dc:
                return
            self.incPC()
        self.timing.whenA3ph2(A3ph2, self)

        def M1ph1(self):
            self.cm_rom.v(0)
            if self.cpu.inst.jms() and self.cpu.inst.dc:
                self.incSP()
        self.timing.whenM1ph1(M1ph1, self)


    def setPH(self):
        self.stack[self.sp] = (self.stack[self.sp] & 0x0FF) | self.data._v << 8

    def setPM(self):
        self.stack[self.sp] = (self.stack[self.sp] & 0xF0F) | self.data._v << 4

    def setPL(self):
        self.stack[self.sp] = (self.stack[self.sp] & 0xFF0) | self.data._v

    def incPC(self):
        self.stack[self.sp] += 1

    def incSP(self):
        self.sp = (self.sp + 1) & 0b11

    def decSP(self):
        self.sp = (self.sp - 1) & 0b11


    def dump(self):
        print("SP/PC:{:02b}/{:<4}".format(self.sp, self.stack[self.sp]), end = '')  