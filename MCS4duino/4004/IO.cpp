#include "IO.h"
#include "INST.h"

#define CM_ROM     A0
#define CM_RAM     A4
#define CM_ROM_ON  PORTC = PORTC |   0b00000001
#define CM_ROM_OFF PORTC = PORTC & (~0b00000001)
#define CM_RAM_ON  PORTC = PORTC |   0b00010000
#define CM_RAM_OFF PORTC = PORTC & (~0b00010000)

#define TEST      7

static bool IO_is_setup = 0 ;
static TIMING *timing ;


void IO_reset(){
  offCM() ;
}


void IO_setup(TIMING *t){
  IO_is_setup = 1 ;
  timing = t ;
  pinMode(CM_ROM, OUTPUT) ;
  pinMode(CM_RAM, OUTPUT) ; 
  IO_reset() ;
  IO_timing() ;
}


void IO_timing(){
  timing->A31([]{   // Turn on cm-rom and cm-ram for the 4001 and 4002 chips that are listening.
    onCM() ;
  }) ;
  
  timing->M21([]{
    if (io()){
      onCM() ;
    }
  }) ;

  auto f = []{
    offCM() ;
  } ;
  timing->M11(f) ;    // Turn on cm-rom and cm-ram for the 4001 and 4002 chips that are listening.
  timing->X11(f) ;
} ;


bool testZero(){
  return !digitalRead(TEST) ;
}


void onCM(){
  if (IO_is_setup){
    CM_ROM_ON ;
    CM_RAM_ON ;
  }
}


void offCM(){
  if (IO_is_setup){
    CM_ROM_OFF ;
    CM_RAM_OFF ;
  }
}
