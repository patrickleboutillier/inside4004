#include "TIMING.h"
#include "ROM.h"
#include "i4003.h"
#include "KEYBOARD.h"

#define DEBUG

#define RESET_ON                PINC &   0b00100000
#define RESET_INPUT             DDRC &= ~0b00100000
#define CM_ON                   PINC &   0b00010000
#define CM_INPUT                DDRC &= ~0b00010000

#define DATA_3                  0b00000001 // PORTB
#define DATA_210                0b11100000 // PORTD
#define READ_DATA               (((PINB & DATA_3) << 3) | ((PIND & DATA_210) >> 5))
#define WRITE_DATA(data)        PORTB = (PORTB & ~DATA_3) | (((data) >> 3) & 1) ; PORTD = (PORTD & ~DATA_210) | (((data) & 0b111) << 5) 
#define DATA_INPUT              DDRB &= ~DATA_3 ; DDRD &= ~DATA_210
#define DATA_OUTPUT             DDRB |=  DATA_3 ; DDRD |=  DATA_210

#define READ_KBD_ROW            ((PINB &  0b00011110) >> 1)
#define KBD_ROW_INPUT           DDRB  &= ~0b00011110

#define READ_PRN_INDEX          ((PINC &  0b00000010) >> 1)
#define PRN_INDEX_INPUT         DDRC  &= ~0b00000010
#define READ_PRN_ADV_BTN        (PINC  &  0b00000001)
#define PRN_ADV_BTN_INPUT       DDRC  &= ~0b00000001

#define SHIFT_DATA              0b00100000
#define WRITE_SHIFT_DATA(d)     PORTB =  (PORTB & ~SHIFT_DATA) | ((d) << 5)
#define SHIFT_DATA_OUTPUT       DDRB  |=  SHIFT_DATA
#define WRITE_SHIFT_CLKS(p, k)  PORTC =  (PORTC & ~0b00001100) | ((p) << 3) | ((k) << 2)
#define SHIFT_CLKS_OUTPUT       DDRC  |=  0b00001100

TIMING TIMING ;
i4003 KSHIFT(0x3FF) ;
KEYBOARD KEYBOARD(&KSHIFT) ;

byte addrh = 0 ;        // The high nibble of the ROM address
byte addrl = 0 ;        // The low nibble of the ROM address
byte rom_select = 0 ;   // Which ROM chip is currently selected for instructions, default 0
int io_select = -1 ;    // Which ROM chip is currently selected for IO, default -1 (none) 
bool src = 0 ;          // An SRC instruction is under way
bool rdr = 0 ;          // An RDR instruction is under way
bool wrr = 0 ;          // A WRR instruction is under way
byte opr = 0 ;          // The OPR for the current instruction
byte opa = 0 ;          // The OPA for the current instruction
bool kb_toggle = 0 ;
unsigned long max_dur = 0 ;


void reset(){
  DATA_INPUT ;
  WRITE_SHIFT_DATA(0) ;
  WRITE_SHIFT_CLKS(0, 0) ;
            
  TIMING.reset() ;
  KSHIFT.reset() ;
  KEYBOARD.reset() ;
    
  addrh = 0 ;
  addrl = 0 ;
  rom_select = 0 ;
  io_select = -1 ;
  src = 0 ; 
  rdr = 0 ;
  wrr = 0 ;
  opr = 0 ;
  opa = 0 ;
  kb_toggle = 0 ;
  max_dur = 0 ;
}


void setup(){
  #ifdef DEBUG
    Serial.begin(2000000) ;
    Serial.println("4001") ;
  #endif
  RESET_INPUT ;
  CM_INPUT ;
  SHIFT_DATA_OUTPUT ;
  SHIFT_CLKS_OUTPUT ;
  PRN_INDEX_INPUT ;
  PRN_ADV_BTN_INPUT ;
  //KBD_ROW_INPUT ;
  TIMING.setup() ;
  KEYBOARD.setup() ;
  reset() ;

  
  TIMING.A12clk1([]{ 
    addrl = READ_DATA ;
  }) ;


  TIMING.A22clk1([]{
    addrh = READ_DATA ;
  }) ;

  
  TIMING.A32clk1([]{
    // If CM is on, the id of the selected ROM chip is on the bus
    if (CM_ON){
      rom_select = READ_DATA ;
    }
  }) ;  


  TIMING.M12clk1([]{
    // Send out OPR
    int pc = rom_select << 8 | addrh << 4 | addrl ;
    byte rom = pgm_read_byte(ROM + pc) ;
    opr = rom >> 4 ;
    opa = rom & 0xF ;
    DATA_OUTPUT ;
    WRITE_DATA(opr) ;
    #ifdef DEBUG
      //Serial.print(pc, HEX) ;
      //Serial.print(":") ;
      //Serial.print(opr, HEX) ;
      //Serial.println(opa, HEX) ;
    #endif
 
    /* if (pc == 3)){ // Before keyboard scanning in main loop
      kb_toggle = !kb_toggle ;
      if (! kb_toggle){
        sendKey() ;
      }
    } */
  }) ;

          
  TIMING.M22clk1([]{
    // Send out opa
    WRITE_DATA(opa) ;
  }) ;


  TIMING.M22clk2([]{
    // If there is a selected chip for IO and CM is on, check OPA to see the type of IO instruction
    // to be performed.
    if ((io_select != -1)&&(CM_ON)){
      rdr = (opa == 0b1010) ;
      wrr = (opa == 0b0010) ;
    }
    else {
      rdr = 0 ;
      wrr = 0 ;
    }
  }) ;

   
  TIMING.X12clk1([](){
    // Disconnect from bus
    DATA_INPUT ; 
  }) ;


  TIMING.X22clk1([]{
    // Is CM is on, an SRC instruction is being processed. Or else, perform the secified IO instruction
    // if required.
    if (CM_ON){
      src = 1 ;
      io_select = READ_DATA ;
    }
    else {
      src = 0 ;

      if (wrr){
        // Grab data for WRR
        if (io_select == 0){
          byte data = READ_DATA ;
          bool shift_data = bitRead(data, 1) ;
          bool kbd_clk = bitRead(data, 0) ;
          bool prn_clk = bitRead(data, 2) ;
          WRITE_SHIFT_DATA(shift_data) ;
          WRITE_SHIFT_CLKS(prn_clk, kbd_clk) ;
          if (kbd_clk){
              KSHIFT.onClock(shift_data) ; 
              KEYBOARD.setKbdRow() ;
          }
        }
      }
      else if (rdr){
        // Send data for RDR
        if (io_select == 1){
          byte data = KEYBOARD.getKbdRow() ; // READ_KBD_ROW ;
          DATA_OUTPUT ;
          WRITE_DATA(data) ;
        }
        else if (io_select == 2){ 
          byte data = (READ_PRN_ADV_BTN << 3) | READ_PRN_INDEX ;
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


void loop(){
  while (1){
    #ifdef DEBUG
        unsigned long start = micros() ;
    #endif
    if (RESET_ON){
      return reset() ;
    }

    TIMING.loop() ;
    KEYBOARD.loop() ;
    
    #ifdef DEBUG
      unsigned long dur = micros() - start ;
      if (dur > max_dur){
        max_dur = dur ;
        Serial.print(F("Max loop: ")) ;
        Serial.print(max_dur) ;
        Serial.println(F("us")) ;
      }
    #endif
  }
}
