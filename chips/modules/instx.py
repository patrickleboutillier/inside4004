import sys
from hdl import *


even = list(range(0, 16, 2))
odd = list(range(1, 16, 2))
any = list(range(16))

active_instx = None
opr = 0
opa = []


def register(f, x, n):
     for i in opa:
        active_instx.dispatch[opr][i][x][n] = f 

def A1ph1(f):
    register(f, 0, 0)

def X1ph1(f):
    register(f, 5, 0)

def X1ph2(f):
    register(f, 5, 2)

def X2pre(f):
    register(f, 5, 3)

def X2ph1(f):
    register(f, 6, 0)

def X2ph2(f):
    register(f, 6, 2)

def X3pre(f):
    register(f, 6, 3)

def X3ph1(f):
    register(f, 7, 0)

def X3ph2(f):
    register(f, 7, 2)


class instx:
    def __init__(self, inst):
        global active_instx
        active_instx = self

        self.inst = inst
        self.dispatch = []
        for i in range(16):
            self.dispatch.append([])
            for j in range(16):
              self.dispatch[i].append([])
              for k in range(8):
                self.dispatch[i][j].append([])
                for l in range(4):
                    self.dispatch[i][j][k].append(None)

        self.register()


    def register(_):
        global opr, opa
        inst = _.inst 

        # NOP
        opr, opa = 0b0000, [0b0000]
        @X1ph1
        def _():
            pass

        # HLT
        opr, opa = 0b0000, [0b0001]
        @X1ph1
        def _():
            print("HALTED!")
            sys.exit()

        # ERR
        opr, opa = 0b0000, [0b0010]
        @X1ph1
        def _():
            sys.exit("ERROR!")

        # JCN
        opr, opa = 0b0001, any
        @X1ph1
        def _():
            inst.dcff = ~inst.dcff & 1
        @X3ph2
        def _():
            if inst.dcff:
                inst.setJCNCond()  

        # FIM
        opr, opa = 0b0010, even
        @X1ph1
        def _():
            inst.dcff = ~inst.dcff & 1

        # FIN
        opr, opa = 0b0011, even
        @X1ph1
        def _():
            inst.dcff = ~inst.dcff & 1

        # JIN
        opr, opa = 0b0011, odd
        @X1ph1
        def _():
            inst.scratch.enableRegPairH()
        @X1ph2
        def _():
            inst.cpu.addr.setPM()
        @X2ph1
        def _():
            inst.scratch.enableRegPairL()
        @X2ph2
        def _():
            inst.cpu.addr.setPL()

        # JUN, JMS
        opa = any
        for opr in [0b0100, 0b0101]:
            @X1ph1
            def _():
                inst.dcff = ~inst.dcff & 1
            @X2ph1
            def _():
                if not inst.dcff:
                    inst.data.v(inst.opa)
            @X2ph2
            def _():
                if not inst.dcff:
                    inst.cpu.addr.setPH()

        # BBL
        opr, opa = 0b1100, any
        @X1ph1
        def _():
            inst.cpu.addr.decSP()
        @X2ph1
        def _():
            inst.data.v(inst.opa)
        @X2ph2
        def _():
            inst.cpu.alu.acc = inst.data._v

        # ISZ
        opr, opa = 0b0111, any
        @X1ph1
        def _():
            inst.dcff = ~inst.dcff & 1
            if inst.dcff:
                # TODO: Find proper timing for these operations
                sum = inst.scratch.index_reg[inst.opa] + 1
                inst.scratch.index_reg[inst.opa] = sum & 0xF
        @X3ph2
        def _():
            if inst.dcff:
                inst.cond = ~inst.scratch.regZero() & 1

        # SRC
        opr, opa = 0b0010, odd
        @X2ph1
        def _():
            inst.cm_rom.v(1)
            inst.cm_ram.v(inst.ram_bank)
            inst.scratch.enableRegPairH()
        @X3ph1
        def _():
            inst.cm_rom.v(0)
            inst.cm_ram.v(0)
            inst.scratch.enableRegPairL()

        # RDM, RDR, RD0/1/2/3
        opr, opa = 0b1110, [0b1001, 0b1010, 0b1100, 0b1101, 0b1110, 0b1111]
        @X2ph2
        def _():
            inst.cpu.alu.acc = inst.data._v

        # WRM, WMP, WRR, WR0/1/2/3
        opr, opa = 0b1110, [0b0000, 0b0001, 0b0010, 0b0100, 0b0101, 0b0110, 0b0111]
        @X2ph1
        def _():
            inst.data.v(inst.cpu.alu.acc)

        # ADM
        opr, opa = 0b1110, [0b1011]
        @X2ph2
        def _():
            inst.cpu.alu.setADA()
            inst.cpu.alu.setADC()
        @A1ph1
        def _():
            inst.cpu.alu.runAdder(saveAcc=True, saveCy=True)

        # SBM
        opr, opa = 0b1110, [0b1000]
        @X2ph2
        def _():
            inst.cpu.alu.setADA()
            inst.cpu.alu.setADC(invert=True)
        @A1ph1
        def _():
            inst.cpu.alu.runAdder(invertADB=True, saveAcc=True, saveCy=True)

        # LDM
        opr, opa = 0b1101, any
        @X2pre
        def _():
            inst.data.v(inst.opa)
        @X3pre
        def _():
            inst.cpu.alu.runAdder(saveAcc=True)

        # LD
        opr, opa = 0b1010, any
        @X2pre
        def _():
            inst.scratch.enableReg()
        @X3pre
        def _():
            inst.cpu.alu.runAdder(saveAcc=True)

        # INC
        opr, opa = 0b0110, any
        @X2pre
        def _():
            inst.scratch.enableReg()
        @X2ph1
        def _():
            inst.cpu.alu.setADC(one=True)
        @X3pre
        def _():
            inst.cpu.alu.runAdder()
            inst.cpu.alu.enableSum()
        @X3ph2
        def _():
            inst.scratch.setReg()            

        # ADD
        opr, opa = 0b1000, any
        @X2pre
        def _():
            inst.scratch.enableReg()
        @X2ph1
        def _():
            inst.cpu.alu.setADA()
            inst.cpu.alu.setADC()
        @X3pre
        def _():
            inst.cpu.alu.runAdder(saveAcc=True, saveCy=True)

        # SUB
        opr, opa = 0b1001, any
        @X2pre
        def _():
            inst.scratch.enableReg()
        @X2ph1
        def _():
            inst.cpu.alu.setADA()
            inst.cpu.alu.setADC(invert=True)
        @X3pre
        def _():
            inst.cpu.alu.runAdder(invertADB=True, saveAcc=True, saveCy=True)

        # XCH
        opr, opa = 0b1011, any
        @X2pre
        def _():
            inst.scratch.enableReg()
        @X3pre
        def _():
            inst.cpu.alu.runAdder(saveAcc=True)
            inst.cpu.alu.enableAccOut()
        @X3ph2
        def _():
            inst.scratch.setReg()

        # CLB
        opr, opa = 0b1111, [0b0000]
        @X2pre
        def _():
            # This is not be required, the bus should be clear if no one is writing to it. I assume pull-down registers are used?
            inst.data.v(0)
        @X3pre
        def _():
            inst.cpu.alu.runAdder(saveAcc=True, saveCy=True)

        # CLC
        opr, opa = 0b1111, [0b0001]
        @X2pre
        def _():
            # This is not be required, the bus should be clear if no one is writing to it. I assume pull-down registers are used?
            inst.data.v(0)
        @X3pre
        def _():
            inst.cpu.alu.runAdder(saveCy=True)

        # IAC


        # CMC
        opr, opa = 0b1111, [0b0011]
        # @X2pre
        # def _():
        #     # This is not be required, the bus should be clear if no one is writing to it. I assume pull-down registers are used?
        #     inst.data.v(0)
        #@X2ph1
        #def _():
        #    inst.cpu.alu.setADC(invert=True)
        #@X3pre
        #def _():
        #    inst.cpu.alu.runAdder(invertADB=True, saveCy=True)

        # CMA
        opr, opa = 0b1111, [0b0100]
        # @X2pre
        # def _():
        #     # This is not be required, the bus should be clear if no one is writing to it. I assume pull-down registers are used?
        #     inst.data.v(0)
        #@X2ph1
        #def _():
        #    inst.cpu.alu.setADA(invert=True)
        #@X3pre
        #def _():
        #    inst.cpu.alu.runAdder(saveAcc=True)

        # RAL
        # RAR
        # TCC
        # DAC
        # TCS
        # STC