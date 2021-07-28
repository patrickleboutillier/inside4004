import fileinput
import sys
import chips.i4001 as i4001, chips.i4002 as i4002, chips.i4004 as i4004


class MCS4:
    def __init__(self):
        self.PROM = [i4001.i4001(0), i4001.i4001(1)]
        self.RAM = [None, [i4002.i4002(0, 0), i4002.i4002(0, 1)]]
        self.CPU = i4004.i4004(self)
        if self.PROM[0].load() == 0:
            sys.exit("ERROR: No instructions loaded!")           

    def getROM(self, chip, addr):
        return self.PROM[chip].getROM(addr)

    def getRAM(self):
        (chip, reg, char) = self.CPU.decodeRAMAddr()
        return self.RAM[self.CPU.cm_ram][chip].getRAM(reg, char)

    def setRAM(self, byte):
        (chip, reg, char) = self.CPU.decodeRAMAddr()
        self.RAM[self.CPU.cm_ram][chip].setRAM(reg, char, byte)

    def getStatus(self, char):
        (chip, reg, _) = self.CPU.decodeRAMAddr()
        return self.RAM[self.CPU.cm_ram][chip].getStatus(reg, char)

    def setStatus(self, char, byte):
        (chip, reg, _) = self.CPU.decodeRAMAddr()
        self.RAM[self.CPU.cm_ram][chip].setStatus(reg, char, byte)

    def getIO(self, chip):
        return self.PROM[chip].getIO()

    def setIO(self, chip, nib):
        self.PROM[chip].setIO(nib)

    def setOutput(self, nib):
        self.RAM[self.CPU.cm_ram].setOutput(nib)

    def fetchInst(self, pc):
        chip = pc >> 8
        addr = pc & 0xFF
        return self.PROM[chip].getROM(addr)

    def loadROM(sel):
        for prom in self.PROM:
            self.prom.load()

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
