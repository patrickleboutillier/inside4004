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

        #@X1ph1
        #def _():
        #    self.acc_out = self.acc
        #    if not self.inst.io():
        #        print("Grabbing ", self.data._v)
        #        self.tmp = self.data._v
        #        self.acc2 = (self.acc ^ 0b1111) & 0xF
        #        self.tmp2 = (self.tmp ^ 0b1010) & 0xF
        #        self.cy2 = 1
        
        #@X2ph1
        #def _():
        #    if self.inst.ld():
        #        (self.acc, _) = self.adder()
        #        print("acc_in is", self.acc, self.acc2, self.tmp2)

        #@X2ph2
        #def _():
        #    if self.inst.io():
        #        self.tmp = self.data._v


    def runAdder(self, readAcc=False, invertAcc=False, invertTmp=False, readCy=False, readCy1=False, invertCy=False,
        saveAcc=False, saveCy=False, saveCy1=False, shiftL=False, shiftR=False):
        if readAcc:
            self.acc2 = self.acc
        if invertAcc:
            self.acc2 = ~self.acc2 & 0xF
        self.tmp2 = self.tmp
        if invertTmp:
            self.tmp2 = ~self.tmp2 & 0xF
        if readCy:
            self.cy2 = self.cy
        elif readCy1:
            self.cy2 = 1
        if invertCy:
            self.cy2 = ~self.cy2 & 1

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


    def setTmp(self):
        self.tmp = self.data._v

    def enableAcc(self):
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

