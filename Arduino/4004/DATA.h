#ifndef DATA_H
#define DATA_H

#include "Arduino.h"

#define DATA_            0b00111100 // PORTD
#define READ_DATA        ((PIND & DATA_) >> 2)
#define WRITE_DATA(data) PORTD = ((PORTD & ~DATA_) | (data << 2))  
#define DATA_INPUT       DDRD &= ~DATA_
#define DATA_OUTPUT      DDRD |=  DATA_


class DATA {
  private:
    bool _z ;
    byte _cache ;
    
  public:
    DATA(){    
      reset() ;
    }
    
    void reset(){
      z() ;
      _cache = 0 ;
    }
    
    void write(byte data){
      DATA_OUTPUT ;
      _z = 0 ;
      WRITE_DATA(data) ;
      _cache = data ;     
    }

    byte read(){
      if (_z){
        // We are disconnected from bus, so we read the real value
        return READ_DATA ;
      }
      else {
        // We are the one driving the bus, so get it from _cache.
        return _cache ;
      }
    }

    void z(){
      DATA_INPUT ;
      _z = 1 ;
    }
} ;

#endif
