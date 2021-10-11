#ifndef INST_H
#define INST_H

#include "Arduino.h"
#include "TIMING.h"
#include "DATA.h"

void INST_reset() ;
void INST_setup(TIMING *t, DATA *d) ;
void INST_timing() ;

bool opa_odd() ;
bool opa_even() ;
bool jcn() ;
bool fim() ;
bool src() ;
bool fin() ;
bool jin() ;
bool jun() ;
bool jms() ;
bool isz() ;
bool io() ;
bool iow() ;
bool ior() ;
bool ld() ;
bool bbl() ;
bool ope() ;
bool tcs() ;
bool daa() ;
bool kbp() ;
bool inh() ;
bool get_sc() ;
byte get_opr() ;
byte get_opa() ;

#endif
