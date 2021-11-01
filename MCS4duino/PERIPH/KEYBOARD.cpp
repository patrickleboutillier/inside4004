#include "KEYBOARD.h"


#define KBD_ROW              0b00011110
#define KBD_ROW_OUTPUT       DDRB |= KBD_ROW
#define WRITE_KBD_ROW(data)  PORTB = (PORTB & ~KBD_ROW) | ((data) << 1) 

#define KBD_SEND_KEY         0b00000010
#define KBD_SEND_KEY_ON      PINC &   KBD_SEND_KEY
#define KBD_SEND_KEY_INPUT   DDRC &= ~KBD_SEND_KEY

static int key_buffer_idx = 0 ;
static const byte key_buffer[] = 
  // {K1, K1, KPLUS, K7, KPLUS, KEQ, 255} ;
  // {K1, K1, KPLUS, K7, KPLUS, KEQ, K5, K5, KMULT, K4, K1, KEQ, K2, KSQ, 255} ;
  {K1, K2, KDOT, K3, K4, KPLUS, 
   K3, K4, KDOT, K5, K6, KMIN,
   K5, K6, KDOT, K7, K8, K9, KPLUS, 
   KPLUS,
   KDOT, K1, K2, K3, KPLUS,
   KEQ, 255} ;
  // {K2, KSQ, 255} ;


KEYBOARD::KEYBOARD(i4003 *input){
  _input = input ;
  key_buffer_idx = 0 ;
  reset() ;
}


void KEYBOARD::reset(){
  WRITE_KBD_ROW(0) ;
  
  for (int i = 0 ; i < 10  ; i++){
    for (int j = 0 ; j < 4 ; j++){
      _buffer[i][j] = 0 ; 
    }
  }
  
  _cur_send_key = 0 ;
  key_buffer_idx = 0 ;
}


void KEYBOARD::setup(){
  KBD_ROW_OUTPUT ;
  KBD_SEND_KEY_INPUT ;
}


void KEYBOARD::loop(){
  // Check the send key signal
  if (KBD_SEND_KEY_ON){
    if (! _cur_send_key){
      sendKey() ;
      _cur_send_key = 1 ;
    }
  }
  else {
    _cur_send_key = 0 ;
  }
}


void KEYBOARD::writeKey(){
  long reg = _input->getReg() ;
  long mask = 1 ;
  for (int i = 0 ; i < 10 ; i++){
    if ((reg & mask) == 0){
      byte data = (_buffer[i][0] << 3) | (_buffer[i][1] << 2) | (_buffer[i][2] << 1) | _buffer[i][3] ;
      WRITE_KBD_ROW(data) ;           
      if ((data != 0)&&(i < 8)){   // Don't reset the switches!
        _buffer[i][0] = 0 ;
        _buffer[i][1] = 0 ;
        _buffer[i][2] = 0 ;
        _buffer[i][3] = 0 ;
      }
    }
    mask = mask << 1 ;
  }     
}


void KEYBOARD::sendKey(){
  byte kc = key_buffer[key_buffer_idx] ;
  if (kc == 255){
    key_buffer_idx = 0 ;
    kc = key_buffer[key_buffer_idx] ;
  }
  
  byte c = kc >> 2 ;
  byte r = 3 - (kc & 0b11) ;
  _buffer[c][r] = 1 ;
  key_buffer_idx++ ;
}


/*
    def incDP(self):
        n = int("".join(map(str, self.dp_sw)), 2)
        n = (n + 1) % 9
        self.dp_sw[:] = list(map(int, list("{:04b}".format(n))))

    def incRND(self):
        n = int("".join(map(str, self.rnd_sw)), 2)
        if n == 0:
            n = 1
            desc = "round"
        elif n == 1:
            n = 8
            desc = "trunc"
        else:
            n = 0
            desc = "float"
        self.rnd_sw[:] = list(map(int, list("{:04b}".format(n))))

    def switches(self):
        dp = int("".join(map(str, self.dp_sw)), 2)
        rnd = int("".join(map(str, self.rnd_sw)), 2)
        if rnd == 0:
            r = "F"
        elif rnd == 1:
            r = "R"
        else:
            r = "T"
        return "DP[{}] RND[{}]".format(dp, r)
 */
