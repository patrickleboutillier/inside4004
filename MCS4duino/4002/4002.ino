#include "TIMING.h"

#define RESET      A1
#define READ_RESET PINC & 0b00000010
#define CM         A0
#define READ_CM    PINC & 0b00000001
#define DATA_3     9
#define DATA_2     8
#define DATA_1     6
#define DATA_0     5
#define DATA_32    0b00000011    // PORTB
#define DATA_10    0b01100000    // PORTD
#define READ_DATA  ((PINB & DATA_32) << 2) | ((PIND & DATA_10) >> 5)
#define WRITE_DATA (data) (PORTB = (PORTB & ~DATA_32) | (((data >> 3) & 1) << 1) | ((data >> 2) & 1) ; PORTD = (PORTD & ~DATA_10) | (((data >> 1) & 1) << 6) | ((data & 1) << 5)  
 
#define PRN_ADV    A3
#define PRN_FIRE   A4
#define PRN_COLOR  A5

TIMING TIMING ;

byte reg = 0 ;
byte chr = 0 ;
bool src = 0 ;
int opa = -1 ;
byte chip_select = 0 ;
byte RAM[4][4][16] ;
byte STATUS[4][4][4] ;


void reset(){
  pinMode(DATA_3, INPUT) ;
  pinMode(DATA_2, INPUT) ;
  pinMode(DATA_1, INPUT) ;
  pinMode(DATA_0, INPUT) ;   
  
  TIMING.reset() ;
  reg = 0 ;
  chr = 0 ;
  src = 0 ;
  opa = -1 ;
  chip_select = 0 ;

  for (int i = 0 ; i < 4  ; i++){
    for (int j = 0 ; j < 4 ; j++){
      for (int k = 0 ; k < 16 ; k++){
        RAM[i][j][k] = 0 ; 
      }
      for (int k = 0 ; k < 4 ; k++){
        STATUS[i][j][k] = 0 ; 
      }
    }
  }
  
  digitalWrite(PRN_ADV, 0) ;
  digitalWrite(PRN_FIRE, 0) ;
  digitalWrite(PRN_COLOR, 0) ;
}


void setup(){
  Serial.begin(115200) ;
  Serial.println("4002") ;
  pinMode(RESET, INPUT) ;
  pinMode(CM, INPUT) ;
  pinMode(PRN_ADV, OUTPUT) ; 
  pinMode(PRN_FIRE, OUTPUT) ;   
  pinMode(PRN_COLOR, OUTPUT) ; 
  TIMING.setup() ;
  reset() ;


  TIMING.M22clk2([]{
    if (READ_CM){
      // If we are the selected chip for RAM/I/O and cm is on, the CPU is telling us that we are processing a RAM/I/O instruction
      // Grab opa
      opa = read_data() ;
    }
    else {
      opa = -1 ;
    }
  }) ;


  TIMING.X22clk1([]{
    if (READ_CM){
      // An SRC instruction is in progress
      byte data = read_data() ;
      chip_select = data >> 2 ;
      // Grab the selected RAM register
      reg = data & 0b0011 ;
      src = 1 ;
    }
    else {
      src = 0 ;
    }                
    
    if (opa != -1){
      // A RAM/I/O instruction is in progress, execute the proper operation according to the value of opa
      int data = -1 ; 
      
      switch (opa){
        case 0b0000:
          RAM[chip_select][reg][chr] = read_data() ;
          break ;
        case 0b0001:
          data = read_data() ;
          if (chip_select == 0){
            digitalWrite(PRN_ADV, (data >> 3) & 1) ;
            digitalWrite(PRN_FIRE, (data >> 1) & 1) ;
            digitalWrite(PRN_COLOR, data & 1) ;
          }
          break ;
        case 0b0100:
          STATUS[chip_select][reg][0] = read_data() ;
          break ;
        case 0b0101:
          STATUS[chip_select][reg][1] = read_data() ;
          break ;
        case 0b0110:
          STATUS[chip_select][reg][2] = read_data() ;
          break ;
        case 0b0111:
          STATUS[chip_select][reg][3] = read_data() ;
          break ;
          
        case 0b1000: 
          data = RAM[chip_select][reg][chr] ;
          break ;
        case 0b1001:
          data = RAM[chip_select][reg][chr] ;
          break ;
        case 0b1011:
          data = RAM[chip_select][reg][chr] ;
          break ;
        case 0b1100:
          data = STATUS[chip_select][reg][0] ;
          break ;
        case 0b1101:
          data = STATUS[chip_select][reg][1] ;
          break ;
        case 0b1110:
          data = STATUS[chip_select][reg][2] ;
          break ;
        case 0b1111:
          data = STATUS[chip_select][reg][3] ;
          break ;
      }

      if (data != -1){
        pinMode(DATA_3, OUTPUT) ;
        pinMode(DATA_2, OUTPUT) ;
        pinMode(DATA_1, OUTPUT) ;
        pinMode(DATA_0, OUTPUT) ;         
        write_data(data) ;      
      }
    }
  }) ;


  TIMING.X32clk1([]{
    // Disconnect from bus
    if (opa != -1){
      pinMode(DATA_3, INPUT) ;
      pinMode(DATA_2, INPUT) ;
      pinMode(DATA_1, INPUT) ;
      pinMode(DATA_0, INPUT) ; 
    }
  }) ;


  TIMING.X32clk2([]{
    // If we are processing an SRC instruction, grab the selected RAM character
    if (src){
      chr = read_data() ;
    }
  }) ;
}


void loop(){
  if (READ_RESET){
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
