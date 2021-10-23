#ifndef PRINTER_H
#define PRINTER_H

#include "i4003.h"


class PRINTER {
  public:
    PRINTER(i4003 *input, int pin_fire, int pin_advance, int pin_color, int pin_sector, int pin_index) ;
    void reset() ;
    void setup() ;
    void loop() ;
    void startSectorPulse() ;
    void endSectorPulse() ;
    void endSectorPeriod() ;
    void fireHammers() ;
    void advanceLine() ;
    void punchChar(byte b) ;

  private:
    i4003 *_input ;
    char _line[23] ;
    int _pin_fire ;
    int _pin_advance ;
    int _pin_color ;
    int _pin_sector ;
    int _pin_index ;
    
    int _cur_sector ; 
    int _cur_cycle ;
    bool _cur_fire ;
    bool _cur_advance ;
    char _cur_color ; 
    bool _cur_sync ;
    long _reg ;
} ;


#endif
