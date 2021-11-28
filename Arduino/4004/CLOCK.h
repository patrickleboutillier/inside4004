#ifndef CLOCK_H
#define CLOCK_H

#include "Arduino.h"
#include "TIMING.h"
#include "DATA.h"

void CLOCK_reset() ;
void CLOCK_setup(TIMING *t) ;
void CLOCK_timing() ;
void CLOCK_tick() ;
void CLOCK_sleep(unsigned int dur) ;

#endif
