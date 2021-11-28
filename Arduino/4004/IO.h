#ifndef IO_H
#define IO_H

#include "Arduino.h"
#include "TIMING.h"

#define CM_ON     PORTB |=  0b00000001
#define CM_OFF    PORTB &= ~0b00000001
#define CM_OUTPUT DDRB  |=  0b00000001

#define TEST_ON       (PINB &   0b00000010)
#define TEST_INPUT    DDRB  &= ~0b00000010



void IO_reset() ;
void IO_setup(TIMING *t) ;
void IO_timing() ;

inline void CMon() __attribute__((always_inline)) ;
void CMon(){
  CM_ON ;
}

inline void CMoff() __attribute__((always_inline)) ;
void CMoff(){
  CM_OFF ;
}

inline bool testZero() __attribute__((always_inline)) ;
bool testZero(){
  return !TEST_ON ;
}

inline void setRAMBank() __attribute__((always_inline)) ;
void setRAMBank(){
  // TODO: but not used in the calculator
}

#endif
