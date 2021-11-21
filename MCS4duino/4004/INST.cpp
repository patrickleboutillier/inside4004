#include "INST.h"
#include "IO.h"
#include "ALU.h"
#include "ADDR.h"


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
  INST_reset() ;
  INST_timing() ;
}


void INST_timing(){
  timing->A12clk1([]{
    // WARNING: Instruction logic here
    if (INST_sc && (fin() || fim() || jun() || jms() || jcn() || isz())){
      INST_sc = 0 ;
    }
    else {
      INST_sc = 1 ;
    }

    if (! INST_sc){
      if (jcn()){
        byte cond = setJCNcond() ;
        INST_cond = cond ;
      }
      if (isz()){
        byte cond = ~addZero() & 1 ;
        INST_cond = cond ;
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
      //Serial.print(getPC(), HEX) ;
      //Serial.print(":") ;
      //Serial.print(INST_opr, HEX) ;
      //Serial.println(INST_opa, HEX) ;
    }
  }) ;
}


// C1 = 0 Do not invert jump INST_condition
// C1 = 1 Invert jump INST_condition
// C2 = 1 Jump if the accumulator content is zero
// C3 = 1 Jump if the carry/link content is 1
// C4 = 1 Jump if test signal (pin 10 on 4004) is zero.
bool setJCNcond(){
  bool z = accZero() ;
  bool c = carryOne() ;
  bool t = testZero() ;
  
  bool invert = (INST_opa & 0b1000) >> 3 ;
  byte zero = INST_opa & 0b0100 ;
  byte cy = INST_opa & 0b0010 ;
  byte test = INST_opa & 0b0001 ;
  bool cond = 0 ;
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
