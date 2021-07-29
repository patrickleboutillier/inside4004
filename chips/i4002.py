from hdl import * 


class i4002:
    def __init__(self, bank, chip, data):
        self.data = data
        self.bank = bank
        self.chip = chip
        self.reg = 0
        self.char = 0
        self.ram = [[0] * 16, [0] * 16, [0] * 16, [0] * 16]
        self.status = [[0] * 4, [0] * 4, [0] * 4, [0] * 4]
        self._output = reg(bus(), wire(), bus(), "OUTPUT")

    def output(self):
        return self._output

    def setReg(self):
        self.reg = self.data.v() & 0b0011

    def setChar(self):
        self.char = self.data.v()

    def enableRAM(self):
        self.data.v(self.ram[self.reg][self.char])

    def setRAM(self):
        self.ram[self.reg][self.char] = self.data.v()

    def enableStatus(self, char):
        self.data.v(self.status[self.reg][char])

    def setStatus(self, char):
        self.status[self.reg][char] = self.data.v()

    def setOutput(self):
        self._output.bi().v(self.data.v())
        self._output.s().v(1)
        self._output.s().v(0)

    def dump(self):
        ss = " ".join(["".join(["{:x}".format(x) for x in self.ram[i]]) + "/" + "".join(["{:x}".format(x) for x in self.status[i]]) for i in range(4)])
        print("RAM {:x}/{:x}:{} OUTPUT:{:04b}".format(self.bank, self.chip, ss, self._output.bo().v()))
