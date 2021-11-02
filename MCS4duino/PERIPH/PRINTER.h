#ifndef PRINTER_H
#define PRINTER_H

#include "i4003.h"


class PRINTER {
  public:
    PRINTER(i4003 *input) ;
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
    
    byte _cur_sector ; 
    int _cur_cycle ;
    bool _cur_fire ;
    bool _cur_advance ;
    char _cur_color ; 
    bool _cur_sync ;
} ;


#endif
