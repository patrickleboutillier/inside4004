#ifndef DATA_H
#define DATA_H

#include "Arduino.h"

#define DATA_32   0b00000011    // PORTB
#define DATA_10   0b01100000    // PORTD


class DATA {
  public:
    DATA(){    
      reset() ;
    }
    
    void reset(){
      DDRB = DDRB & ~DATA_32 ;
      PORTB = PORTB & ~DATA_32 ;
      DDRD = DDRD & ~DATA_10 ;
      PORTD = PORTD & ~DATA_10 ;
    }
    
    void write(byte data){
      DDRB = DDRB | DATA_32 ;
      DDRD = DDRD | DATA_10 ;
      PORTB = (PORTB & ~DATA_32) | (((data >> 3) & 1) << 1) | ((data >> 2) & 1) ;  
      PORTD = (PORTD & ~DATA_10) | (((data >> 1) & 1) << 6) | ((data & 1) << 5) ;      
    }

    byte read(){
      return ((PINB & DATA_32) << 2) | ((PIND & DATA_10) >> 5) ; 
    }

    void z(){
      DDRB = DDRB & ~DATA_32 ;
      PORTB = PORTB & ~DATA_32 ;
      DDRD = DDRD & ~DATA_10 ;
      PORTD = PORTD & ~DATA_10 ; 
    }
} ;

#endif
