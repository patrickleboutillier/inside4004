import chips.modules.timing as timing
import chips.modules.addr as addr, chips.modules.inst as inst, chips.modules.scratch as scratch, chips.modules.arith as arith
from hdl import *


class i4004:
    def __init__(self, ph1, ph2, data, cm_rom, cm_ram, test):
        self.timing = timing.timing(ph1, ph2, None)
        self.sync = self.timing.sync
        self.data = data
        self.scratch = scratch.scratch(data)
        self.arith = arith.arith(data)
        self.addr = addr.addr(self, self.scratch, self.timing, self.data, cm_rom)
        self.inst = inst.inst(self, self.scratch, self.timing, self.data, cm_rom, cm_ram)
        self.scratch.inst = self.inst

        self.test = test


    def testZero(self):
        return 1 if self.test.v() == 0 else 0

    def decodeInst(self):
        opr = self.inst.opr
        if opr == 0b0110:
            self.INC()
        elif opr == 0b1000:
            self.ADD()
        elif opr == 0b1001:
            self.SUB()
        elif opr == 0b1010:
            self.LD()
        elif opr == 0b1011:
            self.XCH()
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
        sum = self.arith.acc + self.scratch.index_reg[self.inst.opa] + self.arith.cy
        self.arith.cy = sum >> 4
        self.arith.acc = sum & 0xF

    def SUB(self):
        sum = self.arith.acc + (~self.scratch.index_reg[self.inst.opa] & 0xF) + (~self.arith.cy & 0b1)
        self.arith.cy = sum >> 4
        self.arith.acc = sum & 0xF

    def LD(self):
        self.arith.acc = self.scratch.index_reg[self.inst.opa]

    def XCH(self):
        tmp = self.scratch.index_reg[self.inst.opa]
        self.scratch.index_reg[self.inst.opa] = self.arith.acc
        self.arith.acc = tmp

    def LDM(self):
        self.arith.acc = self.inst.opa


    def CLB(self):
        self.arith.acc = 0
        self.arith.cy = 0

    def CLC(self):
        self.arith.cy = 0 

    def IAC(self):
        sum = self.arith.acc + 1
        self.arith.cy = sum >> 4
        self.arith.acc = sum & 0xF 

    def CMC(self):
        self.arith.cy = ~self.arith.cy & 0b1

    def CMA(self):
        self.arith.acc = ~self.arith.acc & 0xF

    def RAL(self):
        res = self.arith.acc << 1 | self.arith.cy
        self.arith.cy = res >> 4
        self.arith.acc = res & 0xF 

    def RAR(self):
        co = self.arith.acc & 1
        res = self.arith.cy << 3 | self.arith.acc >> 1 
        self.arith.cy = co
        self.arith.acc = res

    def TCC(self):
        self.arith.acc = self.arith.cy
        self.arith.cy = 0

    def DAC(self):
        sum = self.arith.acc + 0xF
        self.arith.cy = sum >> 4
        self.arith.acc = sum & 0xF 

    def TCS(self):
        self.arith.acc = 0b1010 if self.arith.cy else 0b1001
        self.arith.cy = 0 

    def STC(self):
        self.arith.cy = 1

    def DAA(self):
        if self.arith.cy or self.arith.acc > 9:
            self.arith.acc += 6
            if self.arith.acc & 0x10:
                self.arith.cy = 1
                self.arith.acc = self.arith.acc & 0xF
            
    def KBP(self):
        if self.arith.acc == 4:
            self.arith.acc = 3
        elif self.arith.acc == 8:
            self.arith.acc = 4
        elif self.arith.acc > 2:
            self.arith.acc = 15

    def DCL(self):
        if self.arith.acc & 0b0111 == 0:
            self.inst.ram_bank = 1
        elif self.arith.acc & 0b0111 == 1:
            self.inst.ram_bank = 2
        elif self.arith.acc & 0b0111 == 2:
            self.inst.ram_bank = 4
        elif self.arith.acc & 0b0111 == 3:
            self.inst.ram_bank = 3
        elif self.arith.acc & 0b0111 == 4:
            self.inst.ram_bank = 8
        elif self.arith.acc & 0b0111 == 5:
            self.inst.ram_bank = 10
        elif self.arith.acc & 0b0111 == 6:
            self.inst.ram_bank = 12
        elif self.arith.acc & 0b0111 == 7:
            self.inst.ram_bank = 14

    def execute(self):
        self.decodeInst()

    def dump(self, cycle):
        print("\nCYCLE #{}".format(cycle))
        self.addr.dump() ; print("  ", end='')
        self.inst.dump() ; print("  ", end='')
        self.scratch.dump() ; print("  ", end='')
        print("TEST:{:b}  ACC/CY:{:04b}/{}".format(self.test.v(), self.arith.acc, self.arith.cy))
