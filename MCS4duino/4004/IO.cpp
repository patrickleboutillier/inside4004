#include "IO.h"
#include "INST.h"
#include "PINS.h"

static TIMING *timing ;


void IO_reset(){
  digitalWrite(CM_ROM, LOW) ;
  digitalWrite(CM_RAM, LOW) ;
}


void IO_setup(TIMING *t){
  timing = t ;
  pinMode(CM_ROM, OUTPUT) ;
  pinMode(CM_RAM, OUTPUT) ; 
  IO_reset() ;
  IO_timing() ;
}


void IO_timing(){
  timing->A31([]{   // Turn on cm-rom and cm-ram for the 4001 and 4002 chips that are listening.
    digitalWrite(CM_ROM, HIGH) ;
    digitalWrite(CM_RAM, HIGH) ;
  }) ;
  
  timing->M21([]{
    if (io()){
      digitalWrite(CM_ROM, HIGH) ;
      digitalWrite(CM_RAM, HIGH) ;
    }
  }) ;

  auto f = []{
    digitalWrite(CM_ROM, LOW) ;
    digitalWrite(CM_RAM, LOW) ;  
  } ;
  timing->M11(f) ;    // Turn on cm-rom and cm-ram for the 4001 and 4002 chips that are listening.
  timing->X11(f) ;
} ;


bool testZero(){
  return !digitalRead(TEST) ;
}
