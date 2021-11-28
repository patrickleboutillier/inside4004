#include "CLOCK.h"

#define CLK1      0b000010000   // PORTB
#define CLK2      0b000001000   // PORTB
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


void CLOCK_tick(){
  switch (n & 0b11){
    case 0:
      PORTB |= CLK1 ;
      timing->tick(1, 0) ;
      break ;
    case 1:
      PORTB &= ~CLK1 ;
      timing->tick(0, 0) ;
      break ;
    case 2:
      PORTB |= CLK2 ;
      timing->tick(0, 1) ;
      break ;
    default:
      PORTB &= ~CLK2 ;
      timing->tick(0, 0) ;      
  }
  n++ ; 
}


void CLOCK_sleep(unsigned int dur){
  int dly = CLK_US - dur ;
  if (dly > 0){
    delayMicroseconds(dly < CLK_US ? dly : CLK_US) ; 
  }
}
