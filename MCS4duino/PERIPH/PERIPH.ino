#include "i4003.h"
#include "PRINTER.h"
#include "KEYBOARD.h"

#define READ_RESET          PINC &   0b00000100
#define RESET_INPUT         DDRC &= ~0b00000100

#define KBD_SHFT_CLK  11
#define PRN_SHFT_CLK  8
#define PRN_INDEX     10
#define PRN_ADV_BTN   9
#define SHFT_DATA     12
#define PRN_SECTOR    7
#define SYNC          2

#define PRN_ADV       A3
#define PRN_FIRE      A4
#define PRN_COLOR     A5

i4003 PSHIFT(PRN_SHFT_CLK, SHFT_DATA, 0xFFFFF) ;
i4003 KSHIFT(KBD_SHFT_CLK, SHFT_DATA, 0x3FF) ;
PRINTER PRINTER(&PSHIFT, PRN_FIRE, PRN_ADV, PRN_COLOR, PRN_SECTOR, PRN_INDEX, SYNC) ;
KEYBOARD KEYBOARD(&KSHIFT) ;


void setup(){
  Serial.begin(115200) ;
  Serial.println("Welcome to Busicom 141-PF!") ;
  Serial.print("key buffer: ") ;
  Serial.println(KEYBOARD.getKeyBuffer()) ;
  
  RESET_INPUT ;
  pinMode(KBD_SHFT_CLK, INPUT) ;
  pinMode(SHFT_DATA, INPUT) ;
  pinMode(PRN_SHFT_CLK, INPUT) ;
  pinMode(PRN_ADV_BTN, OUTPUT) ;
  pinMode(SYNC, INPUT) ;
  pinMode(PRN_ADV, INPUT) ;
  pinMode(PRN_FIRE, INPUT) ;
  pinMode(PRN_COLOR, INPUT) ;
  pinMode(PRN_INDEX, OUTPUT) ;
  pinMode(PRN_SECTOR, OUTPUT) ;
  KEYBOARD.setup() ;
  reset() ;
}


unsigned long max_dur = 0 ;
void reset(){
  PSHIFT.reset() ;
  PRINTER.reset() ;
  KSHIFT.reset() ;
  KEYBOARD.reset() ;
  digitalWrite(PRN_ADV_BTN, 0) ;
  digitalWrite(PRN_INDEX, 0) ;  
  digitalWrite(PRN_SECTOR, 0) ; 
  max_dur = 0 ;
}


void loop(){
  while (1){
    unsigned long start = micros() ;
    if (READ_RESET){
      Serial.println("RESET!!!") ;
      return reset() ;
    }
  
    PSHIFT.loop() ;
    PRINTER.loop() ;
    KSHIFT.loop() ;
    KEYBOARD.loop() ;
    unsigned long dur = micros() - start ;
    if (dur > max_dur){
      max_dur = dur ;
      Serial.print("Max loop duration: ") ;
      Serial.print(max_dur) ;
      Serial.println("us ") ;
    }
  }
}
