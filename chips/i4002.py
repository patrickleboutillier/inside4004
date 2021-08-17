import chips.modules.timing as timing
from hdl import * 


class i4002:
    def __init__(self, bank, chip, ph1, ph2, sync, data, cm):
        self.timing = timing.timing(ph1, ph2, sync)
        self.when()
        self.bank = bank
        self.chip = chip
        self.data = data
        self.cm = cm
        self.src = 0
        self.ram_select = 0
        self.ram_inst = 0
        self.opa = 0
        self.reg = 0
        self.char = 0
        self.ram = [[0] * 16, [0] * 16, [0] * 16, [0] * 16]
        self.status = [[0] * 4, [0] * 4, [0] * 4, [0] * 4]
        self.output = bus()


    def when(self):
        def M2ph2(self):
            self.opa = self.data._v
            if self.ram_select and self.cm.v():
                self.ram_inst = 1
            else:
                self.ram_inst = 0
        def X2ph1(self):
            pass
            #if self.ram_inst:
            #    if self.opa == 0b1000:
            #        self.data.v(self.ram[self.reg][self.char])
            #    elif self.opa == 0b1001:
            #        self.data.v(self.ram[self.reg][self.char])
            #    elif self.opa == 0b1011:
            #        self.data.v(self.ram[self.reg][self.char])
            #    elif self.opa == 0b1100:
            #        self.data.v(self.status[self.reg][0])
            #    elif self.opa == 0b1101:
            #        self.data.v(self.status[self.reg][1])
            #    elif self.opa == 0b1110:
            #        self.data.v(self.status[self.reg][2])
            #    elif self.opa == 0b1111:
            #        self.data.v(self.status[self.reg][3])
        def X2ph2(self):
            if self.cm.v():
                # SRC instruction
                if self.chip == (self.data._v >> 2):
                    self.src = 1 
                    self.ram_select = 1
                    self.reg = self.data._v & 0b0011
                else:
                    self.ram_select = 0
            else:
                self.src = 0                
            if self.ram_inst:
                if self.opa == 0b0000:
                    self.ram[self.reg][self.char] = self.data._v
                elif self.opa == 0b0001:
                    self.output.v(self.data._v)
                elif self.opa == 0b0100:
                    self.status[self.reg][0] = self.data._v
                elif self.opa == 0b0101:
                    self.status[self.reg][1] = self.data._v
                elif self.opa == 0b0110:
                    self.status[self.reg][2] = self.data._v
                elif self.opa == 0b0111:
                    self.status[self.reg][3] = self.data._v
        def X3ph2(self):
            if self.src:
                self.char = self.data._v

        self.timing.whenM2ph2(M2ph2, self)
        self.timing.whenX2ph1(X2ph1, self)
        self.timing.whenX2ph2(X2ph2, self)
        self.timing.whenX3ph2(X3ph2, self)


    def setReg(self):
        self.reg = self.data._v & 0b0011
        pass

    def setChar(self):
        self.char = self.data._v
        pass

    def enableRAM(self):
        self.data.v(self.ram[self.reg][self.char])

    #def setRAM(self):
    #    self.ram[self.reg][self.char] = self.data._v

    def enableStatus(self, char):
        self.data.v(self.status[self.reg][char])

    #def setStatus(self, char):
    #    self.status[self.reg][char] = self.data._v

    #def setOutput(self):
    #    self.output.v(self.data._v)

    def dump(self):
        ss = " ".join(["".join(["{:x}".format(x) for x in self.ram[i]]) + "/" + "".join(["{:x}".format(x) for x in self.status[i]]) for i in range(4)])
        print("RAM {:x}/{:x}:{} OUTPUT:{:04b}".format(self.bank, self.chip, ss, self.output._v))


'''

    def SBM(self):
        sum = self.acc + (~self.mcs4.getRAM() & 0xF) + (~self.cy & 0x1)
        self.cy = sum >> 4
        self.acc = sum & 0xF

    def RDM(self):
        self.acc = self.mcs4.getRAM()

    def ADM(self):
        sum = self.acc + self.mcs4.getRAM() + self.cy
        self.cy = sum >> 4
        self.acc = sum & 0xF

    def RD0(self):
        self.acc = self.mcs4.getStatus(0)

    def RD1(self):
        self.acc = self.mcs4.getStatus(1)
    
    def RD2(self):
        self.acc = self.mcs4.getStatus(2)

    def RD3(self):
        self.acc = self.mcs4.getStatus(3)


'''