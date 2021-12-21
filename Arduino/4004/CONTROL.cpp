#include "CONTROL.h"
#include "IO.h"
#include "ADDR.h"
#include "SCRATCH.h"
#include "ALU.h"

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
  timing->A12clk1([]{     dispatch(0, 0) ; }) ;
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

                
void JCN_M12clk2(){
  if (!get_sc()){
    setPM() ;
  }
} ;

void JCN_M22clk2(){
  if (!get_sc()){
    setPL() ;
  }
} ;

void FIM_M12clk2(){
  if (! get_sc()){
    setRegPairH() ;
  }
} ;

void FIM_M22clk2(){
  if (! get_sc()){
    setRegPairL() ;
  }
} ;

void SRC_X21(){
  enableRegPairH() ;
  CMon() ;
} ;

void SRC_X31(){
  CMoff() ;
  enableRegPairL() ;
} ;

void FIN_M12clk2(){
  if (! get_sc()){
    setRegPairH() ;
  }  
} ;

void FIN_M22clk2(){
  if (! get_sc()){
    setRegPairL() ;
  }
} ;

void FIN_X21(){
  if (get_sc()){
    enableRegPairH() ;
  }
} ;

void FIN_X22clk2(){
  if (get_sc()){
    setPM() ;
  }
} ;

void FIN_X31(){
  if (get_sc()){
    enableRegPairL() ;
  }
} ;

void FIN_X32clk2(){
  if (get_sc()){
    setPL() ;
  }
} ;

void JIN_X21(){
  enableRegPairH() ;
} ;

void JIN_X22clk2(){
  setPM() ;
} ;

void JIN_X31(){
  enableRegPairL() ;
} ;

void JIN_X32clk2(){
  setPL() ;
} ;

void JUN_M12clk2(){
    if (! get_sc()){
      setPM() ;
    }
} ;

void JUN_M22clk2(){
    if (! get_sc()){
      setPL() ;
    }
} ;

void JUN_X21(){
    if (! get_sc()){
      data->write(get_opa()) ;
    }
} ;

void JUN_X22clk2(){
    if (! get_sc()){
      setPH() ;
    }
} ;

void JMS_M12clk2(){
    if (! get_sc()){
      setPM() ;
    }
} ;

void JMS_M22clk2(){
    if (! get_sc()){
      // Order not important here since sp is not copied to row_num until x32
      setPL() ;
      decSP() ;
    }
} ;

void JMS_X21(){
  if (! get_sc()){
    data->write(get_opa()) ;
  }
} ;

void JMS_X22clk2(){
    if (! get_sc()){
      setPH() ;
    }
} ;

void INC_X21(){
  enableReg() ;
} ;

void INC_X22clk1(){
  setADC(0, 1) ;
} ;

void INC_X31(){
  runAdder(0, 0, 0, 0, 0) ;
  enableAdd() ;
} ;

void INC_X32clk2(){
  setReg() ;
} ;

void ISZ_M12clk2(){
    if (! get_sc()){
      setPM() ;
    }
} ;

void ISZ_M22clk2(){
    if (! get_sc()){
      setPL() ;
    }
} ;

void ISZ_X21(){
  if (get_sc()){
    enableReg() ;
  }
} ;

void ISZ_X22clk1(){
  if (get_sc()){
    setADC(0, 1) ;
  }
} ;

void ISZ_X31(){
  if (get_sc()){
    runAdder(0, 0, 0, 0, 0) ;
    enableAdd() ;
  }
} ;

void ISZ_X32clk2(){
  if (get_sc()){
    setReg() ;
  }
} ;

void ADD_X21(){
  enableReg() ;
} ;

void ADD_X22clk1(){
  setADA(0) ;
  setADC(0, 0) ;
} ;

void ADD_X31(){
  runAdder(0, 1, 1, 0, 0) ;
} ;

void SUB_X21(){
  enableReg() ;
} ;

void SUB_X22clk1(){
  setADA(0) ;
  setADC(1, 0) ;
} ;

void SUB_X31(){
  runAdder(1, 1, 1, 0, 0) ;
} ;

void LD_X21(){
  enableReg() ;
} ;

void LD_X31(){
  runAdder(0, 1, 0, 0, 0) ;
} ;

void XCH_X21(){
  enableReg() ;
} ;

void XCH_X31(){
  runAdder(0, 1, 0, 0, 0) ;
  enableAccOut() ;
} ;

void XCH_X32clk2(){
  setReg() ;
} ;

void BBL_M22clk2(){
  decSP() ;
} ;

void BBL_X12clk2(){
  decSP() ;
} ;

void BBL_X22clk2(){
  decSP() ;
} ;

void BBL_X21(){
  data->write(get_opa()) ;
} ;

void BBL_X31(){
  runAdder(0, 1, 0, 0, 0) ;
} ;

void LDM_X21(){  
  data->write(get_opa()) ;
} ;

void LDM_X31(){
  runAdder(0, 1, 0, 0, 0) ;
} ;

void WXX_X21(){
  enableAccOut() ;
} ;

void SBM_X22clk2(){
  setADA(0) ;
  setADC(1, 0) ;
} ;

void SBM_A12(){
  runAdder(1, 1, 1, 0, 0) ;
} ;

void RXX_A12(){
  runAdder(0, 1, 0, 0, 0) ;
} ;

void ADM_X22clk2(){
  setADA(0) ;
  setADC(0, 0) ;
} ;

void ADM_A12(){
  runAdder(0, 1, 1, 0, 0) ;
} ;

void CLB_X31(){
  runAdder(0, 1, 1, 0, 0) ;
} ;

void CLC_X31(){
  runAdder(0, 0, 1, 0, 0) ;
} ;

void IAC_X22clk1(){
  setADA(0) ;
  setADC(0, 1) ;
} ;

void IAC_X31(){
  runAdder(0, 1, 1, 0, 0) ;
} ;

void CMC_X22clk1(){
  setADC(1, 0) ;
} ;

void CMC_X31(){
  runAdder(1, 0, 1, 0, 0) ;
} ;

void CMA_X22clk1(){
  setADA(1) ;
} ;

void CMA_X31(){
  runAdder(0, 1, 0, 0, 0) ;
} ;

void RAL_X22clk1(){
  setADA(0) ;
} ;

void RAL_X31(){
  runAdder(0, 0, 0, 1, 0) ;
} ;

void RAR_X22clk1(){
  setADA(0) ;
} ;

void RAR_X31(){
  runAdder(0, 0, 0, 0, 1) ;
} ;

void TCC_X22clk1(){
  setADC(0, 0) ;
} ;

void TCC_X31(){
  runAdder(0, 1, 1, 0, 0) ;
} ;

void DAC_X22clk1(){
  setADA(0) ;
} ;

void DAC_X31(){
  runAdder(0, 1, 1, 0, 0) ;  
} ;

void TCS_X22clk1(){
  setADC(0, 0) ;
} ;

void TCS_X31(){
  runAdder(0, 1, 1, 0, 0) ;
} ;

void STC_X22clk1(){
  setADC(0, 1) ;
} ;

void STC_X31(){
  runAdder(0, 0, 1, 0, 0) ;
} ;

void DAA_X22clk1(){
  setADA(0) ;
} ;

void DAA_X31(){
  runAdder(0, 1, 1, 0, 0) ;
} ;

void KBP_X31(){
  runAdder(0, 1, 0, 0, 0) ;
} ;

void DCL_X21(){
  setRAMBank() ;
} ;
