// This project has different licenses for different files:
// 
// k4004_busicom.ino       : Erturk's code - see license below.
// k4004_busicom_printer.h : Tim McNerney's code - see file for license.
// k4004_busicom_rom.h     : Tim McNerney's code - see file for license
//

////////////////////////////////////////////////////////////////////
// RetroShield 4004
// 2020/10/25
// Version 0.1
// Erturk Kocalar

// The MIT License (MIT)
//
// Copyright (c) 2020 Erturk Kocalar, 8Bitforce.com
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.
//
// Date         Comments                                            Author
// -----------------------------------------------------------------------------
// 06/13/2020   Initial Bring-up.                                   E. Kocalar
// 10/25/2020   Public Release                                      E. Kocalar
//


////////////////////////////////////////////////////////////////////
// Huge THANKS to following people for extracting rare ROM images
// and making them available for public.  Now we can have history
// running.

// Team Personnel (in alphabetical order)
//   Allen E. Armstrong, mechanical engineering
//   Fred Huettig, netlist extraction software, electrical engineering, FPGA programming
//   Lajos Kintli, reverse-engineering, software analysis, commenting, documentation
//   Tim McNerney, conceptual design, project leader, digital design
//   Barry Silverman, reverse-engineering, simulation software
//   Brian Silverman, reverse-engineering, simulation software
// Collaborators and advisors
//   Federico Faggin, CEO Foveon, 4004 chip designer
//   Sellam Ismail, proprietor, Vintage Tech
//   Tom Knight, MIT CSAIL, VLSI history expert
//   Tracey Mazur, Curator, Intel Museum
//   Dag Spicer, Curator, Computer History Museum
//   Rachel Stewart, former Intel archivist
// Other contributors
//   Christian Bassow, owner of a Busicom 141-PF, who kindly sent me photographs of the PCB.
//   Karen Joyce, electronic assembler extraordinaire
//   Matt McNerney, webmaster


////////////////////////////////////////////////////////////////////
// Options
//   outputDEBUG: Print memory access debugging messages.
////////////////////////////////////////////////////////////////////
#define outputDEBUG       0             // hardware debugging
#define outputDEBUG_IO    0             // Print RAM & port I/O details
#define outputDEBUG_dis   0             // disassemble code as executed
bool    uP_IO_executed    = false;      // used by diagnostics output
void(* resetFunc) (void) = 0;           // Reset Arduino programmatically.

////////////////////////////////////////////////////////////////////
// include the library code for LCD shield:
////////////////////////////////////////////////////////////////////
#include <avr/pgmspace.h>
#include "pins2_arduino.h"
#include <DIO2.h>

////////////////////////////////////////////////////////////////////
// 4004 DEFINITIONS
////////////////////////////////////////////////////////////////////

// Delay after clock edges to handle prop delays
#if (1)
  // inherent delay from ATMEL instructions
  #define LEVEL_SHIFT_PROP_DELAY {}
#else
  #define LEVEL_SHIFT_PROP_DELAY (delayMicroseconds(1))
#endif

////////////////////////////////////////////////////////////////////
// MEMORY LAYOUT
////////////////////////////////////////////////////////////////////

// MEMORY
#define RAM_BANKS           8     // CM0: 1x RAM0 + CM3CM2CM1: 7x RAM321
#define RAM_CHIPnREG        16    // 4 chips * 4 registers (D3D2 chip select, D1D0 reg select)
#define RAM_CHARS_PER_REG   16    // D3D2D1D0 char select
#define RAM_STAT_PER_REG    4
#define ROM_BANKS           16     

byte  RAM_CHARS[RAM_BANKS][RAM_CHIPnREG]   [RAM_CHARS_PER_REG];
byte RAM_STATUS[RAM_BANKS][RAM_CHIPnREG]   [RAM_STAT_PER_REG];
byte     RAM_IO[RAM_BANKS][RAM_CHIPnREG>>2];
byte     ROM_IO[ROM_BANKS];
byte SRC_ROM_X2[ROM_BANKS];
byte SRC_RAM_X2[RAM_BANKS];   // Saves SRC info for each bank (DCL can change and expect RAM to remember)
byte SRC_RAM_X3[RAM_BANKS];

// ROM(s) (Monitor)
#define ROM_START   0x0000
#define ROM_END     (ROM_START+sizeof(rom_bin)-1)

////////////////////////////////////////////////////////////////////
// Busicom 141-PF Printer Defines
////////////////////////////////////////////////////////////////////
word          kbd_i4003_shifter_output      = 0;
bool          kbd_i4003_shifter_output_prev = false;

unsigned long prt_i4003_shifter_output      = 0;
bool          prt_i4003_shifter_clk_prev    = false;

////////////////////////////////////////////////////////////////////
// Busicom 141-PF ROM
////////////////////////////////////////////////////////////////////
#include "k4004_busicom_rom.h"


////////////////////////////////////////////////////////////////////
// 4004 Processor Control
////////////////////////////////////////////////////////////////////
//

#define EN_BOOST_15V  29        // Not used 
#define uP_PHI1       40
#define uP_PHI2       41
#define uP_RESET      52
#define uP_TEST       50
#define uP_CMRAM0     22
#define uP_CMRAM1     23
#define uP_CMRAM2     24
#define uP_CMRAM3     25
#define uP_CMROM      26
#define uP_SYNC       27
#define DRIVE_DBUS    38
#define DRIVE_RAMQ    39
#define DRIVE_SYNC    51
#define DRIVE_CMRAM0  53

// Fast routines to drive clock signals high/low; faster than digitalWrite
// required to meet >100kHz clock
//
#define PHI_SET(C)        (PORTG = (PORTG & 0b11111100) | (C & 0b00000011) )
#define PHI2_HIGH         (PORTG = PORTG | 0b00000001)
#define PHI2_LOW          (PORTG = PORTG & 0b11111110)
#define PHI1_HIGH         (PORTG = PORTG | 0b00000010)
#define PHI1_LOW          (PORTG = PORTG & 0b11111101)
#define RESET_HIGH        (PORTB = PORTB | 0b00000010)
#define RESET_LOW         (PORTB = PORTB & 0b11111101)
#define TEST_HIGH         (PORTB = PORTB | 0b00001000)
#define TEST_LOW          (PORTB = PORTB & 0b11110111)
#define DRIVE_DBUS_START  (PORTD = PORTD | 0b10000000)
#define DRIVE_DBUS_STOP   (PORTD = PORTD & 0b01111111)

/* Digital Pin Assignments */
/* Remember - 4004 logic is inverted.  1 means 0, and 0 means 1 */
#define DATA4_OUT(D)      ( PORTC = (PORTC & 0xF0) | (~(D) & 0x0F) )
#define DATA4_IN()        ( (~PINL) & 0x0F)
#define STATE_SYNC        ( (~PINA) & 0x20)
#define STATE_CMROM       (((~PINA) & 0x10) >> 4)
#define STATE_CMRAM       ( (~PINA) & 0x0F)
#define STATE_CMRAM_0321  (STATE_CMRAM >> 1) 
// Swizzle CMRAM0 and CMRAM1/2/3
// so table in datasheet maps to 0,1,2,3,4,5,6,7
#define STATE_RAMQ        (((~PINC) & 0xF0) >> 4)
#define RAMQ4_OUT(D)      ( PORTC = (PORTC & 0x0F) | (((D) & 0x0F)<< 4) )

