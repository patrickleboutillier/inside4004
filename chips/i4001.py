import fileinput


class i4001:
    def __init__(self, id):
        self.id = id
        self.rom = [0] * 256
        self.io = 0

    def load(self):
        addr = 0
        for line in fileinput.input():
            inst = line[0:8]
            if inst[0] in ['0', '1']:
                self.rom[addr] = int(inst, 2)
                addr += 1
                if addr == 256:
                    break
        return addr

    def getROM(self, addr):
        return self.rom[addr]

    def getIO(self):
        return self.io

    def setIO(self, nib):
        self.io = nib

    def dump(self):
        print("ROM {:x}: IO:{:04b}  ".format(self.id, self.io), end = "")
