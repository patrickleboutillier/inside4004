#ifndef IO_H
#define IO_H

#include "Arduino.h"
#include "TIMING.h"

void IO_reset() ;
void IO_setup(TIMING *t) ;
void IO_timing() ;

void CM(bool v) ;
bool testZero() ;

#endif