enum CPU_STATE_T {
  CPU_WAIT_SYNC,              // initial state waiting for SYNC output
  CPU_A1, CPU_A2, CPU_A3,
  CPU_M1, CPU_M2,
  CPU_X1, CPU_X2, CPU_X3
} cpu_state, next_cpu_state;

word uP_ADDR;
byte uP_DATA;
char tmp[70];      // used for debug purposes

inline __attribute__((always_inline))
void uP_init()
{
  // Set directions

  // 15V Supply - Enable
  pinMode(EN_BOOST_15V, OUTPUT);
  digitalWrite(EN_BOOST_15V, HIGH);

  // Arduino DataBus Buffer - Disable (CPU drives databus)
  pinMode(DRIVE_DBUS,  OUTPUT);
  digitalWrite(DRIVE_DBUS, LOW);    // Disable Arduino Data out to stop contention

  // RAM's Q Output Buffer - Disable  (Arduino will drive LED's)
  pinMode(DRIVE_RAMQ,  OUTPUT);
  digitalWrite(DRIVE_RAMQ, LOW);    // RAM IC can not drive LEDs

  // CPU DATA OUT to Arduino
  pinMode(49, INPUT);  // D3
  pinMode(48, INPUT);  // D2
  pinMode(47, INPUT);  // D1
  pinMode(46, INPUT);  // D0
  
  // Arduino DATA OUT to CPU
  pinMode(37, OUTPUT); digitalWrite(37, LOW); // D3
  pinMode(36, OUTPUT); digitalWrite(36, LOW); // D2
  pinMode(35, OUTPUT); digitalWrite(35, LOW); // D1
  pinMode(34, OUTPUT); digitalWrite(34, LOW); // D0
  digitalWrite(DRIVE_DBUS, LOW);

  // CMRAM to Arduino
  pinMode(25, INPUT); // D3
  pinMode(24, INPUT); // D2
  pinMode(23, INPUT); // D1
  pinMode(22, INPUT); // D0

  // RAMQ to Arduino
  pinMode(30, OUTPUT); // D3
  pinMode(31, OUTPUT); // D2
  pinMode(32, OUTPUT); // D1
  pinMode(33, OUTPUT); // D0
  digitalWrite(DRIVE_RAMQ, LOW);

  pinMode(uP_PHI1,    OUTPUT);
  pinMode(uP_PHI2,    OUTPUT);
  pinMode(uP_RESET,   OUTPUT);
  pinMode(uP_TEST,    OUTPUT);
  pinMode(uP_SYNC,    INPUT);
  pinMode(uP_CMRAM0,  INPUT);
  pinMode(uP_CMRAM1,  INPUT);
  pinMode(uP_CMRAM2,  INPUT);
  pinMode(uP_CMRAM3,  INPUT);
  pinMode(uP_CMROM,   INPUT);
  // pinMode(DRIVE_SYNC, OUTPUT);
  // pinMode(DRIVE_CMRAM0, OUTPUT);

  digitalWrite(uP_TEST, LOW);
  digitalWrite(uP_PHI1, HIGH);
  digitalWrite(uP_PHI2, HIGH);
  // digitalWrite(DRIVE_SYNC, LOW);
  // digitalWrite(DRIVE_CMRAM0, LOW);
  
  digitalWrite(uP_RESET,  LOW);   // Assert reset.

  cpu_state = CPU_WAIT_SYNC;
  
  uP_assert_reset();
}

inline __attribute__((always_inline))
void uP_assert_reset()
{
  // Drive RESET conditions
  digitalWrite(uP_RESET,  LOW);     // Assert RESET
}

inline __attribute__((always_inline))
void uP_release_reset()
{
  // Deassert RESET
  digitalWrite(uP_RESET, HIGH);     // Release RESET
}

// Prep memory/devices before execution start
inline __attribute__((always_inline))
void k4004_IO_init()
{  
  for (int a=0; a < RAM_BANKS; a++)
    for (int b=0; b < RAM_CHIPnREG; b++)
        for (int d=0; d < RAM_CHARS_PER_REG; d++)
          RAM_CHARS[a][b][d] = 0x00;
          
  for (int a=0; a < RAM_BANKS; a++)
    for (int b=0; b < RAM_CHIPnREG; b++)
        for (int e=0; e < RAM_STAT_PER_REG; e++)
            RAM_STATUS[a][b][e] = 0x00;

  for (int a=0; a < RAM_BANKS; a++)
    for (int b=0; b < (RAM_CHIPnREG >> 2); b++) 
            RAM_IO[a][b] = 0x00;
  
  for (int a=0; a < ROM_BANKS; a++)
            ROM_IO[a] = 0x00;
}

void k4004_reset_until_sync()
{
  bool synced = false;
  int reset_cycles = (8*1000);
  
  uP_assert_reset();
  while(!synced)       
  {
    while (reset_cycles--) cpu_tick();  
    if (cpu_state != CPU_WAIT_SYNC)
      synced = true;
    else
    {
      Serial.println("INFO: Not sync'ed after one round of RESET. Retrying.");
      reset_cycles = (8*500);
    }
  }  
  while(cpu_state != CPU_A1)       
  cpu_tick();  
}

void print_key_mappings()
{
  Serial.println("'X', 'V', 'Z', 'A',    // CM  RM  M-  M+");
  Serial.println("'S', '%', 'L', 'P',    // SQ  %   M=- M=+");
  Serial.println("'[', '/', '*', '=',    // DIA /   *   =");
  Serial.println("'-', '+', ']', 'O',    // -   +   D2  000");
  Serial.println("'9', '6', '3', '.',    // 9   6   3   .");
  Serial.println("'8', '5', '2', 'I',    // 8   5   2   00");
  Serial.println("'7', '4', '1', '0',    // 7   4   1   0");
  Serial.println("'Q', 'E', '`', 'C'     // SI  EX  CE  C");
  Serial.println("");
  Serial.println(" Use f/F to dec/increase digits after decimal point");
  Serial.println(" Use R to select FLoat/TRuncate/ROund");
  Serial.println(" ? - print this help again.");  
  Serial.println();
}


