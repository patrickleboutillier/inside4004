import chips.modules.timing as timing
import chips.modules.addr as addr, chips.modules.inst as inst, chips.modules.scratch as scratch
from hdl import *


class i4004:
    def __init__(self, ph1, ph2, data, cm_rom, cm_ram, test):
        self.timing = timing.timing(ph1, ph2, None)
        self.sync = self.timing.sync
        self.data = data
        self.scratch = scratch.scratch(data)
        self.addr = addr.addr(self, self.scratch, self.timing, self.data, cm_rom)
        self.inst = inst.inst(self, self.scratch, self.timing, self.data, cm_rom, cm_ram)
        self.scratch.inst = self.inst

        self.cy = 0
        self.acc = 0
        self.test = test


    def decodeInst(self):
        opr = self.inst.opr
        if self.inst.inc():
            self.INC()
        elif opr == 0b1000:
            self.ADD()
        elif opr == 0b1001:
            self.SUB()
        elif opr == 0b1010:
            self.LD()
        elif opr == 0b1011:
            self.XCH()
        elif opr == 0b1100:
            self.BBL()
        elif opr == 0b1101:
            self.LDM()

        elif opr == 0b1111:
            if self.inst.opa == 0b0000:
                self.CLB()
            elif self.inst.opa == 0b0001:
                self.CLC()
            elif self.inst.opa == 0b0010:
                self.IAC()
            elif self.inst.opa == 0b0011:
                self.CMC()
            elif self.inst.opa == 0b0100:
                self.CMA()
            elif self.inst.opa == 0b0101:
                self.RAL()
            elif self.inst.opa == 0b0110:
                self.RAR()
            elif self.inst.opa == 0b0111:
                self.TCC()
            elif self.inst.opa == 0b1000:
                self.DAC()
            elif self.inst.opa == 0b1001:
                self.TCS()
            elif self.inst.opa == 0b1010:
                self.STC()
            elif self.inst.opa == 0b1011:
                self.DAA()
            elif self.inst.opa == 0b1100:
                self.KBP()
            elif self.inst.opa == 0b1101:
                self.DCL()


    def INC(self):
        sum = self.scratch.index_reg[self.inst.opa] + 1
        self.scratch.index_reg[self.inst.opa] = sum & 0xF

    def ADD(self):
        sum = self.acc + self.scratch.index_reg[self.inst.opa] + self.cy
        self.cy = sum >> 4
        self.acc = sum & 0xF

    def SUB(self):
        sum = self.acc + (~self.scratch.index_reg[self.inst.opa] & 0xF) + (~self.cy & 0b1)
        self.cy = sum >> 4
        self.acc = sum & 0xF

    def LD(self):
        self.acc = self.scratch.index_reg[self.inst.opa]

    def XCH(self):
        tmp = self.scratch.index_reg[self.inst.opa]
        self.scratch.index_reg[self.inst.opa] = self.acc
        self.acc = tmp

    def BBL(self):
        self.addr.decSP()
        self.acc = self.inst.opa 

    def LDM(self):
        self.acc = self.inst.opa


    def CLB(self):
        self.acc = 0
        self.cy = 0

    def CLC(self):
        self.cy = 0 

    def IAC(self):
        sum = self.acc + 1
        self.cy = sum >> 4
        self.acc = sum & 0xF 

    def CMC(self):
        self.cy = ~self.cy & 0b1

    def CMA(self):
        self.acc = ~self.acc & 0xF

    def RAL(self):
        res = self.acc << 1 | self.cy
        self.cy = res >> 4
        self.acc = res & 0xF 

    def RAR(self):
        co = self.acc & 1
        res = self.cy << 3 | self.acc >> 1 
        self.cy = co
        self.acc = res

    def TCC(self):
        self.acc = self.cy
        self.cy = 0

    def DAC(self):
        sum = self.acc + 0xF
        self.cy = sum >> 4
        self.acc = sum & 0xF 

    def TCS(self):
        self.acc = 0b1010 if self.cy else 0b1001
        self.cy = 0 

    def STC(self):
        self.cy = 1

    def DAA(self):
        if self.cy or self.acc > 9:
            self.acc += 6
            if self.acc & 0x10:
                self.cy = 1
                self.acc = self.acc & 0xF
            
    def KBP(self):
        if self.acc == 4:
            self.acc = 3
        elif self.acc == 8:
            self.acc = 4
        elif self.acc > 2:
            self.acc = 15

    def DCL(self):
        if self.acc & 0b0111 == 0:
            self.inst.ram_bank = 1
        elif self.acc & 0b0111 == 1:
            self.inst.ram_bank = 2
        elif self.acc & 0b0111 == 2:
            self.inst.ram_bank = 4
        elif self.acc & 0b0111 == 3:
            self.inst.ram_bank = 3
        elif self.acc & 0b0111 == 4:
            self.inst.ram_bank = 8
        elif self.acc & 0b0111 == 5:
            self.inst.ram_bank = 10
        elif self.acc & 0b0111 == 6:
            self.inst.ram_bank = 12
        elif self.acc & 0b0111 == 7:
            self.inst.ram_bank = 14

    def execute(self):
        self.decodeInst()

    def dump(self, inst):
        print("\nCYCLE #{}".format(inst))
        pc = self.addr.getPC()
        print("OPR/OPA:{:04b}/{:04b}  SP/PC:{:02b}/{:<4} ({:03x})  RAM(CM):{:04b}  TEST:{:b}".format(self.inst.opr, self.inst.opa, self.addr.sp, 
            pc, pc, self.inst.cm_ram._v, self.test.v()), end = '')
        print("  ACC/CY:{:04b}/{}  INDEX:{}  DC:{}".format(self.acc, self.cy, "".join(["{:x}".format(x) for x in self.scratch.index_reg]), self.inst.dc))
        print(self.addr.stack)
