#ifndef PRINTER_H
#define PRINTER_H

#include "i4003.h"


class PRINTER {
  public:
    PRINTER(i4003 *input) ;
    void reset() ;
    void setup() ;
    bool loop() ;
    void startSectorPulse() ;
    void endSectorPulse() ;
    void endSectorPeriod() ;
    void fireHammers() ;
    void advanceLine() ;
    void appendOutputBuffer(const char *s) ;
    void printChar() ;
    void punchChar(byte b) ;

  private:
    i4003 *_input ;
    char _line[23] ;
    char _output_buffer[256] ;
    byte _output_buffer_idx ;    
    byte _cur_sector ; 
    int _cur_cycle ;
    bool _cur_fire ;
    bool _cur_advance ;
    char _cur_color[2] ; 
    bool _cur_sync ;
} ;


#endif
