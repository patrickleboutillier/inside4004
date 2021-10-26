#define RESET_1   A1
#define RESET_2   A3
#define CLK1_1    0b000010000   // PORTB
#define CLK1_2    0b000010000   // PORTD
#define CLK2_1    0b000001000   // PORTB
#define CLK2_2    0b000001000   // PORTD

#define CLK_US    200


void reset(){
  DDRB = DDRB | CLK1_1 | CLK2_1 ;
  DDRD = DDRD | CLK1_2 | CLK2_2 ;  
  digitalWrite(RESET_1, HIGH) ;
  digitalWrite(RESET_2, HIGH) ;
  PORTB = PORTB & ~(CLK1_1 | CLK2_1) ;
  PORTD = PORTD & ~(CLK1_2 | CLK2_2) ;
}


void setup(){
  Serial.begin(2000000) ;
  pinMode(RESET_1, OUTPUT) ;
  pinMode(RESET_2, OUTPUT) ;
  reset() ;
  delay(10000) ;
  digitalWrite(RESET_1, LOW) ;
  digitalWrite(RESET_2, LOW) ;
}


void loop(){
  while(1){
    PORTB = PORTB | CLK1_1 ;
    PORTD = PORTD | CLK1_2 ;         
    delayMicroseconds(CLK_US) ;
    PORTB = PORTB & ~CLK1_1 ;
    PORTD = PORTD & ~CLK1_2 ;
    delayMicroseconds(CLK_US) ;
    PORTB = PORTB | CLK2_1 ;
    PORTD = PORTD | CLK2_2 ;
    delayMicroseconds(CLK_US) ;
    PORTB = PORTB & ~CLK2_1 ;
    PORTD = PORTD & ~CLK2_2 ;
    delayMicroseconds(CLK_US) ;
  }
}
