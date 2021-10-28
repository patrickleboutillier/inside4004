#include "KEYBOARD.h"


#define DEFAULT_KEY_BUF      "11+7+="

#define KBD_ROW              0b00011110
#define KBD_ROW_OUTPUT       DDRB |= KBD_ROW
#define WRITE_KBD_ROW(data)  PORTB = (PORTB & ~KBD_ROW) | ((data) << 1) 

#define KBD_SEND_KEY         0b00000010
#define KBD_SEND_KEY_ON      PINC &   KBD_SEND_KEY
#define KBD_SEND_KEY_INPUT   DDRC &= ~KBD_SEND_KEY

 
const char *lookup[] = {
  "CM",  "RM", "M-",     "M+",
  "SQ",  "%",  "M=-",    "M=+",
  NULL,  "/",  "*",      "=",
  "-",   "+",  "#",      NULL,
  "9",   "6",  "3",      ".",
  "8",   "5",  "2",      NULL,
  "7",   "4",  "1",      "0",
  "S-",  "EX", "CE",     "CL"
} ;


KEYBOARD::KEYBOARD(i4003 *input){
  _input = input ;
  _key_buffer[0] = '\0' ;
  reset() ;
}


void KEYBOARD::reset(){
  WRITE_KBD_ROW(0) ;
  
  for (int i = 0 ; i < 10  ; i++){
    for (int j = 0 ; j < 4 ; j++){
      _buffer[i][j] = 0 ; 
    }
  }

  if (strcmp(DEFAULT_KEY_BUF, _key_buffer) != 0){
    _key_buffer[0] = '\0' ;
    appendKeyBuffer(DEFAULT_KEY_BUF) ;
  }
  
  _cur_send_key = 0 ;
  _reg = 0 ;
}


void KEYBOARD::setup(){
  KBD_ROW_OUTPUT ;
  KBD_SEND_KEY_INPUT ;
}


void KEYBOARD::loop(){
  // Check for keyboard input
  if (Serial.available()){ 
    char c = (char)Serial.read() ; 
    if ((c != '\n')&&(c != '\r')){
      char s[2] ;
      s[0] = c ; 
      s[1] = '\0' ;
      appendKeyBuffer(s) ;
    }
  }

  // Check if the keyboard is being scanned
  if (_input->getReg() != _reg){
    _reg = _input->getReg() ;
    //Serial.print("kbd reg ") ;
    //Serial.println(_reg | 0b10000000000, BIN) ;
    writeKey() ;
  }
  
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
  for (int i = 0 ; i < 10 ; i++){
    if (_input->getBit(i) == 0){
      byte data = (_buffer[i][0] << 3) | (_buffer[i][1] << 2) | (_buffer[i][2] << 1) | _buffer[i][3] ;
      /* if (data != 0){
        Serial.print("scanned ") ;
        Serial.print(i) ;
        Serial.print(": ") ;
        Serial.println(data) ;
      } */
      WRITE_KBD_ROW(data) ;           
      if (i < 8){   // Don't reset the switches!
        _buffer[i][0] = 0 ;
        _buffer[i][1] = 0 ;
        _buffer[i][2] = 0 ;
        _buffer[i][3] = 0 ;
      }
    }
  }     
}


const char *KEYBOARD::getKeyBuffer(){
  return _key_buffer ;  
}


void KEYBOARD::appendKeyBuffer(const char *buf){
  strcat(_key_buffer, buf) ;
  Serial.print("key_buffer: ") ;
  Serial.println(_key_buffer) ;
}


const char *KEYBOARD::getKeyBufferHead(){
  static char head[4] ;
  head[0] = '\0' ;
  
  if (strlen(_key_buffer) == 0){
    return head ;
  }

  if ((_key_buffer[0] == 'd')||(_key_buffer[0] == 'r')||(_key_buffer[0] == 'a')||(_key_buffer[0] == 'h')){
    head[0] = _key_buffer[0] ;
    head[1] = '\0' ;
    goto done ;
  }
  
  for (int c = 0 ; c < 8 ; c++){
    for (int r = 0 ; r < 4 ; r++){
      const char *s = lookup[(c << 2) + (3 - r)] ;
      if ((s != NULL)&&(strncmp(s, _key_buffer, strlen(s)) == 0)){
        strcpy(head, s) ;
        goto done ;
      }
    }
  }

  head[0] = _key_buffer[0] ;
  head[1] = '\0' ;
  
  done:
  // Remove head from _key_buffer
  memmove(_key_buffer, _key_buffer+strlen(head), strlen(_key_buffer)-strlen(head)+1) ;

  return head ;
}


void KEYBOARD::sendKey(){
  if (strlen(_key_buffer) > 0){
    Serial.print("sendKey: ") ;
    const char *k = getKeyBufferHead() ;
    Serial.println(k) ;
    Serial.print("key_buffer: ") ;
    Serial.println(_key_buffer) ;
    if (k != NULL){
      for (int c = 0 ; c < 8 ; c++){
        for (int r = 0 ; r < 4 ; r++){
          const char *s = lookup[(c << 2) + (3 - r)] ;
          if ((s != NULL)&&(strcmp(k, s) == 0)){
            _buffer[c][r] = 1 ;
            return ;
          }
        }
      }
      Serial.print(F("!!! ERROR: Unknown key ')")) ;
      Serial.print(k) ;
      Serial.println(F("! Use 'h' for help.")) ;
    }
  }
}
