#include "SCRATCH.h"
#include "INST.h"

static TIMING *timing ;
static DATA *data ;
static byte index_reg[16] ;          // The actual registers
static byte row_num = 0 ;            // The working row number
static byte row_even = 0 ;           // The even register in the working row
static byte row_odd = 0 ;            // The odd register in the working row
static byte data_in = 0 ;            // Data in from the bus


void SCRATCH_reset(){
  for (int i = 0 ; i < 16 ; i++){
    index_reg[i] = 0 ;  
  }
  row_num = 0 ; 
  row_even = 0 ; 
  row_odd = 0 ;  
  data_in = 0 ; 
}


void SCRATCH_setup(TIMING *t, DATA *d){
  timing = t ;
  data = d ;
  SCRATCH_reset() ;
  SCRATCH_timing() ;
}


void SCRATCH_timing(){
  auto f1 = []{
    data_in = data->read() ;  
  } ;
  timing->M12(f1) ;
  timing->M22(f1) ;
  timing->A12clk1(f1) ;
  timing->A22clk1(f1) ;
  timing->A32clk1(f1) ;
  timing->X12clk1(f1) ;
  timing->X22clk1(f1) ;
  timing->X32clk1(f1) ;    // Sample data from the bus at these times.


  auto f2 = []{            // Set working row from the register array. There is a 0 override for FIN during X12.
    if (get_sc()){
      byte r = row_num << 1 ;
      if (timing->x1()){
        // WARNING: a bit of FIN logic here...
        if (fin()){
          r = 0 ;  
        }
      }
      row_even = index_reg[r] ;
      row_odd = index_reg[r + 1] ;
    }
  } ;
  timing->A32clk2(f2) ;
  timing->X12clk2(f2) ;    


  auto f3 = []{
    if (get_sc()){
      byte r = row_num << 1 ;
      index_reg[r] = row_even ;
      index_reg[r + 1] = row_odd ;
    }
  } ;
  timing->A12clk2(f3) ;
  timing->M12clk2(f3) ;


  timing->M22clk2([]{    // Read OPA from the data bus and set the working row.
    if (get_sc()){
      row_num = data->read() >> 1 ;
    }
  }) ;
}


// Enable the working register (according to whether OPA is even or odd) to the bus.
void enableReg(){
  data->write(opa_even() ? row_even : row_odd) ;
  //if (timing->_pass == 0){
  //  Serial.print(timing->_cycle) ;
  //  Serial.print(" enableReg ") ;
  //  Serial.println(opa_even() ? row_even : row_odd) ;
  //}
}

// Enable the even working register to the bus.
void enableRegPairH(){
  data->write(row_even) ;
  //if (timing->_pass == 0){
  //  Serial.print(timing->_cycle) ;
  //  Serial.print(" enableRegPairH ") ;
  //  Serial.println(row_even) ;
  //}
}

// Enable the odd working register to the bus.
void enableRegPairL(){
  data->write(row_odd) ;
  //if (timing->_pass == 0){
  //  Serial.print(timing->_cycle) ;
  //  Serial.print(" enableRegPairL ") ;
  //  Serial.println(row_odd) ;
  //}
}

// Set the proper working register value from data_in.
void setReg(){
  if (opa_even()){
      row_even = data_in ;
  }
  else {
      row_odd = data_in ;
  }
  //if (timing->_pass == 0){
  //  Serial.print(timing->_cycle) ;
  //  Serial.print(" setReg ") ;
  //  Serial.print(opa_even()) ;
  //  Serial.print(" ") ;
  //  Serial.println(data_in) ;
  //}
}

// Set the even (high) working register from data_in
void setRegPairH(){
  row_even = data_in ;
  //if (timing->_pass == 0){
  //  Serial.print(timing->_cycle) ;
  //  Serial.print(" setRegPairH ") ;
  //  Serial.println(row_even) ;
  //}
}

// Set the odd (low) working register from data_in
void setRegPairL(){
  row_odd = data_in ;
  //if (timing->_pass == 0){
  //  Serial.print(timing->_cycle) ;
  //  Serial.print(" setRegPairL ") ;
  //  Serial.println(row_odd) ;
  //}
}
