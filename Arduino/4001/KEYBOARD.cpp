#include "KEYBOARD.h"
#include "TESTS.h"

static int test_idx = 0 ;
static const byte *key_buffer = tests[test_idx] ;
static int key_buffer_idx = 0 ;


KEYBOARD::KEYBOARD(i4003 *input){
  _input = input ;
  reset() ;
}


void KEYBOARD::reset(){
  for (int i = 0 ; i < 10 ; i++){
    _buffer[i] = 0 ; 
  }
  
  _cur_round = 0 ;
  _cur_prec = 0 ;
  _kbd_row = 0 ;
  
  test_idx = 0 ;
  key_buffer = tests[test_idx] ;
  key_buffer_idx = 0 ;
}


void KEYBOARD::setKbdRow(){
  int reg = _input->getReg() ;
  int mask = 1 ;
  for (int i = 0 ; i < 10 ; i++){
    if ((reg & mask) == 0){
      _kbd_row = _buffer[i] ;      
      if (i < 8){   // Don't reset the switches!
        _buffer[i] = 0 ;
      }
    }
    mask = mask << 1 ;
  }     
}


byte KEYBOARD::getKbdRow(){
  return _kbd_row ;  
}


bool KEYBOARD::sendKey(){
  byte kc = key_buffer[key_buffer_idx] ;

  switch (kc){
    case KEND: {
      int next_test = test_idx + 1 ;
      reset() ;
      test_idx = next_test ;
      key_buffer = tests[test_idx] ;
      return (key_buffer == NULL) ; 
    }
    case KD:
      _cur_prec++ ;
      if (_cur_prec == 9){
        _cur_prec = 0 ;
      }
      else if (_cur_prec == 7){
        _cur_prec = 8 ;
      }
      kc = 0b10000000 | _cur_prec ;
      break ;
    case KR:
      if (_cur_round == 0){
        _cur_round = 1 ;
      }
      else if (_cur_round == 1){
        _cur_round = 8 ;
      }
      else {
        _cur_round = 0 ;
      }
      kc = 0b10010000 | _cur_round ;
      break ;
  }
  
  byte c = kc >> 4 ;
  _buffer[c] |= kc & 0xF ; 
  key_buffer_idx++ ;

  return 0 ;
}
