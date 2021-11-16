#include "KEYBOARD.h"
#include "TESTS.h"

#define KBD_ROW              0b00011110
#define KBD_ROW_OUTPUT       DDRB |= KBD_ROW
#define WRITE_KBD_ROW(data)  PORTB = (PORTB & ~KBD_ROW) | ((data) << 1) 

#define KBD_SEND_KEY         0b00000010
#define KBD_SEND_KEY_ON      PINC &   KBD_SEND_KEY
#define KBD_SEND_KEY_INPUT   DDRC &= ~KBD_SEND_KEY

static int test_idx = 0 ;
static const byte *key_buffer = tests[test_idx] ;
static int key_buffer_idx = 0 ;


KEYBOARD::KEYBOARD(i4003 *input, PRINTER *printer){
  _input = input ;
  _printer = printer ;
  reset() ;
}


void KEYBOARD::reset(){
  WRITE_KBD_ROW(0) ;
  
  for (int i = 0 ; i < 10 ; i++){
    _buffer[i] = 0 ; 
  }
  
  _cur_send_key = 0 ;
  _cur_round = 0 ;
  _cur_prec = 0 ;

  test_idx = 0 ;
  key_buffer = tests[test_idx] ;
  key_buffer_idx = 0 ;
}


void KEYBOARD::setup(){
  KBD_ROW_OUTPUT ;
  KBD_SEND_KEY_INPUT ;
}


bool KEYBOARD::loop(){
  // Check the send key signal
  bool ret = 0 ;
  if (KBD_SEND_KEY_ON){
    if (! _cur_send_key){
      noInterrupts() ;
      sendKey() ;
      interrupts() ;
      _cur_send_key = 1 ;
      ret = 1 ;
    }
  }
  else {
    _cur_send_key = 0 ;
  }

  return ret ;
}


void KEYBOARD::writeKey(){
  int reg = _input->getReg() ;
  int mask = 1 ;
  for (int i = 0 ; i < 10 ; i++){
    if ((reg & mask) == 0){
      WRITE_KBD_ROW(_buffer[i]) ;      
      if (i < 8){   // Don't reset the switches!
        if (_buffer[i] != 0){
          Serial.print(" wk:") ;
          Serial.print(i, HEX) ;
          Serial.println(_buffer[i]) ;  
        }   
        _buffer[i] = 0 ;
      }
    }
    mask = mask << 1 ;
  }     
}


void KEYBOARD::sendKey(){
  byte kc = key_buffer[key_buffer_idx] ;
  
  while ((kc == KD)||(kc == KR)){
    if (kc == KD){
      _cur_prec++ ;
      if (_cur_prec == 9){
        _cur_prec = 0 ;
      }
      else if (_cur_prec == 7){
        _cur_prec == 8 ;
      }

      _buffer[8] = _cur_prec ;
    }
    else {
      if (_cur_round == 0){
        _cur_round = 1 ;
      }
      else if (_cur_round == 1){
        _cur_round = 8 ;
      }
      else {
        _cur_round = 0 ;
      }
      
      _buffer[9] = _cur_round ;
    }
    
    key_buffer_idx++ ;
    kc = key_buffer[key_buffer_idx] ;
  }

  if (kc == KEND){
    int t = test_idx ;
    reset() ;
    test_idx = t + 1 ;
    key_buffer = tests[test_idx] ;
    if (key_buffer == NULL){
      Serial.println("HALTED!") ;
      while(1){
        delay(1000) ;
      }
    }
    else {
      char buf[16] ;
      sprintf(buf, "TEST %d\n", test_idx) ;
      _printer->appendOutputBuffer(buf) ;
    }
    kc = key_buffer[key_buffer_idx] ;
  }
  
  byte c = kc >> 4 ;
  _buffer[c] |= kc & 0xF ;
  key_buffer_idx++ ;
  
  Serial.print("sk:") ;
  Serial.println(kc, HEX) ;
}
