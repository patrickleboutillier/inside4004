import chips.modules.timing as timing
from hdl import *


class i4001():
    def __init__(self, chipnum, io_cfg, ph1, ph2, sync, data, cm):
        self.timing = timing.timing(ph1, ph2, sync)
        self.when()
        self.chipnum = chipnum
        self.data = data
        self.addrh = 0 
        self.addrl = 0 
        self.rom = [0] * 256
        self.chipselect = 0 
        self.srcff = 0 
        self.opr = 0
        self.opa = 0
        self.cm = cm
        self.io = bus()
        if io_cfg:
            self.io_output = None
        else:
            self.io_output = reg(bus(), wire(), self.io)

    def when(self):
        def A1ph2(self):
            self.addrl = self.data._v
        def A2ph2(self):
            self.addrh = self.data._v
        def A3ph2(self):
            if self.cm.v():
                self.chipselect = 1 if self.chipnum == self.data._v else 0
        def M1ph1(self):
            if self.chipselect:
                self.opr = self.rom[self.addrh << 4 | self.addrl] >> 4
                self.data.v(self.opr)
        def M1ph2(self):
            if not self.chipselect:
                self.opr = self.data._v
        def M2ph1(self):
            if self.chipselect:
                self.opa = self.rom[self.addrh << 4 | self.addrl] & 0xF
                self.data.v(self.opa)
        def M2ph2(self):
            if not self.chipselect:
                self.opa = self.data._v
        def X2ph1(self):
            if self.srcff and self.opr == 0b1110 and self.opa == 0b1010:
                self.data.v(self.io._v)
        def X2ph2(self):
            if self.cm.v():
                # SRC instruction
                self.srcff = 1 if self.chipnum == self.data._v else 0
            elif self.srcff and self.opr == 0b1110 and self.opa == 0b0010:
                if self.io_output is not None:
                    self.io_output.bi().v(self.data._v)
                    self.io_output.s().v(1)
                    self.io_output.s().v(0)

        self.timing.whenA1ph2(A1ph2, self)
        self.timing.whenA2ph2(A2ph2, self)
        self.timing.whenA3ph2(A3ph2, self)
        self.timing.whenM1ph1(M1ph1, self)
        self.timing.whenM1ph2(M1ph2, self)
        self.timing.whenM2ph1(M2ph1, self)
        self.timing.whenM2ph2(M2ph2, self)
        self.timing.whenX2ph1(X2ph1, self)
        self.timing.whenX2ph2(X2ph2, self)

    def program(self, fi):
        addr = 0
        for line in fi:
            inst = line[0:8]
            if inst[0] in ['0', '1']:
                self.rom[addr] = int(inst, 2)
                addr += 1
                if addr == 256:
                    break
        # Finish of with NOPs
        for x in range(addr, 256):
            self.rom[x] = 0
        return addr

    def dump(self):
        print("ROM {:x}: IO:{:04b}  ".format(self.chipnum, self.io._v), end = "")
