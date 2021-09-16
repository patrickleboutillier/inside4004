#include "i4003.h"
#include "PRINTER.h"

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

#define ADVANCE       A3
#define FIRE          A4
#define COLOR         A5

i4003 PSHIFT(PRN_SHFT_CLK, SHFT_DATA, 0xFFFFF) ;
PRINTER PRINTER(&PSHIFT, FIRE, ADVANCE, COLOR, PRN_SECTOR, PRN_INDEX, SYNC) ;


void setup(){
  Serial.begin(115200) ;
  Serial.println("Welcome to Busicom 141-PF!") ;
  pinMode(KBD_SHFT_CLK, INPUT) ;
  pinMode(SHFT_DATA, INPUT) ;
  pinMode(PRN_SHFT_CLK, INPUT) ;
  pinMode(PRN_ADV_BTN, OUTPUT) ;
  digitalWrite(PRN_ADV_BTN, 0) ;
  pinMode(SYNC, INPUT) ;
  pinMode(ADVANCE, INPUT) ;
  pinMode(FIRE, INPUT) ;
  pinMode(COLOR, INPUT) ;
  pinMode(KBD_ROW_3, OUTPUT) ;
  digitalWrite(KBD_ROW_3, 0) ;
  pinMode(KBD_ROW_2, OUTPUT) ;
  digitalWrite(KBD_ROW_2, 0) ;
  pinMode(KBD_ROW_1, OUTPUT) ;
  digitalWrite(KBD_ROW_1, 0) ;
  pinMode(KBD_ROW_0, OUTPUT) ;
  digitalWrite(KBD_ROW_0, 0) ;
}


void loop(){
  PSHIFT.loop() ;
  PRINTER.loop() ;
}