inline __attribute__((always_inline))
void k4004_IO_process()
{
  //////////////////////////////
  // Printer Shifter

  if ( (ROM_IO[0] & 0b0100) )
  {   
    if ( !prt_i4003_shifter_clk_prev )
    {
      prt_i4003_shifter_output = (prt_i4003_shifter_output << 1) | ( (ROM_IO[0] >> 1) & 0b0001);
      prt_i4003_shifter_output = prt_i4003_shifter_output & 0b00111111111111111111;
  
      if (outputDEBUG)
      {
        Serial.print("PRINTER_SHIFTER: "); Serial.print(prt_i4003_shifter_output, HEX); Serial.println("      "); 
      }
    }
  }
  prt_i4003_shifter_clk_prev = ROM_IO[0] & 0b0100;

  //////////////////////////////
  // Keyboard

  if ( (ROM_IO[0] & 0b0001) )
  {
    if ( !kbd_i4003_shifter_output_prev )
    {
      // rising edge of CP
      kbd_i4003_shifter_output = (kbd_i4003_shifter_output << 1) | ( (ROM_IO[0] >> 1) & 0b0001);
      kbd_i4003_shifter_output = kbd_i4003_shifter_output & 0b1111111111;

      if (outputDEBUG)
      { 
        Serial.print("KBD_SHIFTER: "); Serial.print(kbd_i4003_shifter_output, BIN); Serial.println(""); 
      }
    }
  }
  kbd_i4003_shifter_output_prev = ROM_IO[0] & 0b0001;

#if outputDEBUG_IO

  // Go back to screen corner so we see movement:
  if (uP_IO_executed)
  {
     Serial.write(27);
     Serial.print("[H");
  }

  //////////////////////////////
  // Print RAM and STATUS Contents

  if (uP_IO_executed)
  {
    Serial.write("\n    RAM:\n    ");
      for (int j=0; j<8; j++)
      {
        Serial.print(j, HEX); Serial.print(": ");
        for (int k=0; k<4; k++)
          {
            sprintf(tmp, "%0.1X", RAM_STATUS[0][j][3-k]); 
            Serial.write(tmp);
          }
        Serial.write(" ");
        for (int k=0; k<16; k++)
          {
            sprintf(tmp, "%0.1X", RAM_CHARS[0][j][15-k]); 
            Serial.write(tmp);
          }
        Serial.print("\n    ");
      }

    Serial.write('\n');
  }

  //////////////////////////////
  // Print I/O States
  
  int a;

  if (uP_IO_executed)
  {
    a=0; sprintf(tmp, "    RAM IO : %0.1X%0.1X%0.1X%0.1X", RAM_IO[a][0], RAM_IO[a][1], RAM_IO[a][2], RAM_IO[a][3]); Serial.print(tmp);
    a=1; sprintf(tmp, " %0.1X%0.1X%0.1X%0.1X", RAM_IO[a][0], RAM_IO[a][1], RAM_IO[a][2], RAM_IO[a][3]); Serial.print(tmp);
    a=2; sprintf(tmp, " %0.1X%0.1X%0.1X%0.1X", RAM_IO[a][0], RAM_IO[a][1], RAM_IO[a][2], RAM_IO[a][3]); Serial.print(tmp);
    a=3; sprintf(tmp, " %0.1X%0.1X%0.1X%0.1X", RAM_IO[a][0], RAM_IO[a][1], RAM_IO[a][2], RAM_IO[a][3]); Serial.print(tmp);
    a=4; sprintf(tmp, " %0.1X%0.1X%0.1X%0.1X", RAM_IO[a][0], RAM_IO[a][1], RAM_IO[a][2], RAM_IO[a][3]); Serial.print(tmp);
    a=5; sprintf(tmp, " %0.1X%0.1X%0.1X%0.1X", RAM_IO[a][0], RAM_IO[a][1], RAM_IO[a][2], RAM_IO[a][3]); Serial.print(tmp);
    a=6; sprintf(tmp, " %0.1X%0.1X%0.1X%0.1X", RAM_IO[a][0], RAM_IO[a][1], RAM_IO[a][2], RAM_IO[a][3]); Serial.print(tmp);
    a=7; sprintf(tmp, " %0.1X%0.1X%0.1X%0.1X \n", RAM_IO[a][0], RAM_IO[a][1], RAM_IO[a][2], RAM_IO[a][3]); Serial.print(tmp);    

    sprintf(tmp, "    ROM IO : %0.1X%0.1X%0.1X%0.1X %0.1X%0.1X%0.1X%0.1X ", 
      ROM_IO[0], ROM_IO[1], ROM_IO[2], ROM_IO[3], ROM_IO[4], ROM_IO[5], ROM_IO[6], ROM_IO[7] ); 
      Serial.print(tmp);
    sprintf(tmp, "%0.1X%0.1X%0.1X%0.1X %0.1X%0.1X%0.1X%0.1X \n", 
      ROM_IO[8], ROM_IO[9], ROM_IO[10], ROM_IO[11], ROM_IO[12], ROM_IO[13], ROM_IO[14], ROM_IO[15] ); 
      Serial.println(tmp);
  }
  
  if (uP_IO_executed)
  {
    Serial.print("DRUM_STATE: "); 
    Serial.print(sector); Serial.print(" - "); 
    Serial.print(drum_state); Serial.print(" / "); Serial.print(DRUM_CYCLE_END);
    Serial.println("    ");
  }
#endif
  
  //////////////////////////////
  // Done
  uP_IO_executed = false;
}

bool twobyte=false;

