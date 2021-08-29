//##############################
// Tim's printer code modified for RetroShield 4004 busicom
//+++++ Erturk's Additions/Modifications
//##############################

////////////////////////////////////////////////////////////////////
// Printer Emulation
////////////////////////////////////////////////////////////////////
//-------------------------------------------------------------------------------
// Shinshu Seiki Model-102 printer emulator and exerciser software for PIC18F2320
// Version 1.0.0, released on November 15, 2008.
// Written for CCS C compiler (http://www.ccsinfo.com/)
// Author: Tim McNerney
//-------------------------------------------------------------------------------
//
// LEGAL NOTICE, DO NOT REMOVE
// 
// Notice: This software and documentation is provided "AS IS."  There
//         is no warranty, claims of accuracy or fitness for any
//         purpose other than for education.  The authoritative version
//         of this file can be found at http://www.4004.com
//  
// You are free:
//  
// * to copy, distribute, display, and perform this work
// * to make derivative works
//  
// Under the following conditions:
//  
//   Attribution.  You must attribute the work in the manner specified
//                 by the author or licensor.
//  
//   Noncommercial. You may not use this work for commercial purposes.
//  
//   Share Alike.  If you alter, transform, or build upon this work, you
//                 may distribute the resulting work only under a
//                 license identical to this one.
//  
// * For any reuse or distribution, you must make clear to others the
//   license terms of this work.
// * Any of these conditions can be waived if you get permission from
//   the copyright holder.
//  
// Your fair use and other rights are in no way affected by the above.
// 
// This is a human-readable summary of the Legal Code (the full license)
// available at:
//
//   http://creativecommons.org/licenses/by-nc-sa/2.5/legalcode
//-------------------------------------------------------------------------------
// model-102-printer-sim.c -- Simulator for Shinshu-Seiki Model 102 printer
//-------------------------------------------------------------------------------

////////////////////////////////////////////////////////////////////
// Printer Emulation
////////////////////////////////////////////////////////////////////
//-------------------------------------------------------------------------------
// Shinshu Seiki Model-102 printer emulator and exerciser software for PIC18F2320
// Version 1.0.0, released on November 15, 2008.
// Written for CCS C compiler (http://www.ccsinfo.com/)
// Author: Tim McNerney
//-------------------------------------------------------------------------------

// Printer Parameters

#define START_COL     1 // col 0 for sign
#define LINE_WIDTH    20
#define COL_17A_INDEX 16
#define COL_17B_INDEX 17
#define COL_18A_INDEX 18
#define COL_18B_INDEX 19


//##############################
//+++++ Erturk's Additions
// Convert Printer Drum Timings from time -> cpu cycles.

#define I4004_INSTR_USEC      22  // 10.8uSec rounded.

#define PSYNC_PULSE_WIDTH_MS  15  // Monroe experiments suggest 10ms
#define SAMPLE_DELAY_MS       27  // 7ms from simulation + 42% margin
#define SECTOR_PERIOD_MS      28  // based on Monroe 1330 measurements

#define DRUM_PSYNC_ON         0
#define DRUM_PSYNC_OFF        (1000*PSYNC_PULSE_WIDTH_MS  / I4004_INSTR_USEC)
#define DRUM_SAMPLE           DRUM_CYCLE_END - 5
#define DRUM_CYCLE_END        (1000*SECTOR_PERIOD_MS      / I4004_INSTR_USEC)
//##############################


// Constants

const char printdigits[14] = "0123456789..-";
const char col_17A[14]     = "<    MM  S   ";
const char col_17B[14]     = ">+-x/+-^=q%CR";
const char col_18A[14]     = "     MM   E  ";
const char col_18B[14]     = "#*123+-TKExCM";

// Globals

unsigned char print_hammers_byte0;
unsigned char print_hammers_byte1;
unsigned char print_hammers_byte2;
char          line_buffer[LINE_WIDTH+1];
int           sector;
int           negative;
int           feed;
word          drum_state;


//##############################
//+++++ Erturk's Additions
char key_map[8][4] = {
  /* bit0 */ 'X', 'V', 'Z', 'A',    // CM  RM  M-  M+
  /* bit1 */ 'S', '%', 'L', 'P',    // SQ  %   M=- M=+
  /* bit2 */ '[', '/', '*', '=',    // DIA /   *   =
  /* bit3 */ '-', '+', ']', 'O',    // -   +   D2  000
  /* bit4 */ '9', '6', '3', '.',    // 9   6   3   .
  /* bit5 */ '8', '5', '2', 'I',    // 8   5   2   00
  /* bit6 */ '7', '4', '1', '0',    // 7   4   1   0
  /* bit7 */ 'Q', 'E', '`', 'C'    // SI  EX  CE  C
};

