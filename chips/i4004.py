import chips.modules.timing as timing
import chips.modules.addr as addr, chips.modules.inst as inst, chips.modules.scratch as scratch, chips.modules.alu as alu
from hdl import *


class i4004:
    def __init__(self, ph1, ph2, data, cm_rom, cm_ram, test):
        self.timing = timing.timing(ph1, ph2, None)
        self.sync = self.timing.sync
        self.data = data
        self.scratch = scratch.scratch(self.timing, data)
        self.alu = alu.alu(self.timing, data)
        self.addr = addr.addr(self, self.scratch, self.timing, self.data, cm_rom)
        self.inst = inst.inst(self, self.scratch, self.timing, self.data, cm_rom, cm_ram)
        self.scratch.inst = self.inst
        self.alu.inst = self.inst

        self.test = test


    def testZero(self):
        return 1 if self.test.v() == 0 else 0

    def decodeInst(self):
        opr = self.inst.opr
        if opr == 0b1111:
            #if self.inst.opa == 0b0010:
            #    self.IAC()
            #elif self.inst.opa == 0b0111:
            #    self.TCC()
            #if self.inst.opa == 0b1000:
            #    self.DAC()
            if self.inst.opa == 0b1001:
                self.TCS()
            elif self.inst.opa == 0b1010:
                self.STC()
            elif self.inst.opa == 0b1011:
                self.DAA()
            elif self.inst.opa == 0b1100:
                self.KBP()
            elif self.inst.opa == 0b1101:
                self.DCL()


    def IAC(self):
        sum = self.alu.acc + 1
        self.alu.cy = sum >> 4
        self.alu.acc = sum & 0xF 

    def TCC(self):
        self.alu.acc = self.alu.cy
        self.alu.cy = 0

    def DAC(self):
        sum = self.alu.acc + 0xF
        self.alu.cy = sum >> 4
        self.alu.acc = sum & 0xF 

    def TCS(self):
        self.alu.acc = 0b1010 if self.alu.cy else 0b1001
        self.alu.cy = 0 

    def STC(self):
        self.alu.cy = 1

    def DAA(self):
        if self.alu.cy or self.alu.acc > 9:
            self.alu.acc += 6
            if self.alu.acc & 0x10:
                self.alu.cy = 1
                self.alu.acc = self.alu.acc & 0xF
            
    def KBP(self):
        if self.alu.acc == 4:
            self.alu.acc = 3
        elif self.alu.acc == 8:
            self.alu.acc = 4
        elif self.alu.acc > 2:
            self.alu.acc = 15

    def DCL(self):
        if self.alu.acc & 0b0111 == 0:
            self.inst.ram_bank = 1
        elif self.alu.acc & 0b0111 == 1:
            self.inst.ram_bank = 2
        elif self.alu.acc & 0b0111 == 2:
            self.inst.ram_bank = 4
        elif self.alu.acc & 0b0111 == 3:
            self.inst.ram_bank = 3
        elif self.alu.acc & 0b0111 == 4:
            self.inst.ram_bank = 8
        elif self.alu.acc & 0b0111 == 5:
            self.inst.ram_bank = 10
        elif self.alu.acc & 0b0111 == 6:
            self.inst.ram_bank = 12
        elif self.alu.acc & 0b0111 == 7:
            self.inst.ram_bank = 14

    def execute(self):
        self.decodeInst()

    def dump(self, cycle):
        print("\nCYCLE #{}".format(cycle))
        self.addr.dump() ; print("  ", end='')
        self.inst.dump() ; print("  ", end='')
        self.scratch.dump() ; print("  ", end='')
        print("TEST:{:b}  ACC/CY:{:04b}/{}".format(self.test.v(), self.alu.acc, self.alu.cy))
