#include "CONTROL.h"
#include "CONTROL_TABLE.h"
#include "IO.h"
#include "PINS.h"
#include "SCRATCH.h"

static TIMING *timing ;
static DATA *data ;


void CONTROL_reset(){
}


void CONTROL_setup(TIMING *t, DATA *d){
  timing = t ;
  data = d ;
  CONTROL_reset() ;
  CONTROL_timing() ;
}


void CONTROL_timing(){
  timing->A12([]{     dispatch(0, 0) ; }) ;
  timing->M12clk2([]{ dispatch(3, 2) ; }) ;
  timing->M22clk2([]{ dispatch(4, 2) ; }) ;
  timing->X12clk1([]{ dispatch(5, 0) ; }) ;
  timing->X12clk2([]{ dispatch(5, 2) ; }) ;
  timing->X21([]{     dispatch(5, 3) ; }) ;
  timing->X22clk1([]{ dispatch(6, 0) ; }) ;
  timing->X22clk2([]{ dispatch(6, 2) ; }) ;
  timing->X31([]{     dispatch(6, 3) ; }) ;
  timing->X32clk1([]{ dispatch(7, 0) ; }) ;
  timing->X32clk2([]{ dispatch(7, 2) ; }) ;
}


void dispatch(byte t, byte c){
  long addr = get_opr() << 9 | get_opa() << 5 | t << 2 | c ;
  void (*f)() = (void (*)())pgm_read_ptr(control + addr) ;
  if (f != NULL){
    f() ;
  }
}


void NOP_X12clk1(){
} ;

void JCN_M12clk2(){
} ;

void JCN_M22clk2(){
} ;

void FIM_M12clk2(){
} ;

void FIM_M22clk2(){
} ;

void SRC_X21(){
  // enableRegPairH() ;
  //Serial.print(timing->_cycle) ;
  //Serial.println(" SRC CM on") ;
  CM(HIGH) ;
} ;

void SRC_X31(){
  // enableRegPairL() ;
  //Serial.print(timing->_cycle) ;
  //Serial.println(" SRC CM off") ;
  CM(LOW) ;
} ;

void FIN_M12clk2(){
} ;

void FIN_M22clk2(){
} ;

void FIN_X21(){
} ;

void FIN_X22clk2(){
} ;

void FIN_X31(){
} ;

void FIN_X32clk2(){
} ;

void JIN_X21(){
} ;

void JIN_X22clk2(){
} ;

void JIN_X31(){
} ;

void JIN_X32clk2(){
} ;

void JUN_M12clk2(){
} ;

void JUN_M22clk2(){
} ;

void JUN_X21(){
} ;

void JUN_X22clk2(){
} ;

void JMS_M12clk2(){
} ;

void JMS_M22clk2(){
} ;

void JMS_X21(){
} ;

void JMS_X22clk2(){
} ;

void INC_X21(){
} ;

void INC_X22clk1(){
} ;

void INC_X31(){
} ;

void INC_X32clk2(){
} ;

void ISZ_M12clk2(){
} ;

void ISZ_M22clk2(){
} ;

void ISZ_X21(){
} ;

void ISZ_X22clk1(){
} ;

void ISZ_X31(){
} ;

void ISZ_X32clk2(){
} ;

void ADD_X21(){
} ;

void ADD_X22clk1(){
} ;

void ADD_X31(){
} ;

void SUB_X21(){
} ;

void SUB_X22clk1(){
} ;

void SUB_X31(){
} ;

void LD_X21(){
} ;

void LD_X31(){
} ;

void XCH_X21(){
} ;

void XCH_X31(){
} ;

void XCH_X32clk2(){
} ;

void BBL_X22clk2(){
} ;

void BBL_X12clk2(){
} ;

void BBL_M22clk2(){
} ;

void BBL_X21(){
} ;

void BBL_X31(){
} ;

void LDM_X21(){
} ;

void LDM_X31(){
} ;

void WXX_X21(){
} ;

void SBM_X22clk2(){
} ;

void SBM_A12(){
} ;

void RXX_A12(){
} ;

void ADM_X22clk2(){
} ;

void ADM_A12(){
} ;

void CLB_X31(){
} ;

void CLC_X31(){
} ;

void IAC_X22clk1(){
} ;

void IAC_X31(){
} ;

void CMC_X22clk1(){
} ;

void CMC_X31(){
} ;

void CMA_X22clk1(){
} ;

void CMA_X31(){
} ;

void RAL_X22clk1(){
} ;

void RAL_X31(){
} ;

void RAR_X22clk1(){
} ;

void RAR_X31(){
} ;

void TCC_X22clk1(){
} ;

void TCC_X31(){
} ;

void DAC_X22clk1(){
} ;

void DAC_X31(){
} ;

void TCS_X22clk1(){
} ;

void TCS_X31(){
} ;

void STC_X22clk1(){
} ;

void STC_X31(){
} ;

void DAA_X22clk1(){
} ;

void DAA_X31(){
} ;

void KBP_X31(){
} ;

void DCL_X21(){
} ;
