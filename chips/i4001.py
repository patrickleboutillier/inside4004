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
        self.rom_select = 0 
        self.io_select = 0 
        self.src = 0 
        self.io_inst = 0 
        self.rdr = 0
        self.wrr = 0
        self.cm = cm
        self.io = bus()


    def when(self):
        def A1ph2(self):
            self.addrl = self.data._v
        def A2ph2(self):
            self.addrh = self.data._v
        def A3ph2(self):
            if self.cm.v():
                self.rom_select = 1 if self.chipnum == self.data._v else 0
        def M1ph1(self):
            if self.rom_select:
                opr = self.rom[self.addrh << 4 | self.addrl] >> 4
                self.data.v(opr)
        def M1ph2(self):
            self.io_inst = 1 if self.data._v == 0b1110 else 0
        def M2ph1(self):
            if self.rom_select:
                self.opa = self.rom[self.addrh << 4 | self.addrl] & 0xF
                self.data.v(self.opa)
        def M2ph2(self):
            self.rdr = 1 if self.io_inst and self.data._v == 0b1010 else 0
            self.wrr = 1 if self.io_inst and self.data._v == 0b0010 else 0
        def X2ph1(self):
            if self.io_select and self.rdr:
                self.data.v(self.io._v)
        def X2ph2(self):
            if self.cm.v():
                # SRC instruction
                if self.chipnum == self.data._v:
                    self.src = 1
                    self.io_select = 1
                else:
                    self.io_select = 0
            else:
                self.src = 0
                if self.io_select and self.wrr:
                    self.io.v(self.data._v)
        def X3ph2(self):
            if self.src:
                # Data @ X3 is ignored
                pass

        self.timing.whenA1ph2(A1ph2, self)
        self.timing.whenA2ph2(A2ph2, self)
        self.timing.whenA3ph2(A3ph2, self)
        self.timing.whenM1ph1(M1ph1, self)
        self.timing.whenM1ph2(M1ph2, self)
        self.timing.whenM2ph1(M2ph1, self)
        self.timing.whenM2ph2(M2ph2, self)
        self.timing.whenX2ph1(X2ph1, self)
        self.timing.whenX2ph2(X2ph2, self)
        self.timing.whenX3ph2(X3ph2, self)

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
