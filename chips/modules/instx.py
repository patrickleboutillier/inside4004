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
        self.whenRDR_WRR()
        self.whenJCN_FIM()


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
            inst.data.v(inst.cpu.index_reg[inst.opa.v & 0b1110])
        def X3ph1(inst):
            inst.cpu.cm_rom.v(0)
        self.whenX2ph1(opr, opa, X2ph1)
        self.whenX3ph1(opr, opa, X3ph1)

    # RDR, WRR
    def whenRDR_WRR(self):
        opr, opa = 0b1110, [0b1010]
        def X2ph2(inst):
            print("RDR 4004", inst.data._v)
            inst.cpu.acc = inst.data._v
        self.whenX2ph2(opr, opa, X2ph2)

        opr, opa = 0b1110, [0b0010]
        def X2ph1(inst):
            print("WRR 4004", inst.cpu.acc)
            inst.data.v(inst.cpu.acc)
        self.whenX2ph1(opr, opa, X2ph1)

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