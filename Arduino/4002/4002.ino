#include "TIMING.h"

#define DEBUG

#define RESET_ON                    PINC &   0b00000010
#define RESET_INPUT                 DDRC &= ~0b00000010
#define CM_ON                       PINC &   0b00000001
#define CM_INPUT                    DDRC &= ~0b00000001
#define DATA                        0b00111100 // PORTD
#define READ_DATA                   ((PIND & DATA) >> 2)
#define WRITE_DATA(data)            PORTD = ((PORTD & ~DATA) | (data << 2))  
#define DATA_INPUT                  DDRD &= ~DATA
#define DATA_OUTPUT                 DDRD |=  DATA

#define PRN_ADV_FIRE_COLOR          0b00111000
#define WRITE_ADV_FIRE_COLOR(a, f, c)  PORTC =  ((PORTC & ~PRN_ADV_FIRE_COLOR) | ((c) << 5) | ((f) << 4) | ((a) << 3))  
#define PRN_ADV_FIRE_COLOR_OUTPUT   DDRC  |= PRN_ADV_FIRE_COLOR

#define LIGHTS_MEM                  0b10000000   // PORTD
#define LIGHTS_NEG_OVF              0b00000011   // PORTB
#define WRITE_MEM_NEG_OVF(m, n, o)  PORTD =  ((PORTD & ~LIGHTS_MEM) | ((m) << 7)) ; PORTB = ((PORTB & ~LIGHTS_NEG_OVF) | ((o) << 1) | (n)) 
#define LIGHTS_MEM_NEG_OVF_OUTPUT   DDRD  |= LIGHTS_MEM ; DDRB |= LIGHTS_NEG_OVF

#define LED                     0b00100000
#define LED_OUTPUT              DDRB |= LED
#define LED_ON                  PORTB |= LED
#define LED_OFF                 PORTB &= ~LED

void io_write(byte data) ;
byte io_read() ;

TIMING TIMING ;

byte reg = 0 ;
byte chr = 0 ;
bool src = 0 ;
byte opa = 0 ;
byte opr = 0 ;
int chip_select = -1 ;
bool ram_inst = 0 ;
byte RAM[2][4][16] ;
byte STATUS[2][4][4] ;
unsigned long max_dur = 0 ;


void reset(){
  LED_ON ;
  DATA_INPUT ;   
  
  TIMING.reset() ;
  reg = 0 ;
  chr = 0 ;
  src = 0 ;
  opa = 0 ;
  chip_select = -1 ;
  max_dur = 0 ;
  
  for (byte i = 0 ; i < 2 ; i++){
    for (byte j = 0 ; j < 4 ; j++){
      for (byte k = 0 ; k < 16 ; k++){
        RAM[i][j][k] = 0 ; 
        if (k < 4){
          STATUS[i][j][k] = 0 ; 
        }
      }
    }
  }
  
  WRITE_ADV_FIRE_COLOR(0, 0, 0) ;
  WRITE_MEM_NEG_OVF(0, 0, 0) ;
  LED_OFF ;
}


void setup(){
  #ifdef DEBUG
    Serial.begin(2000000) ;
    Serial.println("4002") ;
  #endif
  RESET_INPUT ;
  CM_INPUT ;
  PRN_ADV_FIRE_COLOR_OUTPUT ;
  LIGHTS_MEM_NEG_OVF_OUTPUT ;
  LED_OUTPUT ;
  TIMING.setup() ;
  reset() ;
  

  TIMING.M22clk2([]{
    // Grab opa
    opa = READ_DATA ;
    if ((chip_select != -1)&&(CM_ON)){
      // If we are the selected chip for RAM/I/O and cm is on, the CPU is telling us that 
      // we are processing a RAM/I/O instruction
      ram_inst = 1 ;
    }
    else {
      ram_inst = 0 ;
    }
  }) ;


  TIMING.X22clk1([]{
    src = 0 ;
    if (CM_ON){
      // An SRC instruction is in progress
      byte data = READ_DATA ;
      byte chip = data >> 2 ;
      if (chip < 2){
        chip_select = chip ;
        // Grab the selected RAM register
        reg = data & 0b0011 ;
        src = 1 ;
      }
      else {
        chip_select = -1 ;
      }
    }
    else {                 
      if (ram_inst){
        // A RAM/I/O instruction is in progress, execute the proper operation according 
        // to the value of opa
        if ((opa & 0b1000) == 0){   // Write instructions
          io_write(READ_DATA) ;
        }
        else {
          byte data = io_read() ;
          if (data != 255){
            DATA_OUTPUT ;
            WRITE_DATA(data) ;
          }
        }
      }
    }
  }) ;


  TIMING.X32clk1([]{
    // Disconnect from bus
    DATA_INPUT ;
    if (src){
      chr = READ_DATA ;
    }
  }) ;
}


void io_write(byte data){
  if (opa == 0b0000){
    Serial.print(data, HEX) ;
    RAM[chip_select][reg][chr] = data ;
  }
  else if (opa == 0b0001){
    if (chip_select == 0){        // Printer
      bool adv = data & 0b1000 ;
      bool fire = data & 0b0010 ;
      bool color = data & 0b0001 ;
      WRITE_ADV_FIRE_COLOR(adv, fire, color) ;
      if (adv){
        Serial.print("\n") ;
      }
    }
    else if (chip_select == 1){   // Lights
      bool mem = data & 0b0001 ;
      bool ovf = data & 0b0010 ;
      bool neg = data & 0b0100 ;
      WRITE_MEM_NEG_OVF(mem, neg, ovf) ;
    }
  }
  else if (opa >= 0b0100){
    byte i = opa & 0b0011 ;
    STATUS[chip_select][reg][i] = data ;
  }
}


byte io_read(){
  byte data = 255 ;

  if ((opa == 0b1000)||(opa == 0b1001)||(opa == 0b1011)){
      data = RAM[chip_select][reg][chr] ;
  }
  else if (opa >= 0b1100){
    byte i = opa & 0b0011 ;
    data = STATUS[chip_select][reg][i] ;
  }

  return data ;
}


void loop(){
  while (1){
    #ifdef DEBUG
      unsigned long start = micros() ;
    #endif
   
    if (RESET_ON){
      return reset() ;
    }
    
    noInterrupts() ;
    TIMING.loop() ;
    interrupts() ;

    #ifdef DEBUG
      unsigned long dur = micros() - start ;
      if (dur > max_dur){
        max_dur = dur ;
        //Serial.print("Max:") ;
        //Serial.println(max_dur) ;
      }
    #endif
  }
}
