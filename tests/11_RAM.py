from asm import *

# See "'P1' button" in http://e4004.szyc.org/emu/

def fill_ram():
    JMS('init')
    LABEL('floop1')
    SRC(p0)
    WRM() ; IAC()
    ISZ(r1, 'floop1')
    INC(r0)
    ISZ(r2, 'floop1')

    JMS('init')
    LABEL('floop2')
    SRC(p0)
    WR0() ; IAC() ; WR1() ; IAC() ; WR2() ; IAC() ; WR3() ; IAC() ;
    INC(r0)
    ISZ(r2, 'floop2')

def test_ram():
    JMS('init')
    LABEL('tloop1')
    SRC(p0)
    RDM() ; XCH(r14) ; JMS('assert:r14_eq_r15') ; INC(r15)
    ISZ(r1, 'tloop1')
    INC(r0)
    ISZ(r2, 'tloop1')

    JMS('init')
    LABEL('tloop2')
    SRC(p0)
    RD0() ; XCH(r14) ; JMS('assert:r14_eq_r15') ; INC(r15)
    RD1() ; XCH(r14) ; JMS('assert:r14_eq_r15') ; INC(r15)
    RD2() ; XCH(r14) ; JMS('assert:r14_eq_r15') ; INC(r15)
    RD3() ; XCH(r14) ; JMS('assert:r14_eq_r15') ; INC(r15)
    INC(r0)
    ISZ(r2, 'tloop2')


fill_ram()
test_ram()
HLT()


LABEL('init')
FIM(p0, 0)
FIM(p1, 0)
FIM(p7, 0)
LDM(12)
XCH(r2)
BBL(0)


from tests import *