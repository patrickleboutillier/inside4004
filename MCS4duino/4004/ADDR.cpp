#include "ADDR.h"
#include "INST.h"

#define H 0
#define M 1 
#define L 2


static TIMING *timing ;
static DATA *data ;
static byte incr_in = 0 ;           // The input to the address incrementer
static bool cy = 0 ;                // The carry (in) for the address incrementer
static bool cy_out = 0 ;            // The carry (out) for the address incrementer
static byte ph = 0 ;                // The high nibble of the program counter 
static byte pl = 0 ;                // The middle nibble of the program counter
static byte pm = 0 ;                // The low nibble of the program counter
static byte sp = 0 ;                // The stack pointer
static byte row_num = 0 ;           // The working row in the stack
static byte stack[4][3] = {{0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}} ;


void ADDR_reset(){
  incr_in = 0 ;
  cy = 0 ;
  cy_out = 0 ;
  ph = 0 ;
  pl = 0 ;
  pm = 0 ;
  sp = 0 ;
  row_num = 0 ;
  for (int i = 0 ; i < 4 ; i++){
    for (int j = 0 ; j < 3 ; j++){
      stack[i][j] = 0 ;
    }
  }
}


void ADDR_setup(TIMING *t, DATA *d){
  timing = t ;
  data = d ;
  ADDR_reset() ;
  ADDR_timing() ;
}


void ADDR_timing(){
  auto f1 = []{
    incr_in = data->read() ;  
  } ;
  timing->M12(f1) ;
  timing->M22(f1) ;
  timing->A12clk1(f1) ;
  timing->A22clk1(f1) ;
  timing->A32clk1(f1) ;
  timing->X12clk1(f1) ;
  timing->X22clk1(f1) ;
  timing->X32clk1(f1) ;    // Sample data from the bus at these times.

  timing->A11([]{        // Output pl to the data bus.
    data->write(pl) ;
  }) ;
  
  timing->A21([]{        // Output pm to the data bus.
    data->write(pm) ;
  }) ;

  timing->A31([]{        // Output ph to the data bus.
    data->write(ph) ;
  }) ;

  timing->M11([]{        // Disconnect from bus
    data->z() ;
  }) ;
  
  timing->A12clk2([]{    // Increment pl
    byte sum = pl + 1 ;
    cy_out = sum >> 4 ;
    pl = sum & 0xF ;
  }) ;

  auto f2 = []{
    cy = cy_out ;
  } ;
  timing->A22clk1(f2) ;
  timing->A32clk1(f2) ;

  timing->A22clk2([]{    // Increment pm
    byte sum = pm + cy ;
    cy_out = sum >> 4 ;
    pm = sum & 0xF ;
  }) ;
  
  timing->A32clk2([]{    // Increment ph
    byte sum = ph + cy ;
    cy_out = sum >> 4 ;
    ph = sum & 0xF ;
  }) ;

  auto f3 = []{
    if (! inh()){
      ph = stack[row_num][H] ;
      pm = stack[row_num][M] ;
      pl = stack[row_num][L] ;
    }
  } ;
  timing->X12clk2(f3) ;
  timing->X32clk2(f3) ;       // Update the program counter with the contents of the stack.

  auto f4 = []{
    if (timing->x2() && inh()){
      return ;
    }
    if (! (fin() && !get_sc())){
      stack[row_num][H] = ph ;
      stack[row_num][M] = pm ;
      stack[row_num][L] = pl ;  
    }
  } ;
  timing->M12clk1(f4) ;
  timing->X22clk1(f4) ;        // Update the stack with the contents of the program counter. 

  timing->X32([]{              // Commit the stack pointer to row_num
    row_num = sp ;
  }) ;
} ;


void setPH(){
  ph = incr_in ;
}


void setPM(){
  pm = incr_in ;
}


void setPL(){
  pl = incr_in ;
}


// Decrement the stack pointer
void decSP(){
  sp = (sp - 1) & 0b11 ;
}


unsigned int getPC(){
  return ph << 8 | pm << 4 | pl ; 
}
