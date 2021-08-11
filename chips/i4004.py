import sys
import chips.modules.timing as timing
import chips.modules.addr as addr, chips.modules.inst as inst
from hdl import *


class i4004(sensor):
    def __init__(self, mcs4, ph1, ph2, data, cm_rom, cm_ram, test):
        self.sync = wire()
        self.timing = timing.timing(ph1, ph2, self.sync)
        # sensor.__init__(self, ph1, ph2, data)
        self.mcs4 = mcs4
        self.data = data
        self.cm_rom = cm_rom
        self.addr = addr.addr(self, self.timing, self.data, self.cm_rom)
        self.inst = inst.inst(self, self.timing, self.data)
        self.index_reg = [0] * 16
        self.cy = 0
        self.acc = 0


        self.cm_ram = reg(bus(v=1), wire(), cm_ram)

        self.test = test


    def always(self, signal):
        pass

    def decodeInst(self):
        opr = self.inst.opr.v 
        if self.inst.nop():
            self.NOP()
        elif self.inst.hlt():
            self.HLT()
        elif self.inst.err():
            self.ERR()

        elif self.inst.jcn():
            self.JCN()
        elif self.inst.fim():
            self.FIM()
        elif self.inst.src():
            self.SRC()
        elif self.inst.fin():
            self.FIN()
        elif self.inst.jin():
            self.JIN()
        elif self.inst.jun():
            self.JUN()
        elif self.inst.jms():
            self.JMS()
        elif self.inst.inc():
            self.INC()
        elif self.inst.isz():
            self.ISZ()

        if opr == 0b1000:
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

        elif opr == 0b1110:
            if self.inst.opa.v == 0b0000:
                self.WRM()
            elif self.inst.opa.v == 0b0001:
                self.WMP()
            elif self.inst.opa.v == 0b0010:
                self.WRR()
            elif self.inst.opa.v == 0b0100:
                self.WR0()
            elif self.inst.opa.v == 0b0101:
                self.WR1()
            elif self.inst.opa.v == 0b0110:
                self.WR2()
            elif self.inst.opa.v == 0b0111:
                self.WR3()
            elif self.inst.opa.v == 0b1000:
                self.SBM()
            elif self.inst.opa.v == 0b1001:
                self.RDM()
            elif self.inst.opa.v == 0b1010:
                self.RDR()
            elif self.inst.opa.v == 0b1011:
                self.ADM()
            elif self.inst.opa.v == 0b1100:
                self.RD0()
            elif self.inst.opa.v == 0b1101:
                self.RD1()
            elif self.inst.opa.v == 0b1110:
                self.RD2()
            elif self.inst.opa.v == 0b1111:
                self.RD3()

        elif opr == 0b1111:
            if self.inst.opa.v == 0b0000:
                self.CLB()
            elif self.inst.opa.v == 0b0001:
                self.CLC()
            elif self.inst.opa.v == 0b0010:
                self.IAC()
            elif self.inst.opa.v == 0b0011:
                self.CMC()
            elif self.inst.opa.v == 0b0100:
                self.CMA()
            elif self.inst.opa.v == 0b0101:
                self.RAL()
            elif self.inst.opa.v == 0b0110:
                self.RAR()
            elif self.inst.opa.v == 0b0111:
                self.TCC()
            elif self.inst.opa.v == 0b1000:
                self.DAC()
            elif self.inst.opa.v == 0b1001:
                self.TCS()
            elif self.inst.opa.v == 0b1010:
                self.STC()
            elif self.inst.opa.v == 0b1011:
                self.DAA()
            elif self.inst.opa.v == 0b1100:
                self.KBP()
            elif self.inst.opa.v == 0b1101:
                self.DCL()


    def NOP(self):
        pass 

    # HLT is used to normal (wanted) termination
    def HLT(self):
        print("HALTED!")
        sys.exit()

    # ERR is used for signaling error conditions. It is mainly used in the test suite.
    def ERR(self):
        sys.exit("ERROR!")

    def JCN(self):
        self.inst.dc = ~self.inst.dc & 1
        if self.inst.dc:
            self.inst.setJCNCond(0 if self.acc else 1, self.cy, ~self.test.v() & 1)      

    def FIM(self):
        self.inst.dc = ~self.inst.dc & 1
    
    def SRC(self):
        self.mcs4.setRAMAddr(self.index_reg[self.inst.opa.v & 0b1110], self.index_reg[self.inst.opa.v | 0b0001])
        self.mcs4.setIOAddr(self.index_reg[self.inst.opa.v & 0b1110])

    def FIN(self):
        self.inst.dc = ~self.inst.dc & 1

    def JIN(self):
        self.addr.setPM(self.index_reg[self.inst.opa.v & 0b1110])
        self.addr.setPL(self.index_reg[self.inst.opa.v | 0b0001])

    def JUN(self):
        self.inst.dc = ~self.inst.dc & 1
        if not self.inst.dc: # TODO: At X1/ph2?
            self.addr.setPH(self.inst.opa.v)

    def JMS(self):
        self.inst.dc = ~self.inst.dc & 1
        if not self.inst.dc: # TODO: At X1/ph2?
            self.addr.setPH(self.inst.opa.v)

    def INC(self):
        sum = self.index_reg[self.inst.opa.v] + 1
        self.index_reg[self.inst.opa.v] = sum & 0xF

    def ISZ(self):
        self.inst.dc = ~self.inst.dc & 1
        if self.inst.dc:
            sum = self.index_reg[self.inst.opa.v] + 1
            self.index_reg[self.inst.opa.v] = sum & 0xF
            self.inst.setISZCond(self.index_reg[self.inst.opa.v])


    def ADD(self):
        sum = self.acc + self.index_reg[self.inst.opa.v] + self.cy
        self.cy = sum >> 4
        self.acc = sum & 0xF

    def SUB(self):
        sum = self.acc + (~self.index_reg[self.inst.opa.v] & 0xF) + (~self.cy & 0b1)
        self.cy = sum >> 4
        self.acc = sum & 0xF

    def LD(self):
        self.acc = self.index_reg[self.inst.opa.v]

    def XCH(self):
        tmp = self.index_reg[self.inst.opa.v]
        self.index_reg[self.inst.opa.v] = self.acc
        self.acc = tmp

    def BBL(self):
        self.addr.decSP()
        self.acc = self.inst.opa.v 

    def LDM(self):
        self.acc = self.inst.opa.v


    def WRM(self):
        self.mcs4.setRAM(self.acc)

    def WMP(self):
        self.mcs4.setOutput(self.acc)

    def WRR(self):
        self.mcs4.setIO(self.acc)

    def WR0(self):
        self.mcs4.setStatus(0, self.acc)

    def WR1(self):
        self.mcs4.setStatus(1, self.acc)
   
    def WR2(self):
        self.mcs4.setStatus(2, self.acc)

    def WR3(self):
        self.mcs4.setStatus(3, self.acc)

    def SBM(self):
        sum = self.acc + (~self.mcs4.getRAM() & 0xF) + (~self.cy & 0x1)
        self.cy = sum >> 4
        self.acc = sum & 0xF

    def RDM(self):
        self.acc = self.mcs4.getRAM()

    def RDR(self):
        self.acc = self.mcs4.getIO()

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
        self.cm_ram.s().v(1)
        if self.acc & 0b0111 == 0:
            self.cm_ram.bi().v(1)
        elif self.acc & 0b0111 == 1:
            self.cm_ram.bi().v(2)
        elif self.acc & 0b0111 == 2:
            self.cm_ram.bi().v(4)
        elif self.acc & 0b0111 == 3:
            self.cm_ram.bi().v(3)
        elif self.acc & 0b0111 == 4:
            self.cm_ram.bi().v(8)
        elif self.acc & 0b0111 == 5:
            self.cm_ram.bi().v(10)
        elif self.acc & 0b0111 == 6:
            self.cm_ram.bi().v(12)
        elif self.acc & 0b0111 == 7:
            self.cm_ram.bi().v(14)
        self.cm_ram.s().v(0)

    def execute(self):
        self.decodeInst()

    def dump(self, inst):
        print("\nINST #{}".format(inst))
        pc = self.addr.getPC
        print("OPR/OPA:{:04b}/{:04b}  SP/PC:{:02b}/{:<4} ({:03x})  RAM(CM):{:04b}  TEST:{:b}".format(self.inst.opr.v, self.inst.opa.v, self.addr.sp, 
            pc, pc, self.cm_ram.bo().v(), self.test.v()), end = '')
        print("  ACC/CY:{:04b}/{}  INDEX:{}  DC:{}".format(self.acc, self.cy, "".join(["{:x}".format(x) for x in self.index_reg]), self.inst.dc))
        print(self.addr.stack)
