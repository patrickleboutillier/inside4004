#include "ALU.h"
#include "INST.h"

static TIMING *timing ;
static DATA *data ;
static byte acc = 0 ;               // The accumulator
static byte tmp = 0 ;               // The tmp register
static bool cy = 0 ;                // Carry
static byte ada = 0 ;               // Input A of the adder (4 bits)
static byte adb = 0 ;               // Input B of the adder (4 bits)
static bool adc = 0 ;               // Input C od the adder (1 bit)
static byte acc_out = 0 ;           // Accumulator output
static bool cy_out = 0 ;            // Carry output
static byte add = 0 ;               // The result of the adder (not a register in the real 4004 as the adder is combinational)


void ALU_reset(){
  acc = 0 ;
  tmp = 0 ;
  cy = 0 ;
  ada = 0 ;
  adb = 0 ;
  adc = 0 ;
  acc_out = 0 ;
  cy_out = 0 ;
  add = 0 ;
}


void ALU_setup(TIMING *t, DATA *d){
  timing = t ;
  data = d ;
  ALU_reset() ;
  ALU_timing() ;
}


void ALU_timing(){
  timing->M12([]{    // Initialize the ALU before each instruction
    ada = 0 ;
    tmp = 0xF ;
    adc = 0 ;
  }) ;
  
  timing->X12([]{    // Save acc and cy to their output registers. 
    acc_out = acc ;
    cy_out = cy ;
    #ifdef DEBUG
      if (timing->_pass == 0){
        Serial.print(timing->_cycle) ;  
        Serial.print(" acc_out ") ;
        Serial.print(acc_out) ;
        Serial.print(" cy_out ") ;
        Serial.println(cy_out) ;
      }
    #endif
  }) ;
          
  timing->X21([]{    // Set the bus with the proper initialization value, depending on the current instruction.
    if (ope()){
      enableInitializer() ;
    }
  }) ;
          
  timing->X22clk1([]{  // Set input B by sampling data from the bus (n0342, for non IO instructions).
    if (! io()){
      tmp = data->read() ;
      #ifdef DEBUG
        if (timing->_pass == 0){
          Serial.print(timing->_cycle) ;  
          Serial.print(" tmp ") ;
          Serial.println(tmp) ;
        }
      #endif
    }
  }) ;
  
  timing->X22clk2([]{  // Set input B by sampling data from the bus (n0342, for IO instructions).
    if (io()){
      tmp = data->read() ;
      #ifdef DEBUG
        if (timing->_pass == 0){
          Serial.print(timing->_cycle) ;  
          Serial.print(" tmp ") ;
          Serial.println(tmp) ;
        }
      #endif
    }
  }) ;
}


// The Adder implementation
void runAdder(bool invertADB, bool saveAcc, bool saveCy, bool shiftL, bool shiftR){
  adb = tmp ;
  if (invertADB){
    adb = ~adb & 0xF ;
  }

  add = ada + adb + adc ;
  bool co = add >> 4 ;
  add = add & 0xF ;

  if (shiftL){
    cy = add >> 3 ;
    acc = (add << 1 | cy_out) & 0xF ;
  }    
  else if (shiftR){
    cy = add & 1 ;
    acc = cy_out << 3 | add >> 1 ;
  }
  else {
    if (saveAcc){
      acc = add ;
    }
    if (saveCy){
      // WARNING: a bit of DAA logic here...
      if (daa() && (cy_out || acc_out > 9)){
        cy = 1 ;
      }
      else {
        cy = co ;
      }
    }
  }

  #ifdef DEBUG
    if (timing->_pass == 0){
      Serial.print(timing->_cycle) ; 
      Serial.print(" ") ;
      Serial.print(get_opr()) ;
      Serial.print(" ") ;
      Serial.print(get_opa()) ;
      Serial.print(" runAdder ") ;
      Serial.print(add) ;
      Serial.print(" ") ;   
      Serial.println(cy) ;   
    }
  #endif
}


// Set input A
void setADA(bool invert){
  ada = acc ;
  if (invert){
    ada = ~ada & 0xF ;
  }

  #ifdef DEBUG
    if (timing->_pass == 0){
      Serial.print(timing->_cycle) ; 
      Serial.print(" setADA ") ;
      Serial.println(ada) ;
    }
  #endif
}


// Set input C
void setADC(bool invert, bool one){
  if (one){
    adc = 1 ;
  }
  else {
    adc = cy ;
    if (invert){
      adc = ~adc & 1 ;
    }
  }

  #ifdef DEBUG
    if (timing->_pass == 0){
      Serial.print(timing->_cycle) ;
      Serial.print(" setADC ") ;
      Serial.println(adc) ;
    }
  #endif
}

      
// Place acc_out on the bus.
void enableAccOut(){
  data->write(acc_out) ;
  #ifdef DEBUG
    if (timing->_pass == 0){
      Serial.print(timing->_cycle) ;
      Serial.print(" enableAccOut ") ;
      Serial.println(acc_out) ;
    }
  #endif
}


// Place adder result on the bus
void enableAdd(){
  data->write(add) ;
  #ifdef DEBUG
    if (timing->_pass == 0){
      Serial.print(timing->_cycle) ;
      Serial.print(" enableAdd ") ;
      Serial.println(add) ;
    }
  #endif
}


// Place carry out on the bus
void enableCyOut(){
  data->write(cy_out) ;
  #ifdef DEBUG
    if (timing->_pass == 0){
      Serial.print(timing->_cycle) ;
      Serial.print(" enableCyOut ") ;
      Serial.println(cy_out) ;
    }
  #endif
}


// Bus initialization routine. This is really clever...
void enableInitializer(){
  byte d = 0 ;
  if (get_opa() >> 3){
    if (daa()){
      if (cy_out || acc_out > 9){
        d = 6 ;
      }
      else {
        d = 0 ;
      } 
    }
    else if (tcs()){
      d = 9 ;
    }
    else if (kbp()){
      if (acc_out == 4){
        d = 3 ;
      }
      else if (acc_out == 8){
        d = 4 ;
      }
      else if (acc_out > 2){
        d = 15 ;
      }
      else {
        d = acc_out ;
      }
    }
    else {
      d = 0xF ;
    } 
  }
  
  data->write(d) ;
  #ifdef DEBUG
    if (timing->_pass == 0){
      Serial.print(timing->_cycle) ;
      Serial.print(" enableInitializer ") ;
      Serial.println(d) ;
    }
  #endif
}


// Is acc == 0?
bool accZero(){
  #ifdef DEBUG
    if (timing->_pass == 0){
      Serial.print(timing->_cycle) ;
      Serial.print(" accZero ") ;
      Serial.println(acc_out == 0) ;
    }
  #endif
  return acc_out == 0 ;
}


// Is adder result == 0?
bool addZero(){
  #ifdef DEBUG
    if (timing->_pass == 0){
      Serial.print(timing->_cycle) ;
      Serial.print(" addZero ") ;
      Serial.println(add == 0) ;
    }
  #endif
  return add == 0 ;
}


// Is carry == 1?
bool carryOne(){
  #ifdef DEBUG
    if (timing->_pass == 0){
      Serial.print(timing->_cycle) ;
      Serial.print(" carryOne ") ;
      Serial.println(cy_out) ;
    }
  #endif
  return cy_out ;
}