inline __attribute__((always_inline))
void k4004_disassemble(word adr, byte opr, byte opa)
{

  //////////////////////////////
  // TODO: This code does not
  // handle multiple conditions
  // etc.
  //////////////////////////////
  
  if (twobyte)
  {
    sprintf(tmp, "%0.3X: %0.1X%0.1X         ; ^^^^^^^^ ^^^^^^^^", adr, opr, opa);
    Serial.println(tmp);
    twobyte = false;
  }
  else
  {
    switch (opr)
    {
      case 0b0000:
        sprintf(tmp, "%0.3X: %0.1X%0.1X NOP", adr, opr, opa);
        Serial.println(tmp);
        break;      
        
      case 0b0001:
        sprintf(tmp, "%0.3X: %0.1X%0.1X JCN ", adr, opr, opa);
        Serial.print(tmp);
        // TODO: Check if these bits can be set simultaneously
        // Dwight: there are all zeros and invert-only interesting cases.
        //         invert-only = SKIP.
        //         all zeroes = JMP.
        switch(opa)
        {
          case 0b0001:
            Serial.println("TZ  ; test=0");
            break;
          case 0b0010:
            Serial.println("C1  ; cy=1");
            break;
          case 0b0100:
            Serial.println("AZ  ; accumulator=0");
            break;
          case 0b1001:
            Serial.println("TN  ; test=1");
            break;
          case 0b1010:
            Serial.println("C0  ; cy=0");
            break;
          case 0b1100:
            Serial.println("AN  ; accumulator!=0");
            break;            
        }
        twobyte = true;
        break;      
        
      case 0b0010:
        if ((opa & 0x01) == 0x00)
        {
          // FIM Instruction
          sprintf(tmp, "%0.3X: %0.1X%0.1X FIM", adr, opr, opa);
          Serial.print(tmp);
          Serial.print("     ; Fetch immediate from ROM into reg pair ");
          Serial.print(2*(opa >> 1), HEX); Serial.print("_");
          Serial.println(2*(opa >> 1)+1, HEX);
          twobyte = true;
        }
        else
        {
          // SRC
          sprintf(tmp, "%0.3X: %0.1X%0.1X SRC", adr, opr, opa);
          Serial.print(tmp);
          Serial.print("     ; Send Register Control ");
          Serial.print( 2*(opa >> 1), HEX); Serial.print("/");
          Serial.println(2*(opa >> 1)+1, HEX);      
        }
        break;      

      case 0b0011:
        if ((opa & 0x01) == 0x00)
        {
          // FIN Instruction
          sprintf(tmp, "%0.3X: %0.1X%0.1X FIN", adr, opr, opa);
          Serial.print(tmp);
          Serial.print("  ; Fetch indirect from ROM thru reg pair ");
          Serial.print(2*(opa >> 1), HEX); Serial.print("_");
          Serial.println(2*(opa >> 1)+1, HEX);
        }
        else
        {
          // JIN
          sprintf(tmp, "%0.3X: %0.1X%0.1X JIN", adr, opr, opa);
          Serial.print(tmp);
          Serial.print("  ; Jump indirect (8bit PC = register pair ");
          Serial.print(2*(opa >> 1), HEX); Serial.print("_");
          Serial.println(2*(opa >> 1)+1, HEX);      
        }
        break;      

      case 0b0100:
        sprintf(tmp, "%0.3X: %0.1X%0.1X JUN   ; jump unconditional", adr, opr, opa);
        Serial.println(tmp);
        twobyte = true;
        break;      
    
      case 0b0101:
        sprintf(tmp, "%0.3X: %0.1X%0.1X JMS    ; jump to subroutine", adr, opr, opa);
        Serial.println(tmp);
        twobyte = true;
        break;      

      case 0b0110:
        sprintf(tmp, "%0.3X: %0.1X%0.1X INC   ; increment register ", adr, opr, opa);
        Serial.print(tmp);
        Serial.println(opa, HEX);
        break;      

      case 0b0111:
        sprintf(tmp, "%0.3X: %0.1X%0.1X ISZ      ; increment register ", adr, opr, opa);
        Serial.print(tmp);
        Serial.print(opa, HEX);
        Serial.println(", jump to address if non-zero");
        twobyte = true;
        break;      

      case 0b1000:
        sprintf(tmp, "%0.3X: %0.1X%0.1X ADD CY   ; add register ", adr, opr, opa);
        Serial.print(tmp);
        Serial.print(opa, HEX);
        Serial.println(" and carry to accumulator");
        break;      

      case 0b1001:
        sprintf(tmp, "%0.3X: %0.1X%0.1X SUB CY   ; subtract register ", adr, opr, opa);
        Serial.print(tmp);
        Serial.print(opa, HEX);
        Serial.println(" and borrow from accumulator");
        break;      

      case 0b1010:
        sprintf(tmp, "%0.3X: %0.1X%0.1X LD      ; load registter ", adr, opr, opa);
        Serial.print(tmp);
        Serial.print(opa, HEX);
        Serial.println(" into accumulator");
        break;      

      case 0b1011:
        sprintf(tmp, "%0.3X: %0.1X%0.1X XCH     ; exchange registter ", adr, opr, opa);
        Serial.print(tmp);
        Serial.print(opa, HEX);
        Serial.println(" with accumulator");
        break;      

      case 0b1100:
        sprintf(tmp, "%0.3X: %0.1X%0.1X BBL     ; branch back and load data ", adr, opr, opa);
        Serial.print(tmp);
        Serial.print(opa, HEX);
        Serial.println(" to accumulator");
        break;      

      case 0b1101:
        sprintf(tmp, "%0.3X: %0.1X%0.1X LDM     ; load data ", adr, opr, opa);
        Serial.print(tmp);
        Serial.print(opa, HEX);
        Serial.println(" into accumulator");
        break;      

      case 0b1110:
        switch (opa) 
        {
          case 0b0000: // WRM - write ACC to memory
            sprintf(tmp, "%0.3X: %0.1X%0.1X WRM     ; write ACC to memory", adr, opr, opa);
            Serial.println(tmp);
            break;
          case 0b0001: // WMP - write ACC to RAM output port
            sprintf(tmp, "%0.3X: %0.1X%0.1X WMP     ; write ACC to RAM output port", adr, opr, opa);
            Serial.println(tmp);
            break;
          case 0b0010: // WRR - write ACC to ROM output port
            sprintf(tmp, "%0.3X: %0.1X%0.1X WRR     ; write ACC to ROM output port", adr, opr, opa);
            Serial.println(tmp);
            break;
          case 0b0011: // WPM - write ACC to executable RAM (4008/4009 only)
            sprintf(tmp, "%0.3X: %0.1X%0.1X WPM     ; write ACC to executable RAM (4008/4009 only)", adr, opr, opa);
            Serial.println(tmp);
            break;
          case 0b0100: // WR0 - write ACC to RAM status 0
            sprintf(tmp, "%0.3X: %0.1X%0.1X WR0     ; write ACC to RAM status 0", adr, opr, opa);
            Serial.println(tmp);
            break;
          case 0b0101: // WR1 - write ACC to RAM status 1
            sprintf(tmp, "%0.3X: %0.1X%0.1X WR1     ; write ACC to RAM status 1", adr, opr, opa);
            Serial.println(tmp);
            break;
          case 0b0110: // WR2 - write ACC to RAM status 2
            sprintf(tmp, "%0.3X: %0.1X%0.1X WR2     ; write ACC to RAM status 2", adr, opr, opa);
            Serial.println(tmp);
            break;
          case 0b0111: // WR3 - write ACC to RAM status 3
            sprintf(tmp, "%0.3X: %0.1X%0.1X WR3     ; write ACC to RAM status 3", adr, opr, opa);
            Serial.println(tmp);
            break;
          case 0b1000: // SBM - subtract RAM character from ACC
            sprintf(tmp, "%0.3X: %0.1X%0.1X SBM CY  ; subtract RAM character and borrow from ACC", adr, opr, opa);
            Serial.println(tmp);
            break;
          case 0b1001: // RDM - read RAM char to ACC
            sprintf(tmp, "%0.3X: %0.1X%0.1X RDM     ; read RAM char to ACC", adr, opr, opa);
            Serial.println(tmp);
            break;
          case 0b1010: // RDR - read ROM input port to ACC
            sprintf(tmp, "%0.3X: %0.1X%0.1X RDR     ; read ROM input port to ACC", adr, opr, opa);
            Serial.println(tmp);
            break;
          case 0b1011: // ADM - add RAM char to ACC
            sprintf(tmp, "%0.3X: %0.1X%0.1X ADM CY  ; add RAM char and carry to ACC", adr, opr, opa);
            Serial.println(tmp);
            break;
          case 0b1100: // RD0 - read RAM status 0 to ACC
            sprintf(tmp, "%0.3X: %0.1X%0.1X RD0     ; read RAM status 0 to ACC", adr, opr, opa);
            Serial.println(tmp);
            break;
          case 0b1101: // RD1 - read RAM status 1 to ACC
            sprintf(tmp, "%0.3X: %0.1X%0.1X RD1     ; read RAM status 1 to ACC", adr, opr, opa);
            Serial.println(tmp);
            break;
          case 0b1110: // RD2 - read RAM status 2 to ACC
            sprintf(tmp, "%0.3X: %0.1X%0.1X RD2     ; read RAM status 2 to ACC", adr, opr, opa);
            Serial.println(tmp);
            break;
          case 0b1111: // RD3 - read RAM status 3 to ACC
            sprintf(tmp, "%0.3X: %0.1X%0.1X RD3     ; read RAM status 3 to ACC", adr, opr, opa);
            Serial.println(tmp);
            break;
          default: // Error
            Serial.write("ERROR - unknown I/O cmd OPA\n"); 
        }        
        break;      

      case 0b1111:
        // TODO: Check if these bits can be set simultaneously
        switch (opa) 
        {
          case 0b0000:
            sprintf(tmp, "%0.3X: %0.1X%0.1X CLB 0   ; clear both accumulator and carry", adr, opr, opa);
            Serial.println(tmp);
            break;
          case 0b0001:
            sprintf(tmp, "%0.3X: %0.1X%0.1X CLC 0   ; clear carry", adr, opr, opa);
            Serial.println(tmp);
            break;
          case 0b0010:
            sprintf(tmp, "%0.3X: %0.1X%0.1X IAC CY  ; increment accumulator", adr, opr, opa);
            Serial.println(tmp);
            break;
          case 0b0011:
            sprintf(tmp, "%0.3X: %0.1X%0.1X CMC CY  ; complement carry", adr, opr, opa);
            Serial.println(tmp);
            break;
          case 0b0100:
            sprintf(tmp, "%0.3X: %0.1X%0.1X CMA     ; complement accumulator", adr, opr, opa);
            Serial.println(tmp);
            break;
          case 0b0101: 
            sprintf(tmp, "%0.3X: %0.1X%0.1X RAL CY  ; rotate accumulator left thru carry", adr, opr, opa);
            Serial.println(tmp);
            break;
          case 0b0110:
            sprintf(tmp, "%0.3X: %0.1X%0.1X RAR CY  ; rotate accumulator right thru carry", adr, opr, opa);
            Serial.println(tmp);
            break;
          case 0b0111: 
            sprintf(tmp, "%0.3X: %0.1X%0.1X TCC 0   ; transmit carry to accumulator and clear carry", adr, opr, opa);
            Serial.println(tmp);
            break;
          case 0b1000: 
            sprintf(tmp, "%0.3X: %0.1X%0.1X DAC CY  ; decrement accumulator", adr, opr, opa);
            Serial.println(tmp);
            break;
          case 0b1001: 
            sprintf(tmp, "%0.3X: %0.1X%0.1X TCS 0   ; transmit carry subtract and clear carry", adr, opr, opa);
            Serial.println(tmp);
            break;
          case 0b1010: 
            sprintf(tmp, "%0.3X: %0.1X%0.1X STC 1   ; set carry", adr, opr, opa);
            Serial.println(tmp);
            break;
          case 0b1011: 
            sprintf(tmp, "%0.3X: %0.1X%0.1X DAA CY  ; decimal adjust accumulator", adr, opr, opa);
            Serial.println(tmp);
            break;
          case 0b1100: 
            sprintf(tmp, "%0.3X: %0.1X%0.1X KBP     ; keyboard process", adr, opr, opa);
            Serial.println(tmp);
            break;
          case 0b1101: 
            sprintf(tmp, "%0.3X: %0.1X%0.1X DCL     ; designate command line", adr, opr, opa);
            Serial.println(tmp);
            break;
          default: // Error
            Serial.write("ERROR - unknown OPA for 0b1111 cmd \n"); 
        }        
        break;
    } 
  }
}

