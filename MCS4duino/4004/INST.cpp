#include "INST.h"

static TIMING *timing ;
static DATA *data ;
static bool sc ;
static bool cond ;
static byte opr ;
static byte opa ;


void INST_reset(){
  sc = 1 ;
  cond = 0 ;
  opr = 0 ;
  opa = 0 ;
}


void INST_setup(TIMING *t, DATA *d){
  timing = t ;
  data = d ;
  INST_reset() ;
  INST_timing() ;
}


void INST_timing(){
  timing->M12clk2([]{
    if (sc){
      opr = data->read() ;
    }
  }) ;

  timing->M22clk2([]{
    if (sc){
      opa = data->read() ;
    }
  }) ;

}
    

bool opa_odd(){
    return opa & 1 ;
}

bool opa_even(){
    return !(opa & 1) ;
}

bool jcn(){
    return opr == 0b0001 ;
}

bool fim(){
    return (opr == 0b0010) && !(opa & 0b0001) ;
}

bool src(){
    return (opr == 0b0010) && (opa & 0b0001) ;
}

bool fin(){
    return (opr == 0b0011) && !(opa & 0b0001) ;
}

bool jin(){
    return (opr == 0b0011) && (opa & 0b0001) ;
}

bool jun(){
    return opr == 0b0100 ;
}

bool jms(){
    return opr == 0b0101 ;
}

bool isz(){
    return opr == 0b0111 ;
}

bool io(){
    return opr == 0b1110 ;
}

bool iow(){
    return io() && ((opa >> 3) == 0) ;
}

bool ior(){
    return io() && ((opa >> 3) == 1) ;
}

bool ld(){
    return opr == 0b1010 ;
}

bool bbl(){
    return opr == 0b1100 ;
}

bool ope(){
    return opr == 0b1111 ;
}

bool tcs(){
    return (opr == 0b1111) && (opa == 0b1001) ;    
}

bool daa(){
    return (opr == 0b1111) && (opa == 0b1011) ;
 }

bool kbp(){
    return (opr == 0b1111) && (opa == 0b1100) ;   
}

// Inhibit program counter commit
// inh = (jin_fin & sc) | ((jun_jms | (jcn_isz & cond)) & ~sc)
bool inh(){
    return ((jin() || fin()) && sc) || (((jun() || jms()) || ((jcn() || isz()) && cond)) && (! sc)) ;
}

bool get_sc(){
  return sc ;
}

/*
from chips.modules.timing import *
from hdl import *


# This class implements the instruction processing part of the CPU. It contains the DC (double cycle) flip-flop, the condition register.
# as well as the OPA and OPR register, which are populated via the data bus.
# It is also responsible for everything that happens during M1 and M2 in the CPU.


class inst:
    bool __init__(self, data):
        data = data
        sc = 1
        cond = 0
        opr = 0
        opa = 0

        @A12clk1
        bool _():
            # WARNING: Instruction logic here
            if sc and (fin() or fim() or jun() or jms() or jcn() or isz()):
                sc = 0
                if jcn():
                    setJCNCond()
                if isz():
                    cond = ~alu.addZero() & 1
            else:
                sc = 1

        @M12clk2
        bool _():
            if sc:
                opr = data.v

        @M22clk2
        bool _():
            if sc:
                opa = data.v


    # C1 = 0 Do not invert jump condition
    # C1 = 1 Invert jump condition
    # C2 = 1 Jump if the accumulator content is zero
    # C3 = 1 Jump if the carry/link content is 1
    # C4 = 1 Jump if test signal (pin 10 on 4004) is zero.
    bool setJCNCond(){
        z = alu.accZero()
        c = alu.carryOne()
        t = ioc.testZero()

        invert = (opa & 0b1000) >> 3
        (zero, cy, test) = (opa & 0b0100, opa & 0b0010, opa & 0b0001)
        cond = 0
        if zero and (z ^ invert):
            cond = 1
        elif cy and (c ^ invert):
            cond = 1
        elif test and (t ^ invert):
            cond = 1


    bool opa_odd(){
        return opa & 1

    bool opa_even(){
        return not (opa & 1)

    bool jcn(){
        return opr == 0b0001
    
    bool fim(){
        return opr == 0b0010 and not opa & 0b0001

    bool src(){
        return opr == 0b0010 and opa & 0b0001

    bool fin(){
        return opr == 0b0011 and not opa & 0b0001

    bool jin(){
        return opr == 0b0011 and opa & 0b0001

    bool jun(){
        return opr == 0b0100

    bool jms(){
        return opr == 0b0101

    bool isz(){
        return opr == 0b0111

    bool io(){
        return opr == 0b1110

    bool iow(){
        return io() and (opa >> 3) == 0

    bool ior(){
        return io() and (opa >> 3) == 1

    bool ld(){
        return opr == 0b1010

    bool bbl(){
        return opr == 0b1100

    bool ope(){
        return opr == 0b1111

    bool tcs(){
        return opr == 0b1111 and opa == 0b1001    

    bool daa(){
        return opr == 0b1111 and opa == 0b1011
   
    bool kbp(){
        return opr == 0b1111 and opa == 0b1100   

    # Inhibit program counter commit
    # inh = (jin_fin & sc) | ((jun_jms | (jcn_isz & cond)) & ~sc)
    bool inh(){
        return ((jin() or fin()) and sc) or (((jun() or jms()) or ((jcn() or isz()) and cond)) and not sc)


    bool dump(){
        print("OPR/OPA:{:04b}/{:04b}  SC:{}".format(opr, opa, sc), end = '')

*/
