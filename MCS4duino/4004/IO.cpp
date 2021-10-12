#include "IO.h"
#include "INST.h"
#include "PINS.h"

static bool IO_is_setup = 0 ;
static TIMING *timing ;


void IO_reset(){
  CM(LOW) ;
}


void IO_setup(TIMING *t){
  IO_is_setup = 1 ;
  timing = t ;
  pinMode(CM_ROM, OUTPUT) ;
  //pinMode(CM_RAM, OUTPUT) ; 
  IO_reset() ;
  IO_timing() ;
}


void IO_timing(){
  timing->A31([]{   // Turn on cm-rom and cm-ram for the 4001 and 4002 chips that are listening.
    CM(HIGH) ;
  }) ;
  
  timing->M21([]{
    if (io()){
      CM(HIGH) ;
    }
  }) ;

  auto f = []{
    CM(LOW) ;
  } ;
  timing->M11(f) ;    // Turn on cm-rom and cm-ram for the 4001 and 4002 chips that are listening.
  timing->X11(f) ;
} ;


void CM(bool v){
  if (IO_is_setup){
    digitalWrite(CM_ROM, v) ;
    //digitalWrite(CM_RAM, v) ;    
  }
}


bool testZero(){
  return !digitalRead(TEST) ;
}
