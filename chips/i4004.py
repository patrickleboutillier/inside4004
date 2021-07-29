import sys
from hdl import *


class i4004:
    def __init__(self, mcs4, data, ram_lines):
        self.mcs4 = mcs4
        self.data = data
        self.sp = 0
        self.stack = [{'h':0, 'm':0, 'l':0}, {'h':0, 'm':0, 'l':0}, {'h':0, 'm':0, 'l':0}, {'h':0, 'm':0, 'l':0}]
        self.index_reg = [0] * 16
        self.cy = 0
        self.acc = 0
        self.opr = 0
        self.opa = 0
        self.cm_ram = reg(bus(), wire(), ram_lines, "CM-RAM")
        # Initialize CM-RAM to 1 (see DCL)
        self.cm_ram.bi().v(1)
        self.cm_ram.s().v(1)
        self.cm_ram.s().v(0)
        self.test = 0

    def getPH(self):
        return self.stack[self.sp]['h']

    def getPM(self):
        return self.stack[self.sp]['m']

    def getPL(self):
        return self.stack[self.sp]['l']

    def setPH(self, ph):
        self.stack[self.sp]['h'] = ph

    def setPM(self, pm):
        self.stack[self.sp]['m'] = pm

    def setPL(self, pl):
        self.stack[self.sp]['l'] = pl

    def incPC(self):
        pc = self.stack[self.sp]['h'] << 8 | self.stack[self.sp]['m'] << 4 | self.stack[self.sp]['l']
        pc += 1  
        self.stack[self.sp]['h'] = pc >> 8
        self.stack[self.sp]['m'] = pc >> 4 & 0xF
        self.stack[self.sp]['l'] = pc & 0xF

    def fetchInst(self, incPC=True):
        (insth, instl) = self.mcs4.fetchInst(self.getPH(), self.getPM(), self.getPL())
        if incPC:
            self.incPC()
        return (insth, instl)

    def decodeInst(self):
        if self.opr == 0b0000:
            if self.opa == 0b0000:
                self.NOP()
            elif self.opa == 0b0001:
                self.HLT()
            elif self.opa == 0b0010:
                self.ERR()

        elif self.opr == 0b0001:
            self.JCN()
        elif self.opr == 0b0010:
            if not (self.opa & 0b1):
                self.FIM()
            elif self.opa & 0b1:
                self.SRC()
        elif self.opr == 0b0011:
            if not (self.opa & 0b1):
                self.FIN()
            elif self.opa & 0b1:
                self.JIN()
        elif self.opr == 0b0100:
            self.JUN()
        elif self.opr == 0b0101:
            self.JMS()
        elif self.opr == 0b0110:
            self.INC()
        elif self.opr == 0b0111:
            self.ISZ()
        elif self.opr == 0b1000:
            self.ADD()
        elif self.opr == 0b1001:
            self.SUB()
        elif self.opr == 0b1010:
            self.LD()
        elif self.opr == 0b1011:
            self.XCH()
        elif self.opr == 0b1100:
            self.BBL()
        elif self.opr == 0b1101:
            self.LDM()

        elif self.opr == 0b1110:
            if self.opa == 0b0000:
                self.WRM()
            elif self.opa == 0b0001:
                self.WMP()
            elif self.opa == 0b0010:
                self.WRR()
            elif self.opa == 0b0100:
                self.WR0()
            elif self.opa == 0b0101:
                self.WR1()
            elif self.opa == 0b0110:
                self.WR2()
            elif self.opa == 0b0111:
                self.WR3()
            elif self.opa == 0b1000:
                self.SBM()
            elif self.opa == 0b1001:
                self.RDM()
            elif self.opa == 0b1010:
                self.RDR()
            elif self.opa == 0b1011:
                self.ADM()
            elif self.opa == 0b1100:
                self.RD0()
            elif self.opa == 0b1101:
                self.RD1()
            elif self.opa == 0b1110:
                self.RD2()
            elif self.opa == 0b1111:
                self.RD3()

        elif self.opr == 0b1111:
            if self.opa == 0b0000:
                self.CLB()
            elif self.opa == 0b0001:
                self.CLC()
            elif self.opa == 0b0010:
                self.IAC()
            elif self.opa == 0b0011:
                self.CMC()
            elif self.opa == 0b0100:
                self.CMA()
            elif self.opa == 0b0101:
                self.RAL()
            elif self.opa == 0b0110:
                self.RAR()
            elif self.opa == 0b0111:
                self.TCC()
            elif self.opa == 0b1000:
                self.DAC()
            elif self.opa == 0b1001:
                self.TCS()
            elif self.opa == 0b1010:
                self.STC()
            elif self.opa == 0b1011:
                self.DAA()
            elif self.opa == 0b1100:
                self.KBP()
            elif self.opa == 0b1101:
                self.DCL()


    def NOP(self):
        pass 

    # HLT is used to normal (wanted) termination
    def HLT(self):
        print("HALTED!")
        sys.exit()

    # ERR is used for signaling error conditions. It is mainly ued in the test suite.
    def ERR(self):
        sys.exit("ERROR!")

    def JCN(self):
        (insth, instl) = self.fetchInst()
        invert = bool(self.opa & 0b1000)
        (zero, cy, test) = (self.opa & 0b0100, self.opa & 0b0010, self.opa & 0b0001)
        jump = False
        if zero and ((~self.acc & 0b1) ^ invert):
            jump = True
        if cy and (self.cy ^ invert):
            jump = True
        if test and (self.test ^ invert):
            jump = True
        if jump:
            self.setPM(insth)
            self.setPL(instl)            

    def FIM(self):
        (datah, datal) = self.fetchInst()
        self.index_reg[self.opa & 0b1110] = datah
        self.index_reg[self.opa | 0b0001] = datal
    
    def SRC(self):
        self.mcs4.setRAMAddr(self.index_reg[self.opa & 0b1110], self.index_reg[self.opa | 0b0001])

    def FIN(self):
        (addrh, addrl) = self.mcs4.getROM(self.getPH(), self.index_reg[0], self.index_reg[1])
        self.setPM(addrh)
        self.setPL(addrl)

    def JIN(self):
        self.setPM(self.index_reg[self.opa & 0b1110])
        self.setPL(self.index_reg[self.opa | 0b0001])

    def JUN(self):
        self.setPH(self.opa)
        (insth, instl) = self.fetchInst()
        self.setPM(insth)
        self.setPL(instl)

    def JMS(self):
        (insth, instl) = self.fetchInst()
        # Now PC points to the instruction after the jump
        self.sp += 1
        self.setPH(self.opa)
        self.setPM(insth)
        self.setPL(instl)

    def INC(self):
        sum = self.index_reg[self.opa] + 1
        self.index_reg[self.opa] = sum & 0xF

    def ISZ(self):
        sum = self.index_reg[self.opa] + 1
        self.index_reg[self.opa] = sum & 0xF
        (insth, instl) = self.fetchInst()
        if self.index_reg[self.opa]:
            self.setPM(insth)
            self.setPL(instl)

    def ADD(self):
        sum = self.acc + self.index_reg[self.opa] + self.cy
        self.cy = sum >> 4
        self.acc = sum & 0xF

    def SUB(self):
        sum = self.acc + (~self.index_reg[self.opa] & 0xF) + (~self.cy & 0b1)
        self.cy = sum >> 4
        self.acc = sum & 0xF

    def LD(self):
        self.acc = self.index_reg[self.opa]

    def XCH(self):
        tmp = self.index_reg[self.opa]
        self.index_reg[self.opa] = self.acc
        self.acc = tmp

    def BBL(self):
        self.sp -= 1
        self.acc = self.opa 

    def LDM(self):
        self.acc = self.opa


    def WRM(self):
        self.mcs4.setRAM(self.acc)

    def WMP(self):
        self.mcs4.setOutput(self.acc)

    def WRR(self):
        chip = self.ram_addr >> 4
        self.mcs4.setIO(chip, self.acc)

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
        chip = self.ram_addr >> 4
        self.acc = self.mcs4.getIO(chip)

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

    def run(self):
        nb = 0
        while (True):
            (self.opr, self.opa) = self.fetchInst()
            self.mcs4.dump(nb)
            self.decodeInst()
            nb += 1

    def dump(self, inst):
        print("\nINST #{}".format(inst))
        print("OPR/OPA:{:04b}/{:04b}  SP/PC:{:02b}/{:<4}  RAM(CM):{:04b}".format(self.opr, self.opa, self.sp, 
            (self.getPH()*16*16 + self.getPM()*16 + self.getPL()), self.cm_ram.bo().v()), end = '')
        print("  ACC/CY:{:04b}/{}  INDEX:{}".format(self.acc, self.cy, "".join(["{:x}".format(x) for x in self.index_reg])))
