#include "i4003.h"
#include "PRINTER.h"

#define RESET         A2
#define KBD_SHFT_CLK  12
#define PRN_SHFT_CLK  11
#define PRN_INDEX     10
#define PRN_ADV_BTN   9
#define SHFT_DATA     8
#define PRN_SECTOR    7
#define KBD_ROW_3     6
#define KBD_ROW_2     5
#define KBD_ROW_1     4
#define KBD_ROW_0     3
#define SYNC          2

#define PRN_ADV       A3
#define PRN_FIRE      A4
#define PRN_COLOR     A5

i4003 PSHIFT(PRN_SHFT_CLK, SHFT_DATA, 0xFFFFF) ;
PRINTER PRINTER(&PSHIFT, PRN_FIRE, PRN_ADV, PRN_COLOR, PRN_SECTOR, PRN_INDEX, SYNC) ;


void setup(){
  Serial.begin(115200) ;
  Serial.println("Welcome to Busicom 141-PF!") ;
  pinMode(RESET, INPUT) ;
  pinMode(KBD_SHFT_CLK, INPUT) ;
  pinMode(SHFT_DATA, INPUT) ;
  pinMode(PRN_SHFT_CLK, INPUT) ;
  pinMode(PRN_ADV_BTN, OUTPUT) ;
  pinMode(SYNC, INPUT) ;
  pinMode(PRN_ADV, INPUT) ;
  pinMode(PRN_FIRE, INPUT) ;
  pinMode(PRN_COLOR, INPUT) ;
  pinMode(KBD_ROW_3, OUTPUT) ;
  pinMode(KBD_ROW_2, OUTPUT) ;
  pinMode(KBD_ROW_1, OUTPUT) ;
  pinMode(KBD_ROW_0, OUTPUT) ;
  pinMode(PRN_INDEX, OUTPUT) ;
  pinMode(PRN_SECTOR, OUTPUT) ;
  reset() ;
}


void reset(){
  PRINTER.reset() ;
  PSHIFT.reset() ;
  digitalWrite(PRN_ADV_BTN, 0) ;
  digitalWrite(KBD_ROW_3, 0) ;
  digitalWrite(KBD_ROW_2, 0) ;
  digitalWrite(KBD_ROW_1, 0) ;
  digitalWrite(KBD_ROW_0, 0) ; 
  digitalWrite(PRN_INDEX, 0) ;  
  digitalWrite(PRN_SECTOR, 0) ; 
}


void loop(){
  if (digitalRead(RESET)){
    return reset() ;
  }

  PSHIFT.loop() ;
  PRINTER.loop() ;
}
