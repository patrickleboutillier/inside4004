import chips.modules.timing as timing
from hdl import *


class i4001():
    def __init__(self, id, io_cfg, ph1, ph2, sync, data, cm_rom):
        self.timing = timing.timing(ph1, ph2, sync, data, cm_rom)
        self.when()
        self._id = id
        self.data = data
        self.addrh = 0 
        self.addrl = 0 
        self.rom = [0] * 256
        self.active_rom = 0 
        self.cm_rom = cm_rom
        self.io = bus()
        if io_cfg:
            self.io_output = None
        else:
            self.io_output = reg(bus(), wire(), self.io)

    def when(self):
        def A1ph1(self):
            self.addrl = self.data._v
        def A2ph1(self):
            self.addrh = self.data._v
        def A3ph1(self):
            if self.cm_rom.v():
                id = self.data._v
                self.active_rom = 1 if self._id == id else 0
        def M1ph1(self):
            if self.active_rom:
                self.data.v(self.rom[self.addrh << 4 | self.addrl] >> 4)
        def M2ph1(self):
            if self.active_rom:
                self.data.v(self.rom[self.addrh << 4 | self.addrl] & 0xF)

        self.timing.whenA1ph1(A1ph1, self)
        self.timing.whenA2ph1(A2ph1, self)
        self.timing.whenA3ph1(A3ph1, self)
        self.timing.whenM1ph1(M1ph1, self)
        self.timing.whenM2ph1(M2ph1, self)

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

    def enableIO(self):
        self.data.v(self.io._v)

    def setIO(self):
        if self.io_output is not None:
            self.io_output.bi().v(self.data._v)
            self.io_output.s().v(1)
            self.io_output.s().v(0)

    def dump(self):
        print("ROM {:x}: IO:{:04b}  ".format(self.id, self.io._v), end = "")
