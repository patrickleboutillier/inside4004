import sys


class i4004:
    def __init__(self, mcs4):
        self.mcs4 = mcs4
        self.sp = 0 
        self.stack = [0, 0, 0, 0]
        self.index_reg = [0] * 16
        self.cy = 0
        self.acc = 0
        self.opr = 0
        self.opa = 0
        self.cm_ram = 1
        self.ram_addr = 0
        self.test = 0 

    def getPC(self):
        return self.stack[self.sp]

    def setPC(self, h, ml):
        if h is None:
            h = self.getPC() >> 8
        self.stack[self.sp] = h << 8 | ml

    def incPC(self):
        self.stack[self.sp] += 1

    def fetchInst(self, incPC=True):
        inst = self.mcs4.fetchInst(self.getPC())
        if incPC:
            self.incPC()
        return inst 

    def decodeRAMAddr(self):
        chip = self.ram_addr >> 6
        reg = self.ram_addr >> 4 & 0b0011
        char = self.ram_addr & 0xF
        return (chip, reg, char)

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
        print("ERROR!", file=sys.stderr)
        sys.exit(1)

    def JCN(self):
        inst = self.fetchInst()
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
            self.setPC(None, inst)            

    def FIM(self):
        data = self.fetchInst()
        self.index_reg[self.opa & 0b1110] = data >> 4
        self.index_reg[self.opa | 0b0001] = data & 0xF
    
    def SRC(self):
        self.ram_addr = self.index_reg[self.opa & 0b1110] << 4 | self.index_reg[self.opa | 0b0001]

    def FIN(self):
        chip = self.getPC() >> 8
        addr = self.index_reg[0] << 4 | self.index_reg[1]
        self.setPC(None, self.mcs4.getROM(chip, addr))

    def JIN(self):
        addr = (self.index_reg[self.opa & 0b1110]) << 4 | self.index_reg[self.opa | 0b0001]
        self.setPC(None, addr)

    def JUN(self):
        self.setPC(self.opa, self.fetchInst())

    def JMS(self):
        inst = self.fetchInst()
        # Now PC points to the instruction after the jump
        self.sp += 1
        self.setPC(self.opa, inst)

    def INC(self):
        sum = self.index_reg[self.opa] + 1
        self.index_reg[self.opa] = sum & 0xF

    def ISZ(self):
        sum = self.index_reg[self.opa] + 1
        self.index_reg[self.opa] = sum & 0xF
        inst = self.fetchInst()
        if self.index_reg[self.opa]:
            self.setPC(None, inst)

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
      if self.acc & 0b0111 == 0:
        self.cm_ram = 1
      if self.acc & 0b0111 == 1:
        self.cm_ram = 2
      if self.acc & 0b0111 == 2:
        self.cm_ram = 4
      if self.acc & 0b0111 == 3:
        self.cm_ram = 3
      if self.acc & 0b0111 == 4:
        self.cm_ram = 8
      if self.acc & 0b0111 == 5:
        self.cm_ram = 10
      if self.acc & 0b0111 == 6:
        self.cm_ram = 12
      if self.acc & 0b0111 == 7:
        self.cm_ram = 14


    def run(self):
        nb = 0
        while (True):
            inst = self.fetchInst()
            self.opr = inst >> 4
            self.opa = inst & 0xF
            self.mcs4.dump(nb)
            self.decodeInst()
            nb += 1

    def dump(self, inst):
        print("\nINST #{}".format(inst))
        print("OPR/OPA:{:04b}/{:04b}  SP/PC:{:02b}/{:<4}  RAM(CM/ADDR):{:04b}/{:<3}".format(self.opr, self.opa, self.sp, 
            self.getPC(), self.cm_ram, self.ram_addr), end = '')
        print("  ACC/CY:{:04b}/{}  INDEX:{}".format(self.acc, self.cy, "".join(["{:x}".format(x) for x in self.index_reg])))
