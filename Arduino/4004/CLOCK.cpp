#include "CLOCK.h"

#define CLK1      0b00010000   // PORTB
#define CLK2      0b00001000   // PORTB
#define CLK_US    36
const unsigned int CLK_CYCLES = CLK_US * 16 ; 


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
  noInterrupts() ;
  TCNT1 = 0 ;
  TCCR1B = 1 ;
  timing->tick0() ;
  PORTB |= CLK1 ;
  timing->tick_dispatch() ;
  TCCR1B = 0 ; 
  interrupts() ;
  CLOCK_delay(TCNT1) ;
  
  noInterrupts() ;
  TCNT1 = 0 ;
  TCCR1B = 1 ;
  timing->tick1() ;
  PORTB &= ~CLK1 ;
  timing->tick_dispatch() ;
  TCCR1B = 0 ;
  interrupts() ;
  CLOCK_delay(TCNT1) ;

  noInterrupts() ;
  TCNT1 = 0 ;
  TCCR1B = 1 ;
  timing->tick2() ;
  PORTB |= CLK2 ;
  timing->tick_dispatch() ;
  TCCR1B = 0 ;
  interrupts() ;
  CLOCK_delay(TCNT1) ;

  noInterrupts() ;
  TCNT1 = 0 ;
  TCCR1B = 1 ;
  timing->tick3() ;
  PORTB &= ~CLK2 ;
  timing->sync() ;
  timing->tick_dispatch() ;
  TCCR1B = 0 ;
  interrupts() ;
  CLOCK_delay(TCNT1) ;
}


unsigned int CLOCK_delay(unsigned int cycles){
  int target = CLK_CYCLES - cycles ;
  if (target > 0){
    TCNT1 = 0 ;
    TCCR1B = 1 ;
    while (TCNT1 < target){
      // waste cycles....
    }
    TCCR1B = 0 ;
    return TCNT1 ;
  }
  return 0 ;
}
