#ifndef I4003_H
#define I4003_H

#include "Arduino.h"


class i4003 {
  public:
    i4003(long mask) ;
    void reset() ;
    void loop(bool clk, bool data) ;
    void onClock(bool data) ;
    long getReg() ;
  private:
    long _mask ;
    volatile long _reg ;
    bool _cur_clock ;
} ;


#endif
