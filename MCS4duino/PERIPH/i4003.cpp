#include "i4003.h"


i4003::i4003(long mask){
  _mask = mask ;
  reset() ;
}


void i4003::reset(){
  _reg = 0 ;
  _cur_clock = 0 ;
}


void i4003::loop(bool clk, bool data){
  if (clk){
    if (! _cur_clock){
      onClock(data) ;
     _cur_clock = 1 ;  
    }
  }
  else {
    _cur_clock = 0 ;
  }
}


void i4003::onClock(bool data){
  _reg = ((_reg << 1) | data) & _mask ;
}


long i4003::getReg(){
  return _reg ;
}


bool i4003::getBit(int b){
  long t = 1L << b ;
  return _reg & t ;
}
