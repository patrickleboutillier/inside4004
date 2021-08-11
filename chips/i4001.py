import chips.modules.timing as timing
from hdl import *


class i4001(sensor):
    def __init__(self, id, io_cfg, ph1, ph2, sync, data, cm_rom):
        self.timing = timing.timing(ph1, ph2, sync)
        sensor.__init__(self, self.timing.ph1, data, cm_rom)
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


    def always(self, signal):
        if self.timing.ph1.v():
            if self.timing.a1.v():
                self.addrl = self.data.v()
            elif self.timing.a2.v():
                self.addrh = self.data.v()
            elif self.timing.a3.v(): 
                if self.cm_rom.v():
                    id = self.data.v()
                    self.active_rom = 1 if self._id == id else 0
            elif self.timing.m1.v():
                if self.active_rom:
                    self.data.v(self.rom[self.addrh << 4 | self.addrl] >> 4)
            elif self.timing.m2.v():
                if self.active_rom:
                    self.data.v(self.rom[self.addrh << 4 | self.addrl] & 0xF)

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
        self.data.v(self.io.v())

    def setIO(self):
        if self.io_output is not None:
            self.io_output.bi().v(self.data.v())
            self.io_output.s().v(1)
            self.io_output.s().v(0)

    def dump(self):
        print("ROM {:x}: IO:{:04b}  ".format(self.id, self.io.v()), end = "")
