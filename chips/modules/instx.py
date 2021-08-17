import sys
from hdl import *


X1 = 0
X2 = 1
X3 = 2

ph1 = 0
ph2 = 1

even = list(range(0, 16, 2))
odd = list(range(1, 16, 2))
any = list(range(16))


class instx:
    def __init__(self, inst):
        self.inst = inst
        self.dispatch = []
        for i in range(16):
            self.dispatch.append([])
            for j in range(16):
              self.dispatch[i].append([])
              for k in range(3):
                self.dispatch[i][j].append([])
                for l in range(2):
                    self.dispatch[i][j][k].append(None)

        self.when()

    
    def when(self):
        self.whenNOP()
        self.whenSRC()
        self.whenJCN_FIM()
        self.whenRDM_RDR_RD0123()
        self.whenWRM_WMP_WRR_WR0123()
        self.whenSBM() ; self.whenADM()

    def whenX1ph1(self, opr, opa, f):
        global X1, ph1
        for i in opa:
            self.dispatch[opr][i][X1][ph1] = f

    def whenX1ph2(self, opr, opa, f):
        global X1, ph2
        for i in opa:
            self.dispatch[opr][i][X1][ph2] = f

    def whenX2ph1(self, opr, opa, f):
        global X2, ph1
        for i in opa:
            self.dispatch[opr][i][X2][ph1] = f

    def whenX2ph2(self, opr, opa, f):
        global X2, ph2
        for i in opa:
            self.dispatch[opr][i][X2][ph2] = f

    def whenX3ph1(self, opr, opa, f):
        global X3, ph1
        for i in opa:
            self.dispatch[opr][i][X3][ph1] = f

    def whenX3ph2(self, opr, opa, f):
        global X3, ph2
        for i in opa:
            self.dispatch[opr][i][X3][ph2] = f


    # NOP, HLT, ERR
    def whenNOP(self):
        opr, opa = 0b0000, [0b0000]
        def X1ph1(inst):
            pass
        self.whenX1ph1(opr, opa, X1ph1)

        opr, opa = 0b0000, [0b0001]
        def X1ph1(inst):
            print("HALTED!")
            sys.exit()
        self.whenX1ph1(opr, opa, X1ph1)

        opr, opa = 0b0000, [0b0010]
        def X1ph1(inst):
            sys.exit("ERROR!")
        self.whenX1ph1(opr, opa, X1ph1)

    # SRC
    def whenSRC(self):
        opr, opa = 0b0010, odd
        def X2ph1(inst):
            inst.cpu.cm_rom.v(1)
            inst.cpu.cm_ram.v(inst.cpu.ram_bank)
            inst.data.v(inst.cpu.index_reg[inst.opa.v & 0b1110])
        def X3ph1(inst):
            inst.cpu.cm_rom.v(0)
            inst.cpu.cm_ram.v(0)
            inst.data.v(inst.cpu.index_reg[inst.opa.v | 0b0001])
        self.whenX2ph1(opr, opa, X2ph1)
        self.whenX3ph1(opr, opa, X3ph1)

    # JCN, FIM
    def whenJCN_FIM(self):
        opr, opa = 0b0001, any
        def X1ph1(inst):
            inst.dc = ~inst.dc & 1
            if inst.dc:
                inst.setJCNCond(0 if inst.cpu.acc else 1, inst.cpu.cy, ~inst.cpu.test.v() & 1)  
        self.whenX1ph1(opr, opa, X1ph1)

        opr, opa = 0b0010, even
        def X1ph1(inst):
            inst.dc = ~inst.dc & 1
        self.whenX1ph1(opr, opa, X1ph1)

    # WRM, WMP, WRR, WR0/1/2/3
    def whenWRM_WMP_WRR_WR0123(self):
        opr, opa = 0b1110, [0b0000, 0b0001, 0b0010, 0b0100, 0b0101, 0b0110, 0b0111]
        def X2ph1(inst):
            inst.data.v(inst.cpu.acc)
        self.whenX2ph1(opr, opa, X2ph1)
 
     # RDM, RD0/1/2/3
    def whenRDM_RDR_RD0123(self):
        opr, opa = 0b1110, [0b1001, 0b1010, 0b1100, 0b1101, 0b1110, 0b1111]
        def X2ph2(inst):
            inst.cpu.acc = inst.data._v
        self.whenX2ph2(opr, opa, X2ph2)

    def whenSBM(self):
        opr, opa = 0b1110, [0b1000]
        def X2ph2(inst):
            sum = inst.cpu.acc + (~inst.data._v & 0xF) + (~inst.cpu.cy & 1)
            inst.cpu.cy = sum >> 4
            inst.cpu.acc = sum & 0xF
        self.whenX2ph2(opr, opa, X2ph2)

    def whenADM(self):
        opr, opa = 0b1110, [0b1011]
        def X2ph2(inst):
            sum = inst.cpu.acc + inst.data._v + inst.cpu.cy
            inst.cpu.cy = sum >> 4
            inst.cpu.acc = sum & 0xF
        self.whenX2ph2(opr, opa, X2ph2)


    '''
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

    def ISZ(self):
        self.inst.dc = ~self.inst.dc & 1
        if self.inst.dc:
            sum = self.index_reg[self.inst.opa.v] + 1
            self.index_reg[self.inst.opa.v] = sum & 0xF
            self.inst.setISZCond(self.index_reg[self.inst.opa.v])
'''