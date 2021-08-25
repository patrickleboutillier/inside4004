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
        self.add = 0

        self.timing = timing

        @M12
        def _():
            self.ada = 0
            self.tmp = 0xF
            self.adc = 0

        @X12
        def _():
            self.acc_out = self.acc
            self.cy_out = self.cy
        
        @X21
        def _():
            if self.inst.ope():
                self.enableInitializer()
        
        @X2clk1  # n0342, for non IO instructions
        def _():
            if not self.inst.io():
                self.tmp = self.data.v

        @X2clk2  # n0342, for IO instructions
        def _():
            if self.inst.io():
                self.tmp = self.data.v


    def runAdder(self, invertADB=False, saveAcc=False, saveCy=False, shiftL=False, shiftR=False):
        self.adb = self.tmp
        if invertADB:
            self.adb = ~self.adb & 0xF

        self.add = self.ada + self.adb + self.adc
        co = self.add >> 4
        self.add = self.add & 0xF

        # print("acc:{} ada:{} tmp:{} adb:{} cy:{}, adc:{}".format(self.acc, self.ada, self.tmp, self.adb, self.cy, self.adc))
        # print("add:{} co:{}".format(self.add, co))

        if shiftL:
            self.cy = self.add >> 3
            self.acc = self.acc << 1 | self.cy_out
        elif shiftR:
            self.cy = self.add & 1
            self.acc = self.cy_out << 3 | self.add >> 1
        else:
            if saveAcc:
                self.acc = self.add
            if saveCy:
                if self.inst.daa() and (self.cy_out or self.acc_out > 9):
                    self.cy = 1
                else:
                    self.cy = co

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

    def enableAdd(self):
        self.data.v = self.add

    def enableCyOut(self):
        self.data.v = self.cy_out

    def enableInitializer(self):
        if self.inst.opa >> 3:
            if self.inst.daa():
                if self.cy_out or self.acc_out > 9:
                    self.data.v = 6
                else:
                    self.data.v = 0 
            elif self.inst.tcs():
                self.data.v = 9
            elif self.inst.kbp():
                if self.acc_out == 4:
                    self.data.v = 3
                elif self.acc_out == 8:
                    self.data.v = 4
                elif self.acc_out > 2:
                    self.data.v = 15
                else:
                    self.data.v = self.acc_out
            else:
                self.data.v = 0xF 
        else:
            self.data.v = 0

    def accZero(self):
        return 1 if self.acc_out == 0 else 0

    def addZero(self):
        return 1 if self.add == 0 else 0

    def carryOne(self):
        return self.cy_out

