#include "ADDR.h"

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


/*

class addr:
    def __init__(self, inst, timing, data):
data = data            # The data bus 
inst = inst
inst.addr = self
incr_in = 0            # The input to the address incrementer
cy = 0                 # The carry (in) for the address incrementer
cy_out = 0             # The carry (out) for the address incrementer
ph = 0                 # The high nibble of the program counter 
pl = 0                 # The middle nibble of the program counter
pm = 0                 # The low nibble of the program counter
sp = 0                 # The stack pointer
row_num = 0            # The working row in the stack
stack = [{'h':0, 'm':0, 'l':0}, {'h':0, 'm':0, 'l':0}, {'h':0, 'm':0, 'l':0}, {'h':0, 'm':0, 'l':0}]

timing = timing

        @M12
        @M22
        @A12clk1
        @A22clk1
        @A32clk1
        @X12clk1
        @X22clk1
        @X32clk1    # Sample data from the bus at these times.
        def _():
    incr_in = self.data.v

        @A11        # Output pl to the data bus.
        def _():
    data.v = self.pl

        @A21        # Output pm to the data bus.
        def _():
    data.v = self.pm

        @A31        # Output ph to the data bus.
        def _():
    data.v = self.ph

        @M11    # Disconnect from bus
        def _():
    data.v = None

        @A12clk2    # Increment pl
        def _():
            sum = self.pl + 1
    cy_out = sum >> 4
    pl = sum & 0xF

        @A22clk1
        @A32clk1
        def _():
    cy = self.cy_out

        @A22clk2    # Increment pm
        def _():
            sum = self.pm + self.cy
    cy_out = sum >> 4
    pm = sum & 0xF

        @A32clk2    # Increment ph
        def _():
            sum = self.ph + self.cy
    cy_out = sum >> 4
    ph = sum & 0xF

        @X12clk2
        @X32clk2       # Update the program counter with the contents of the stack.
        def _():
            if not self.inst.inh():
        ph = self.stack[self.row_num]['h']
        pm = self.stack[self.row_num]['m']
        pl = self.stack[self.row_num]['l']
                #print("restored", self.ph << 8 | self.pm << 4 | self.pl)

        @M12clk1
        @X22clk1        # Update the stack with the contents of the program counter. 
        def _():
            if self.timing.x2() and self.inst.inh:
                return
            if not (self.inst.fin() and not self.inst.sc):
                #print("commit", self.timing.slave, self.ph << 8 | self.pm << 4 | self.pl)
        stack[self.row_num]['h'] = self.ph
        stack[self.row_num]['m'] = self.pm
        stack[self.row_num]['l'] = self.pl

        @X32            # Commit the stack pointer to row_num
        def _():
    row_num = self.sp

    # Used in the calculator simulator to check the value of the program counter. 
    def isPCin(self, addrs):
        pc = self.ph << 8 | self.pm << 4 | self.pl
        for addr in addrs:
            if pc == addr:
                return True
        return False

    def setPH(self):
ph = self.incr_in

    def setPM(self):
pm = self.incr_in

    def setPL(self):
pl = self.incr_in

    # Increment the stack pointer
    def decSP(self):
sp = (self.sp - 1) & 0b11

 */
