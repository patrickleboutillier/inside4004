import chips.modules.timing as timing
from hdl import *


even = list(range(0, 16, 2))
odd = list(range(1, 16, 2))
any = list(range(16))

active_control = None
opr = 0
opa = []


def register(f, x, n):
     for i in opa:
        active_control.dispatch[opr][i][x][n] = f 

def A12(f):
    register(f, 0, 0)
    return f

def M12clk2(f):
    register(f, 3, 2)
    return f

def M22clk2(f):
    register(f, 4, 2)
    return f

def X12clk1(f):
    register(f, 5, 0)
    return f

def X12clk2(f):
    register(f, 5, 2)
    return f

def X21(f):
    register(f, 5, 3)
    return f

def X22clk1(f):
    register(f, 6, 0)
    return f

def X22clk2(f):
    register(f, 6, 2)
    return f

def X31(f):
    register(f, 6, 3)
    return f

def X32clk1(f):
    register(f, 7, 0)
    return f

def X32clk2(f):
    register(f, 7, 2)
    return f


class control:
    def __init__(self, inst):
        global active_control
        active_control = self

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

        def dispatch(x, n):
            f = self.dispatch[self.inst.opr][self.inst.opa][x][n]
            if f is not None:
                f()

        @timing.A12
        def _():
            dispatch(0, 0)

        @timing.M12clk2
        def _():
            dispatch(3, 2)

        @timing.M22clk2
        def _():
            dispatch(4, 2)

        @timing.X12clk1
        def _():
            dispatch(5, 0)

        @timing.X12clk2
        def _():
            dispatch(5, 2)

        @timing.X21
        def _():
            dispatch(5, 3)

        @timing.X22clk1
        def _():
            dispatch(6, 0)

        @timing.X22clk2
        def _():
            dispatch(6, 2)

        @timing.X31
        def _():
            dispatch(6, 3)

        @timing.X32clk1
        def _():
            dispatch(7, 0)

        @timing.X32clk2
        def _():
            dispatch(7, 2)


