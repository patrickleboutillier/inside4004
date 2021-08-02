from hdl import *


class arith:
    def __init__(self, data):
        self.data = data
        self.a = 0
        self.b = 0
        self.ci = 0
        self.co = 0
        self.acc = 0

    def clearA(self)
        self.a = 0

    def setA(self, data):
        self.a = data

    def clearB(self, invert=False):
        self.b = 0xF if invert else 0

    def setB(self, data, invert=False):
        self.b = ~data & 0xF if invert else data

    def clearCI(self, invert=False):
        self.ci = 1 if invert else 0

    def setCI(self, cy, invert=False):
        self.ci = ~cy & 0x1 if invert else cy

    def getAcc(self):
        return self.acc

    def setAcc(self, data):
        self.acc = data

    def getCO(self):
        return self.co

    def getSum(self):
        pass

    def getDiff(self):
        pass

    def getRotateR(self):
        pass

    def getRotateL(self):
        pass

    def getComplement(self):
        pass

    def setCO(self):
        pass

# TCC
# TCS
# DAA
# KBP