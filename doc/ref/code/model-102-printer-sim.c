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

// TO DO list
//
// Manual feed - NYI

#include <18f2320.h>

// Parameters

//#define TEST
#define CRLF // for regular terminal emulator, LCD doesn't need this
//#define TRACE
#define START_COL 1 // col 0 for sign
//#define LINE_WIDTH 20
//#define COL_17A_INDEX 17
//#define COL_17B_INDEX 18
//#define COL_18A_INDEX 19
//#define COL_18B_INDEX 20
#define LINE_WIDTH 20
#define COL_17A_INDEX 16
#define COL_17B_INDEX 17
#define COL_18A_INDEX 18
#define COL_18B_INDEX 19

// Print hammer/colums -> PIC ports

// Col -> Ports
// 01 02 03 04 05 06 07 08  09 10 11 12 13 14 15 16  17 18
// a0 a1 a2 a3 a4 a5 a6 a7  b3 b4 b5 c0 c1 c2 c3 nc  c4 c5

// Ports -> Col
// a7 a6 a5 a4 a3 a2 a1 a0  -- -- b5 b4 b3 -- -- --  c7 c6 c5 c4 c3 c2 c1 c0
// 08 07 06 05 04 03 02 01  -- -- 11 10 09 -- -- --  ng fd 18 17 15 14 13 12

// Byte (after packing)
// --2--  -----------1-----------  -----------0-----------
// c5 c4  nc c3 c2 c1 c0 b5 b4 b3  a7 a6 a5 a4 a3 a2 a1 a0
// 18 17  16 15 14 13 12 11 10 09  08 07 06 05 04 03 02 01 

// Shift registers
// 01 02 03 04  05 06 07 08  09 10 11 12  13 14 15 16  17 18 19 20  SR
// -- -- 15 14  13 12 11 10  09 08 07 06  05 04 03 02  01 -- 18 17  Col
// -- -- c3 c2  c1 c0 b5 b4  b3 a7 a6 a5  a4 a3 a2 a1  a0 -- c5 c4  Port
// 19 18 17 16  15 14 13 12  11 10 09 08  07 06 05 04  03 02 01 00  >>

// porta = (printshift  >>  3) & 0x00ff;
// portb = (printshift  >>  8) & 0x0038;
// portc = ((printshift >> 12) & 0x000f) 
//       | ((printshift <<  4) & 0x0030)
//       | negative_pin << 7 | feed_pin << 6;

// NOTE: Simulator assumes positive logic

// For testing
// c6 = feed
// c7 = negative

#define PORTA_PC_BYTE0_MASK 0xff
#define PORTB_PC_BYTE1_MASK 0x38
#define PORTC_PC_BYTE1_MASK 0x0f
#define PORTC_PC_BYTE2_MASK 0x30

#define PORTA_PC_BYTE0_SHIFT // 0
#define PORTB_PC_BYTE1_SHIFT >> 3
#define PORTC_PC_BYTE1_SHIFT << 3
#define PORTC_PC_BYTE2_SHIFT >> 4

#define PC01_PIN     PIN_A0
#define PC02_PIN     PIN_A1
#define PC03_PIN     PIN_A2
#define PC04_PIN     PIN_A3
#define PC05_PIN     PIN_A4
#define PC06_PIN     PIN_A5
#define PC07_PIN     PIN_A6
#define PC08_PIN     PIN_A7
#define PC09_PIN     PIN_B3
#define PC10_PIN     PIN_B4
#define PC11_PIN     PIN_B5
#define PC12_PIN     PIN_C0
#define PC13_PIN     PIN_C1
#define PC14_PIN     PIN_C2
#define PC15_PIN     PIN_C3
#define PC17_PIN     PIN_C4
#define PC18_PIN     PIN_C5

#define MAN_FEED_PIN PIN_B0
#define FEED_PIN     PIN_B1
#define RED_INK_PIN  PIN_B2

#define PSYNC_PIN    PIN_B6
#define SECTOR0_PIN  PIN_B7

#define TX_PIN       PIN_C6
#define RX_PIN       PIN_C7

#fuses PUT, NOWDT, INTRC_IO, NOLVP  // power-up-timer, no Watchdog timer,
                                    // osc=Internal 8MHz, no LV prog
