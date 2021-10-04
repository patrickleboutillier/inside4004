#ifndef KEYBOARD_H
#define KEYBOARD_H

#include "i4003.h"


class KEYBOARD {
  public:
    KEYBOARD(i4003 *input, int pin_kbd_row_3, int pin_kbd_row_2, int pin_kbd_row_1, int pin_kbd_row_0) ;
    void reset() ;
    void loop() ;

  private:
    i4003 *_input ;
    int _pin_kbd_row_3 ;
    int _pin_kbd_row_2 ;
    int _pin_kbd_row_1 ;
    int _pin_kbd_row_0 ;
    byte _buffer[10][4] ;
    char _kbd_buffer[129] ;
} ;


#endif
