#include "CLOCK.h"

#define CLK1      0b00010000   // PORTB
#define CLK2      0b00001000   // PORTB
#define CLK_US    36


static TIMING *timing ;
static unsigned long n = 0 ;


void CLOCK_reset(){
  n = 0 ;
  PORTB &= ~(CLK1 | CLK2) ;
}


void CLOCK_setup(TIMING *t){
  timing = t ; 
  DDRB |= (CLK1 | CLK2) ; 
  CLOCK_reset() ;
}


void CLOCK_period(){
  unsigned long start = micros() ;
  timing->tick0() ;
  PORTB |= CLK1 ;
  timing->tick_dispatch() ;
  CLOCK_sleep(micros() - start) ;

  start = micros() ;
  timing->tick1() ;
  PORTB &= ~CLK1 ;
  timing->tick_dispatch() ;
  CLOCK_sleep(micros() - start) ;

  start = micros() ;
  timing->tick2() ;
  PORTB |= CLK2 ;
  timing->tick_dispatch() ;
  CLOCK_sleep(micros() - start) ;

  start = micros() ;
  timing->tick3() ;
  PORTB &= ~CLK2 ;
  if (timing->_slave == 6){
    timing->sync(1) ;
  }
  if (timing->_slave == 7){
    timing->sync(0) ;            
  }
  timing->tick_dispatch() ;
  CLOCK_sleep(micros() - start) ;
}


void CLOCK_sleep(unsigned int dur){
  int dly = CLK_US - dur ;
  if (dly > 0){
    delayMicroseconds(dly < CLK_US ? dly : CLK_US) ; 
  }
}
