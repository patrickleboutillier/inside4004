
class i4002:
    def __init__(self, bank, chip):
        self.bank = bank
        self.chip = chip
        self.reg = [[0] * 16, [0] * 16, [0] * 16, [0] * 16] 
        self.status = [[0] * 4, [0] * 4, [0] * 4, [0] * 4]
        self.output = 0

    def getRAM(self, reg, char):
        return self.reg[reg][char]

    def setRAM(self, reg, char, byte):
        self.reg[reg][char] = byte

    def getStatus(self, reg, char):
        return self.status[reg][char]

    def setStatus(self, reg, char, byte):
        self.status[reg][char] = byte

    def setOutput(self, nib):
        self.output = nib

    def dump(self):
        ss = " ".join(["".join(["{:x}".format(x) for x in self.reg[i]]) + "/" + "".join(["{:x}".format(x) for x in self.status[i]]) for i in range(4)])
        print("RAM {:x}/{:x}:{} OUT:{:04b}".format(self.bank, self.chip, ss, self.output))
