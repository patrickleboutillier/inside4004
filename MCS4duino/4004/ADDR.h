#ifndef ADDR_H
#define ADDR_H

#include "Arduino.h"
#include "TIMING.h"
#include "DATA.h"

void ADDR_reset() ;
void ADDR_setup(TIMING *t, DATA *d) ;
void ADDR_timing() ;

void setPH() ;
void setPM() ;
void setPL() ;
void decSP() ;

#endif
