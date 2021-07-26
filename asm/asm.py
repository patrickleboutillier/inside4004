# A simple DSL assembler for the Intel 4004.

class reg:
    def __init__(self, id):
        self.id = id
    
class regp:
    def __init__(self, pid):
        self.pid = pid << 1


r0, r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14, r15 = map(reg, range(16))
p0, p1, p2, p3, p4, p5, p6, p7 = map(regp, range(8))


_insts = []
_labels = {}
_pc = 0
_err = False

def _done():
    global _pca
    if _err:
        return
    _pc = 0
    for (opr, opa, addr, desc) in _insts:
        if opr is None and opa is None and addr is None: # Label
            print("        \t# --@0d{:04}: Label '{}'".format(_pc, desc))
        else:
            if addr is not None:    # resolve labels if present
                label = ''
                if type(addr) is str:
                    label = addr + '@'
                    addr = _labels[addr]
            if opr is None and opa is None:
                opr = (addr >> 4) & 0xF
                opa = addr & 0xF
            elif addr is not None:
                desc += " {}{}".format(label, addr)
            if opa is None:
                opa = addr >> 8
            inst = opr << 4 | opa
            print("{:08b}\t# 0x{:02x}@0d{:04}: {}".format(inst, inst, _pc, desc))
            _pc += 1

def _grow_insts():
    if _pc >= len(_insts):
        for i in range(len(_insts), _pc+1):
            _insts.append((0b0000, 0b0000, None, "NOP"))

def _add_inst(opr, opa, addr, desc):
    global _pc
    if opr is None and opa is None and addr is None:    # Label definition
        _labels[desc] = _pc - len(_labels)
    _grow_insts()
    _insts[_pc] = (opr, opa, addr, desc)
    _pc += 1
    if addr is not None:
        _grow_insts()
        _insts[_pc] = (None, None, addr, "...")
        _pc += 1


def LABEL(str):
    _add_inst(None, None, None, str)

# Set PC to the specified value
def PC(addr = -1):
    global _pc
    if addr >= 0:
        addr += len(_labels)
        _pc = addr
    return _pc - len(_labels)

# Insert a byte of data in the code at PC 
def BYTE(data):
    _add_inst(data >> 4, data & 0xF, None, "BYTE 0d{:03}".format(data))

def NOP():
    _add_inst(0b0000, 0b0000, None, "NOP")

def HLT():
    _add_inst(0b0000, 0b0001, None, "HLT")

def ERR():
    _add_inst(0b0000, 0b0010, None, "ERR")


def JCN(cond, addr):
    _add_inst(0b0001, cond, addr, "JCN 0b{:04b},".format(cond))

def FIM(regp, data):
    _add_inst(0b0010, regp.pid, data, "FIM p{},".format(regp.pid))

def SRC(regp):
    _add_inst(0b0010, regp.pid | 0x1, None, "SRC p{}".format(regp.pid))
 
def FIN(regp):
    _add_inst(0b0011, regp.pid, None, "FIN p{}".format(regp.pid))

def JIN(regp):
    _add_inst(0b0011, regp.pid | 0x1, None, "JIN p{}".format(regp.pid))

def JUN(addr):
    _add_inst(0b0100, None, addr, "JUN")

def JMS(addr):
    _add_inst(0b0101, None, addr, "JMS")

def INC(reg):
    _add_inst(0b0110, reg.id, None, "INC r{}".format(reg.id))

def ISZ(reg, addr):
    _add_inst(0b0111, reg.id, addr, "ISZ r{},".format(reg.id))

def ADD(reg):
    _add_inst(0b1000, reg.id, None, "ADD r{}".format(reg.id))

def SUB(reg):
    _add_inst(0b1001, reg.id, None, "SUB r{}".format(reg.id))

def LD(reg):
    _add_inst(0b1010, reg.id, None, "LD r{}".format(reg.id))

def XCH(reg):
    _add_inst(0b1011, reg.id, None, "XCH r{}".format(reg.id))

def BBL(data):
    _add_inst(0b1100, data, None, "BBL 0b{:04b} ({})".format(data, data))

def LDM(data):
    _add_inst(0b1101, data, None, "LDM 0b{:04b} ({})".format(data, data))


def WRM():
    _add_inst(0b1110, 0b0000, None, "WRM")

def WMP():
    _add_inst(0b1110, 0b0001, None, "WMP")

def WRR():
    _add_inst(0b1110, 0b0010, None, "WRR")

def WR0():
    _add_inst(0b1110, 0b0100, None, "WR0")

def WR1():
    _add_inst(0b1110, 0b0101, None, "WR1")

def WR2():
    _add_inst(0b1110, 0b0110, None, "WR2")

def WR3():
    _add_inst(0b1110, 0b0111, None, "WR3")

def SBM():
    _add_inst(0b1110, 0b1000, None, "SBM")

def RDM():
    _add_inst(0b1110, 0b1001, None, "RDM")

def RDR():
    _add_inst(0b1110, 0b1010, None, "RDR")

def ADM():
    _add_inst(0b1110, 0b1011, None, "ADM")

def RD0():
    _add_inst(0b1110, 0b1100, None, "RD0")

def RD1():
    _add_inst(0b1110, 0b1101, None, "RD1")

def RD2():
    _add_inst(0b1110, 0b1110, None, "RD2")

def RD3():
    _add_inst(0b1110, 0b1111, None, "RD3")


def CLB():
    _add_inst(0b1111, 0b0000, None, "CLB")

def CLC():
    _add_inst(0b1111, 0b0001, None, "CLC")

def IAC():
    _add_inst(0b1111, 0b0010, None, "IAC")

def CMC():
    _add_inst(0b1111, 0b0011, None, "CMC")

def CMA():
    _add_inst(0b1111, 0b0100, None, "CMA")

def RAL():
    _add_inst(0b1111, 0b0101, None, "RAL")

def RAR():
    _add_inst(0b1111, 0b0110, None, "RAR")

def TCC():
    _add_inst(0b1111, 0b0111, None, "TCC")

def DAC():
    _add_inst(0b1111, 0b1000, None, "DAC")

def TCS():
    _add_inst(0b1111, 0b1001, None, "TCS")

def STC():
    _add_inst(0b1111, 0b1010, None, "STC")

def DAA():
    _add_inst(0b1111, 0b1011, None, "DAA")

def KBP():
    _add_inst(0b1111, 0b1100, None, "KBP")

def DCL():
    _add_inst(0b1111, 0b1101, None, "DCL")
