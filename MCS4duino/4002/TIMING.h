#ifndef TIMING_h
#define TIMING_h

#include "Arduino.h"

#define CLK1       12
#define CLK2       11
#define SYNC       10
#define READ_CLK1  PINB & 0b00010000
#define READ_CLK2  PINB & 0b00001000
#define READ_SYNC  PINB & 0b00000100


class TIMING {
  private:
    byte _slave ;
    byte _master ;
    int _phase ;
    bool _reset ;
    void (*_dispatch[8][4][8])() ;
  public:
      unsigned long _cycle ;
        
  public:
    TIMING(){  
      for (int i = 0 ; i < 8 ; i++){
        for (int j = 0 ; j < 4 ; j++){
          for (int k = 0 ; k < 8 ; k++){
            _dispatch[i][j][k] = NULL ;     
          }
        }
      }
                
      reset() ;
    }

    
    void reset(){
      _slave = 0 ;
      _master = 0 ;
      _phase = -1 ;
      _reset = 1 ;
      _cycle = 0 ;
    }

    
    void setup(){
      pinMode(CLK1, INPUT) ;
      pinMode(CLK2, INPUT) ;
      pinMode(SYNC, INPUT) ;     
    }

    
    void loop(){
      bool clk1 = READ_CLK1 ;
      bool clk2 = READ_CLK2 ;
      
      if ((clk1)&&(!clk2)){
        _slave = _master ;
        if ((_slave == 0)&&(_reset)){   // 0 == state A1!
          _reset = 0 ;
          _phase = -1 ;
          _cycle = 0 ;
        }
        if (_phase != 0){
          _cycle++ ;
        }
        _phase = 0 ;
      }
      else if ((!clk1)&&(clk2)){
        if (READ_SYNC){
          _master = 0 ;
        }
        else {
          _master = (_slave + 1) & 0x7 ;
        }
        _phase = 2 ;
      }
      else if ((!clk1)&&(!clk2)){
        if (_slave == _master){
          _phase = 1 ;
        }
        else {
          _phase = 3 ;
        }
      }
    
      if (_reset){
        return ;
      }
 
      // Do dispatch
      int i = 0 ;
      while (_dispatch[_slave][_phase][i] != NULL){
        _dispatch[_slave][_phase][i]() ;
        i++ ;
      }
    }
    
    
    void append(byte state, byte phase, void (*f)()){
      int i = 0 ;
      while (_dispatch[state][phase][i] != NULL){
        i++ ;
      }
      _dispatch[state][phase][i] = f ;
    }
    
    
    void A12(void (*f)()){
      A12clk1(f) ;
    }
    
    
    void A12clk1(void (*f)()){
      append(0, 0, f) ;
    }
    
    
    void A12clk2(void (*f)()){
      append(0, 2, f) ;
    }
    
    
    void A21(void (*f)()){
      append(0, 3, f) ;
    }
    
    
    void A22(void (*f)()){
      A22clk1(f) ;
    }
    
    
    void A22clk1(void (*f)()){
      append(1, 0, f) ;
    }
    
    
    void A22clk2(void (*f)()){
      append(1, 2, f) ;
    }
    
    
    void A31(void (*f)()){
      append(1, 3, f) ;
    }
    
    
    void A32(void (*f)()){
      A32clk1(f) ;
    }
    
    
    void A32clk1(void (*f)()){
      append(2, 0, f) ;
    }
    
    
    void A32clk2(void (*f)()){
      append(2, 2, f) ;
    }
    
    
    void M11(void (*f)()){
      append(2, 3, f) ;
    }
    
    
    void M12(void (*f)()){
      M12clk1(f) ;
    }
    
    
    void M12clk1(void (*f)()){
      append(3, 0, f) ;
    }
    
    
    void M12clk2(void (*f)()){
      append(3, 2, f) ;
    }
    
    
    void M21(void (*f)()){
      append(3, 3, f) ;
    }
    
    
    void M22(void (*f)()){
      M22clk1(f) ;
    }
    
    
    void M22clk1(void (*f)()){
      append(4, 0, f) ;
    }
    
    
    void M22clk2(void (*f)()){
      append(4, 2, f) ;
    }
    
    
    void X11(void (*f)()){
      append(4, 3, f) ;
    }
    
    
    void X12(void (*f)()){
      X12clk1(f) ;
    }
    
    
    void X12clk1(void (*f)()){
      append(5, 0, f) ;
    }
    
    
    void X12clk2(void (*f)()){
      append(5, 2, f) ;
    }
    
    
    void X21(void (*f)()){
      append(5, 3, f) ;
    }
    
    
    void X22(void (*f)()){
      X22clk1(f) ;
    }
    
    
    void X22clk1(void (*f)()){
      append(6, 0, f) ;
    }
    
    
    void X22clk2(void (*f)()){
      append(6, 2, f) ;
    }
    
    
    void X31(void (*f)()){
      append(6, 3, f) ;
    }
    
    
    void X32(void (*f)()){
      X32clk1(f) ;
    }
    
    void X32clk1(void (*f)()){
      append(7, 0, f) ;
    }
    
    
    void X32clk2(void (*f)()){
      append(7, 2, f) ;
    }
    
    
    void A11(void (*f)()){
      append(7, 3, f) ;
    }
} ;

#endif
