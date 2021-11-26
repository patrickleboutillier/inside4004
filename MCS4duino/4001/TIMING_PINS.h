#ifndef TIMING_PINS_H
#define TIMING_PINS_H

#define CLK1        0b00010000
#define CLK2        0b00001000
#define CLK_REG     PIND
#define CLK1_INPUT  DDRD &= ~CLK1
#define CLK2_INPUT  DDRD &= ~CLK2
#define SYNC_ON     PIND &   0b00000100
#define SYNC_INPUT  DDRD &= ~0b00000100

#endif
