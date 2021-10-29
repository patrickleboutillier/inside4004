#include "i4003.h"
#include "PRINTER.h"
#include "KEYBOARD.h"

#define RESET_ON            PINC &   0b00000100
#define RESET_INPUT         DDRC &= ~0b00000100

#define SHIFT_DATA            0b00000001
#define READ_SHIFT_DATA       (PINB & SHIFT_DATA)
#define SHIFT_DATA_INPUT      DDRB &= ~SHIFT_DATA
#define KBD_SHIFT_CLK         0b00001000
#define KBD_SHIFT_CLK_INPUT   DDRD &= ~KBD_SHIFT_CLK
#define PRN_SHIFT_CLK         0b00000100
#define PRN_SHIFT_CLK_INPUT   DDRD &= ~PRN_SHIFT_CLK

i4003 PSHIFT(0xFFFFF) ;
i4003 KSHIFT(0x3FF) ;
PRINTER PRINTER(&PSHIFT) ;
KEYBOARD KEYBOARD(&KSHIFT) ;


void kbd_clk(){  
  KSHIFT.onClock(READ_SHIFT_DATA) ; 
  KEYBOARD.writeKey() ;
}


void prn_clk(){ 
  PSHIFT.onClock(READ_SHIFT_DATA) ; 
}


void setup(){
  Serial.begin(2000000) ;
  Serial.println("Welcome to Busicom 141-PF!") ;
  Serial.print("key buffer: ") ;
  Serial.println(KEYBOARD.getKeyBuffer()) ;
  
  RESET_INPUT ;
  SHIFT_DATA_INPUT ;
  KBD_SHIFT_CLK_INPUT ;
  attachInterrupt(digitalPinToInterrupt(3), kbd_clk, RISING) ;
  PRN_SHIFT_CLK_INPUT ;
  attachInterrupt(digitalPinToInterrupt(2), prn_clk, RISING) ;
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
  max_dur = 0 ;
}


void loop(){
  while (1){
    unsigned long start = micros() ;
    if (RESET_ON){
      Serial.println("RESET!!!") ;
      return reset() ;
    }

    PRINTER.loop() ;
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
