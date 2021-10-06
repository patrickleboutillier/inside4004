#ifndef KEYBOARD_H
#define KEYBOARD_H

#include "i4003.h"


class KEYBOARD {
  public:
    KEYBOARD(i4003 *input, int pin_kbd_row_3, int pin_kbd_row_2, int pin_kbd_row_1, int pin_kbd_row_0, int pin_send_key) ;
    void reset() ;
    void loop() ;
    const char *getKeyBuffer() ;
    void appendKeyBuffer(const char *buffer) ;
    const char *getKeyBufferHead() ;
    void sendKey() ;

  private:
    i4003 *_input ;
    int _pin_kbd_row_3 ;
    int _pin_kbd_row_2 ;
    int _pin_kbd_row_1 ;
    int _pin_kbd_row_0 ;
    int _pin_send_key ;
    byte _buffer[10][4] ;
    char _key_buffer[129] ;
    bool _cur_send_key ;
    long _reg ;
} ;


#endif