byte key_pressed              = 0;
char keypress_which           = '?';      // Converted to upper case.
char keypress_which_raw       = '?';      // unconverted to upper case.
word keypress_column;
byte keypress_row;
word keypress_delay           = 350;      // wait this many cpu instructions between key presses.
byte busicom_sw_digital_point = 3;        // digits after decimal point.
byte busicom_sw_round         = 0;        // FLoat/ROund/TRuncate

//////////////////////////////////////////////////
// Because 4004 is running slower on Arduino (~200kHz)
// we need to add some delay between key presses
// so 4004 can keep up.  I use "keypress_delay"
// to wait that many cpu cycles between presses.
// 350 seems like a good delay. If you miss key presses
// we can increase it more.
//////////////////////////////////////////////////

inline __attribute__((always_inline))
void k4004_keyboard_map()
{

  // digit point switch, value 0,1,2,3,4,5,6,8 can be switched
  if ( ~kbd_i4003_shifter_output & 0b0100000000)
  {
    ROM_IO[1] = busicom_sw_digital_point;
  }
  else
  // (rounding switch, value 0,1,8 can be switched)
  if ( ~kbd_i4003_shifter_output & 0b1000000000)
  {
    ROM_IO[1] = busicom_sw_round;
  }
  else
  if (key_pressed)
  {
    // Emulate key press as long as "key_pressed cycle"
    if ( ~kbd_i4003_shifter_output & keypress_column )
    {
      ROM_IO[1] = keypress_row;
      key_pressed--;   
      keypress_delay = 350;
      
      if (outputDEBUG)
      {
        Serial.print("PUSHING ["); Serial.print(keypress_which); Serial.print("] ");
        Serial.print(keypress_column); Serial.print(" / "); Serial.println(keypress_row);
        Serial.println(~kbd_i4003_shifter_output, BIN);
        Serial.println(keypress_column, BIN);
      }
    }
  }
  else
  if ((--keypress_delay) == 0)
  {
    keypress_delay = 350;
    
    // Check if we received a key from Arduino UART
    if ( (RAM_STATUS[0][0][3] == 0) && (Serial.available()) )
    {
      keypress_which = toupper( keypress_which_raw = Serial.read() );
      for (int i=0; i<8; i++)
        for (int j=0; j<4; j++)
          if (key_map[i][j] == keypress_which)
          {
            // Found the key; press it.
            key_pressed = 12;
            keypress_column = (1 << i);
            keypress_row = (1 << j);
            
            if (outputDEBUG)
            {
              Serial.print("KEY PRESSED ["); Serial.print(keypress_which); Serial.print("] => ");
              Serial.print(i); Serial.print(" / "); Serial.println(j);
            }
          }
      if (key_pressed == 0)
      {        
        // a key was pressed but not processed by busicom
        // f/F : to adjust floating point location.
        // R   : to adjust FLoat/ROund/TRuncate

        if (keypress_which_raw == '?')
        {
          print_key_mappings();
        }
        else
        if (keypress_which_raw == 'f')
        {       
          if (busicom_sw_digital_point == 0)
            busicom_sw_digital_point = 0;
          else
            busicom_sw_digital_point--;
          Serial.print(" Fdigit set to "); Serial.println(busicom_sw_digital_point);
        }
        else
        if (keypress_which_raw == 'F')
        {       
          busicom_sw_digital_point++;
          if (busicom_sw_digital_point == 9)
            busicom_sw_digital_point = 8;
          Serial.print(" Fdigit set to "); Serial.println(busicom_sw_digital_point);
        }       
        else
        if (keypress_which == 'R')
        {       
          switch(busicom_sw_round)
          {
            case 0: busicom_sw_round = 1; Serial.println("ROund"); break;
            case 1: busicom_sw_round = 8; Serial.println("TRuncate"); break;
            case 8: busicom_sw_round = 0; Serial.println("FLoat"); break;
            default: busicom_sw_round = 0;
          }
        }       
      }
    }
   
  }
  else
  {
    // Key delay mode.
    ROM_IO[1] = 0x00;
  }
}
//##############################


//  ;bit00    column 17 special characters
//  ;bit01    column 18 special characters
//  ;bit02    -   not used
//  ;bit03    column 1  digit or digit point
//  ;bit04    column 2  digit or digit point
//  ;bit05    column 3  digit or digit point
//  ;bit06    column 4  digit or digit point
//  ;bit07    column 5  digit or digit point
//  ;bit08    column 6  digit or digit point
//  ;bit09    column 7  digit or digit point
//  ;bit10    column 8  digit or digit point
//  ;bit11    column 9  digit or digit point
//  ;bit12    column 10 digit or digit point
//  ;bit13    column 11 digit or digit point
//  ;bit14    column 12 digit or digit point
//  ;bit15    column 13 digit or digit point
//  ;bit16    column 14 digit or digit point
//  ;bit17    column 15 digit or digit point
//  ;bit18    -   not used
//  ;bit19    -   not used

