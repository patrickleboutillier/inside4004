#include "i4003.h"
#include "PRINTER.h"
#include "KEYBOARD.h"

#define READ_RESET          PINC &   0b00000100
#define RESET_INPUT         DDRC &= ~0b00000100

#define SHFT_DATA           0b00010000
#define SHFT_DATA_INPUT     DDRB &= ~SHFT_DATA
#define KBD_SHFT_CLK        0b00001000
#define KBD_SHFT_CLK_INPUT  DDRB &= ~KBD_SHFT_CLK
#define PRN_SHFT_CLK        0b00000001
#define PRN_SHFT_CLK_INPUT  DDRB &= ~PRN_SHFT_CLK

#define PRN_INDEX     10
#define PRN_ADV_BTN   9
#define PRN_SECTOR    7

i4003 PSHIFT(0xFFFFF) ;
i4003 KSHIFT(0x3FF) ;
PRINTER PRINTER(&PSHIFT, PRN_SECTOR, PRN_INDEX) ;
KEYBOARD KEYBOARD(&KSHIFT) ;


void setup(){
  Serial.begin(2000000) ;
  Serial.println("Welcome to Busicom 141-PF!") ;
  Serial.print("key buffer: ") ;
  Serial.println(KEYBOARD.getKeyBuffer()) ;
  
  RESET_INPUT ;
  SHFT_DATA_INPUT ;
  KBD_SHFT_CLK_INPUT ;
  PRN_SHFT_CLK_INPUT ;
  pinMode(PRN_ADV_BTN, OUTPUT) ;
  pinMode(PRN_INDEX, OUTPUT) ;
  pinMode(PRN_SECTOR, OUTPUT) ;
  KEYBOARD.setup() ;
  PRINTER.setup() ;
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

    byte shift = PINB ;
    PSHIFT.loop(shift & PRN_SHFT_CLK, shift & SHFT_DATA) ;
    PRINTER.loop() ;
    KSHIFT.loop(shift & KBD_SHFT_CLK, shift & SHFT_DATA) ;
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
