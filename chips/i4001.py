import fileinput
from hdl import *

class i4001:
    def __init__(self, id, data):
        self.data = data
        self.id = id
        self.addrh = 0
        self.addrl = 0
        self.rom = [0] * 256
        self.io = 0

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
        self.data.v(self.io)

    def setIO(sel):
        self.io = self.data.v()

    def dump(self):
        print("ROM {:x}: IO:{:04b}  ".format(self.id, self.io), end = "")
