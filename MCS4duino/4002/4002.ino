#include "TIMING.h"

#define RESET  A1
#define CM     A0
#define CLK1   12
#define CLK2   11
#define SYNC   10
#define DATA_3 9
#define DATA_2 8
#define DATA_1 6
#define DATA_0 5
#define PRN_ADV   A3
#define PRN_FIRE  A4
#define PRN_COLOR A5

TIMING TIMING(CLK1, CLK2, SYNC) ;

byte opa = 0 ;
byte reg = 0 ;
byte chr = 0 ;
bool src = 0 ;
bool ram_inst = 0 ;
byte chip_select = 0 ;
byte RAM[4][4][16] ;
byte STATUS[4][4][4] ;


void reset(){
  TIMING.reset() ;
  opa = 0 ;
  reg = 0 ;
  chr = 0 ;
  src = 0 ;
  ram_inst = 0 ;
  chip_select = 0 ;
  
  digitalWrite(PRN_ADV, 0) ;
  digitalWrite(PRN_FIRE, 0) ;
  digitalWrite(PRN_COLOR, 0) ;
}


void setup(){
  Serial.begin(115200) ;
  Serial.println("4002") ;
  pinMode(RESET, INPUT) ;
  pinMode(CM, INPUT) ;
  pinMode(CLK1, INPUT) ;
  pinMode(CLK2, INPUT) ;
  pinMode(SYNC, INPUT) ;
  pinMode(DATA_3, INPUT) ;
  pinMode(DATA_2, INPUT) ;
  pinMode(DATA_1, INPUT) ;
  pinMode(DATA_0, INPUT) ; 
  pinMode(PRN_ADV, OUTPUT) ; 
  pinMode(PRN_FIRE, OUTPUT) ;   
  pinMode(PRN_COLOR, OUTPUT) ; 
  reset() ;


  TIMING.M22clk2([]{
    // Grab opa
    opa = read_data() ;
    if (digitalRead(CM)){
      // If we are the selected chip for RAM/I/O and cm is on, the CPU is telling us that we are processing a RAM/I/O instruction
      // NOTE: We could have just checked that opr == 0b1110 during M1...
      Serial.print("opa ") ;
      Serial.println(opa) ;
      ram_inst = 1 ;
    }
    else {
      ram_inst = 0 ;
    }
  }) ;


  TIMING.X22clk1([]{
    if (ram_inst){
      int data = -1 ;
      // A RAM/I/O instruction is on progress, execute the proper operation according to the value of opa
      switch (opa){
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
        Serial.print("IO write ") ;
        Serial.print(chip_select) ;
        Serial.print(" ") ;
        Serial.print(opa) ;
        Serial.print(" ") ;
        Serial.print(reg) ;
        Serial.print(" ") ;
        Serial.print(chr) ;
        Serial.print(" ") ;
        Serial.println(data) ;  
        pinMode(DATA_3, OUTPUT) ;
        pinMode(DATA_2, OUTPUT) ;
        pinMode(DATA_1, OUTPUT) ;
        pinMode(DATA_0, OUTPUT) ;         
        write_data(data) ;
      }
    }
  }) ;


  TIMING.X22clk2([]{
    if (digitalRead(CM)){
      // An SRC instruction is in progress
      byte data = read_data() ;
      chip_select = data >> 2 ;
      // Grab the selected RAM register
      reg = data & 0b0011 ;
      src = 1 ;
      Serial.print("SRC ") ;
      Serial.print(data >> 2) ;
      Serial.print(" ") ;
      Serial.println(reg) ;
    }
    else {
      src = 0 ;
    }                
    if (ram_inst){
      // A RAM/I/O instruction is in progress, execute the proper operation according to the value of opa
      byte data = read_data() ;
      bool wrote = 0 ;
      
      switch (opa){
        case 0b0000:
          RAM[chip_select][reg][chr] = data ;
          wrote = 1 ;
          break ;
        case 0b0001:
          if (chip_select == 0){
            digitalWrite(PRN_ADV, (data >> 3) & 1) ;
            digitalWrite(PRN_FIRE, (data >> 1) & 1) ;
            digitalWrite(PRN_COLOR, data & 1) ;
          }
          wrote = 1 ;
          break ;
        case 0b0100:
          STATUS[chip_select][reg][0] = data ;
          wrote = 1 ;
          break ;
        case 0b0101:
          STATUS[chip_select][reg][1] = data ;
          wrote = 1 ;
          break ;
        case 0b0110:
          STATUS[chip_select][reg][2] = data ;
          wrote = 1 ;
          break ;
        case 0b0111:
          STATUS[chip_select][reg][3] = data ;
          wrote = 1 ;
          break ;
      }

      if (wrote){
        Serial.print("IO read ") ;
        Serial.print(chip_select) ;
        Serial.print(" ") ;
        Serial.print(opa) ;
        Serial.print(" ") ;
        Serial.print(reg) ;
        Serial.print(" ") ;
        Serial.print(chr) ;
        Serial.print(" ") ;
        Serial.println(data) ;
      }
    }
  }) ;


  TIMING.X31([]{
    // Disconnect from bus
    if (ram_inst){
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
      Serial.print("SRC char ") ;
      Serial.println(chr) ;
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


/*
class i4002:
    def __init__(self, bank, chip, clk1, clk2, sync, data, cm):
        bank = bank                            # The bank that this RAM belongs to. For dump purposes only.
        chip = chip                            # The chip number or identifier (0-3). Bit 1 is the model number (-1 or -2) and bit 0 is the P0 signal
        data = data                            # The data bus
        cm = cm                                # The command line
        output = pbus()                         # The output bus
        src = 0                                # 1 if we are currently processing a SRC instruction
        ram_select = 0                         # 1 if this chip is selected (by SRC during X2) for RAM/I/O instructions
        ram_inst = 0                           # 1 if we are currently processing an RAM/I/O instruction
        opa = 0                                # opa, saves during M2
        reg = 0                                # The selected (by SRC) RAM register
        char = 0                               # The selected (by SRC) RAM character
        ram = [[0] * 16, [0] * 16, [0] * 16, [0] * 16] # The actual RAM cells
        status = [[0] * 4, [0] * 4, [0] * 4, [0] * 4]  # The actual status cells                    
   
        timing = timing(clk1, clk2, sync)        # The timing module and associated callback functions
 
        @M22clk2
        def _():
            # Grab opa
            opa = data.v
            if ram_select and cm.v:
                # If we are the selected chip for RAM/I/O and cm is on, the CPU is telling us that we are processing a RAM/I/O instruction
                # NOTE: We could have just checked that opr == 0b1110 during M1...
                ram_inst = 1
            else:
                ram_inst = 0

        @X22clk1
        def _():
            if ram_inst:
                # A RAM/I/O instruction is on progress, execute the proper operation according to the value of opa
                if opa == 0b1000:
                    write_data(ram[reg][char]
                elif opa == 0b1001:
                    write_data(ram[reg][char]
                elif opa == 0b1011:
                    write_data(ram[reg][char]
                elif opa == 0b1100:
                    write_data(status[reg][0]
                elif opa == 0b1101:
                    write_data(status[reg][1]
                elif opa == 0b1110:
                    write_data(status[reg][2]
                elif opa == 0b1111:
                    write_data(status[reg][3]

        @X22clk2
        def _():
            if cm.v:
                # An SRC instruction is in progress
                if chip == (data.v >> 2):
                    # We are the selected RAM chip for RAM/I/O if chip == (data.v >> 2)
                    src = 1
                    ram_select = 1
                    # Grab the selected RAM register
                    reg = data.v & 0b0011
                else:
                    ram_select = 0
            else:
                src = 0                
            if ram_inst:
                # A RAM/I/O instruction is on progress, execute the proper operation according to the value of opa
                if opa == 0b0000:
                    ram[reg][char] = data.v
                elif opa == 0b0001:
                    output.v(data.v)
                elif opa == 0b0100:
                    status[reg][0] = data.v
                elif opa == 0b0101:
                    status[reg][1] = data.v
                elif opa == 0b0110:
                    status[reg][2] = data.v
                elif opa == 0b0111:
                    status[reg][3] = data.v

        @X31
        def _():    # Disconnect from bus
            if ram_inst:
                write_data(None

        @X32clk2
        def _():
            # If we are processing an SRC instruction, grab the selected RAM character
            if src:
                char = data.v
 */
