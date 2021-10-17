#include "INST.h"
#include "IO.h"

#define COND    A2 

static TIMING *timing ;
static DATA *data ;
bool INST_sc ;
bool INST_cond ;
byte INST_opr ;
byte INST_opa ;


void INST_reset(){
  INST_sc = 1 ;
  INST_cond = 0 ;
  INST_opr = 0 ;
  INST_opa = 0 ;
}


void INST_setup(TIMING *t, DATA *d){
  timing = t ;
  data = d ;
  pinMode(COND, INPUT) ;
  INST_reset() ;
  INST_timing() ;
}


void INST_timing(){
  timing->A12clk1([]{
    // WARNING: Instruction logic here
    if (timing->_pass == 0){
      if (INST_sc && (fin() || fim() || jun() || jms() || jcn() || isz())){
        INST_sc = 0 ;
      }
      else {
        INST_sc = 1 ;
      }
    }

    if (! INST_sc){
      if (jcn()){
        INST_cond = digitalRead(COND) ;
        // INST_cond = setJCNcond() ;
      }
      if (isz()){
        INST_cond = digitalRead(COND) ;
        // INST_cond = ~alu.addZero() & 1
      }
    }
  }) ;
  
  timing->M12clk2([]{
    if (INST_sc){
      INST_opr = data->read() ;
    }
  }) ;

  timing->M22clk2([]{
    if (INST_sc){
      INST_opa = data->read() ;
    }
  }) ;
}


// C1 = 0 Do not invert jump INST_condition
// C1 = 1 Invert jump INST_condition
// C2 = 1 Jump if the accumulator content is zero
// C3 = 1 Jump if the carry/link content is 1
// C4 = 1 Jump if test signal (pin 10 on 4004) is zero.
byte setJCNcond(){
  bool z = 0 ; // alu.accZero() ;
  bool c = 0 ; // alu.carryOne() ;
  bool t = testZero() ;

  bool invert = (INST_opa & 0b1000) >> 3 ;
  byte zero = INST_opa & 0b0100 ;
  byte cy = INST_opa & 0b0010 ;
  byte test = INST_opa & 0b0001 ;
  byte cond = 0 ;
  if (zero && (z ^ invert)){
      cond = 1 ;
  }
  else if (cy && (c ^ invert)){
      cond = 1 ;
  }
  else if (test && (t ^ invert)){
      cond = 1 ;
  }

  return cond ;
}







/*
from chips.modules.timing import *
from hdl import *


# This class implements the instruction processing part of the CPU. It contains the DC (double cycle) flip-flop, the INST_condition register.
# as well as the INST_opa and INST_opr register, which are populated via the data bus.
# It is also responsible for everything that happens during M1 and M2 in the CPU.


class inst:
    bool __init__(self, data):
        data = data
        INST_sc = 1
        INST_cond = 0
        INST_opr = 0
        INST_opa = 0

        @A12clk1
        bool _():
            # WARNING: Instruction logic here
            if INST_sc and (fin() or fim() or jun() or jms() or jcn() or isz()):
                INST_sc = 0
                if jcn():
                    setJCNINST_cond()
                if isz():
                    INST_cond = ~alu.addZero() & 1
            else:
                INST_sc = 1

        @M12clk2
        bool _():
            if INST_sc:
                INST_opr = data.v

        @M22clk2
        bool _():
            if INST_sc:
                INST_opa = data.v


    # C1 = 0 Do not invert jump INST_condition
    # C1 = 1 Invert jump INST_condition
    # C2 = 1 Jump if the accumulator content is zero
    # C3 = 1 Jump if the carry/link content is 1
    # C4 = 1 Jump if test signal (pin 10 on 4004) is zero.
    bool setJCNINST_cond(){
        z = alu.accZero()
        c = alu.carryOne()
        t = ioc.testZero()

        invert = (INST_opa & 0b1000) >> 3
        (zero, cy, test) = (INST_opa & 0b0100, INST_opa & 0b0010, INST_opa & 0b0001)
        INST_cond = 0
        if zero and (z ^ invert):
            INST_cond = 1
        elif cy and (c ^ invert):
            INST_cond = 1
        elif test and (t ^ invert):
            INST_cond = 1

*/
