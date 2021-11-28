#include "i4003.h"


i4003::i4003(long mask){
  _mask = mask ;
  reset() ;
}


void i4003::reset(){
  _reg = 0 ;
  _cur_clock = 0 ;
}


bool i4003::loop(bool clk, bool data){
  bool ret = 0 ;
  if (clk){
    if (! _cur_clock){
      _reg = ((_reg << 1) | data) & _mask ;
     _cur_clock = 1 ;
     ret = 1 ;  
    }
  }
  else {
    _cur_clock = 0 ;
  }

  return ret ;
}


long i4003::getReg(){
  return _reg ;
}