#use delay(clock=8000000, restart_wdt) // 8MHz
#use rs232(baud=9600, xmit=TX_PIN, DISABLE_INTS) // why disable ints?
#use fixed_io (b_outputs=PSYNC_PIN, SECTOR0_PIN)

// Parameters

#define PSYNC_PULSE_WIDTH_MS   5  // Monroe experiments suggest 10ms
#define SECTOR_PERIOD_MS      28  // based on Monroe 1330 measurements
#define SAMPLE_DELAY_MS       10  // 7ms from simulation + 42% margin

// Constants

const char printdigits[14] = "0123456789..-";
//const char col_17A[14]     = "<+-x/MM^=S%CR";
//const char col_17B[14]     = ">    +-  q   ";
//const char col_18A[14]     = "#*123MMTKEECM";
//const char col_18B[14]     = "     +-   x  ";
const char col_17A[14]     = "<    MM  S   ";
const char col_17B[14]     = ">+-x/+-^=q%CR";
const char col_18A[14]     = "     MM   E  ";
const char col_18B[14]     = "#*123+-TKExCM";

// Globals

unsigned char print_hammers_byte0;
unsigned char print_hammers_byte1;
unsigned char print_hammers_byte2;
char line_buffer[LINE_WIDTH+1];
int sector;
int negative;
int feed;

// Prototypes

void main (void);
void sample_print_signals (void);
unsigned char sample_print_byte0 (void);
unsigned char sample_print_byte1 (void);
unsigned char sample_print_byte2 (void);
void act_on_signals (void);
void init_output_string (void);
void add_sign (void);
int read_feed_pin (void);
int read_negative_pin (void);
unsigned int hammer_porta (void);
unsigned int hammer_portb (void);
unsigned int hammer_portc (void);
void psync_start (void);
void psync_end (void);
void sector0_start (void);
void sector0_end (void);
void advance_state (void);

// Procedures

void main (void)
{
  setup_oscillator(OSC_8MHZ);
  delay_ms(100);

  // init output pins
  output_high(PSYNC_PIN);
  output_high(SECTOR0_PIN);

  init_output_string();

  puts("");
  printf("Busicom Replica\r\n");
  printf(__DATE__ " " __TIME__ "\r\n");

 vsync:
  for (sector = 0; sector < 13; sector++) {
    if (sector == 0) {
      sector0_start();
    }
    psync_start();
    delay_ms(PSYNC_PULSE_WIDTH_MS);
    psync_end();
    
    delay_ms(SAMPLE_DELAY_MS - PSYNC_PULSE_WIDTH_MS);
    
    sample_print_signals();
    act_on_signals();

#ifndef TEST
    delay_ms(SECTOR_PERIOD_MS - SAMPLE_DELAY_MS);
#endif //~TEST

    if (sector == 0) {
      sector0_end();
    }
  }
  goto vsync;
}

void sample_print_signals (void)
{
  advance_state(); // for testing only
  print_hammers_byte0 = sample_print_byte0();
  print_hammers_byte1 = sample_print_byte1();
  print_hammers_byte2 = sample_print_byte2();
#ifdef TRACE
  printf("%x %x %x\r\n",
	 print_hammers_byte2,
	 print_hammers_byte1,
	 print_hammers_byte0);
#endif // TRACE
  negative = negative | !read_negative_pin();
  feed = !read_feed_pin();
}

unsigned char sample_print_byte0 (void)
{
  //return (~hammer_porta() & PORTA_PC_BYTE0_MASK) PORTA_PC_BYTE0_SHIFT;
  return ~hammer_porta();
}

unsigned char sample_print_byte1 (void)
{
  return (  ((~hammer_portb() & PORTB_PC_BYTE1_MASK) PORTB_PC_BYTE1_SHIFT)
	  | ((~hammer_portc() & PORTC_PC_BYTE1_MASK) PORTC_PC_BYTE1_SHIFT));
}

unsigned char sample_print_byte2 (void)
{
  return ((~hammer_portc() & PORTC_PC_BYTE2_MASK) PORTC_PC_BYTE2_SHIFT);
}

