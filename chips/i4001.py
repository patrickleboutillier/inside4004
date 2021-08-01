import fileinput
from hdl import *

class i4001:
    def __init__(self, id, iocfg):
        self._id = id
        self._data = bus()
        self._addrh = reg(bus(), wire(), bus())
        self._addrl = reg(bus(), wire(), bus())
        self._rom = [0] * 256
        self._cm_rom = wire()
        self._input = bus()
        self._output = reg(bus(), wire(), bus())
        ios = []
        for n in range(3, -1, -1):
            if iocfg & (1 << n):
                ios.append(self._input.wire(n))
            else:
                ios.append(self._output.bo().wire(n))
        self._io = bus.make(ios)

    def data(self):
        return self._data

    def cm_rom(self):
        return self._cm_rom

    def io(self):
        return self._io 

    def program(self):
        addr = 0
        for line in fileinput.input():
            inst = line[0:8]
            if inst[0] in ['0', '1']:
                self._rom[addr] = int(inst, 2)
                addr += 1
                if addr == 256:
                    break
        return addr

    def setROMAddrHigh(self):
        self._addrh.bi().v(self._data.v())
        self._addrh.s().v(1)
        self._addrh.s().v(0)

    def setROMAddrLow(self):
        self._addrl.bi().v(self._data.v())
        self._addrl.s().v(1)
        self._addrl.s().v(0)

    def enableROMHigh(self):
        self._data.v(self._rom[self._addrh.bo().v() << 4 | self._addrl.bo().v()] >> 4)

    def enableROMLow(self):
        self._data.v(self._rom[self._addrh.bo().v() << 4 | self._addrl.bo().v()] & 0xF)

    def enableIO(self):
        self._data.v(self._input.v())

    def setIO(self):
        self._output.bi().v(self._data.v())
        self._output.s().v(1)
        self._output.s().v(0)

    def dump(self):
        print("ROM {:x}: IO:{:04b}  ".format(self._id, self._io.v()), end = "")
