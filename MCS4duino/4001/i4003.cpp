#include "i4003.h"


i4003::i4003(long mask){
  _mask = mask ;
  reset() ;
}


void i4003::reset(){
  _reg = 0 ;
}


void i4003::onClock(bool data){
  _reg = ((_reg << 1) | data) & _mask ;
}


long i4003::getReg(){
  return _reg ;
}
