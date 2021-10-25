#include "CLOCK.h"

#define MIN_CLK_US  100 

static TIMING *timing ;
static unsigned long n = 0 ;


void CLOCK_reset(){
  n = 0 ;
}


void CLOCK_setup(TIMING *t){
  timing = t ;
  CLOCK_reset() ;
}


void tick(int nb){
  for (int i = 0 ; i < nb ; i++){
    unsigned long start = micros() ;
    if (n == 0){
      timing->tick(1, 0) ;
    }
    else if (n == 1){
      timing->tick(0, 0) ;
    }
    else if (n == 2){
      timing->tick(0, 1) ;
    }
    else { // n == 3
      timing->tick(0, 0) ;
    }
    n = (n + 1) & 0b11 ;

    unsigned long diff = micros() - start ;
    if (diff < MIN_CLK_US){
      delayMicroseconds(MIN_CLK_US - diff) ;
    }
  }
}
