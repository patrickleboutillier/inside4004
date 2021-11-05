#ifndef KEYBOARD_H
#define KEYBOARD_H

#include "i4003.h"


class KEYBOARD {
  public:
    KEYBOARD(i4003 *input) ;
    void reset() ;
    void setup() ;
    void loop() ;
    void writeKey() ;
    void sendKey() ;

  private:
    i4003 *_input ;
    bool _buffer[10][4] ;
    bool _cur_send_key ;
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

#define KCM    0  
#define KRM    1
#define KMM    2
#define KMP    3

#define KSQ    4
#define KPCT   5
#define KMEM   6
#define KMEP   7

#define KDIV   9
#define KMULT  10
#define KEQ    11

#define KMIN   12
#define KPLUS  13
#define KHASH  14

#define K9     16
#define K6     17
#define K3     18
#define KDOT   19

#define K8     20
#define K5     21
#define K2     22

#define K7     24
#define K4     25
#define K1     26
#define K0     27

#endif
