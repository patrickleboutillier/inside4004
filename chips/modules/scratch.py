from hdl import *


class scratch:
    def __init__(self, data):
        self.data = data            # The data bus
        self.inst = None            # Must be set after initialisation
        self.index_reg = [0] * 16   # The actual registers


    def enableReg(self):
        self.data.v(self.index_reg[self.inst.opa])

    def enableReg0(self):
        self.data.v(self.index_reg[0])

    def enableReg1(self):
        self.data.v(self.index_reg[1])

    def enableRegPairH(self):
        self.data.v(self.index_reg[self.inst.opa & 0b1110])

    def enableRegPairL(self):
        self.data.v(self.index_reg[self.inst.opa | 0b0001])

    def setReg(self):
        self.index_reg[self.inst.opa] = self.data._v

    def setRegPairH(self):
        self.index_reg[self.inst.opa & 0b1110] = self.data._v

    def setRegPairL(self):
        self.index_reg[self.inst.opa | 0b0001] = self.data._v


    def dump(self):
        print("INDEX:{}".format("".join(["{:x}".format(x) for x in self.index_reg])), end='')

    