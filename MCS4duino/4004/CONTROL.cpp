#include "CONTROL.h"
#include "IO.h"
#include "ADDR.h"
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
} ;

void FIM_M22clk2(){
} ;

void SRC_X21(){
  // enableRegPairH() ;
  CMon() ;
} ;

void SRC_X31(){
  // enableRegPairL() ;
  CMoff() ;
} ;

void FIN_M12clk2(){
} ;

void FIN_M22clk2(){
} ;

void FIN_X21(){
} ;

void FIN_X22clk2(){
  if (get_sc()){
    setPM() ;
  }
} ;

void FIN_X31(){
} ;

void FIN_X32clk2(){
  if (get_sc()){
    setPL() ;
  }
} ;

void JIN_X21(){
} ;

void JIN_X22clk2(){
  setPM() ;
} ;

void JIN_X31(){
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
      // Order not important here since sp in not copied to row_num until x32
      setPL() ;
      decSP() ;
    }
} ;

void JMS_X21(){
} ;

void JMS_X22clk2(){
    if (! get_sc()){
      setPH() ;
    }
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


/*

        # NOP
        opr, opa = 0b0000, [0b0000]
        @X12clk1
        def _():
            pass

        # HLT
        opr, opa = 0b0000, [0b0001]
        @X12clk1
        def _():
            print("HALTED!")
            sys.exit()

        # ERR
        opr, opa = 0b0000, [0b0010]
        @X12clk1
        def _():
            sys.exit("ERROR!")

        # JCN
        opr, opa = 0b0001, any

        @M22clk2 
        def _():
            if not inst.sc:
                addr.setPL()

        # FIM
        opr, opa = 0b0010, even
        @M12clk2 
        def _():
            if not inst.sc:
                scratch.setRegPairH()
        @M22clk2 
        def _():
            if not inst.sc:
                scratch.setRegPairL()

        # SRC
        opr, opa = 0b0010, odd
        @X21
        def _():
            scratch.enableRegPairH()
            # ioc.cm_rom.v = 1
            # ioc.cm_ram.v = ioc.ram_bank & 1
        @X31
        def _():
            scratch.enableRegPairL()
            # ioc.cm_rom.v = 0
            # ioc.cm_ram.v = 0

        # FIN
        opr, opa = 0b0011, even
        @M12clk2 
        def _():
            if not inst.sc:
                scratch.setRegPairH()
        @M22clk2 
        def _():
            if not inst.sc:
                scratch.setRegPairL()
        @X21
        def _():
            if inst.sc:
                scratch.enableRegPairH()
        @X22clk2
        def _():
            if inst.sc:
                addr.setPM()
        @X31
        def _():
            if inst.sc:
                scratch.enableRegPairL()
        @X32clk2
        def _():
            if inst.sc:
                addr.setPL()

        # JIN
        opr, opa = 0b0011, odd
        @X21
        def _():
            scratch.enableRegPairH()
        @X22clk2
        def _():
            addr.setPM()
        @X31
        def _():
            scratch.enableRegPairL()
        @X32clk2
        def _():
            addr.setPL()

        # JUN
        opr, opa = 0b0100, any
        @M12clk2 
        def _():
            if not inst.sc:
                addr.setPM()
        @M22clk2 
        def _():
            if not inst.sc:
                addr.setPL()
        @X21
        def _():
            if not inst.sc:
                inst.data.v = inst.opa
        @X22clk2
        def _():
            if not inst.sc:
                addr.setPH()

        # JMS
        opr, opa = 0b0101, any 
        @M12clk2 
        def _():
            if not inst.sc:
                addr.setPM()
        @M22clk2 
        def _():
            if not inst.sc:
                # Order not important here since sp in not copied to row_num until x32
                addr.setPL()
                addr.decSP()
        @X21
        def _():
            if not inst.sc:
                inst.data.v = inst.opa
        @X22clk2
        def _():
            if not inst.sc:
                addr.setPH()

        # INC
        opr, opa = 0b0110, any
        @X21
        def _():
            scratch.enableReg()
        @X22clk1
        def _():
            alu.setADC(one=True)
        @X31
        def _():
            alu.runAdder()
            alu.enableAdd()
        @X32clk2
        def _():
            scratch.setReg()    

        # ISZ
        opr, opa = 0b0111, any
        @M12clk2 
        def _():
            if not inst.sc:
                addr.setPM()
        @M22clk2 
        def _():
            if not inst.sc:
                addr.setPL()
        @X21
        def _():
            if inst.sc:
                scratch.enableReg()
        @X22clk1
        def _():
            if inst.sc:
                alu.setADC(one=True)
        @X31
        def _():
            if inst.sc:
                alu.runAdder()
                alu.enableAdd()
        @X32clk2
        def _():
            if inst.sc:
                scratch.setReg()     

        # ADD
        opr, opa = 0b1000, any
        @X21
        def _():
            scratch.enableReg()
        @X22clk1
        def _():
            alu.setADA()
            alu.setADC()
        @X31
        def _():
            alu.runAdder(saveAcc=True, saveCy=True)

        # SUB
        opr, opa = 0b1001, any
        @X21
        def _():
            scratch.enableReg()
        @X22clk1
        def _():
            alu.setADA()
            alu.setADC(invert=True)
        @X31
        def _():
            alu.runAdder(invertADB=True, saveAcc=True, saveCy=True)

        # LD
        opr, opa = 0b1010, any
        @X21
        def _():
            scratch.enableReg()
        @X31
        def _():
            alu.runAdder(saveAcc=True)

        # XCH
        opr, opa = 0b1011, any
        @X21
        def _():
            scratch.enableReg()
        @X31
        def _():
            alu.runAdder(saveAcc=True)
            alu.enableAccOut()
        @X32clk2
        def _():
            scratch.setReg()

        # BBL
        opr, opa = 0b1100, any
        @M22clk2
        @X12clk2
        @X22clk2
        def _():
            addr.decSP()
        @X21
        def _():
            inst.data.v = inst.opa
        @X31
        def _():
            alu.runAdder(saveAcc=True)

        # LDM
        opr, opa = 0b1101, any
        @X21
        def _():
            inst.data.v = inst.opa
        @X31
        def _():
            alu.runAdder(saveAcc=True)


        # WRM, WMP, WRR, WR0/1/2/3
        opr, opa = 0b1110, [0b0000, 0b0001, 0b0010, 0b0100, 0b0101, 0b0110, 0b0111]
        @X21
        def _():
            inst.data.v = alu.acc

        # SBM
        opr, opa = 0b1110, [0b1000]
        @X22clk2
        def _():
            alu.setADA()
            alu.setADC(invert=True)
        @A12
        def _():
            alu.runAdder(invertADB=True, saveAcc=True, saveCy=True)

        # RDM, RDR, RD0/1/2/3
        opr, opa = 0b1110, [0b1001, 0b1010, 0b1100, 0b1101, 0b1110, 0b1111]
        @A12
        def _():
            alu.runAdder(saveAcc=True)

        # ADM
        opr, opa = 0b1110, [0b1011]
        @X22clk2
        def _():
            alu.setADA()
            alu.setADC()
        @A12
        def _():
            alu.runAdder(saveAcc=True, saveCy=True)


        # CLB
        opr, opa = 0b1111, [0b0000]
        @X31
        def _():
            alu.runAdder(saveAcc=True, saveCy=True)

        # CLC
        opr, opa = 0b1111, [0b0001]
        @X31
        def _():
            alu.runAdder(saveCy=True)

        # IAC
        opr, opa = 0b1111, [0b0010]
        @X22clk1
        def _():
            alu.setADA()
            alu.setADC(one=True)
        @X31
        def _():
            alu.runAdder(saveAcc=True, saveCy=True)

        # CMC
        opr, opa = 0b1111, [0b0011]
        @X22clk1
        def _():
            alu.setADC(invert=True)
        @X31
        def _():
            alu.runAdder(invertADB=True, saveCy=True)

        # CMA
        opr, opa = 0b1111, [0b0100]
        @X22clk1
        def _():
            alu.setADA(invert=True)
        @X31
        def _():
            alu.runAdder(saveAcc=True)

        # RAL
        opr, opa = 0b1111, [0b0101]
        @X22clk1
        def _():
            alu.setADA()
        @X31
        def _():
            alu.runAdder(shiftL=True)

        # RAR
        opr, opa = 0b1111, [0b0110]
        @X22clk1
        def _():
            alu.setADA()
        @X31
        def _():
            alu.runAdder(shiftR=True)
            
        # TCC
        opr, opa = 0b1111, [0b0111] 
        @X22clk1
        def _():
            alu.setADC()
        @X31
        def _():
            alu.runAdder(saveAcc=True, saveCy=True)

        # DAC
        opr, opa = 0b1111, [0b1000]
        @X22clk1
        def _():
            alu.setADA()
        @X31
        def _():
            alu.runAdder(saveAcc=True, saveCy=True)

        # TCS
        opr, opa = 0b1111, [0b1001]
        @X22clk1
        def _():
            alu.setADC()
        @X31
        def _():
            alu.runAdder(saveAcc=True, saveCy=True)

        # STC
        opr, opa = 0b1111, [0b1010]
        @X22clk1
        def _():
            alu.setADC(one=True)
        @X31
        def _():
            alu.runAdder(saveCy=True)

        # DAA
        opr, opa = 0b1111, [0b1011]
        @X22clk1
        def _():
            alu.setADA()
        @X31
        def _():
            alu.runAdder(saveAcc=True, saveCy=True)

        # KBP
        opr, opa = 0b1111, [0b1100]
        @X31
        def _():
            alu.runAdder(saveAcc=True)

        # DCL
        opr, opa = 0b1111, [0b1101]
        @X21
        def _():
            ioc.setRAMBank()

*/
