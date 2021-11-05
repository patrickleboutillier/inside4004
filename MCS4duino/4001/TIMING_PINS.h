#ifndef TIMING_PINS_H
#define TIMING_PINS_H

#define CLK1        0b00010000
#define READ_CLK1   PIND &   CLK1
#define CLK1_INPUT  DDRD &= ~CLK1
#define CLK2        0b00001000
#define READ_CLK2   PIND &   CLK2
#define CLK2_INPUT  DDRD &= ~CLK2
#define READ_SYNC   PIND &   0b00000100
#define SYNC_INPUT  DDRD &= ~0b00000100

#endif
