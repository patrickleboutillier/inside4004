from hdl import *


class scratch:
    def __init__(self, data):
        self.data = data
        self.inst = None    # Must be set after initialisation
        self.index_reg = [0] * 16

    def getReg(self):
        self.data.v(self.data.v(self.index_reg[self.inst.opa]))

    def getReg0(self):
        self.data.v(self.data.v(self.index_reg[0]))

    def getReg1(self):
        self.data.v(self.data.v(self.index_reg[1]))

    def getRegPL(self):
        self.data.v(self.index_reg[self.inst.opa & 0b1110])

    def getRegPH(self):
        self.data.v(self.index_reg[self.inst.opa | 0b0001])

    def setReg(self):
        self.index_reg[self.inst.opa] = self.data._v

    def setRegPL(self):
        self.index_reg[self.inst.opa & 0b1110] = self.data._v

    def setRegPH(self):
        self.index_reg[self.inst.opa | 0b0001] = self.data._v

    