#ifndef IO_H
#define IO_H

#include "Arduino.h"
#include "TIMING.h"

#define CM_ROM_ON     PORTC |=  0b00000001
#define CM_ROM_OFF    PORTC &= ~0b00000001
#define CM_ROM_OUTPUT DDRC  |=  0b00000001
#define CM_RAM_ON     PORTC |=  0b00010000
#define CM_RAM_OFF    PORTC &= ~0b00010000
#define CM_RAM_OUTPUT DDRC  |=  0b00010000

#define READ_TEST     PIND  &   0b10000000
#define TEST_INPUT    DDRD  &= ~0b10000000



void IO_reset() ;
void IO_setup(TIMING *t) ;
void IO_timing() ;

inline void CMon() __attribute__((always_inline)) ;
void CMon(){
  CM_ROM_ON ;
  CM_RAM_ON ;
}

inline void CMoff() __attribute__((always_inline)) ;
void CMoff(){
  CM_ROM_OFF ;
  CM_RAM_OFF ;
}

inline bool testZero() __attribute__((always_inline)) ;
bool testZero(){
  return !(READ_TEST) ;
}

inline void setRAMBank() __attribute__((always_inline)) ;
void setRAMBank(){
  // TODO: but not used in the calculator
}

#endif