void act_on_signals (void)
{
  int col;
  int bit;
  unsigned mask;

  if (feed) {
    if (negative) {
      add_sign();
      negative = 0;
    }
    // send string to LCD
#ifdef CRLF
    puts(line_buffer);
#else //~CRLF
    printf("%s", line_buffer); // 20-char width LCD wrops, no line feed
#endif // CRLF
    init_output_string();
    feed = 0;
    
    return; // never any printing during feed
  }

  col = START_COL;
  mask = 0x01;

  // columns 1-8
  for (bit = 0; bit < 8; bit++) {
    if (print_hammers_byte0 & mask) {
      line_buffer[col] = printdigits[sector];
    }
    mask <<= 1;
    col++;
  }

  // columns 9-15 (no col 16)
  mask = 0x01;
  for (bit = 0; bit < 7; bit++) {
    if (print_hammers_byte1 & mask) {
      line_buffer[col] = printdigits[sector];
    }
    mask <<= 1;
    col++;
  }

  // columns 17 and 18
  mask = 0x01;
  if (print_hammers_byte2 & mask) {
    line_buffer[COL_17A_INDEX] = col_17A[sector];
    line_buffer[COL_17B_INDEX] = col_17B[sector];
  }
  mask = 0x02;
  if (print_hammers_byte2 & mask) {
    line_buffer[COL_18A_INDEX] = col_18A[sector];
    line_buffer[COL_18B_INDEX] = col_18B[sector];
  }
}

void init_output_string (void)
{
  int i;
  for (i = 0; i < LINE_WIDTH; i++) {
    line_buffer[i] = ' ';
  }
  line_buffer[LINE_WIDTH] = '\0';
}

void add_sign (void)
{
  signed int i;
  if(!negative) return; // redundant check
  for (i=(START_COL+15-1); i>=0; i--){
    if (line_buffer[i]==' ') {
      line_buffer[i] = '-'; 
      return;
    }
  }
}

#ifdef TEST

unsigned long test_pc = 0;

#define TEST_DATA_SIZE 480 //520 //676

unsigned int test_sector;
unsigned int test_data_a;
unsigned int test_data_b;
unsigned int test_data_c;

const unsigned int test_data [TEST_DATA_SIZE] = 
#include "model-102-test-data.c"
;

void advance_state (void)
{
  if (test_pc >= TEST_DATA_SIZE) {
    //test_data_a = 0;
    //test_data_b = 0;
    //test_data_c = 0;
    //    puts("");
    //    puts("Done");
    goto spin_loop;
  }
  else {
    test_sector = test_data[test_pc++];
    test_data_a = test_data[test_pc++];
    test_data_b = test_data[test_pc++];
    test_data_c = test_data[test_pc++];

    if (test_sector != sector) {
      printf ("Sector foo %d!=%d\r", test_sector, sector);
    spin_loop: 
      goto spin_loop;
    }
  }
}

int read_feed_pin (void)
{
  return !((test_data_c >> 6) & 0x1);
}

int read_negative_pin (void)
{
  return !((test_data_c >> 7) & 0x1);
}

unsigned int hammer_porta (void)
{
  return ~test_data_a;
}

unsigned int hammer_portb (void)
{
  return ~test_data_b;
}

unsigned int hammer_portc (void)
{
  return ~test_data_c;
}

void psync_start (void)
{
  //test_step++;
}

void psync_end (void)
{
  // nop
}

void sector0_start (void)
{
  // nop
}

void sector0_end (void)
{
  // nop
}

#else //~TEST

void advance_state (void)
{
  // nop
}

int read_feed_pin (void)
{
  return input(FEED_PIN);
}

int read_negative_pin (void)
{
  return input(RED_INK_PIN);
}

unsigned int hammer_porta (void)
{
  return input_a();
}

unsigned int hammer_portb (void)
{
  return input_b();
}

unsigned int hammer_portc (void)
{
  return input_c();
}

void psync_start (void)
{
  output_low(PSYNC_PIN);
}

void psync_end (void)
{
  output_high(PSYNC_PIN);
}

void sector0_start (void)
{
  output_low(SECTOR0_PIN);
}

void sector0_end (void)
{
  output_high(SECTOR0_PIN);
}

#endif // TEST

