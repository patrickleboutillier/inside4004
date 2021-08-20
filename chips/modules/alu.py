from chips.modules.timing import *
from hdl import *


class alu:
    def __init__(self, timing, data):
        self.data = data
        self.inst = None            # Must be set after initialization
        self.acc = 0
        self.tmp = 0
        self.cy = 0 
        self.acc2 = 0
        self.tmp2 = 0
        self.cy2 = 0 
        self.acc_out = 0
        self.cy_out = 0
        self.acc_in = 0

        self.timing = timing

        @M1ph1
        def _():
            self.acc2 = 0
            self.tmp = 0xF
            self.cy2 = 0

        @X1ph1
        def _():
            self.acc_out = self.acc
            self.cy_out = self.cy
        
        @X2ph1  # n0342, for non IO instructions
        def _():
            if not self.inst.io():
                self.tmp = self.data._v

        @X2ph2  # n0342, for IO instructions
        def _():
            if self.inst.io():
                self.tmp = self.data._v


    def runAdder(self, invertADB=False, saveAcc=False, saveCy=False, saveCy1=False, shiftL=False, shiftR=False):
        self.tmp2 = self.tmp
        if invertADB:
            self.tmp2 = ~self.tmp2 & 0xF

        # print("acc:{} acc2:{} tmp:{} tmp2:{} cy:{}, cy2:{}".format(self.acc, self.acc2, self.tmp, self.tmp2, self.cy, self.cy2))

        self.acc_in = self.acc2 + self.tmp2 + self.cy2
        co = self.acc_in >> 4
        self.acc_in = self.acc_in & 0xF

        if shiftL:
            self.cy = self.acc_in >> 3
            self.acc = self.acc << 1 | self.cy_out
        elif shiftR:
            self.cy = self.acc_in & 1
            self.acc = self.cy_out << 3 | self.acc_in
        else:
            if saveAcc:
                self.acc = self.acc_in
            if saveCy:
                self.cy = co
            elif saveCy1:
                self.cy = 1


    #def setTmp(self):
    #    self.tmp = self.data._v

    def setADA(self, invert=False):
        self.acc2 = self.acc
        if invert:
            self.acc2 = ~self.acc2 & 0xF

    def setADC(self, invert=False, one=False):
        if one:
            self.cy2 = 1
        else:
            self.cy2 = self.cy
            if invert:
                self.cy2 = ~self.cy2 & 1
        

    def enableAccOut(self):
        self.data.v(self.acc_out)

    def enableAdd(self):
        self.data.v(self.acc_in)

    def enableCy(self):
        self.data.v(self.cy_out)

    def enableKBP(self):
        pass

    def accZero(self):
        return 1 if self.acc == 0 else 0

    def addZero(self):
        return 1 if self.acc_in == 0 else 0

