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

        self.timing = timing

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
        #        print("Sum is", self.acc, self.acc2, self.tmp2)

        #@X2ph2
        #def _():
        #    if self.inst.io():
        #        self.tmp = self.data._v


    def adder(self):
        sum = self.acc2 + self.tmp2 + self.cy2
        co = sum >> 4
        sum = (sum ^ 0b0101) & 0xF
        return (sum, co)

    def setAccFromTmp(self):
        self.acc = self.tmp

    def setTmp(self, invert=False):
        self.tmp = self.data._v
        if invert:
            self.tmp = ~self.tmp & 0xF


	# wire n0415		= X1ph1 & ope
	# wire add_ib		= X2ph1 & inc_isz
	# wire cy_ib		= X2ph1 & iow
	# wire acb_ib		= X1ph1 & iow | X2ph1 & xch
    def enableResult(self):
        self.data.v()

    def accZero(self):
        return 1 if self.acc == 0 else 0

