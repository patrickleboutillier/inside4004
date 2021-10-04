#include "PRINTER.h"


const char *specialChars_0[] = {"<>",  "+ ",  "- ",  "X ",  "/ ",  "M+",  "M-",  "^ ",  "= ",  "SQ",  "% ",  "C ",  "R "} ;
const char *specialChars_1[] = {"#  ", "*  ", "I  ", "II ", "III", "M+ ", "M- ", "T  ", "K  ", "E  ", "Ex ", "C  ", "M  "} ;
const char *digits[] = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"} ;
const char *dot = "." ;
const char *dash = "-" ;

// Units are CPU cycles
const long sector_pulse =  (5 * 1000) / 22 ;
const long sector_period = (28 * 1000) / 22 ;


PRINTER::PRINTER(i4003 *input, int pin_fire, int pin_advance, int pin_color, int pin_sector, int pin_index, int pin_sync){
  _input = input ;
  _pin_fire = pin_fire ;
  _pin_advance = pin_advance ;
  _pin_color = pin_color ;
  _pin_sector = pin_sector ;
  _pin_index = pin_index ;
  _pin_sync = pin_sync ;
  reset() ;
}


void PRINTER::reset(){
  strcpy(_line, "                      ") ;
  _cur_sector = 0 ; 
  _cur_cycle = 0 ;
  _cur_fire = 0 ;
  _cur_advance = 0 ;
  _cur_color = ' ' ;
  _cur_sync = 0 ;  
}


void PRINTER::loop(){
  // TODO: For now we use the sync signal as a cycle indicator.
  // Once the 4004 is in the Nano, we will know the real clock period and will be able to 
  // have the printer manage it's own timing independently, based on setting sector_pulse and sector_period.
  if (digitalRead(_pin_sync)){
    if (! _cur_sync){
      if (_cur_cycle == 0){
          startSectorPulse() ;
      }
      else if (_cur_cycle == sector_pulse){
          endSectorPulse() ;
      }
      else if (_cur_cycle == sector_period){
          endSectorPeriod() ;
      }
      else {
          _cur_cycle += 1 ;
      }
      _cur_sync = 1 ;
    }
  }
  else {
    _cur_sync = 0 ; 
  }
  
  if (digitalRead(_pin_fire)){
      if (! _cur_fire){
        fireHammers() ;
        _cur_fire = 1 ;
      }
  }
  else {
    _cur_fire = 0 ;
  }
  
  if (digitalRead(_pin_advance)){
    if (! _cur_advance){
      advanceLine() ;
      _cur_color = ' ' ;   // Reset line color
      _cur_advance = 1 ;
    }
  }
  else{
    _cur_advance = 0 ;
  }
  
  if (digitalRead(_pin_color)){
    _cur_color = '-' ;    // Set color to "red", meaning negative value.
  }  
}


void PRINTER::startSectorPulse(){
  digitalWrite(_pin_sector, 1) ;
  if (_cur_sector == 0){
      digitalWrite(_pin_index, 1) ;
      Serial.println("INDEX ON") ;
  }
  _cur_cycle += 1 ;
}


void PRINTER::endSectorPulse(){
  digitalWrite(_pin_sector, 0) ;
  _cur_cycle += 1 ;
}


void PRINTER::endSectorPeriod(){
  if (_cur_sector == 0){
      digitalWrite(_pin_index, 0) ;
      Serial.println("INDEX OFF") ;
  }
  _cur_sector = (_cur_sector + 1) % 13 ;
  Serial.print("SECTOR ") ;
  Serial.println(_cur_sector) ;
  _cur_cycle = 0 ;
}


void PRINTER::fireHammers(){
  Serial.print("FIRE HAMMERS ") ;
  Serial.println(_input->getReg() | 0b100000000000000000000, BIN) ;
  for (int i = 0 ; i < 20 ; i++){
    if (_input->getBit(i)){
      punchChar(i) ;
    }
  }
  Serial.print("  ") ;
  Serial.println(_line) ;
}


void PRINTER::advanceLine(){
  // print previous line
  Serial.print(">>> ") ;
  Serial.print(_cur_color) ;
  Serial.print("|") ;
  Serial.print(_line) ;
  Serial.println("|") ;
  for (int i = 0 ; _line[i] != '\0' ; i++){
    _line[i] = ' ' ;
  }
}


void PRINTER::punchChar(byte b){
  const char *str = NULL ;
  int pos = -1 ;
  if (b == 0){
    str = specialChars_0[_cur_sector] ;
    pos = 16 ;
  }
  else if (b == 1){
    str = specialChars_1[_cur_sector] ;
    pos = 19 ;
  }
  else if (b <= 17 && b >= 3){
    if (_cur_sector <= 9){
      str = digits[_cur_sector] ;
      pos = b - 3 ;
    }
    else if (_cur_sector == 10 || _cur_sector == 11){
      str = dot ;
      pos = b - 3 ;
    }
    else {
      str = dash ;
      pos = b - 3 ;
    }
  }
  
  if (str != NULL){ 
    strncpy(_line + pos, str, strlen(str)) ;
  }
}
