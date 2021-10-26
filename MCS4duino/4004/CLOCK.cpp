#include "CLOCK.h"

#define CLK1_1    0b000010000   // PORTB
#define CLK1_2    0b000010000   // PORTD
#define CLK2_1    0b000001000   // PORTB
#define CLK2_2    0b000001000   // PORTD
#define CLK_US    75 

static TIMING *timing ;
static unsigned long n = 0 ;


void CLOCK_reset(){
  n = 0 ;
  PORTB = PORTB & ~(CLK1_1 | CLK2_1) ;
  PORTD = PORTD & ~(CLK1_2 | CLK2_2) ;
}


void CLOCK_setup(TIMING *t){
  timing = t ;
  DDRB = DDRB | CLK1_1 | CLK2_1 ;
  DDRD = DDRD | CLK1_2 | CLK2_2 ;  
  CLOCK_reset() ;
}


void CLOCK_tick(){
  unsigned long start = micros() ;
  while ((micros() - start) < CLK_US){
    switch (n & 0b11){
      case 0:
        PORTB = PORTB | CLK1_1 ;
        PORTD = PORTD | CLK1_2 ; 
        timing->tick(1, 0) ;
        break ;
      case 1:
        PORTB = PORTB & ~CLK1_1 ;
        PORTD = PORTD & ~CLK1_2 ;
        timing->tick(0, 0) ;
        break ;
      case 2:
        PORTB = PORTB | CLK2_1 ;
        PORTD = PORTD | CLK2_2 ;  
        timing->tick(0, 1) ;
        break ;
      default:
        PORTB = PORTB & ~CLK2_1 ;
        PORTD = PORTD & ~CLK2_2 ;
        timing->tick(0, 0) ;      
    }
  }
  n++ ; 
}
