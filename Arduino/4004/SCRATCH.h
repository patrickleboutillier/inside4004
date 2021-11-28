#ifndef SCRATCH_H
#define SCRATCH_H

#include "Arduino.h"
#include "TIMING.h"
#include "DATA.h"

void SCRATCH_reset() ;
void SCRATCH_setup(TIMING *t, DATA *d) ;
void SCRATCH_timing() ;

void enableReg() ;
void enableRegPairH() ;
void enableRegPairL() ;
void setReg() ;
void setRegPairH() ;
void setRegPairL() ;

#endif