// Need to sample bytes according to above order:

//##############################
//+++++ Erturk's Modifications
inline __attribute__((always_inline))
void sample_print_signals (void)
{
  print_hammers_byte0 = ( (prt_i4003_shifter_output>>3) & 0x000FF);       // sample_print_byte0();
  print_hammers_byte1 = ( (prt_i4003_shifter_output>>3) & 0x0FF00) >> 8;  // sample_print_byte1();
  print_hammers_byte2 = ( (prt_i4003_shifter_output   ) & 0b11);          // sample_print_byte2();

  negative  = negative | (RAM_STATUS[0][1][0] & 0b0001);
  feed      = RAM_IO[0][0] & 0b1000;

  if (0)
  {
    Serial.print("\nSAMPLE_PRINTER: ");
    Serial.print(print_hammers_byte2, HEX); Serial.print(":");
    Serial.print(print_hammers_byte1, HEX); Serial.print(":");
    Serial.print(print_hammers_byte0, HEX); Serial.print("  Neg: ");
    Serial.print(negative, HEX);            Serial.print(" feed:");
    Serial.print(feed);
  }
}
//##############################


inline __attribute__((always_inline))
void add_sign (void)
{
  signed int i;

  if (!negative) return; // redundant check
  
  for ( i=(START_COL+15-1); i>=0; i--)
  {
    if (line_buffer[i] == ' ')
    {
      line_buffer[i] = '-'; 
      return;
    }
  }
}

inline __attribute__((always_inline))
void act_on_signals (void)
{
  int col;
  int bitx;
  unsigned mask;

  if (feed) 
  {
    // Print current line to printer/screen.

    if (negative) 
    {
      add_sign();
      negative = 0;
    }
    // send string to LCD

    Serial.println(line_buffer);

    init_output_string();
    feed = 0;
    
    return; // never any printing during feed
  }
  else
  {
    col = START_COL;
    mask = 0x01;

    // columns 1-8
    for (bitx = 0; bitx < 8; bitx++)
    {
      if (print_hammers_byte0 & mask) 
      {
        line_buffer[col] = printdigits[sector];
      }
      mask <<= 1;
      col++;
    }

    // columns 9-15 (no col 16)
    mask = 0x01;
    for (bitx = 0; bitx < 7; bitx++)
    {
      if (print_hammers_byte1 & mask)
      {
        line_buffer[col] = printdigits[sector];
      }
      mask <<= 1;
      col++;
    }

    // columns 17 and 18
    mask = 0x01;
    if (print_hammers_byte2 & mask)
    {
      line_buffer[COL_17A_INDEX] = col_17A[sector];
      line_buffer[COL_17B_INDEX] = col_17B[sector];
    }
    mask = 0x02;
    if (print_hammers_byte2 & mask)
    {
      line_buffer[COL_18A_INDEX] = col_18A[sector];
      line_buffer[COL_18B_INDEX] = col_18B[sector];
    }
  }  
}

inline __attribute__((always_inline))
void init_output_string (void)
{
  int i;
  for (i = 0; i < LINE_WIDTH; i++) {
    line_buffer[i] = ' ';
  }
  line_buffer[LINE_WIDTH] = '\0';
}

//##############################
//+++++ Erturk's Modifications

inline __attribute__((always_inline))
void set_sector0(bool st)
{
  if (st)
    // set high
    ROM_IO[2] = ROM_IO[2] | 0b0001;       // Set high
  else
    // set low
    ROM_IO[2] = ROM_IO[2] & 0b1110;       // Set low
}

inline __attribute__((always_inline))
void set_psync(bool st)
{
  if (st)
    // set high
    TEST_LOW;
  else
    // set low
    TEST_HIGH;
}

inline __attribute__((always_inline))
void printer_init()
{
  // init output pins
  
  // output_high(PSYNC_PIN);
  // output_high(SECTOR0_PIN);

  sector = 0;
  drum_state = 0;
  
  set_sector0(true);
  set_psync(true);
  
  init_output_string();

}

bool drum_fast_forward = false;

