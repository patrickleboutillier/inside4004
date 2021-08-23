from chips.modules.timing import *
from hdl import *


class alu:
    def __init__(self, timing, data):
        self.data = data
        self.inst = None            # Must be set after initialization
        self.acc = 0
        self.tmp = 0
        self.cy = 0 
        self.ada = 0
        self.adb = 0
        self.adc = 0 
        self.acc_out = 0
        self.cy_out = 0
        self.sum = 0

        self.timing = timing

        @M1ph1
        def _():
            self.ada = 0
            self.tmp = 0xF
            self.adc = 0

        @X1ph1
        def _():
            self.acc_out = self.acc
            self.cy_out = self.cy
        
        @X2ph1  # n0342, for non IO instructions
        def _():
            if not self.inst.io():
                self.tmp = self.data.v

        @X2ph2  # n0342, for IO instructions
        def _():
            if self.inst.io():
                self.tmp = self.data.v


    def runAdder(self, invertADB=False, saveAcc=False, saveCy=False, saveCy1=False, shiftL=False, shiftR=False):
        self.adb = self.tmp
        if invertADB:
            self.adb = ~self.adb & 0xF

        # print("acc:{} ada:{} tmp:{} adb:{} cy:{}, adc:{}".format(self.acc, self.ada, self.tmp, self.adb, self.cy, self.adc))

        self.sum = self.ada + self.adb + self.adc
        co = self.sum >> 4
        self.sum = self.sum & 0xF

        if shiftL:
            self.cy = self.sum >> 3
            self.acc = self.acc << 1 | self.cy_out
        elif shiftR:
            self.cy = self.sum & 1
            self.acc = self.cy_out << 3 | self.sum >> 1
        else:
            if saveAcc:
                self.acc = self.sum
            if saveCy:
                self.cy = co
            elif saveCy1:
                self.cy = 1


    def setADA(self, invert=False):
        self.ada = self.acc
        if invert:
            self.ada = ~self.ada & 0xF

    def setADC(self, invert=False, one=False):
        if one:
            self.adc = 1
        else:
            self.adc = self.cy
            if invert:
                self.adc = ~self.adc & 1
        
    def enableAccOut(self):
        self.data.v = self.acc_out

    def enableSum(self):
        self.data.v = self.sum

    def enableCyOut(self):
        self.data.v = self.cy_out

    def enableKBP(self):
        pass

    def accZero(self):
        return 1 if self.acc == 0 else 0

    def addZero(self):
        return 1 if self.sum == 0 else 0

