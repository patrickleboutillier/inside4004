from hdl import * 


class i4002:
    def __init__(self, bank, chip, data, cm):
        self._data = data
        self._cm = cm
        self._bank = bank
        self._chip = chip
        self._reg = 0
        self._char = 0
        self._ram = [[0] * 16, [0] * 16, [0] * 16, [0] * 16]
        self._status = [[0] * 4, [0] * 4, [0] * 4, [0] * 4]
        self._output = reg(bus(), wire(), bus())


    def output(self):
        return self._output.bo()

    def setReg(self):
        self._reg = self._data.v() & 0b0011

    def setChar(self):
        self._char = self._data.v()

    def enableRAM(self):
        self._data.v(self._ram[self._reg][self._char])

    def setRAM(self):
        self._ram[self._reg][self._char] = self._data.v()

    def enableStatus(self, char):
        self._data.v(self._status[self._reg][char])

    def setStatus(self, char):
        self._status[self._reg][char] = self._data.v()

    def setOutput(self):
        self._output.bi().v(self._data.v())
        self._output.s().v(1)
        self._output.s().v(0)

    def dump(self):
        ss = " ".join(["".join(["{:x}".format(x) for x in self._ram[i]]) + "/" + "".join(["{:x}".format(x) for x in self._status[i]]) for i in range(4)])
        print("RAM {:x}/{:x}:{} OUTPUT:{:04b}".format(self._bank, self._chip, ss, self._output.bo().v()))
