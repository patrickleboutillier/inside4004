import fileinput
import sys
import chips.i4001 as i4001, chips.i4002 as i4002, chips.i4004 as i4004
from hdl import *


class MCS4:
    def __init__(self):
        self.data = bus("DATA")
        self.rom_chip_rom = 0               # This represents the currently active ROM chip (for ROM access)
        self.rom_chip_io = 0                # This represents the currently active ROM chip (for IO)
        self.rom_line = wire("ROM_LINE")
        self.ram_chip = 0                   # This represents the currently active RAM chip
        self.ram_lines = bus("RAM_LINES")
        self.PROM = [i4001.i4001(0, 0b1111, self.data), i4001.i4001(1, 0b1111, self.data), i4001.i4001(2, 0b0000, self.data), i4001.i4001(3, 0b1111, self.data)]
        self.RAM = [None, [i4002.i4002(0, 0, self.data), i4002.i4002(0, 1, self.data)]]
        self.CPU = i4004.i4004(self, self.data, self.ram_lines)
        # Install buffers between the RAM outputs and the ROM inputs
        for i in range(4):
            self.RAM[1][0].output().bo().wire(i).connect(self.PROM[0].io().wire(i))
            self.RAM[1][1].output().bo().wire(i).connect(self.PROM[1].io().wire(i))       
            self.PROM[2].io().wire(i).connect(self.PROM[3].io().wire(i))

        if self.PROM[0].program() == 0:
            sys.exit("ERROR: No instructions loaded!") 
        elif len(self.PROM) > 1:
            for p in self.PROM[1:]:
                p.program()
        # TODO: Make sure stdin is empty

    def setROMAddrHigh(self, addr):
        self.rom_chip_rom = addr

    def setROMAddrMed(self, addr):
        self.data.v(addr)
        self.PROM[self.rom_chip_rom].setROMAddrHigh()

    def setROMAddrLow(self, addr):
        self.data.v(addr)
        self.PROM[self.rom_chip_rom].setROMAddrLow()

    def setROMAddr(self, addrh, addrm, addrl):
        self.setROMAddrHigh(addrh)
        self.setROMAddrMed(addrm)
        self.setROMAddrLow(addrl)

    def getROMHigh(self):
        self.PROM[self.rom_chip_rom].enableROMHigh()
        return self.data.v()

    def getROMLow(self):
        self.PROM[self.rom_chip_rom].enableROMLow()
        return self.data.v()

    def getROM(self, addrh, addrm, addrl):
        self.setROMAddr(addrh, addrm, addrl)
        return (self.getROMHigh(), self.getROMLow())

    def setIOAddr(self, addr):
        self.rom_chip_io = addr

    def getIO(self):
        self.PROM[self.rom_chip_io].enableIO()
        return self.data.v()

    def setIO(self, nib):
        self.data.v(nib)
        self.PROM[self.rom_chip_io].setIO()

    def setRAMAddrHigh(self, addrh):
        self.ram_chip = addrh >> 2
        self.data.v(addrh)
        self.RAM[self.ram_lines.v()][self.ram_chip].setReg()

    def setRAMAddrLow(self, addrl):
        self.data.v(addrl)
        self.RAM[self.ram_lines.v()][self.ram_chip].setChar()

    def setRAMAddr(self, addrh, addrl):
        self.setRAMAddrHigh(addrh)
        self.setRAMAddrLow(addrl)

    def getRAM(self):
        self.RAM[self.ram_lines.v()][self.ram_chip].enableRAM()
        return self.data.v()

    def setRAM(self, byte):
        self.data.v(byte)
        self.RAM[self.ram_lines.v()][self.ram_chip].setRAM()

    def getStatus(self, char):
        self.RAM[self.ram_lines.v()][self.ram_chip].enableStatus(char)
        return self.data.v()

    def setStatus(self, char, byte):
        self.data.v(byte)
        self.RAM[self.ram_lines.v()][self.ram_chip].setStatus(char)

    def setOutput(self, nib):
        self.data.v(nib)
        self.RAM[self.ram_lines.v()][self.ram_chip].setOutput()

    def fetchInst(self, ph, pm, pl):
        self.setROMAddr(ph, pm, pl)
        return self.getROM(ph, pm, pl)

    def programROM(sel):
        for prom in self.PROM:
            self.prom.program()

    def run(self):
        self.CPU.run()

    def dump(self, nb):
        self.CPU.dump(nb)
        self.RAM[1][0].dump()
        self.RAM[1][1].dump()
        for r in self.PROM:
            r.dump()
        print()

if __name__ == "__main__":
    MCS4 = MCS4()
    MCS4.run()
