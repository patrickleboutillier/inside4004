import fileinput
from hdl import *

class i4001:
    def __init__(self, id, iocfg, data):
        self.data = data
        self.id = id
        self.addrh = 0
        self.addrl = 0
        self.rom = [0] * 256
        self._input = bus()
        self._output = reg(bus(), wire(), bus(), "OUTPUT")
        ios = []
        for n in range(3, -1, -1):
            if iocfg & (1 << n):
                ios.append(self._input.wire(n))
            else:
                ios.append(self._output.bo().wire(n))
        self._io = bus.make(ios)

    # def input(self):
    #     return self._input

    # def output(self):
    #     return self._output

    def io(self):
        return self._io 

    def program(self):
        addr = 0
        for line in fileinput.input():
            inst = line[0:8]
            if inst[0] in ['0', '1']:
                self.rom[addr] = int(inst, 2)
                addr += 1
                if addr == 256:
                    break
        return addr

    def setROMAddrHigh(self):
        self.addrh = self.data.v()

    def setROMAddrLow(self):
        self.addrl = self.data.v()

    def enableROMHigh(self):
        self.data.v(self.rom[self.addrh << 4 | self.addrl] >> 4)

    def enableROMLow(self):
        self.data.v(self.rom[self.addrh << 4 | self.addrl] & 0xF)

    def enableIO(self):
        self.data.v(self._input.v())

    def setIO(self):
        self._output.bi().v(self.data.v())
        self._output.s().v(1)
        self._output.s().v(0)

    def dump(self):
        print("ROM {:x}: INPUT.OUTPUT:{:04b}/{:04b}  ".format(self.id, self._input.v(), self._output.bo().v()), end = "")
