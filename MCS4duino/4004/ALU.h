#ifndef ALU_H
#define ALU_H

#include "Arduino.h"
#include "TIMING.h"
#include "DATA.h"

void ALU_reset() ;
void ALU_setup(TIMING *t, DATA *d) ;
void ALU_timing() ;

void setADA(bool invert) ;
void setADC(bool invert, bool one) ;
void enableAccOut() ;
void enableAdd() ;
void enableCyOut() ;
void enableInitializer() ;
bool accZero() ;
bool addZero() ;
bool carryOne() ;

#endif
