import fileinput
from hdl import *


class i4001:
    def __init__(self, id, io_cfg, data, cm_rom):
        self._id = id
        self._data = data
        self._addrh = 0 # reg(bus(), wire(), bus())
        self._addrl = 0 # reg(bus(), wire(), bus())
        self._rom = [0] * 256
        self._cm_rom = cm_rom
        self._io_cfg = io_cfg
        self._io = bus()
        if io_cfg:
            self._io_output = None
        else:
            self._io_output = reg(bus(), wire(), self.io())

        #for n in range(4):
        #    if iocfg & (1 << n): # input
        #        buf(self._io.wire(n), self._io_input.wire(n))
        #    else:   # output
        #        buf(self._io_output.bo().wire(n), self._io.wire(n))


    def io(self):
        return self._io

    def program(self, fi):
        addr = 0
        for line in fi:
            inst = line[0:8]
            if inst[0] in ['0', '1']:
                self._rom[addr] = int(inst, 2)
                addr += 1
                if addr == 256:
                    break
        # Finish of with NOPs
        for x in range(addr, 256):
            self._rom[x] = 0
        return addr

    def setROMAddrHigh(self):
        self._addrh = self._data.v()

    def setROMAddrLow(self):
        self._addrl = self._data.v()

    def enableROMHigh(self):
        self._data.v(self._rom[self._addrh << 4 | self._addrl] >> 4)

    def enableROMLow(self):
        self._data.v(self._rom[self._addrh << 4 | self._addrl] & 0xF)

    def enableIO(self):
        self._data.v(self._io.v())

    def setIO(self):
        if self._io_output is not None:
            self._io_output.bi().v(self._data.v())
            self._io_output.s().v(1)
            self._io_output.s().v(0)

    def dump(self):
        print("ROM {:x}: IO:{:04b}  ".format(self._id, self._io.v()), end = "")
