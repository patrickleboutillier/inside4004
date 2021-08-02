import fileinput
from hdl import *


class i4001:
    def __init__(self, id, iocfg):
        self._id = id
        self._data = bus()
        self._addrh = reg(bus(), wire(), bus())
        self._addrl = reg(bus(), wire(), bus())
        # addr is just a concatenation of addrh and addrl into a single bus
        self._addr = bus.make(self._addrh.bo().wires() + self._addrl.bo().wires())
        self._cur_romh = bus()
        self._cur_roml = bus()
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

    def program(self, fi):
        addr = 0
        romh = []
        roml = []
        for line in fi:
            inst = line[0:8]
            if inst[0] in ['0', '1']:
                bh = bus.make([wire.GND if c == '0' else wire.VCC for c in inst[0:4]])
                bl = bus.make([wire.GND if c == '0' else wire.VCC for c in inst[4:8]])
                romh.append(bh)
                roml.append(bl)
                addr += 1
                if addr == 256:
                    break
        # Finish off with NOPs
        for _ in range(addr, 256):
            romh.append(bus.make([wire.GND] * 8))
            roml.append(bus.make([wire.GND] * 8))

        romh.reverse()
        roml.reverse()
        muxhis = [[], [], [], []]
        muxlis = [[], [], [], []]
        for i in range(256):
            for j in range(4):
                muxhis[j].append(romh[i].wire(7-j))
                muxlis[j].append(roml[i].wire(3-j))
            
        for j in range(4):
            mux(bus.make(muxhis[j]), self._addr, self._cur_romh.wire(3-j))
            mux(bus.make(muxlis[j]), self._addr, self._cur_roml.wire(3-j))

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
        self._data.v(self._cur_romh.v())

    def enableROMLow(self):
        self._data.v(self._cur_roml.v())

    def enableIO(self):
        self._data.v(self._input.v())

    def setIO(self):
        self._output.bi().v(self._data.v())
        self._output.s().v(1)
        self._output.s().v(0)

    def dump(self):
        print("ROM {:x}: IO:{:04b}  ".format(self._id, self._io.v()), end = "")
