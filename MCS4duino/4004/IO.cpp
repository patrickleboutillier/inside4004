#include "IO.h"
#include "INST.h"


static TIMING *timing ;


void IO_reset(){
  CMoff() ;
}


void IO_setup(TIMING *t){
  timing = t ;
  CM_ROM_OUTPUT ;
  CM_RAM_OUTPUT ; 
  TEST_INPUT ;
  IO_reset() ;
  IO_timing() ;
}


void IO_timing(){
  timing->A31([]{   // Turn on cm-rom and cm-ram for the 4001 and 4002 chips that are listening.
    CMon() ;
  }) ;
  
  timing->M21([]{
    if (io()){
      CMon() ;
    }
  }) ;

  auto f = []{
    CMoff() ;
  } ;
  timing->M11(f) ;    // Turn on cm-rom and cm-ram for the 4001 and 4002 chips that are listening.
  timing->X11(f) ;
} ;
