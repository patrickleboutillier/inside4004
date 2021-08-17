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

        self.whenNOP()
        self.whenSRC()
        self.whenJCN_FIM_FIN_JIN_JUN_JMS_ISZ()
        self.whenRDM_RDR_RD0123()
        self.whenWRM_WMP_WRR_WR0123()
        self.whenADM_SBM()


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
            inst.data.v(inst.cpu.index_reg[inst.opa & 0b1110])
        def X3ph1(inst):
            inst.cpu.cm_rom.v(0)
            inst.cpu.cm_ram.v(0)
            inst.data.v(inst.cpu.index_reg[inst.opa | 0b0001])
        self.whenX2ph1(opr, opa, X2ph1)
        self.whenX3ph1(opr, opa, X3ph1)


    # JCN, FIM, FIN, JIN, JUN, JMS, ISZ
    def whenJCN_FIM_FIN_JIN_JUN_JMS_ISZ(self):
        # JCN
        opr, opa = 0b0001, any
        def X1ph1(inst):
            inst.dc = ~inst.dc & 1
            if inst.dc:
                inst.setJCNCond(0 if inst.cpu.acc else 1, inst.cpu.cy, ~inst.cpu.test.v() & 1)  
        self.whenX1ph1(opr, opa, X1ph1)

        # FIM
        opr, opa = 0b0010, even
        def X1ph1(inst):
            inst.dc = ~inst.dc & 1
        self.whenX1ph1(opr, opa, X1ph1)

        # FIN
        opr, opa = 0b0011, even
        def X1ph1(inst):
            inst.dc = ~inst.dc & 1
        self.whenX1ph1(opr, opa, X1ph1)

        # JIN
        opr, opa = 0b0011, odd
        def X1ph1(inst):
            # TODO: Find proper timing for these operations
            inst.cpu.addr.setPM(inst.cpu.index_reg[inst.opa & 0b1110])
            inst.cpu.addr.setPL(inst.cpu.index_reg[inst.opa | 0b0001])
        self.whenX1ph1(opr, opa, X1ph1)

        # JUN, JMS
        def X1ph1(inst):
            inst.dc = ~inst.dc & 1
            if not inst.dc: # TODO: At X1/ph2?
                inst.cpu.addr.setPH(inst.opa)
        for opr in [0b0100, 0b0101]:
            self.whenX1ph1(opr, any, X1ph1)

        # ISZ
        opr, opa = 0b0111, any
        def X1ph1(inst):
            inst.dc = ~inst.dc & 1
            if inst.dc:
                # TODO: Find proper timing for these operations
                sum = inst.cpu.index_reg[inst.opa] + 1
                inst.cpu.index_reg[inst.opa] = sum & 0xF
                inst.setISZCond(inst.cpu.index_reg[inst.opa])
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


    # ADM, SBM
    def whenADM_SBM(self):
        # ADM
        opr, opa = 0b1110, [0b1011]
        def X2ph2(inst):
            sum = inst.cpu.acc + inst.data._v + inst.cpu.cy
            inst.cpu.cy = sum >> 4
            inst.cpu.acc = sum & 0xF
        self.whenX2ph2(opr, opa, X2ph2)

        # SBM
        opr, opa = 0b1110, [0b1000]
        def X2ph2(inst):
            sum = inst.cpu.acc + (~inst.data._v & 0xF) + (~inst.cpu.cy & 1)
            inst.cpu.cy = sum >> 4
            inst.cpu.acc = sum & 0xF
        self.whenX2ph2(opr, opa, X2ph2)
