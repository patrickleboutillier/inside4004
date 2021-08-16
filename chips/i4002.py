import chips.modules.timing as timing
from hdl import * 


class i4002:
    def __init__(self, bank, chip, ph1, ph2, sync, data, cm):
        self.timing = timing.timing(ph1, ph2, sync)
        # self.when()
        self.bank = bank
        self.chip = chip
        self.data = data
        self.cm = cm
        self.srcff = 0
        self.inst = 0
        self.opa = 0
        self.reg = 0
        self.char = 0
        self.ram = [[0] * 16, [0] * 16, [0] * 16, [0] * 16]
        self.status = [[0] * 4, [0] * 4, [0] * 4, [0] * 4]
        self.output = bus()
        self.output_reg = reg(bus(), wire(), self.output)


    def when(self):
        def M2ph2(self):
            self.opa = self.data._v
            # if self.cm.v() and self.srcff:


        def X2ph2(self):
            if self.cm.v():
                # SRC instruction
                if self.chip == (self.data._v >> 2):
                    self.srcff = 1 
                    self.reg = self.data._v & 0b0011
                else:
                    self.srcff = 0
        def X3ph2(self):
            if self.srcff:
                # SRC instruction
                char = self.data._v 


    def setReg(self):
        self.reg = self.data._v & 0b0011

    def setChar(self):
        self.char = self.data._v

    def enableRAM(self):
        self.data.v(self.ram[self.reg][self.char])

    def setRAM(self):
        self.ram[self.reg][self.char] = self.data._v

    def enableStatus(self, char):
        self.data.v(self.status[self.reg][char])

    def setStatus(self, char):
        self.status[self.reg][char] = self.data._v

    def setOutput(self):
        self.output_reg.bi().v(self.data._v)
        self.output_reg.s().v(1)
        self.output_reg.s().v(0)

    def dump(self):
        ss = " ".join(["".join(["{:x}".format(x) for x in self.ram[i]]) + "/" + "".join(["{:x}".format(x) for x in self.status[i]]) for i in range(4)])
        print("RAM {:x}/{:x}:{} OUTPUT:{:04b}".format(self.bank, self.chip, ss, self.output._v))


'''
    def when(self):
        def M2ph2(self):
            if self.cm.v() and self.src:
                self.opa = self.data._v
                self.inst = 1
            else:
                self.inst = 0
        def X2ph2(self):
            if self.cm.v():
                # SRC instruction
                if self.chip == (self.data._v >> 2):
                    self.srcff = 1 
                else:
                    self.srcff = 0

            if self.cm.v():
                # SRC instruction
                if (self.data._v >> 2) == self.chip:
                    self.src = 1
                    self.reg = self.data._v & 0b0011
                else:
                    self.src = 0 
            elif self.inst:
                # Do whatever opa requires at this step
                pass
        def X3ph2(self):
            if self.src:
                if not self.inst:
                    # SRC instruction
                    char = self.data._v 
                else:
                    # Do whatever opa requires at this step
                    pass
'''