////////////////////////////////////////////////////////////////////
// Processor Control Loop
////////////////////////////////////////////////////////////////////
// This is where the action is.
// it reads processor control signals and acts accordingly.
//

// Variables to keep track of IO operations
// SRC instructions sends 8bit during X2 & X3.
// I/O instructions use M1 4-bit to process 4-bit during M2.
//
byte OPR          = 0;
byte OPA          = 0;
byte M1_OPR       = 0;
byte M2_OPA       = 0;
byte M2_CMROM     = 0;
byte M2_CMRAM     = 0;
byte X2_CMROM     = 0;
byte X2_CMRAM     = 0;
byte X2_CHIPnREG  = 0;
byte X3_CHAR      = 0;
bool SRC_issued   = false;
bool IO_inst_exec = false;

// Debug
byte count  = 0;

inline __attribute__((always_inline))
void cpu_tick()
{   
  // Details are implemented based on the book
  // Microcomputers/Microprocessors: Hardware, Software, and Applications
  // John L. Hilburn, Paul M. Julich
  
  //##################################################//
  // 4004 has 8 clock cycles in one instruction cycle
  // A1, A2, A3, M1, M2, X1, X3, X3
  // we start w/ WAIT_SYNC state to synchronize w/ 4004
  // then loop and verify SYNC continously.

  switch(cpu_state) {

    // ##################################################
    // ##################################################
    // ##################################################
    case CPU_WAIT_SYNC:
      PHI_SET(0b01); PHI_SET(0b01);   // PHI1=0, PHI2=1
      LEVEL_SHIFT_PROP_DELAY;         // 550ns max prop delay in CD4504B
      PHI_SET(0b11);                  // PHI1=1, PHI2=1
      
      if (outputDEBUG)
      {
        sprintf(tmp, "W. SYNC=%0.1X ", STATE_SYNC);
        Serial.write(tmp);
        count++;
        if (count == 10)
        {
          count = 0;
          Serial.write("\n");
        }
      }

      if (STATE_SYNC)
      {
        // Found SYNC signal, yay.
        if (outputDEBUG) Serial.write("S\n");
        next_cpu_state = CPU_A1;
      }
      else if (digitalRead(uP_RESET) == true)
      {
        // Reset released before we can SYNC
        Serial.println("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");
        Serial.print(count);
        Serial.println(" ERROR: RESET RELEASED B4 SYNC");
        Serial.println("!!!!!!!!!! halted !!!!!!!!!!!!");
        while(1);                
      }
      else
      {
        // keep waiting for sync
#if (outputDEBUG)
        sprintf(tmp, "W. SYNC=%0.1X ", digitalRead(uP_SYNC));
        Serial.write(tmp);
        count++;
        if (count == 4)
        {
          count = 0;
          Serial.write("\n");
        }
#endif
      }
      LEVEL_SHIFT_PROP_DELAY;

      PHI_SET(0b10); PHI_SET(0b10);   // PHI1=1, PHI2=0      
      PHI_SET(0b11);                  // PHI1=1, PHI2=1
      // LEVEL_SHIFT_PROP_DELAY;
      break;
      
    // ##################################################
    // ##################################################
    // ##################################################
    case CPU_A1:
      if (outputDEBUG) Serial.write("A1");

      PHI_SET(0b01); PHI_SET(0b01);   // PHI1=0, PHI2=1
      DRIVE_DBUS_STOP;
      LEVEL_SHIFT_PROP_DELAY;
      
      uP_ADDR = DATA4_IN();

      PHI_SET(0b11);                  // PHI1=1, PHI2=1
      LEVEL_SHIFT_PROP_DELAY;
      PHI_SET(0b10); PHI_SET(0b10);   // PHI1=1, PHI2=0      
      PHI_SET(0b11);                  // PHI1=1, PHI2=1
      // LEVEL_SHIFT_PROP_DELAY;
      next_cpu_state = CPU_A2;
      break;
 
    // ##################################################
    // ##################################################
    // ##################################################
    case CPU_A2:
      if (outputDEBUG) Serial.write("2");
      
      PHI_SET(0b01); PHI_SET(0b01);   // PHI1=0, PHI2=1
      LEVEL_SHIFT_PROP_DELAY;

      uP_ADDR = uP_ADDR | (DATA4_IN() << 4);

      PHI_SET(0b11);                  // PHI1=1, PHI2=1
      LEVEL_SHIFT_PROP_DELAY;
      PHI_SET(0b10); PHI_SET(0b10);   // PHI1=1, PHI2=0      
      PHI_SET(0b11);                  // PHI1=1, PHI2=1
      // LEVEL_SHIFT_PROP_DELAY;
      next_cpu_state = CPU_A3;
      break;

    // ##################################################
    // ##################################################
    // ##################################################
    case CPU_A3:
      if (outputDEBUG) Serial.write("3");

      PHI_SET(0b01); PHI_SET(0b01);   // PHI1=0, PHI2=1
      LEVEL_SHIFT_PROP_DELAY;

      uP_ADDR = uP_ADDR | (DATA4_IN() << 8);
      
      if (outputDEBUG)
      {
        sprintf(tmp, " ADDR=%0.3X ", uP_ADDR);
        Serial.write(tmp);
        sprintf(tmp, " CMRO/A=%0.2X:%0.2X ", STATE_CMROM, STATE_CMRAM);
        Serial.write(tmp);
      }

      PHI_SET(0b11);                  // PHI1=1, PHI2=1
      LEVEL_SHIFT_PROP_DELAY;
      PHI_SET(0b10); PHI_SET(0b10);   // PHI1=1, PHI2=0      
      PHI_SET(0b11);                  // PHI1=1, PHI2=1
      // LEVEL_SHIFT_PROP_DELAY;

      next_cpu_state = CPU_M1;
      break;

    // ##################################################
    // ##################################################
    // ##################################################
    case CPU_M1:
      if (outputDEBUG) Serial.write("M1");

      PHI_SET(0b01); PHI_SET(0b01);   // PHI1=0, PHI2=1
      DRIVE_DBUS_START;

      if ( (ROM_START <= uP_ADDR) && (uP_ADDR <= ROM_END) )
      {
        OPR = (rom_bin [ (uP_ADDR - ROM_START) ]) >> 4;
        if (outputDEBUG) Serial.write("#");
      }
      else
      {
        OPR = 0x00;
        Serial.print("JUMP TO NON-EXISTENT ROM ADDRESS: ");
        Serial.print("--       RESETting             -- ");
        Serial.println(uP_ADDR, HEX);
        // while(1);        
        resetFunc();
      } 
      DATA4_OUT( OPR );    // FIXME - why?

      // Keep track for I/O operations.
      M1_OPR = OPR;

      LEVEL_SHIFT_PROP_DELAY;

      PHI_SET(0b11);                  // PHI1=1, PHI2=1
      LEVEL_SHIFT_PROP_DELAY;
      PHI_SET(0b10); PHI_SET(0b10);   // PHI1=1, PHI2=0      
      PHI_SET(0b11);                  // PHI1=1, PHI2=1
      // LEVEL_SHIFT_PROP_DELAY;

      next_cpu_state = CPU_M2;
      break;

    // ##################################################
    // ##################################################
    // ##################################################
    case CPU_M2:
      if (outputDEBUG) Serial.write("2");        

      PHI_SET(0b01); PHI_SET(0b01);   // PHI1=0, PHI2=1

      // Continue ROM read
      if ( (ROM_START <= uP_ADDR) && (uP_ADDR <= ROM_END) )
      {
        OPA = (rom_bin [ (uP_ADDR - ROM_START) ]) & 0x0F;
        if (outputDEBUG) Serial.write("@");
      }
      else
      {
        OPA = 0x00;
        Serial.print("JUMP TO NON-EXISTENT ROM ADDRESS: ");
        Serial.print("--       RESETting             -- ");
        Serial.println(uP_ADDR, HEX);
        // while(1);
        resetFunc();
      }
      DATA4_OUT( OPA );    // FIXME

      if ( (STATE_CMROM > 0) | (STATE_CMRAM > 0) )
      {
        // Need to latch this state because some instructions like FIN
        // take 2 instruction cycles.  I had a bug where IO WPM was 
        // getting executed by mistake.

        IO_inst_exec = true;

        // Save in case of I/O for X2/X3.
        M2_OPA    = OPA;
        M2_CMROM  = STATE_CMROM;
        M2_CMRAM  = STATE_CMRAM_0321;
      }      

      LEVEL_SHIFT_PROP_DELAY;
      
#if outputDEBUG
      if (IO_inst_exec) // (M1_OPR == 0x0E)
      {
        sprintf(tmp, " IO CMRO/A=%0.1X:%0.1X  INSTR=%0.1X%0.1X ", STATE_CMROM, STATE_CMRAM_0321, M1_OPR, M2_OPA );
        Serial.println(tmp);
      }
#endif

      PHI_SET(0b11);                  // PHI1=1, PHI2=1
      LEVEL_SHIFT_PROP_DELAY;
      PHI_SET(0b10); PHI_SET(0b10);   // PHI1=1, PHI2=0      
      PHI_SET(0b11);                  // PHI1=1, PHI2=1
      // LEVEL_SHIFT_PROP_DELAY;
     
      next_cpu_state = CPU_X1;
      break;
 
    // ##################################################
    // ##################################################
    // ##################################################
    case CPU_X1:
      
      if (outputDEBUG) Serial.write("X1");

      PHI_SET(0b01); PHI_SET(0b01);   // PHI1=0, PHI2=1      
      DRIVE_DBUS_STOP;
      
      if (outputDEBUG)
      {
        sprintf(tmp, " OPA=%0.1X ", DATA4_IN() );
        Serial.write(tmp);
      }
      LEVEL_SHIFT_PROP_DELAY;

      PHI_SET(0b11);                  // PHI1=1, PHI2=1
      LEVEL_SHIFT_PROP_DELAY;
      PHI_SET(0b10); PHI_SET(0b10);   // PHI1=1, PHI2=0      
      PHI_SET(0b11);                  // PHI1=1, PHI2=1
      // LEVEL_SHIFT_PROP_DELAY;

      next_cpu_state = CPU_X2;
      break;
 
    // ##################################################
    // ##################################################
    // ##################################################
    case CPU_X2:
      if (outputDEBUG) Serial.print("2");

      PHI_SET(0b01); PHI_SET(0b01);   // PHI1=0, PHI2=1
      LEVEL_SHIFT_PROP_DELAY;
      
      //////////////////////////////////////////////////
      // Check if SRC instruction
      if ( (STATE_CMROM > 0) || (STATE_CMRAM > 0) )
      {
#if outputDEBUG
        sprintf(tmp, "  SRC CMRO/A=%0.1X:%0.1X  CHIPnREG=%0.1X ", STATE_CMROM, STATE_CMRAM_0321, DATA4_IN() );
        Serial.write(tmp);
#endif

        X2_CMROM    = STATE_CMROM;
        X2_CMRAM    = STATE_CMRAM_0321;      // >>1 required for bank0=0x08
        X2_CHIPnREG = DATA4_IN();

        // Selected bank ROM/RAM latches X2 & X3 during SRC
        SRC_RAM_X2[X2_CMRAM] = X2_CHIPnREG;    // Selected RAM latches X2 (Chip & Reg)
        SRC_ROM_X2[X2_CMROM] = X2_CHIPnREG;    // Selected ROM latches X2 (Chip 4bits)

        SRC_issued = true;
      }
      else
      //////////////////////////////////////////////////
      // Check if this was I/O cycle
      if (IO_inst_exec)
      {
        IO_inst_exec = false;

        // We have to do what the OPA means:
        switch (M2_OPA) 
        {
          case 0b0000: // WRM - write ACC to memory
            uP_IO_executed = true;
            RAM_CHARS[M2_CMRAM][ SRC_RAM_X2[M2_CMRAM] ][ SRC_RAM_X3[M2_CMRAM] ] = DATA4_IN();
            if (outputDEBUG) 
            {
              sprintf(tmp, " WRM %0.1X-%0.1X-%0.1X D:%0.1X", M2_CMRAM, SRC_RAM_X2[M2_CMRAM], SRC_RAM_X3[M2_CMRAM], DATA4_IN());
              Serial.write(tmp);
            }            
            break;
            
          case 0b0001: // WMP - write ACC to RAM output port
            uP_IO_executed = true;
            RAM_IO[M2_CMRAM][ SRC_RAM_X2[M2_CMRAM]>>2 ] = DATA4_IN();
            if (outputDEBUG) Serial.print(" WMP ");
            break;
            
          case 0b0010: // WRR - write ACC to ROM output port
            uP_IO_executed = true;
            ROM_IO[ SRC_ROM_X2[M2_CMROM] ] = DATA4_IN();
            if (outputDEBUG) { Serial.print(" WRR ");Serial.print(X2_CHIPnREG, HEX);Serial.print(" "); }
            break;
            
          case 0b0011: // WPM - write ACC to executable RAM (4008/4009 only)
            uP_IO_executed = true;
            if (1) 
            {
              Serial.println(" WPM NOT SUPPORTED YET !!! ");
              Serial.print  ("ADDR          : "); Serial.print(uP_ADDR, HEX); Serial.println("   ");
              Serial.print  ("M2_CMRAM      : "); Serial.print(M2_CMRAM, HEX); Serial.println("   ");
              Serial.print  ("SRC_X2_ChipReg: "); Serial.print(SRC_RAM_X2[M2_CMRAM], HEX); Serial.println("   ");
              Serial.print  ("SRC_X2_Char   : "); Serial.print(SRC_RAM_X3[M2_CMRAM], HEX); Serial.println("   ");
            }
            while(1);       // we should not see this w/ busicom
            break;
            
          case 0b0100: // WR0 - write ACC to RAM status 0
            uP_IO_executed = true;
            RAM_STATUS[M2_CMRAM][ SRC_RAM_X2[M2_CMRAM] ][0] = DATA4_IN();
            if (outputDEBUG) 
            {
              sprintf(tmp, " WR0 %0.1X-%0.1X D:%0.1X", M2_CMRAM, SRC_RAM_X2[M2_CMRAM], DATA4_IN());
              Serial.write(tmp);
            }
            break;
            
          case 0b0101: // WR1 - write ACC to RAM status 1
            uP_IO_executed = true;
            RAM_STATUS[M2_CMRAM][ SRC_RAM_X2[M2_CMRAM] ][1] = DATA4_IN();
            if (outputDEBUG) 
            {
              sprintf(tmp, " WR1 %0.1X-%0.1X D:%0.1X", M2_CMRAM, SRC_RAM_X2[M2_CMRAM], DATA4_IN());
              Serial.write(tmp);
            }
            break;
            
          case 0b0110: // WR2 - write ACC to RAM status 2
            uP_IO_executed = true;
            RAM_STATUS[M2_CMRAM][ SRC_RAM_X2[M2_CMRAM] ][2] = DATA4_IN();
            if (outputDEBUG) 
            {
              sprintf(tmp, " WR2 %0.1X-%0.1X D:%0.1X", M2_CMRAM, SRC_RAM_X2[M2_CMRAM], DATA4_IN());
              Serial.write(tmp);              
            }
            break;
            
          case 0b0111: // WR3 - write ACC to RAM status 3
            uP_IO_executed = true;
            RAM_STATUS[M2_CMRAM][ SRC_RAM_X2[M2_CMRAM] ][3] = DATA4_IN();
            if (outputDEBUG) 
            {
              sprintf(tmp, " WR3 %0.1X-%0.1X D:%0.1X", M2_CMRAM, SRC_RAM_X2[M2_CMRAM], DATA4_IN());
              Serial.write(tmp);              
            }
            break;
            
          case 0b1000: // SBM - subtract RAM character from ACC
            uP_IO_executed = true;
            DRIVE_DBUS_START;
            DATA4_OUT( RAM_CHARS[M2_CMRAM][ SRC_RAM_X2[M2_CMRAM] ][ SRC_RAM_X3[M2_CMRAM] ] );
            if (outputDEBUG) 
            {
              sprintf(tmp, " SBM %0.1X-%0.1X-%0.1X D:%0.1X", M2_CMRAM, SRC_RAM_X2[M2_CMRAM], SRC_RAM_X3[M2_CMRAM], RAM_CHARS[M2_CMRAM][SRC_RAM_X2[M2_CMRAM]][SRC_RAM_X3[M2_CMRAM]]);
              Serial.write(tmp);              
            }
            break;
            
          case 0b1001: // RDM - read RAM char to ACC
            uP_IO_executed = true;
            DRIVE_DBUS_START;
            DATA4_OUT( RAM_CHARS[M2_CMRAM][ SRC_RAM_X2[M2_CMRAM] ][ SRC_RAM_X3[M2_CMRAM] ] );
            if (outputDEBUG) 
            {
              sprintf(tmp, " RDM %0.1X-%0.1X-%0.1X D:%0.1X", M2_CMRAM, SRC_RAM_X2[M2_CMRAM], SRC_RAM_X3[M2_CMRAM], RAM_CHARS[M2_CMRAM][SRC_RAM_X2[M2_CMRAM]][SRC_RAM_X3[M2_CMRAM]]);
              Serial.write(tmp);              
            }
            break;
            
          case 0b1010: // RDR - read ROM input port to ACC
            uP_IO_executed = true;
            DRIVE_DBUS_START;
            DATA4_OUT( ROM_IO[ SRC_ROM_X2[M2_CMROM] ] );
            if (outputDEBUG) Serial.print(" RDR ");
            break;
            
          case 0b1011: // ADM - add RAM char to ACC
            uP_IO_executed = true;
            DRIVE_DBUS_START;
            DATA4_OUT( RAM_CHARS[M2_CMRAM][ SRC_RAM_X2[M2_CMRAM] ][ SRC_RAM_X3[M2_CMRAM] ] );
            if (outputDEBUG) 
            {
              sprintf(tmp, " ADM %0.1X-%0.1X-%0.1X D:%0.1X", M2_CMRAM, SRC_RAM_X2[M2_CMRAM], SRC_RAM_X3[M2_CMRAM], RAM_CHARS[M2_CMRAM][SRC_RAM_X2[M2_CMRAM]][SRC_RAM_X3[M2_CMRAM]]);
              Serial.write(tmp);              
            }
            break;
            
          case 0b1100: // RD0 - read RAM status 0 to ACC
            uP_IO_executed = true;
            DRIVE_DBUS_START;
            DATA4_OUT( RAM_STATUS[M2_CMRAM][ SRC_RAM_X2[M2_CMRAM] ][0] );
            if (outputDEBUG) 
            {
              sprintf(tmp, " RD0 %0.1X-%0.1X D:%0.1X", M2_CMRAM, SRC_RAM_X2[M2_CMRAM], RAM_STATUS[M2_CMRAM][SRC_RAM_X2[M2_CMRAM]][0]);
              Serial.write(tmp);              
            }
            break;
            
          case 0b1101: // RD1 - read RAM status 1 to ACC
            uP_IO_executed = true;
            DRIVE_DBUS_START;
            DATA4_OUT( RAM_STATUS[M2_CMRAM][ SRC_RAM_X2[M2_CMRAM] ][1] );
            if (outputDEBUG) 
            {
              sprintf(tmp, " RD1 %0.1X-%0.1X D:%0.1X", M2_CMRAM, SRC_RAM_X2[M2_CMRAM], RAM_STATUS[M2_CMRAM][SRC_RAM_X2[M2_CMRAM]][1]);
              Serial.write(tmp);              
            }
            break;
            
          case 0b1110: // RD2 - read RAM status 2 to ACC
            uP_IO_executed = true;
            DRIVE_DBUS_START;
            DATA4_OUT( RAM_STATUS[M2_CMRAM][ SRC_RAM_X2[M2_CMRAM] ][2] );
            if (outputDEBUG) 
            {
              sprintf(tmp, " RD2 %0.1X-%0.1X D:%0.1X", M2_CMRAM, SRC_RAM_X2[M2_CMRAM], RAM_STATUS[M2_CMRAM][SRC_RAM_X2[M2_CMRAM]][2]);
              Serial.write(tmp);              
            }
            break;
            
          case 0b1111: // RD3 - read RAM status 3 to ACC
            uP_IO_executed = true;
            DRIVE_DBUS_START;
            DATA4_OUT( RAM_STATUS[M2_CMRAM][ SRC_RAM_X2[M2_CMRAM] ][3] );
            if (outputDEBUG) 
            {
              sprintf(tmp, " RD3 %0.1X-%0.1X D:%0.1X", M2_CMRAM, SRC_RAM_X2[M2_CMRAM], RAM_STATUS[M2_CMRAM][SRC_RAM_X2[M2_CMRAM]][3]);
              Serial.write(tmp);
            }
            break;
            
          default: // Error
            Serial.write("ERROR - unknown I/O cmd OPA\n"); 
        }
      }
      // One more???
      // LEVEL_SHIFT_PROP_DELAY;

      PHI_SET(0b11);                  // PHI1=1, PHI2=1
      PHI_SET(0b11);                  // PHI1=1, PHI2=1
      LEVEL_SHIFT_PROP_DELAY;

      PHI_SET(0b10); PHI_SET(0b10);   // PHI1=1, PHI2=0      
      PHI_SET(0b11);                  // PHI1=1, PHI2=1
      // LEVEL_SHIFT_PROP_DELAY;
      
      next_cpu_state = CPU_X3;
      break;
 
    // ##################################################
    // ##################################################
    // ##################################################
    case CPU_X3:
      if (outputDEBUG) Serial.write("3");

      PHI_SET(0b01); PHI_SET(0b01);   // PHI1=0, PHI2=1
      DRIVE_DBUS_STOP;
      
      if (SRC_issued)
      {
        SRC_issued = false;

        X3_CHAR = DATA4_IN();
        SRC_RAM_X3[X2_CMRAM] = X3_CHAR;
        // ROM ignores X3.
          
        if (outputDEBUG) 
        {
          sprintf(tmp, " CHAR=%0.1X ", X3_CHAR );
          Serial.println(tmp);          
        }
      }
      
      if (outputDEBUG)
        if (STATE_SYNC) 
          Serial.write(" +SYNC\n");
        else 
          Serial.write("MISSING SYNC\n");

      PHI_SET(0b11);                  // PHI1=1, PHI2=1
      LEVEL_SHIFT_PROP_DELAY;
      PHI_SET(0b10); PHI_SET(0b10);   // PHI1=1, PHI2=0      
      PHI_SET(0b11);                  // PHI1=1, PHI2=1
      LEVEL_SHIFT_PROP_DELAY;

      next_cpu_state = CPU_A1;
      count = 0;
      
      if (outputDEBUG_dis)
        k4004_disassemble(uP_ADDR, M1_OPR, M2_OPA);

      break;
  }
    
  // ##################################################
  // ##################################################
  // ##################################################
  cpu_state = next_cpu_state;
  // delayMicroseconds(100);
}

