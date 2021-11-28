#include "PRINTER.h"

const char *specialChars_0[] = {"<>",  "+ ",  "- ",  "X ",  "/ ",  "M+",  "M-",  "^ ",  "= ",  "SQ",  "% ",  "C ",  "R "} ;
const char *specialChars_1[] = {"#  ", "*  ", "I  ", "II ", "III", "M+ ", "M- ", "T  ", "K  ", "E  ", "Ex ", "C  ", "M  "} ;
const char *digits[] = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"} ;
const char *dot = "." ;
const char *dash = "-" ;

// Units are CPU cycles
const long sector_pulse =  (14 * 1000) / 22 ;
const long sector_period = (28 * 1000) / 22 ;

#define SYNC_INPUT          DDRD &= ~0b00010000
#define SYNC_ON             PIND &   0b00010000

#define PRN_ADV             0b00001000
#define PRN_ADV_INPUT       DDRC &= ~PRN_ADV
#define PRN_FIRE            0b00010000
#define PRN_FIRE_INPUT      DDRC &= ~PRN_FIRE
#define PRN_COLOR           0b00100000
#define PRN_COLOR_INPUT     DDRC &= ~PRN_COLOR

#define PRN_INDEX           0b00100000
#define PRN_INDEX_ON        PORTD |=  PRN_INDEX
#define PRN_INDEX_OFF       PORTD &= ~PRN_INDEX
#define PRN_INDEX_OUTPUT    DDRD  |=  PRN_INDEX
#define PRN_ADV_BTN         0b01000000
#define PRN_ADV_BTN_ON      PORTD |=  PRN_ADV_BTN
#define PRN_ADV_BTN_OFF     PORTD &= ~PRN_ADV_BTN
#define PRN_ADV_BTN_OUTPUT  DDRD  |=  PRN_ADV_BTN
#define PRN_SECTOR          0b10000000
#define PRN_SECTOR_ON       PORTD |=  PRN_SECTOR
#define PRN_SECTOR_OFF      PORTD &= ~PRN_SECTOR
#define PRN_SECTOR_OUTPUT   DDRD  |=  PRN_SECTOR


PRINTER::PRINTER(i4003 *input){
  _input = input ;
  reset() ;
}


void PRINTER::reset(){
  strcpy(_line, "                      ") ;
  _output_buffer[0] = '\0' ;
  _cur_sector = 0 ; 
  _cur_cycle = 0 ;
  _cur_fire = 0 ;
  _cur_advance = 0 ;
  strcpy(_cur_color, " ") ;
  _cur_sync = 0 ;  
  _output_buffer[0] = '\0' ;
  _output_buffer_idx = 0 ;
  
  PRN_ADV_BTN_OFF ;
  PRN_INDEX_OFF ;  
  PRN_SECTOR_OFF ; 
}


void PRINTER::setup(){
  SYNC_INPUT ;
  PRN_ADV_INPUT ;
  PRN_FIRE_INPUT ;
  PRN_COLOR_INPUT ;
  PRN_ADV_BTN_OUTPUT ;
  PRN_INDEX_OUTPUT ;
  PRN_SECTOR_OUTPUT ;
}


bool PRINTER::loop(){
  // TODO: For now we use the sync signal as a cycle indicator.
  // Once the 4004 is in the Nano, we will know the real clock period and will be able to 
  // have the printer manage it's own timing independently, based on setting sector_pulse and sector_period.
  bool ret = 0 ;
  
  if (SYNC_ON){
    if (! _cur_sync){
      if (_cur_cycle == 0){
          ret = 1 ;
          startSectorPulse() ;
      }
      else if (_cur_cycle == sector_pulse){
          ret = 1 ;
          endSectorPulse() ;
      }
      else if (_cur_cycle == sector_period){
          ret = 1 ;
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

  byte data = PINC ;
  if (data & PRN_FIRE){
      if (! _cur_fire){
        fireHammers() ;
        _cur_fire = 1 ;
        ret = 1 ;
      }
  }
  else {
    _cur_fire = 0 ;
  }

  if (data & PRN_ADV){
    if (! _cur_advance){
      advanceLine() ;
      strcpy(_cur_color, " ") ;   // Reset line color
      _cur_advance = 1 ;
      ret = 1 ;
    }
  }
  else{
    _cur_advance = 0 ;
  }
  
  if (data & PRN_COLOR){
    strcpy(_cur_color, "-") ;    // Set color to "red", meaning negative value.
    ret = 1 ;
  }  

  return ret ;
}


void PRINTER::startSectorPulse(){
  PRN_SECTOR_ON ;
  if (_cur_sector == 0){
      PRN_INDEX_ON ;
  }
  _cur_cycle += 1 ;
}


void PRINTER::endSectorPulse(){
  PRN_SECTOR_OFF ;
  _cur_cycle += 1 ;
}


void PRINTER::endSectorPeriod(){
  if (_cur_sector == 0){
      PRN_INDEX_OFF ;
  }
  _cur_sector++ ;
  if (_cur_sector == 13){
    _cur_sector = 0 ;
  }
  _cur_cycle = 0 ;
}


void PRINTER::fireHammers(){
  long reg = _input->getReg() ;
  long mask = 1L ;
  for (int i = 0 ; i < 20 ; i++){
    if (reg & mask){
      punchChar(i) ;
    }
    mask = mask << 1 ;
  }
}


void PRINTER::advanceLine(){
  // print previous line
  _output_buffer[0] = '\0' ;
  _output_buffer_idx = 0 ;
  appendOutputBuffer(">>> ") ;
  appendOutputBuffer(_cur_color) ;
  appendOutputBuffer("|") ;
  appendOutputBuffer(_line) ;
  appendOutputBuffer("|\n") ;
  for (int i = 0 ; _line[i] != '\0' ; i++){
    _line[i] = ' ' ;
  }
}


void PRINTER::appendOutputBuffer(const char *s){
  strcat(_output_buffer, s) ;
}


void PRINTER::printChar(){
  char c = _output_buffer[_output_buffer_idx] ;
  if (c != '\0'){
    Serial.print(c) ;
    _output_buffer_idx++ ;
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
