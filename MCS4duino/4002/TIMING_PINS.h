#ifndef TIMING_PINS_H
#define TIMING_PINS_H

#define CLK1        0b00010000
#define CLK2        0b00001000
#define READ_CLK1   PINB &   CLK1
#define CLK1_INPUT  DDRB &= ~CLK1
#define READ_CLK2   PINB &   CLK2
#define CLK2_INPUT  DDRB &= ~CLK2
#define READ_SYNC   PINB &   0b00000100
#define SYNC_INPUT  DDRB &= ~0b00000100

#endif
