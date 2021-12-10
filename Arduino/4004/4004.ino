#include "TIMING.h"
#include "DATA.h"
#include "IO.h"
#include "INST.h"
#include "CONTROL.h"
#include "ADDR.h"
#include "SCRATCH.h"
#include "ALU.h"
#include "CLOCK.h"


#define READ_RESET  PIND &   0b01000000
#define RESET_INPUT DDRD &= ~0b01000000

#define LED                     0b00100000
#define LED_OUTPUT              DDRB |= LED
#define LED_ON                  PORTB |= LED
#define LED_OFF                 PORTB &= ~LED

TIMING TIMING ;
DATA DATA ;

unsigned int max_dur = 0 ;


void reset(){  
  LED_ON ;
  max_dur = 0 ;

  TIMING.reset() ;
  DATA.reset() ;
  INST_reset() ;
  CONTROL_reset() ;
  IO_reset() ;
  ADDR_reset() ;
  SCRATCH_reset() ;
  ALU_reset() ;
  CLOCK_reset() ;
  LED_OFF ;

}


void setup(){
  Serial.begin(2000000) ;
  Serial.println("4004") ;
  TCCR1A = 0 ;
  TCCR1B = 0 ;
  TCCR1C = 0 ;
  RESET_INPUT ;
  LED_OUTPUT ;
  
  INST_setup(&TIMING, &DATA) ;
  CONTROL_setup(&TIMING, &DATA) ;
  IO_setup(&TIMING) ;
  ADDR_setup(&TIMING, &DATA) ;
  SCRATCH_setup(&TIMING, &DATA) ;
  ALU_setup(&TIMING, &DATA) ;
  TIMING.setup() ;
  CLOCK_setup(&TIMING) ;
  reset() ;
}


void loop(){
  while (1){
    if (READ_RESET){
      return reset() ;
    }

    CLOCK_period() ;
  }
}
