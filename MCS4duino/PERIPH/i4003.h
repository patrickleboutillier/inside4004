#ifndef I4003_H
#define I4003_H

#include "Arduino.h"


class i4003 {
  public:
    i4003(int pin_clock, int pin_data_in, long mask) ;
    void loop() ;
    long getReg() ;
    bool getBit(int b) ;
  private:
    int _pin_clock ;
    int _pin_data_in ;
    long _mask ;
    long _reg ;
    bool _cur_clock ;
} ;


#endif
