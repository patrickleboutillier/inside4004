#ifndef INST_H
#define INST_H

#include "Arduino.h"
#include "TIMING.h"
#include "DATA.h"

extern bool INST_sc ;
extern bool INST_cond ;
extern byte INST_opr ;
extern byte INST_opa ;

void INST_reset() ;
void INST_setup(TIMING *t, DATA *d) ;
void INST_timing() ;

bool setJCNcond() ;


inline bool opa_odd() __attribute__((always_inline)) ;
bool opa_odd(){
    return INST_opa & 1 ;
}

inline bool opa_even() __attribute__((always_inline)) ;
bool opa_even(){
    return !(INST_opa & 1) ;
}

inline bool jcn() __attribute__((always_inline)) ;
bool jcn(){
    return INST_opr == 0b0001 ;
}

inline bool fim() __attribute__((always_inline)) ;
bool fim(){
    return (INST_opr == 0b0010) && !(INST_opa & 0b0001) ;
}

inline bool src() __attribute__((always_inline)) ;
bool src(){
    return (INST_opr == 0b0010) && (INST_opa & 0b0001) ;
}

inline bool fin() __attribute__((always_inline)) ;
bool fin(){
    return (INST_opr == 0b0011) && !(INST_opa & 0b0001) ;
}

inline bool jin() __attribute__((always_inline)) ;
bool jin(){
    return (INST_opr == 0b0011) && (INST_opa & 0b0001) ;
}

inline bool jun() __attribute__((always_inline)) ;
bool jun(){
    return INST_opr == 0b0100 ;
}

inline bool jms() __attribute__((always_inline)) ;
bool jms(){
    return INST_opr == 0b0101 ;
}

inline bool isz() __attribute__((always_inline)) ;
bool isz(){
    return INST_opr == 0b0111 ;
}

inline bool io() __attribute__((always_inline)) ;
bool io(){
    return INST_opr == 0b1110 ;
}

inline bool iow() __attribute__((always_inline)) ;
bool iow(){
    return io() && ((INST_opa >> 3) == 0) ;
}

inline bool ior() __attribute__((always_inline)) ;
bool ior(){
    return io() && ((INST_opa >> 3) == 1) ;
}

inline bool ld() __attribute__((always_inline)) ;
bool ld(){
    return INST_opr == 0b1010 ;
}

inline bool bbl() __attribute__((always_inline)) ;
bool bbl(){
    return INST_opr == 0b1100 ;
}

inline bool ope() __attribute__((always_inline)) ;
bool ope(){
    return INST_opr == 0b1111 ;
}

inline bool tcs() __attribute__((always_inline)) ;
bool tcs(){
    return (INST_opr == 0b1111) && (INST_opa == 0b1001) ;    
}

inline bool daa() __attribute__((always_inline)) ;
bool daa(){
    return (INST_opr == 0b1111) && (INST_opa == 0b1011) ;
}

inline bool kbp() __attribute__((always_inline)) ;
bool kbp(){
    return (INST_opr == 0b1111) && (INST_opa == 0b1100) ;   
}

inline bool inh() __attribute__((always_inline))  ;
// Inhibit program counter commit
// inh = (jin_fin & INST_sc) | ((jun_jms | (jcn_isz & INST_cond)) & ~INST_sc)
bool inh(){
    return ((jin() || fin()) && INST_sc) || (((jun() || jms()) || ((jcn() || isz()) && INST_cond)) && (! INST_sc)) ;
}

inline bool get_sc() __attribute__((always_inline)) ;
bool get_sc(){
  return INST_sc ;
}

inline byte get_opr() __attribute__((always_inline)) ;
byte get_opr(){
  return INST_opr ;
}

inline byte get_opa() __attribute__((always_inline)) ;
byte get_opa(){
  return INST_opa ;
}

#endif
