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

def A1clk1(f):
    register(f, 0, 0)

def X1clk1(f):
    register(f, 5, 0)

def X1clk2(f):
    register(f, 5, 2)

def X21(f):
    register(f, 5, 3)

def X2clk1(f):
    register(f, 6, 0)

def X2clk2(f):
    register(f, 6, 2)

def X31(f):
    register(f, 6, 3)

def X3clk1(f):
    register(f, 7, 0)

def X3clk2(f):
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
        @X1clk1
        def _():
            pass

        # HLT
        opr, opa = 0b0000, [0b0001]
        @X1clk1
        def _():
            print("HALTED!")
            sys.exit()

        # ERR
        opr, opa = 0b0000, [0b0010]
        @X1clk1
        def _():
            sys.exit("ERROR!")

        # JCN
        opr, opa = 0b0001, any
        @X1clk1
        def _():
            inst.dcff = ~inst.dcff & 1
        @X3clk2
        def _():
            if inst.dcff:
                inst.setJCNCond()  

        # FIM
        opr, opa = 0b0010, even
        @X1clk1
        def _():
            inst.dcff = ~inst.dcff & 1

        # SRC
        opr, opa = 0b0010, odd
        @X21
        def _():
            inst.scratch.enableRegPairH()
            inst.cm_rom.v = 1
            inst.cm_ram.v(inst.ram_bank)
        @X31
        def _():
            inst.scratch.enableRegPairL()
            inst.cm_rom.v = 0
            inst.cm_ram.v(0)

        # FIN
        opr, opa = 0b0011, even
        @X1clk1
        def _():
            inst.dcff = ~inst.dcff & 1

        # JIN
        opr, opa = 0b0011, odd
        @X1clk1
        def _():
            inst.scratch.enableRegPairH()
        @X1clk2
        def _():
            inst.cpu.addr.setPM()
        @X2clk1
        def _():
            inst.scratch.enableRegPairL()
        @X2clk2
        def _():
            inst.cpu.addr.setPL()

        # JUN, JMS
        opa = any
        for opr in [0b0100, 0b0101]:
            @X1clk1
            def _():
                inst.dcff = ~inst.dcff & 1
            @X2clk1
            def _():
                if not inst.dcff:
                    inst.data.v = inst.opa
            @X2clk2
            def _():
                if not inst.dcff:
                    inst.cpu.addr.setPH()

        # INC
        opr, opa = 0b0110, any
        @X21
        def _():
            inst.scratch.enableReg()
        @X2clk1
        def _():
            inst.cpu.alu.setADC(one=True)
        @X31
        def _():
            inst.cpu.alu.runAdder()
            inst.cpu.alu.enableAdd()
        @X3clk2
        def _():
            inst.scratch.setReg()    

        # ISZ
        opr, opa = 0b0111, any
        @X1clk1
        def _():
            inst.dcff = ~inst.dcff & 1
        @X21
        def _():
            if inst.dcff:
                inst.scratch.enableReg()
        @X2clk1
        def _():
            if inst.dcff:
                inst.cpu.alu.setADC(one=True)
        @X31
        def _():
            if inst.dcff:
                inst.cpu.alu.runAdder()
                inst.cpu.alu.enableAdd()
        @X3clk2
        def _():
            if inst.dcff:
                inst.scratch.setReg()
                # TODO fix timing here
                inst.cond = ~inst.scratch.regZero() & 1        

        # ADD
        opr, opa = 0b1000, any
        @X21
        def _():
            inst.scratch.enableReg()
        @X2clk1
        def _():
            inst.cpu.alu.setADA()
            inst.cpu.alu.setADC()
        @X31
        def _():
            inst.cpu.alu.runAdder(saveAcc=True, saveCy=True)

        # SUB
        opr, opa = 0b1001, any
        @X21
        def _():
            inst.scratch.enableReg()
        @X2clk1
        def _():
            inst.cpu.alu.setADA()
            inst.cpu.alu.setADC(invert=True)
        @X31
        def _():
            inst.cpu.alu.runAdder(invertADB=True, saveAcc=True, saveCy=True)

        # LD
        opr, opa = 0b1010, any
        @X21
        def _():
            inst.scratch.enableReg()
        @X31
        def _():
            inst.cpu.alu.runAdder(saveAcc=True)

        # XCH
        opr, opa = 0b1011, any
        @X21
        def _():
            inst.scratch.enableReg()
        @X31
        def _():
            inst.cpu.alu.runAdder(saveAcc=True)
            inst.cpu.alu.enableAccOut()
        @X3clk2
        def _():
            inst.scratch.setReg()

        # BBL
        opr, opa = 0b1100, any
        @X1clk1
        def _():
            inst.cpu.addr.decSP()
        @X2clk1
        def _():
            inst.data.v = inst.opa
        @X2clk2
        def _():
            inst.cpu.alu.acc = inst.data.v

        # LDM
        opr, opa = 0b1101, any
        @X21
        def _():
            inst.data.v = inst.opa
        @X31
        def _():
            inst.cpu.alu.runAdder(saveAcc=True)


        # RDM, RDR, RD0/1/2/3
        opr, opa = 0b1110, [0b1001, 0b1010, 0b1100, 0b1101, 0b1110, 0b1111]
        @A1clk1
        def _():
            inst.cpu.alu.runAdder(saveAcc=True)

        # WRM, WMP, WRR, WR0/1/2/3
        opr, opa = 0b1110, [0b0000, 0b0001, 0b0010, 0b0100, 0b0101, 0b0110, 0b0111]
        @X2clk1
        def _():
            inst.data.v = inst.cpu.alu.acc

        # ADM
        opr, opa = 0b1110, [0b1011]
        @X2clk2
        def _():
            inst.cpu.alu.setADA()
            inst.cpu.alu.setADC()
        @A1clk1
        def _():
            inst.cpu.alu.runAdder(saveAcc=True, saveCy=True)

        # SBM
        opr, opa = 0b1110, [0b1000]
        @X2clk2
        def _():
            inst.cpu.alu.setADA()
            inst.cpu.alu.setADC(invert=True)
        @A1clk1
        def _():
            inst.cpu.alu.runAdder(invertADB=True, saveAcc=True, saveCy=True)


        # CLB
        opr, opa = 0b1111, [0b0000]
        @X31
        def _():
            inst.cpu.alu.runAdder(saveAcc=True, saveCy=True)

        # CLC
        opr, opa = 0b1111, [0b0001]
        @X31
        def _():
            inst.cpu.alu.runAdder(saveCy=True)

        # IAC
        opr, opa = 0b1111, [0b0010]
        @X2clk1
        def _():
            inst.cpu.alu.setADA()
            inst.cpu.alu.setADC(one=True)
        @X31
        def _():
            inst.cpu.alu.runAdder(saveAcc=True, saveCy=True)

        # CMC
        opr, opa = 0b1111, [0b0011]
        @X2clk1
        def _():
            inst.cpu.alu.setADC(invert=True)
        @X31
        def _():
            inst.cpu.alu.runAdder(invertADB=True, saveCy=True)

        # CMA
        opr, opa = 0b1111, [0b0100]
        @X2clk1
        def _():
            inst.cpu.alu.setADA(invert=True)
        @X31
        def _():
            inst.cpu.alu.runAdder(saveAcc=True)

        # RAL
        opr, opa = 0b1111, [0b0101]
        @X2clk1
        def _():
            inst.cpu.alu.setADA()
        @X31
        def _():
            inst.cpu.alu.runAdder(shiftL=True)

        # RAR
        opr, opa = 0b1111, [0b0110]
        @X2clk1
        def _():
            inst.cpu.alu.setADA()
        @X31
        def _():
            inst.cpu.alu.runAdder(shiftR=True)
            
        # TCC
        opr, opa = 0b1111, [0b0111] 
        @X2clk1
        def _():
            inst.cpu.alu.setADC()
        @X31
        def _():
            inst.cpu.alu.runAdder(saveAcc=True, saveCy=True)

        # DAC
        opr, opa = 0b1111, [0b1000]
        @X2clk1
        def _():
            inst.cpu.alu.setADA()
        @X31
        def _():
            inst.cpu.alu.runAdder(saveAcc=True, saveCy=True)

        # TCS
        opr, opa = 0b1111, [0b1001]
        @X2clk1
        def _():
            inst.cpu.alu.setADC()
        @X31
        def _():
            inst.cpu.alu.runAdder(saveAcc=True, saveCy=True)

        # STC
        opr, opa = 0b1111, [0b1010]
        @X2clk1
        def _():
            inst.cpu.alu.setADC(one=True)
        @X31
        def _():
            inst.cpu.alu.runAdder(saveCy=True)

        # DAA
        opr, opa = 0b1111, [0b1011]
        @X2clk1
        def _():
            inst.cpu.alu.setADA()
        @X31
        def _():
            inst.cpu.alu.runAdder(saveAcc=True, saveCy=True)

        # KBP
        opr, opa = 0b1111, [0b1100]
        @X31
        def _():
            inst.cpu.alu.runAdder(saveAcc=True)

        # DCL
        opr, opa = 0b1111, [0b1101]
        @X21
        def _():
            inst.setRAMBank()