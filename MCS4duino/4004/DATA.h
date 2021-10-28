#ifndef DATA_H
#define DATA_H

#include "Arduino.h"

#define DATA_            0b00111100 // PORTD
#define READ_DATA        ((PIND & DATA_) >> 2)
#define WRITE_DATA(data) PORTD = ((PORTD & ~DATA_) | (data << 2))  
#define DATA_INPUT       DDRD &= ~DATA_
#define DATA_OUTPUT      DDRD |=  DATA_


class DATA {
  public:
    DATA(){    
      reset() ;
    }
    
    void reset(){
      z() ;
    }
    
    void write(byte data){
      DATA_OUTPUT ;
      WRITE_DATA(data) ;     
    }

    byte read(){
      return READ_DATA ; 
    }

    void z(){
      DATA_INPUT ;
    }
} ;

#endif
