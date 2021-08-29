from chips.modules.timing import *
from hdl import *


# Tihs class implemts the ALU of the 4004.


class alu:
    def __init__(self, inst, data):
        self.data = data
        self.inst = inst
        self.inst.alu = self
        self.acc = 0                # The accumulator
        self.tmp = 0                # The tmp register
        self.cy = 0                 # Carry
        self.ada = 0                # Input A of the adder (4 bits)
        self.adb = 0                # Input B of the adder (4 bits)
        self.adc = 0                # Input C od the adder (1 bit)
        self.acc_out = 0            # Accumulator output
        self.cy_out = 0             # Carry output
        self.add = 0                # The result of the adder (not a register in the real 4004 as the adder is combinational)
 
        @M12    # Initialize the ALU before each instruction
        def _():
            self.ada = 0
            self.tmp = 0xF
            self.adc = 0

        @X12    # Save acc and cy to their output registers. 
        def _():
            self.acc_out = self.acc
            self.cy_out = self.cy
        
        @X21    # Set the bus with the proper initialization value, depending on the current instruction.
        def _():
            if self.inst.ope():
                self.enableInitializer()
        
        @X22clk1  # Set input B by sampling data from the bus (n0342, for non IO instructions).
        def _():
            if not self.inst.io():
                self.tmp = self.data.v

        @X22clk2  # Set input B by sampling data from the bus (n0342, for IO instructions).
        def _():
            if self.inst.io():
                self.tmp = self.data.v


    # The Adder implementation
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
                # WARNING: a bit of DAA logic here...
                if self.inst.daa() and (self.cy_out or self.acc_out > 9):
                    self.cy = 1
                else:
                    self.cy = co

    # Set input A
    def setADA(self, invert=False):
        self.ada = self.acc
        if invert:
            self.ada = ~self.ada & 0xF

    # Set input C
    def setADC(self, invert=False, one=False):
        if one:
            self.adc = 1
        else:
            self.adc = self.cy
            if invert:
                self.adc = ~self.adc & 1
        
    # Place acc_out on the bus.
    def enableAccOut(self):
        self.data.v = self.acc_out

    # Place adder result on the bus
    def enableAdd(self):
        self.data.v = self.add

    # Place carry out on the bus
    def enableCyOut(self):
        self.data.v = self.cy_out

    # Bus initialisation routine. This is really clever...
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

    # Is acc == 0?
    def accZero(self):
        return 1 if self.acc_out == 0 else 0

    # Is adder result == 0?
    def addZero(self):
        return 1 if self.add == 0 else 0

    # Is carry == 1?
    def carryOne(self):
        return self.cy_out

