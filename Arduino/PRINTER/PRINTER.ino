#include "i4003.h"
#include "PRINTER.h"

#define RESET_ON              PORTC |=  0b00000100
#define RESET_OFF             PORTC &= ~0b00000100
#define RESET_OUTPUT          DDRC  |=  0b00000100

#define SHIFT_DATA            0b00001000
#define SHIFT_DATA_ON         (PIND & SHIFT_DATA)
#define SHIFT_DATA_INPUT      DDRD &= ~SHIFT_DATA
#define PRN_SHIFT_CLK         0b00000100
#define PRN_SHIFT_CLK_ON      (PIND & PRN_SHIFT_CLK)
#define PRN_SHIFT_CLK_INPUT   DDRD &= ~PRN_SHIFT_CLK

i4003 PSHIFT(0xFFFFF) ;
PRINTER PRINTER(&PSHIFT) ;

unsigned long max_dur = 0 ;


void reset(){
  PSHIFT.reset() ;
  PRINTER.reset() ;
  max_dur = 0 ;
}


void setup(){
  RESET_OUTPUT ;
  RESET_ON ;
  
  Serial.begin(2000000) ;
  Serial.println("Welcome to Busicom 141-PF!") ;
  
  SHIFT_DATA_INPUT ;
  PRN_SHIFT_CLK_INPUT ;
  PRINTER.setup() ;

  Serial.print("Sending reset signal... ") ;
  delay(1000) ;
  reset() ;
  delay(1000) ;
  Serial.println("done. ") ;
  RESET_OFF ;
}


void loop(){
  while (1){
    noInterrupts() ;
    bool data = SHIFT_DATA_ON ;
    PSHIFT.loop(PRN_SHIFT_CLK_ON, data) ;
    bool worked = PRINTER.loop() ;
    interrupts() ;
    if (! worked){  
      PRINTER.printChar() ;
    }
  }
}