inline __attribute__((always_inline))
void printer_rotate()
{
  switch(drum_state++)
  {
    case DRUM_PSYNC_ON:
      if (outputDEBUG) { Serial.print("DRUM_PSYNC_ON - SECTOR "); Serial.println(sector); }

      set_psync(true);
      if (sector == 0) set_sector0(true);

      // Development
      if (sector == 0)
        // Turn on LED bit3 to indicate drum SYNC
        RAMQ4_OUT( 0b1001 );
      else
        RAMQ4_OUT( 0b0001 );

      drum_fast_forward = false;
      break;

    case DRUM_PSYNC_OFF:
      if (outputDEBUG) { Serial.print("DRUM_PSYNC_OFF"); }
      set_psync(false);

      RAMQ4_OUT( 0b0000 );

      drum_fast_forward = false;
      break;

    case DRUM_SAMPLE:
      if (outputDEBUG) { Serial.print("DRUM_SAMPLE "); Serial.print(RAM_IO[0][0] & 0b0010, HEX); }

      if (RAM_IO[0][0] & 0b1010)     // Fire print hammers OR advance printer paper
      {
        sample_print_signals();
        act_on_signals();
      }

      // drum_fast_forward = false;
      break;

    case DRUM_CYCLE_END:
      if (outputDEBUG) { Serial.print("DRUM_CYCLE_END"); } 
      if (sector == 0) set_sector0(false);
      if (++sector == 13) sector=0;
      drum_state = 0;   
      drum_fast_forward = false;
      break;

    default:
      // Advance drum to prevent wasted CPU cycles.

      // Print special JCN TZ and JCN TN address to see which drum_state they correspond
      // So we can skip forward
      //

      if (!drum_fast_forward)
      {
        if (uP_ADDR == 0x001)
        {
          if ( (drum_state > 800) ) 
          {
            drum_state = DRUM_SAMPLE-3; 
            drum_fast_forward = true; 
          }
        }
        else
        if (uP_ADDR == 0x0fd)
        {
          if (drum_state < 683) 
          {
            drum_state = DRUM_PSYNC_OFF-3; 
            drum_fast_forward = true; 
          }
        }
        else
        if (uP_ADDR == 0x26e)
        {
          if (drum_state < 683) 
          {
            drum_state = DRUM_PSYNC_OFF-3; 
            drum_fast_forward = true;
          }
        }
        else
        if (uP_ADDR == 0x23f)
        {
          if (drum_state > 1000) 
          {
            drum_state = DRUM_SAMPLE-3; 
            drum_fast_forward = true; 
          }
        }        
        else
        if (uP_ADDR == 0x22c)
        {
          if ((drum_state > 900) )
          {
            drum_state = DRUM_SAMPLE-3; 
            drum_fast_forward = true; 
          }
        }
        else
        if (uP_ADDR == 0x24b)
        {
          if ( (drum_state > 1200) )
          {
            drum_state = DRUM_SAMPLE-3; 
            drum_fast_forward = true; 
          }
        }
        else
        if (uP_ADDR == 0x04b)
        {
          if ( (drum_state > 900) )
          {
            drum_state = DRUM_SAMPLE-3; 
            drum_fast_forward = true; 
          }
        }        
      }

//      if (uP_ADDR == 0x0fd)
//      { Serial.print("0x0fd - JCN TN - "); Serial.print(drum_state); Serial.print(" / "); Serial.println(DRUM_CYCLE_END); }
//      else
//      if (uP_ADDR == 0x26e)
//      { Serial.print("0x26e - JCN TN - "); Serial.print(drum_state); Serial.print(" / "); Serial.println(DRUM_CYCLE_END); }
//      else      
//      if (uP_ADDR == 0x001)
//      { Serial.print("0x001 - JCN TZ - "); Serial.print(drum_state); Serial.print(" / "); Serial.println(DRUM_CYCLE_END); }
//      else
//      if (uP_ADDR == 0x04b)
//      { Serial.print("0x04b - JCN TZ - "); Serial.print(drum_state); Serial.print(" / "); Serial.println(DRUM_CYCLE_END); }
//      else
//      if (uP_ADDR == 0x22c)
//      { Serial.print("0x22c - JCN TZ - "); Serial.print(drum_state); Serial.print(" / "); Serial.println(DRUM_CYCLE_END); }
//      else
//      if (uP_ADDR == 0x23f)
//      { Serial.print("0x23f - JCN TZ - "); Serial.print(drum_state); Serial.print(" / "); Serial.println(DRUM_CYCLE_END); }
//      else
//      if (uP_ADDR == 0x24b)
//      { Serial.print("0x24b - JCN TZ - "); Serial.print(drum_state); Serial.print(" / "); Serial.println(DRUM_CYCLE_END); }
//      else
//      if (uP_ADDR == 0x402)
//      { Serial.print("0x402 - JCN TZ - "); Serial.print(drum_state); Serial.print(" / "); Serial.println(DRUM_CYCLE_END); }
//      else
//      if (uP_ADDR == 0x272)
//      { Serial.print("0x272 - fire hammer - "); Serial.print(drum_state); Serial.print(" / "); Serial.println(DRUM_CYCLE_END); }
              
      break;
  }  
}
//##############################
