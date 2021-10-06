#include "TIMING.h"
#include "ROM.h"

#define RESET   A5
#define CM      A4
#define CLK1    4
#define CLK2    3
#define SYNC    2
#define DATA_3  8
#define DATA_2  7
#define DATA_1  6
#define DATA_0  5
#define SHFT_DATA     13
#define KBD_SHFT_CLK  12
#define PRN_SHFT_CLK  11
#define PRN_INDEX     10
#define PRN_ADV_BTN   9

#define KBD_ROW_3     A0
#define KBD_ROW_2     A1
#define KBD_ROW_1     A2
#define KBD_ROW_0     A3

TIMING TIMING(CLK1, CLK2, SYNC) ;

byte addrh = 0 ;  // The high nibble of the ROM address
byte addrl = 0 ;  // The low nibble of the ROM address
byte rom_select = 0 ;
int io_select = -1 ;
bool io_inst = 0 ;
bool src = 0 ;
bool rdr = 0 ;
bool wrr = 0 ;


void reset(){
  pinMode(DATA_3, INPUT) ;
  pinMode(DATA_2, INPUT) ;
  pinMode(DATA_1, INPUT) ;
  pinMode(DATA_0, INPUT) ;   
  
  TIMING.reset() ;
  addrh = 0 ;
  addrl = 0 ;
  rom_select = 0 ;
  io_select = -1 ;
  io_inst = 0 ;
  src = 0 ; 
  rdr = 0 ;
  wrr = 0 ;
}


void setup(){
  Serial.begin(115200) ;
  Serial.println("4001") ;
  pinMode(RESET, INPUT) ;
  pinMode(CM, INPUT) ;
  pinMode(CLK1, INPUT) ;
  pinMode(CLK2, INPUT) ;
  pinMode(SYNC, INPUT) ;
  pinMode(KBD_SHFT_CLK, OUTPUT) ;
  pinMode(SHFT_DATA, OUTPUT) ;
  pinMode(PRN_SHFT_CLK, OUTPUT) ;
  pinMode(PRN_INDEX, INPUT) ;
  pinMode(PRN_ADV_BTN, INPUT) ;
  pinMode(KBD_ROW_3, INPUT) ;
  pinMode(KBD_ROW_2, INPUT) ;
  pinMode(KBD_ROW_1, INPUT) ;
  pinMode(KBD_ROW_0, INPUT) ;
  reset() ;

  
  TIMING.A12clk1([]{ 
    addrl = read_data() ;
  }) ;


  TIMING.A22clk1([]{
    addrh = read_data() ;
  }) ;

  
  TIMING.A32clk1([]{
    // If cm is on, we are the selected ROM chip for instructions if chipnum == data
    if (digitalRead(CM)){
      rom_select = read_data() ;
    }
  }) ;  


  TIMING.M12clk1([]{
    pinMode(DATA_3, OUTPUT) ;
    pinMode(DATA_2, OUTPUT) ;
    pinMode(DATA_1, OUTPUT) ;
    pinMode(DATA_0, OUTPUT) ;  
    // If we are the selected chip for instructions, send out opr
    int addr = (rom_select * 256) + (addrh << 4 | addrl) ;
    byte opr = pgm_read_byte(ROM + addr) >> 4 ;
    write_data(opr) ;
  }) ;


  TIMING.M12clk2([]{
    // opr is on the bus, no matter who put it there (us or another ROM chip). Check if an I/O instruction is in progress
    io_inst = (read_data() == 0b1110 ? 1 : 0) ;
  }) ;

          
  TIMING.M22clk1([]{
    // If we are the selected chip for instructions, send out opa
    int addr = (rom_select * 256) + (addrh << 4 | addrl) ;
    byte opa = pgm_read_byte(ROM + addr) & 0xF ;
    write_data(opa) ;
  }) ;


  TIMING.M22clk2([]{
    // opa is on the bus, no matter who put it there (us or another ROM chip). 
    byte data = read_data() ;
    rdr = (io_inst && (data == 0b1010) ? 1 : 0) ;
    wrr = (io_inst && (data == 0b0010) ? 1 : 0) ;
  }) ;

   
  TIMING.X12clk1([](){
    // Disconnect from bus
    pinMode(DATA_3, INPUT) ;
    pinMode(DATA_2, INPUT) ;
    pinMode(DATA_1, INPUT) ;
    pinMode(DATA_0, INPUT) ;  
  }) ;


  TIMING.X22clk1([]{
    if (digitalRead(CM)){
      io_select = read_data() ;
      src = 1 ;
    }
    else {
      src = 0 ;
      if (wrr){
        // Grab data for WRR
        if (io_select == 0){
          digitalWrite(SHFT_DATA, digitalRead(DATA_1)) ;
          digitalWrite(KBD_SHFT_CLK, digitalRead(DATA_0)) ;
          digitalWrite(PRN_SHFT_CLK, digitalRead(DATA_2)) ;
        }
      }
      else if (rdr){
        // Send data for RDR
        if (io_select == 1){
          /* byte data = (digitalRead(KBD_ROW_3) << 3) | (digitalRead(KBD_ROW_2) << 2) | 
            (digitalRead(KBD_ROW_1) << 1) | digitalRead(KBD_ROW_0) ;
          pinMode(DATA_3, OUTPUT) ;
          pinMode(DATA_2, OUTPUT) ;
          pinMode(DATA_1, OUTPUT) ;
          pinMode(DATA_0, OUTPUT) ; 
          write_data(data) ; */
        }
        else if (io_select == 2){ 
          byte data = (digitalRead(PRN_ADV_BTN) << 3) | digitalRead(PRN_INDEX) ;
          pinMode(DATA_3, OUTPUT) ;
          pinMode(DATA_2, OUTPUT) ;
          pinMode(DATA_1, OUTPUT) ;
          pinMode(DATA_0, OUTPUT) ; 
          write_data(data) ; 
          /* Serial.print("RDR ") ;
          Serial.print(TIMING._cycle) ;
          Serial.print(" ") ;
          Serial.println(data) ; */
        }
      }
    }
  }) ;

                        
  TIMING.X32clk1([]{
    if (rdr){
      // Disconnect from bus
      pinMode(DATA_3, INPUT) ;
      pinMode(DATA_2, INPUT) ;
      pinMode(DATA_1, INPUT) ;
      pinMode(DATA_0, INPUT) ; 
    }
  }) ;
}


void loop(){
  if (digitalRead(RESET)){
    return reset() ;
  }

  TIMING.loop() ;
}


byte read_data(){
  return (digitalRead(DATA_3) << 3) | (digitalRead(DATA_2) << 2) | 
    (digitalRead(DATA_1) << 1) | digitalRead(DATA_0) ;
}


void write_data(byte data){
  digitalWrite(DATA_3, (data >> 3) & 1) ;
  digitalWrite(DATA_2, (data >> 2) & 1) ;
  digitalWrite(DATA_1, (data >> 1) & 1) ;
  digitalWrite(DATA_0, data & 1) ;
}
