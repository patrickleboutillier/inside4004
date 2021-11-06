#include "TIMING.h"

#define DEBUG

#define READ_RESET       PINC &   0b00000010
#define RESET_INPUT      DDRC &= ~0b00000010
#define READ_CM          PINC &   0b00000001
#define CM_INPUT         DDRC &= ~0b00000001
#define DATA             0b00111100 // PORTD
#define READ_DATA        ((PIND & DATA) >> 2)
#define WRITE_DATA(data) PORTD = ((PORTD & ~DATA) | (data << 2))  
#define DATA_INPUT       DDRD &= ~DATA
#define DATA_OUTPUT      DDRD |=  DATA

#define PRN_ADV_FIRE_COLOR          0b00111000
#define WRITE_ADV_FIRE_COLOR(data)  PORTC  = ((PORTC & ~PRN_ADV_FIRE_COLOR) | (data << 3))  
#define PRN_ADV_FIRE_COLOR_OUTPUT   DDRC  |= PRN_ADV_FIRE_COLOR

TIMING TIMING ;

byte reg = 0 ;
byte chr = 0 ;
bool src = 0 ;
byte opa = 0 ;
int chip_select = -1 ;
bool ram_inst = 0 ;
byte RAM[4][4][16] ;
byte STATUS[4][4][4] ;
unsigned long max_dur = 0 ;


void reset(){
  DATA_INPUT ;   
  
  TIMING.reset() ;
  reg = 0 ;
  chr = 0 ;
  src = 0 ;
  opa = 0 ;
  chip_select = -1 ;
  max_dur = 0 ;

  for (int i = 0 ; i < 4  ; i++){
    for (int j = 0 ; j < 4 ; j++){
      for (int k = 0 ; k < 16 ; k++){
        RAM[i][j][k] = 0 ; 
        if (k < 4){
          STATUS[i][j][k] = 0 ; 
        }
      }
    }
  }
  
  WRITE_ADV_FIRE_COLOR(0) ;
}


void setup(){
  #ifdef DEBUG
    Serial.begin(2000000) ;
    Serial.println("4002") ;
  #endif
  RESET_INPUT ;
  CM_INPUT ;
  PRN_ADV_FIRE_COLOR_OUTPUT ;
  TIMING.setup() ;
  reset() ;


  TIMING.M22clk2([]{
    // Timing a tight here, we need to check only the first time around
    //if (TIMING._pass == 0){
      // Grab opa
      opa = READ_DATA ;
      if ((chip_select != -1)&&(READ_CM)){
        // If we are the selected chip for RAM/I/O and cm is on, the CPU is telling us that we are processing a RAM/I/O instruction
        ram_inst = 1 ;
      }
      else {
        ram_inst = 0 ;
      }
    //}
  }) ;


  TIMING.X22clk1([]{
    if (READ_CM){
      // An SRC instruction is in progress
      byte data = READ_DATA ;
      chip_select = data >> 2 ;
      // Grab the selected RAM register
      reg = data & 0b0011 ;
      src = 1 ;
    }
    else {
      src = 0 ;                 
      if (ram_inst){
        // A RAM/I/O instruction is in progress, execute the proper operation according to the value of opa
        
        // Read instructions
        switch (opa){
          case 0b0000:
            RAM[chip_select][reg][chr] = READ_DATA ;
            break ;
          case 0b0001:
            if (chip_select == 0){
              byte data = READ_DATA ;
              byte d = 0 ;
              if ((data >> 3) & 1){ // A3
                d |= 0b001 ;
              }
              if ((data >> 1) & 1){ // A4
                d |= 0b010 ;
              }
              if (data & 1){        // A5
                d |= 0b100 ;
              }
              WRITE_ADV_FIRE_COLOR(d) ;
            }
            break ;
          case 0b0100:
            STATUS[chip_select][reg][0] = READ_DATA ;
            break ;
          case 0b0101:
            STATUS[chip_select][reg][1] = READ_DATA ;
            break ;
          case 0b0110:
            STATUS[chip_select][reg][2] = READ_DATA ;
            break ;
          case 0b0111:
            STATUS[chip_select][reg][3] = READ_DATA ;
            break ;
  
          // Write instructions        
          case 0b1000: 
            DATA_OUTPUT ;  
            WRITE_DATA(RAM[chip_select][reg][chr]) ;
            break ;
          case 0b1001:
            DATA_OUTPUT ;  
            WRITE_DATA(RAM[chip_select][reg][chr]) ;
            break ;
          case 0b1011:
            DATA_OUTPUT ;  
            WRITE_DATA(RAM[chip_select][reg][chr]) ;
            break ;
          case 0b1100:
            DATA_OUTPUT ;  
            WRITE_DATA(STATUS[chip_select][reg][0]) ;
            break ;
          case 0b1101:
            DATA_OUTPUT ;  
            WRITE_DATA(STATUS[chip_select][reg][1]) ;
            break ;
          case 0b1110:
            DATA_OUTPUT ;  
            WRITE_DATA(STATUS[chip_select][reg][2]) ;
            break ;
          case 0b1111:
            DATA_OUTPUT ;  
            WRITE_DATA(STATUS[chip_select][reg][3]) ;
            break ;
        }
      }
    }
  }) ;


  TIMING.X32clk1([]{
    // Disconnect from bus
    if (ram_inst){
      DATA_INPUT ;
    }
  }) ;


  TIMING.X32clk2([]{
    // If we are processing an SRC instruction, grab the selected RAM character
    if (src){
      chr = READ_DATA ;
    }
  }) ;
}


void loop(){
  while (1){
    #ifdef DEBUG
      unsigned long start = micros() ;
    #endif
    if (READ_RESET){
      return reset() ;
    }

    TIMING.loop() ;
    #ifdef DEBUG
      unsigned long dur = micros() - start ;
      if (dur > max_dur){
        max_dur = dur ;
        Serial.print("Max loop duration: ") ;
        Serial.print(max_dur) ;
        Serial.println("us") ;
      }
    #endif
  }
}
