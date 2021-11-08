#ifndef KEYBOARD_H
#define KEYBOARD_H

#include "i4003.h"
#include "PRINTER.h"


class KEYBOARD {
  public:
    KEYBOARD(i4003 *input, PRINTER *printer) ;
    void reset() ;
    void setup() ;
    bool loop() ;
    void writeKey() ;
    void sendKey() ;

  private:
    i4003 *_input ;
    PRINTER *_printer ;
    byte _buffer[10] ;
    bool _cur_send_key ;
    byte _cur_round ;
    byte _cur_prec ;
} ;


/* 
;shifter  ROM1 bit0 ROM1 bit1 ROM1 bit2 ROM1 bit3
;bit0     CM (81)   RM (82)   M- (83)   M+ (84)
;bit1     SQRT (85) % (86)    M=- (87)  M=+ (88)
;bit2     diamond (89)  / (8a)    * (8b)    = (8c)
;bit3     - (8d)    + (8e)    diamond2 (8f) 000 (90)
;bit4     9 (91)    6 (92)    3 (93)    . (94)
;bit5     8 (95)    5 (96)    2 (97)    00 (98)
;bit6     7 (99)    4 (9a)    1 (9b)    0 (9c)
;bit7     Sign (9d) EX (9e)   CE (9f)   C (a0)
;bit8     dp0   dp1   dp2   dp3 (digit point switch, value 0,1,2,3,4,5,6,8 can be switched)
;bit9     sw1   (unused)  (unused)  sw2 (rounding switch, value 0,1,8 can be switched)
*/

#define KCM    0b00000001  
#define KRM    0b00000010
#define KMM    0b00000100
#define KMP    0b00001000

#define KSQ    0b00010001
#define KPCT   0b00010010
#define KMEM   0b00010100
#define KMEP   0b00011000

// diamond
#define KDIV   0b00100010
#define KMULT  0b00100100
#define KEQ    0b00101000

#define KMIN   0b00110001
#define KPLUS  0b00110010
#define KHASH  0b00110100
// 000

#define K9     0b01000001
#define K6     0b01000010
#define K3     0b01000100
#define KDOT   0b01001000

#define K8     0b01010001
#define K5     0b01010010
#define K2     0b01010100
// 00

#define K7     0b01100001
#define K4     0b01100010
#define K1     0b01100100
#define K0     0b01101000

#define KSIGN  0b01110001
#define KEX    0b01110010
#define KCE    0b01110100
#define KCL    0b01111000

#define KD     250
#define KR     251

#define KEND   255

#endif
