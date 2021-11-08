#include "TIMING.h"
#include "DATA.h"
#include "IO.h"
#include "INST.h"
#include "CONTROL.h"
#include "ADDR.h"
#include "SCRATCH.h"
#include "ALU.h"
#include "CLOCK.h"

// #define DEBUG

#define READ_RESET  PIND &   0b01000000
#define RESET_INPUT DDRD &= ~0b01000000

TIMING TIMING ;
DATA DATA ;

unsigned long max_dur = 0 ;


void reset(){  
  TIMING.reset() ;
  DATA.reset() ;
  INST_reset() ;
  CONTROL_reset() ;
  IO_reset() ;
  ADDR_reset() ;
  SCRATCH_reset() ;
  ALU_reset() ;
  CLOCK_reset() ;
  max_dur = 0 ;
}


void setup(){
  #ifdef DEBUG
    Serial.begin(2000000) ;
    Serial.println("4004") ;
  #endif
  RESET_INPUT ;

  INST_setup(&TIMING, &DATA) ;
  CONTROL_setup(&TIMING, &DATA) ;
  IO_setup(&TIMING) ;
  ADDR_setup(&TIMING, &DATA) ;
  SCRATCH_setup(&TIMING, &DATA) ;
  ALU_setup(&TIMING, &DATA) ;
  TIMING.setup() ;
  CLOCK_setup(&TIMING) ;
  reset() ;
}


void loop(){
  while (1){
    #ifdef DEBUG
      unsigned long start = micros() ;
    #endif
    if (READ_RESET){
      return reset() ;
    }

    CLOCK_tick() ;

    #ifdef DEBUG
      unsigned long dur = micros() - start ;
      if (dur > max_dur){
        max_dur = dur ;
        Serial.print("Max loop duration: ") ;
        Serial.print(max_dur) ;
        Serial.print("us ") ;
        Serial.print(INST_opr, HEX) ;
        Serial.print(INST_opa, HEX) ;
        Serial.print(" ") ;
        Serial.println(TIMING._cycle) ;
      }
    #endif
  }
}
