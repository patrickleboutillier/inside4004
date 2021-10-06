#include "i4003.h"


i4003::i4003(int pin_clock, int pin_data_in, long mask){
  _pin_clock = pin_clock ;
  _pin_data_in = pin_data_in ;
  _mask = mask ;
  reset() ;
}


void i4003::reset(){
  _reg = 0 ;
  _cur_clock = 0 ;
}


void i4003::loop(){
  if (digitalRead(_pin_clock)){
    if (! _cur_clock){
      _reg = ((_reg << 1) | digitalRead(_pin_data_in)) & _mask ;
      _cur_clock = 1 ;  
    }
  }
  else {
    _cur_clock = 0 ;
  }
}


long i4003::getReg(){
  return _reg ;
}


bool i4003::getBit(int b){
  long t = 1L << b ;
  return _reg & t ;
}