////////////////////////////////////////////////////////////////////
// Setup
////////////////////////////////////////////////////////////////////

void setup() 
{

  Serial.begin(115200);

  Serial.write("\n");
  Serial.write(27);       // ESC command
  Serial.print("[2J");    // clear screen command
  Serial.write(27);
  Serial.print("[H");
  Serial.println("\n");
  Serial.println("=======================================================");
  Serial.println("Retro Shield 4004 - Busicom-141PF emulation");
  Serial.println(">>> HUGE THANKS to Tim McNerney for helping me figure out details.");
  Serial.println("License Notes:");
  Serial.println("ROM contents taken from Busicom-141PF simulator ");
  Serial.println("by Fred Huettig. See LICENSE_ROM_CODE for his license.");
  Serial.println("");
  Serial.println("Printer emulation modified from model-102-printer-sim.c");
  Serial.println("by Tim McNerney. See model-102-printer.sim.c for license.");
  Serial.println("=======================================================");
  print_key_mappings();
      
  if (outputDEBUG_IO)
  {
    delay(1000);
    // Clear screen 
    Serial.write(27);       // ESC command
    Serial.print("[2J");    // clear screen command
    Serial.write(27);
    Serial.print("[H");    
  }
    
  // Reset processor
  //
  // Serial.println("Resetting");
  
  // Initialize processor GPIO'
  k4004_IO_init();
  printer_init();
  uP_init();
    
  k4004_reset_until_sync();
    
  // Go, go, go
  uP_release_reset();

}

////////////////////////////////////////////////////////////////////
// Loop()
////////////////////////////////////////////////////////////////////

void loop()
{
  
  // Loop forever
  //
  while(1)
  {    
    cpu_tick();

    if (cpu_state == CPU_A1)
    {
      k4004_IO_process();       // process I/O ports.
      printer_rotate();         // rotate printer
      k4004_keyboard_map();     // process keyboard
    }
        
    // delay(100);
  }
}
