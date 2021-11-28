#ifndef I4003_H
#define I4003_H

#include "Arduino.h"


class i4003 {
  public:
    i4003(long mask) ;
    void reset() ;
    bool loop(bool clk, bool data) ;
    long getReg() ;
  private:
    long _mask ;
    long _reg ;
    bool _cur_clock ;
} ;


#endif
