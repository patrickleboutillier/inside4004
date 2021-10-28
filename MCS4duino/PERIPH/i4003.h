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
    bool getBit(int b) ;
  private:
    long _mask ;
    long _reg ;
    bool _cur_clock ;
} ;


#endif