###############################################################################


    def register(_):
        global opr, opa
        inst = _.inst 

        # NOP
        opr, opa = 0b0000, [0b0000]
        @X12clk1
        def _():
            pass

        # HLT
        opr, opa = 0b0000, [0b0001]
        @X12clk1
        def _():
            print("HALTED!")
            sys.exit()

        # ERR
        opr, opa = 0b0000, [0b0010]
        @X12clk1
        def _():
            sys.exit("ERROR!")

        # JCN
        opr, opa = 0b0001, any
        @M12clk2 
        def _():
            if not inst.sc:
                inst.cpu.addr.setPM()
        @M22clk2 
        def _():
            if not inst.sc:
                inst.cpu.addr.setPL()

        # FIM
        opr, opa = 0b0010, even
        @M12clk2 
        def _():
            if not inst.sc:
                inst.cpu.scratch.setRegPairH()
        @M22clk2 
        def _():
            if not inst.sc:
                inst.cpu.scratch.setRegPairL()

        # SRC
        opr, opa = 0b0010, odd
        @X21
        def _():
            inst.cpu.scratch.enableRegPairH()
            inst.cm_rom.v = 1
            inst.cm_ram.v(inst.ram_bank)
        @X31
        def _():
            inst.cpu.scratch.enableRegPairL()
            inst.cm_rom.v = 0
            inst.cm_ram.v(0)

        # FIN
        opr, opa = 0b0011, even
        @M12clk2 
        def _():
            if not inst.sc:
                inst.cpu.scratch.setRegPairH()
        @M22clk2 
        def _():
            if not inst.sc:
                inst.cpu.scratch.setRegPairL()
        @X21
        def _():
            if inst.sc:
                inst.cpu.scratch.enableRegPairH()
        @X22clk2
        def _():
            if inst.sc:
                inst.cpu.addr.setPM()
        @X31
        def _():
            if inst.sc:
                inst.cpu.scratch.enableRegPairL()
        @X32clk2
        def _():
            if inst.sc:
                inst.cpu.addr.setPL()

        # JIN
        opr, opa = 0b0011, odd
        @X21
        def _():
            inst.cpu.scratch.enableRegPairH()
        @X22clk2
        def _():
            inst.cpu.addr.setPM()
        @X31
        def _():
            inst.cpu.scratch.enableRegPairL()
        @X32clk2
        def _():
            inst.cpu.addr.setPL()

        # JUN
        opr, opa = 0b0100, any
        @M12clk2 
        def _():
            if not inst.sc:
                inst.cpu.addr.setPM()
        @M22clk2 
        def _():
            if not inst.sc:
                inst.cpu.addr.setPL()
        @X21
        def _():
            if not inst.sc:
                inst.data.v = inst.opa
        @X22clk2
        def _():
            if not inst.sc:
                inst.cpu.addr.setPH()

        # JMS
        opr, opa = 0b0101, any 
        @M12clk2 
        def _():
            if not inst.sc:
                inst.cpu.addr.setPM()
        @M22clk2 
        def _():
            if not inst.sc:
                # Order not important here since sp in not copied to row_num until x32
                inst.cpu.addr.setPL()
                inst.cpu.addr.decSP()
        @X21
        def _():
            if not inst.sc:
                inst.data.v = inst.opa
        @X22clk2
        def _():
            if not inst.sc:
                inst.cpu.addr.setPH()

        # INC
        opr, opa = 0b0110, any
        @X21
        def _():
            inst.cpu.scratch.enableReg()
        @X22clk1
        def _():
            inst.cpu.alu.setADC(one=True)
        @X31
        def _():
            inst.cpu.alu.runAdder()
            inst.cpu.alu.enableAdd()
        @X32clk2
        def _():
            inst.cpu.scratch.setReg()    

        # ISZ
        opr, opa = 0b0111, any
        @M12clk2 
        def _():
            if not inst.sc:
                inst.cpu.addr.setPM()
        @M22clk2 
        def _():
            if not inst.sc:
                inst.cpu.addr.setPL()
        @X21
        def _():
            if inst.sc:
                inst.cpu.scratch.enableReg()
        @X22clk1
        def _():
            if inst.sc:
                inst.cpu.alu.setADC(one=True)
        @X31
        def _():
            if inst.sc:
                inst.cpu.alu.runAdder()
                inst.cpu.alu.enableAdd()
        @X32clk2
        def _():
            if inst.sc:
                inst.cpu.scratch.setReg()     

        # ADD
        opr, opa = 0b1000, any
        @X21
        def _():
            inst.cpu.scratch.enableReg()
        @X22clk1
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
            inst.cpu.scratch.enableReg()
        @X22clk1
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
            inst.cpu.scratch.enableReg()
        @X31
        def _():
            inst.cpu.alu.runAdder(saveAcc=True)

        # XCH
        opr, opa = 0b1011, any
        @X21
        def _():
            inst.cpu.scratch.enableReg()
        @X31
        def _():
            inst.cpu.alu.runAdder(saveAcc=True)
            inst.cpu.alu.enableAccOut()
        @X32clk2
        def _():
            inst.cpu.scratch.setReg()

        # BBL
        opr, opa = 0b1100, any
        @M22clk2
        @X12clk2
        @X22clk2
        def _():
            inst.cpu.addr.decSP()
        @X21
        def _():
            inst.data.v = inst.opa
        @X31
        def _():
            inst.cpu.alu.runAdder(saveAcc=True)

        # LDM
        opr, opa = 0b1101, any
        @X21
        def _():
            inst.data.v = inst.opa
        @X31
        def _():
            inst.cpu.alu.runAdder(saveAcc=True)


        # WRM, WMP, WRR, WR0/1/2/3
        opr, opa = 0b1110, [0b0000, 0b0001, 0b0010, 0b0100, 0b0101, 0b0110, 0b0111]
        @X22clk1
        def _():
            inst.data.v = inst.cpu.alu.acc

        # SBM
        opr, opa = 0b1110, [0b1000]
        @X22clk2
        def _():
            inst.cpu.alu.setADA()
            inst.cpu.alu.setADC(invert=True)
        @A12
        def _():
            inst.cpu.alu.runAdder(invertADB=True, saveAcc=True, saveCy=True)

        # RDM, RDR, RD0/1/2/3
        opr, opa = 0b1110, [0b1001, 0b1010, 0b1100, 0b1101, 0b1110, 0b1111]
        @A12
        def _():
            inst.cpu.alu.runAdder(saveAcc=True)

        # ADM
        opr, opa = 0b1110, [0b1011]
        @X22clk2
        def _():
            inst.cpu.alu.setADA()
            inst.cpu.alu.setADC()
        @A12
        def _():
            inst.cpu.alu.runAdder(saveAcc=True, saveCy=True)


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
        @X22clk1
        def _():
            inst.cpu.alu.setADA()
            inst.cpu.alu.setADC(one=True)
        @X31
        def _():
            inst.cpu.alu.runAdder(saveAcc=True, saveCy=True)

        # CMC
        opr, opa = 0b1111, [0b0011]
        @X22clk1
        def _():
            inst.cpu.alu.setADC(invert=True)
        @X31
        def _():
            inst.cpu.alu.runAdder(invertADB=True, saveCy=True)

        # CMA
        opr, opa = 0b1111, [0b0100]
        @X22clk1
        def _():
            inst.cpu.alu.setADA(invert=True)
        @X31
        def _():
            inst.cpu.alu.runAdder(saveAcc=True)

        # RAL
        opr, opa = 0b1111, [0b0101]
        @X22clk1
        def _():
            inst.cpu.alu.setADA()
        @X31
        def _():
            inst.cpu.alu.runAdder(shiftL=True)

        # RAR
        opr, opa = 0b1111, [0b0110]
        @X22clk1
        def _():
            inst.cpu.alu.setADA()
        @X31
        def _():
            inst.cpu.alu.runAdder(shiftR=True)
            
        # TCC
        opr, opa = 0b1111, [0b0111] 
        @X22clk1
        def _():
            inst.cpu.alu.setADC()
        @X31
        def _():
            inst.cpu.alu.runAdder(saveAcc=True, saveCy=True)

        # DAC
        opr, opa = 0b1111, [0b1000]
        @X22clk1
        def _():
            inst.cpu.alu.setADA()
        @X31
        def _():
            inst.cpu.alu.runAdder(saveAcc=True, saveCy=True)

        # TCS
        opr, opa = 0b1111, [0b1001]
        @X22clk1
        def _():
            inst.cpu.alu.setADC()
        @X31
        def _():
            inst.cpu.alu.runAdder(saveAcc=True, saveCy=True)

        # STC
        opr, opa = 0b1111, [0b1010]
        @X22clk1
        def _():
            inst.cpu.alu.setADC(one=True)
        @X31
        def _():
            inst.cpu.alu.runAdder(saveCy=True)

        # DAA
        opr, opa = 0b1111, [0b1011]
        @X22clk1
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


