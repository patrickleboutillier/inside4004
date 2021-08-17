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
        self.stack = [{'h':0, 'm':0, 'l':0}, {'h':0, 'm':0, 'l':0}, {'h':0, 'm':0, 'l':0}, {'h':0, 'm':0, 'l':0}]


    def when(self):
        def A1ph1(self):
            if self.cpu.inst.fin() and self.cpu.inst.dc:
                self.data.v(self.scratch.index_reg[1])
            else:
                self.data.v(self.stack[self.sp]['l'])
        def A2ph1(self):
            if self.cpu.inst.fin() and self.cpu.inst.dc:
                self.data.v(self.scratch.index_reg[0])
            else:
                self.data.v(self.stack[self.sp]['m'])
        def A3ph1(self):
            # Order not important here
            self.cm_rom.v(1)
            self.data.v(self.stack[self.sp]['h'])
        def A3ph2(self):
            if self.cpu.inst.fin() and self.cpu.inst.dc:
                pass
            else:
                # TODO: Fix this sequencing!!!!
                self.incPC()
                if self.cpu.inst.jms() and self.cpu.inst.dc:
                    self.incSP()
        def M1ph1(self):
            self.cm_rom.v(0)

        self.timing.whenA1ph1(A1ph1, self)
        self.timing.whenA2ph1(A2ph1, self)
        self.timing.whenA3ph1(A3ph1, self)
        self.timing.whenA3ph2(A3ph2, self)
        self.timing.whenM1ph1(M1ph1, self)

 
    def getPC(self):        # For debugging
        return self.stack[self.sp]['h'] << 8 | self.stack[self.sp]['m'] << 4 | self.stack[self.sp]['l']

    def setPH(self, ph):
        self.stack[self.sp]['h'] = ph

    def setPM(self, pm):
        self.stack[self.sp]['m'] = pm

    def setPL(self, pl):
        self.stack[self.sp]['l'] = pl

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