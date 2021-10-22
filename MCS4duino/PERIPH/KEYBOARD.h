#ifndef KEYBOARD_H
#define KEYBOARD_H

#include "i4003.h"


class KEYBOARD {
  public:
    KEYBOARD(i4003 *input) ;
    void reset() ;
    void setup() ;
    void loop() ;
    const char *getKeyBuffer() ;
    void appendKeyBuffer(const char *buffer) ;
    const char *getKeyBufferHead() ;
    void sendKey() ;

  private:
    i4003 *_input ;
    byte _buffer[10][4] ;
    char _key_buffer[129] ;
    bool _cur_send_key ;
    long _reg ;
} ;


#endif
