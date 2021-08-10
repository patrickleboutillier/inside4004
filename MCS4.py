import sys, fileinput
import chips.i4001 as i4001, chips.i4002 as i4002, chips.i4004 as i4004
import chips.clock as clock
from hdl import *


class MCS4:
    def __init__(self):
        self._rom_chip_rom = 0               # This represents the currently active ROM chip (for ROM access)
        self._rom_chip_io = 0                # This represents the currently active ROM chip (for IO)
        self._ram_chip = 0                   # This represents the currently active RAM chip

        self._clock = clock.clock()
        self._ph1 = self._clock.ph1()
        self._ph2 = self._clock.ph2()
 
        self._data = bus()
        self._cm_rom = wire()
        self._cm_ram = bus()
        self._test = wire()
        self._CPU = i4004.i4004(self, self._clock.ph1(), self._clock.ph2(), self._data, self._cm_rom, self._cm_ram, self._test)

        self._PROM = []
        self._RAM = [None, [], [], None, [], None, None, None, []]
        self._SR = []
      
    def ph1(self):
        return self._ph1
    
    def ph2(self):
        return self._ph2

    def data(self):
        return self._data

    def cm_rom(self):
        return self._cm_rom

    def cm_ram(self):
        return self._cm_ram

    def test(self):
        return self._test

    def addROM(self, rom):
        self._PROM.append(rom)

    def addRAM(self, bank, ram):
        idx = 1 << bank
        self._RAM[idx].append(ram)

    def addSR(self, sr):
        self._SR.append(sr)


    def setROMAddrHigh(self, addr):
        self._rom_chip_rom = addr

    def setROMAddrMed(self, addr):
        self._data.v(addr)
        self._PROM[self._rom_chip_rom].setROMAddrHigh()

    def setROMAddrLow(self, addr):
        self._data.v(addr)
        self._PROM[self._rom_chip_rom].setROMAddrLow()

    def setROMAddr(self, addrh, addrm, addrl):
        self.setROMAddrHigh(addrh)
        self.setROMAddrMed(addrm)
        self.setROMAddrLow(addrl)

    def getROMHigh(self):
        self._PROM[self._rom_chip_rom].enableROMHigh()
        return self._data.v()

    def getROMLow(self):
        self._PROM[self._rom_chip_rom].enableROMLow()
        return self._data.v()

    def getROM(self, addrh, addrm, addrl):
        self.setROMAddr(addrh, addrm, addrl)
        return (self.getROMHigh(), self.getROMLow())

    def setIOAddr(self, addr):
        self._rom_chip_io = addr

    def getIO(self):
        self._PROM[self._rom_chip_io].enableIO()
        return self._data.v()

    def setIO(self, nib):
        self._data.v(nib)
        self._PROM[self._rom_chip_io].setIO()

    def setRAMAddrHigh(self, addrh):
        self._ram_chip = addrh >> 2
        self._data.v(addrh)
        self._RAM[self._cm_ram.v()][self._ram_chip].setReg()

    def setRAMAddrLow(self, addrl):
        self._data.v(addrl)
        self._RAM[self._cm_ram.v()][self._ram_chip].setChar()

    def setRAMAddr(self, addrh, addrl):
        self.setRAMAddrHigh(addrh)
        self.setRAMAddrLow(addrl)

    def getRAM(self):
        self._RAM[self._cm_ram.v()][self._ram_chip].enableRAM()
        return self._data.v()

    def setRAM(self, byte):
        self._data.v(byte)
        self._RAM[self._cm_ram.v()][self._ram_chip].setRAM()

    def getStatus(self, char):
        self._RAM[self._cm_ram.v()][self._ram_chip].enableStatus(char)
        return self._data.v()

    def setStatus(self, char, byte):
        self._data.v(byte)
        self._RAM[self._cm_ram.v()][self._ram_chip].setStatus(char)

    def setOutput(self, nib):
        self._data.v(nib)
        self._RAM[self._cm_ram.v()][self._ram_chip].setOutput()

    def fetchInst(self, ph, pm, pl):
        self.setROMAddr(ph, pm, pl)
        return self.getROM(ph, pm, pl)

    def program(self):
        fi = fileinput.input()
        if self._PROM[0].program(fi) == 0:
            sys.exit("ERROR: No instructions loaded!") 
        elif len(self._PROM) > 1:
            for p in self._PROM[1:]:
                p.program(fi)
        # TODO: Make sure stdin is empty
        fi.close()

    def run(self, callback=None, dump=False):
        nb = 0
        while (True):
            if callback is not None:
                callback(nb)
            for _ in range(5):
                self._clock.tick(4)
            # self._CPU.fetch()
            if dump:
                self.dump(nb)
            self._CPU.execute()
            for _ in range(3):
                self._clock.tick(4)
            nb += 1

    def dump(self, nb):
        self._CPU.dump(nb)
        self._RAM[1][0].dump()
        self._RAM[1][1].dump()
        for r in self._PROM:
            r.dump()
        print()
        for s in self._SR:
            s.dump()
        print()