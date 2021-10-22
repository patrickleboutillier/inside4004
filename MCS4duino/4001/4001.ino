#include "TIMING.h"
#include "ROM.h"

#define READ_RESET          PINC &   0b00100000
#define RESET_INPUT         DDRC &= ~0b00100000
#define READ_CM             PINC &   0b00010000
#define CM_INPUT            DDRC &= ~0b00010000

#define DATA_3              0b00000001 // PORTB
#define DATA_210            0b11100000 // PORTD
#define READ_DATA           (((PINB & DATA_3) << 3) | ((PIND & DATA_210) >> 5))
#define WRITE_DATA(data)    PORTB = (PORTB & ~DATA_3) | ((data >> 3) & 1) ; PORTD = (PORTD & ~DATA_210) | ((data & 0b111) << 5) 
#define DATA_INPUT          DDRB &= ~DATA_3 ; DDRD &= ~DATA_210
#define DATA_OUTPUT         DDRB |=  DATA_3 ; DDRD |=  DATA_210

#define SHIFT               0b00111000
#define WRITE_SHIFT(data)   PORTB = (PORTB & ~SHIFT) | (data << 3) 
#define SHIFT_OUTPUT        DDRB  |=  SHIFT

#define READ_PRN_INDEX      PINB  &   0b00000100
#define PRN_INDEX_INPUT     DDRB  &= ~0b00000100
#define READ_PRN_ADV_BTN    PINB  &   0b00000010
#define PRN_ADV_BTN_INPUT   DDRB  &= ~0b00000010
#define READ_KBD_ROW        PINC  &   0b00001111
#define KBD_ROW_INPUT       DDRC  &= ~0b00001111

TIMING TIMING ;

byte addrh = 0 ;  // The high nibble of the ROM address
byte addrl = 0 ;  // The low nibble of the ROM address
byte rom_select = 0 ;
int io_select = -1 ;
bool io_inst = 0 ;
bool src = 0 ;
bool rdr = 0 ;
bool wrr = 0 ;


void reset(){
  DATA_INPUT ;
  
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
  RESET_INPUT ;
  CM_INPUT ;
  SHIFT_OUTPUT ;
  PRN_INDEX_INPUT ;
  PRN_ADV_BTN_INPUT ;
  KBD_ROW_INPUT ;
  TIMING.setup() ;
  reset() ;

  
  TIMING.A12clk1([]{ 
    addrl = READ_DATA ;
  }) ;


  TIMING.A22clk1([]{
    addrh = READ_DATA ;
  }) ;

  
  TIMING.A32clk1([]{
    // If cm is on, we are the selected ROM chip for instructions if chipnum == data
    if (READ_CM){
      rom_select = READ_DATA ;
    }
  }) ;  


  TIMING.M12clk1([]{
    DATA_OUTPUT ;
    // If we are the selected chip for instructions, send out opr
    int addr = (rom_select << 8) + (addrh << 4 | addrl) ;
    byte opr = pgm_read_byte(ROM + addr) >> 4 ;
    WRITE_DATA(opr) ;
  }) ;


  TIMING.M12clk2([]{
    // opr is on the bus, no matter who put it there (us or another ROM chip). Check if an I/O instruction is in progress
    io_inst = (READ_DATA == 0b1110 ? 1 : 0) ;
  }) ;

          
  TIMING.M22clk1([]{
    // If we are the selected chip for instructions, send out opa
    int addr = (rom_select << 8) + (addrh << 4 | addrl) ;
    byte opa = pgm_read_byte(ROM + addr) & 0xF ;
    WRITE_DATA(opa) ;
  }) ;


  TIMING.M22clk2([]{
    // opa is on the bus, no matter who put it there (us or another ROM chip). 
    byte data = READ_DATA ;
    rdr = (io_inst && (data == 0b1010) ? 1 : 0) ;
    wrr = (io_inst && (data == 0b0010) ? 1 : 0) ;
  }) ;

   
  TIMING.X12clk1([](){
    // Disconnect from bus
    DATA_INPUT ; 
  }) ;


  TIMING.X22clk1([]{
    if (READ_CM){
      io_select = READ_DATA ;
      src = 1 ;
    }
    else {
      src = 0 ;
      if (wrr){
        // Grab data for WRR
        if (io_select == 0){
          byte data = READ_DATA ;
          WRITE_SHIFT(data) ;
        }
      }
      else if (rdr){
        // Send data for RDR
        if (io_select == 1){
          byte data = READ_KBD_ROW ;
          DATA_OUTPUT ;
          WRITE_DATA(data) ;
        }
        else if (io_select == 2){ 
          byte data = ((READ_PRN_ADV_BTN) << 2) | ((READ_PRN_INDEX) >> 2) ;
          DATA_OUTPUT ;
          WRITE_DATA(data) ;
        }
      }
    }
  }) ;

                        
  TIMING.X32clk1([]{
    if (rdr){
      // Disconnect from bus
      DATA_INPUT ;
    }
  }) ;
}


unsigned long max_dur = 0 ;
void loop(){
  while (1){
    unsigned long start = micros() ;
    if (READ_RESET){
      return reset() ;
    }

    TIMING.loop() ;
    unsigned long dur = micros() - start ;
    if (dur > max_dur){
      max_dur = dur ;
      Serial.print("Max loop duration: ") ;
      Serial.print(max_dur) ;
      Serial.println("us") ;
    }
  }
}
