#include "KEYBOARD.h"


#define DEFAULT_KEY_BUF   "11+7+="

 
const char *lookup[] = {
  "CM",  "RM", "M-",     "M+",
  "SQ",  "%",  "M=-",    "M=+",
  NULL,  "/",  "*",      "=",
  "-",   "+",  "#",      NULL,
  "9",   "6",  "3",      ".",
  "8",   "5",  "2",      NULL,
  "7",   "4",  "1",      "0",
  "S-",  "EX", "CE",     "CL"
} ;


KEYBOARD::KEYBOARD(i4003 *input, int pin_kbd_row_3, int pin_kbd_row_2, int pin_kbd_row_1, int pin_kbd_row_0, 
  int pin_send_key){
  _input = input ;
  _pin_kbd_row_3 = pin_kbd_row_3 ;
  _pin_kbd_row_2 = pin_kbd_row_2 ;
  _pin_kbd_row_1 = pin_kbd_row_1 ;
  _pin_kbd_row_0 = pin_kbd_row_0 ;
  _pin_send_key = pin_send_key ;
  _key_buffer[0] = '\0' ;
  reset() ;
}


void KEYBOARD::reset(){
  Serial.println("KEYBOARD reset") ;
  for (int i = 0 ; i < 10  ; i++){
    for (int j = 0 ; j < 4 ; j++){
      _buffer[i][j] = 0 ; 
    }
  }

  if (strcmp(DEFAULT_KEY_BUF, _key_buffer) != 0){
    _key_buffer[0] = '\0' ;
    appendKeyBuffer(DEFAULT_KEY_BUF) ;
  }
  
  _cur_send_key = 0 ;
  _reg = 0 ;
}


void KEYBOARD::loop(){
  // Check for keyboard input
  if (Serial.available()){ 
    char c = (char)Serial.read() ; 
    if ((c != '\n')&&(c != '\r')){
      char s[2] ;
      s[0] = c ; 
      s[1] = '\0' ;
      appendKeyBuffer(s) ;
    }
  }

  // Check if the keyboard is being scanned
  if (_input->getReg() != _reg){
    _reg = _input->getReg() ;
    //Serial.print("reg ") ;
    //Serial.println(_reg | 0b10000000000, BIN) ;
    for (int i = 0 ; i < 10 ; i++){
      if (_input->getBit(i) == 0){
        //Serial.print("scanning ") ;
        //Serial.print(i) ;
        //Serial.print(": ") ;
        byte data = (_buffer[i][3] << 3) | (_buffer[i][2] << 2) | (_buffer[i][1] << 1) | _buffer[i][0] ;
        //Serial.println(data) ;
        digitalWrite(_pin_kbd_row_3, _buffer[i][0]) ;
        digitalWrite(_pin_kbd_row_2, _buffer[i][1]) ;
        digitalWrite(_pin_kbd_row_1, _buffer[i][2]) ; 
        digitalWrite(_pin_kbd_row_0, _buffer[i][3]) ;            
        if (i < 8){   // Don't reset the switches!
          _buffer[i][0] = 0 ;
          _buffer[i][1] = 0 ;
          _buffer[i][2] = 0 ;
          _buffer[i][3] = 0 ;
        }
      }
    }   
  }
  
  // Check the send key signal
  if (digitalRead(_pin_send_key)){
      if (! _cur_send_key){
        sendKey() ;
        _cur_send_key = 1 ;
      }
  }
  else {
    _cur_send_key = 0 ;
  }
}


const char *KEYBOARD::getKeyBuffer(){
  return _key_buffer ;  
}


void KEYBOARD::appendKeyBuffer(const char *buf){
  strcat(_key_buffer, buf) ;
  Serial.print("key_buffer: ") ;
  Serial.println(_key_buffer) ;
}


const char *KEYBOARD::getKeyBufferHead(){
  static char head[4] ;
  head[0] = '\0' ;
  
  if (strlen(_key_buffer) == 0){
    return head ;
  }

  if ((_key_buffer[0] == 'd')||(_key_buffer[0] == 'r')||(_key_buffer[0] == 'a')||(_key_buffer[0] == 'h')){
    head[0] = _key_buffer[0] ;
    head[1] = '\0' ;
    goto done ;
  }
  
  for (int c = 0 ; c < 8 ; c++){
    for (int r = 0 ; r < 4 ; r++){
      const char *s = lookup[(c * 4) + (3 - r)] ;
      if ((s != NULL)&&(strncmp(s, _key_buffer, strlen(s)) == 0)){
        strcpy(head, s) ;
        goto done ;
      }
    }
  }

  head[0] = _key_buffer[0] ;
  head[1] = '\0' ;
  
  done:
  // Remove head from _key_buffer
  memmove(_key_buffer, _key_buffer+strlen(head), strlen(_key_buffer)-strlen(head)+1) ;

  return head ;
}


void KEYBOARD::sendKey(){
  if (strlen(_key_buffer) > 0){
    Serial.print("sendKey: ") ;
    const char *k = getKeyBufferHead() ;
    Serial.println(k) ;
    Serial.print("key_buffer: ") ;
    Serial.println(_key_buffer) ;
    if (k != NULL){
      for (int c = 0 ; c < 8 ; c++){
        for (int r = 0 ; r < 4 ; r++){
          const char *s = lookup[(c * 4) + (3 - r)] ;
          if ((s != NULL)&&(strcmp(k, s) == 0)){
            _buffer[c][r] = 1 ;
            return ;
          }
        }
      }
      Serial.print(F("!!! ERROR: Unknown key ')")) ;
      Serial.print(k) ;
      Serial.println(F("! Use 'h' for help.")) ;
    }
  }
}

          
/*
import sys
from hdl import *

'''
;shifter  ROM1 bit0     ROM1 bit1 ROM1 bit2     ROM1 bit3
;----------------------------------------------------------------------------------------------------------------------------------
;bit0   CM (81)       RM (82)   M- (83)       M+ (84)
;bit1   SQRT (85)     % (86)    M=- (87)      M=+ (88)
;bit2   diamond (89)  / (8a)    * (8b)        = (8c)
;bit3   - (8d)        + (8e)    diamond2 (8f) 000 (90)
;bit4   9 (91)        6 (92)    3 (93)        . (94)
;bit5   8 (95)        5 (96)    2 (97)        00 (98)
;bit6   7 (99)        4 (9a)    1 (9b)        0 (9c)
;bit7   Sign (9d)     EX (9e)   CE (9f)       C (a0)
;bit8   dp0           dp1       dp2           dp3 (digit point switch, value 0,1,2,3,4,5,6,8 can be switched)
;bit9   sw1           (unused)  (unused)      sw2 (rounding switch, value 0,1,8 can be switched)
;----------------------------------------------------------------------------------------------------------------------------------
'''
_lookup = [
    ["CM",  "RM", "M-",     "M+"],
    ["SQ",  "%",  "M=-",    "M=+"],
    [None,  "/",  "*",      "="],
    ["-",   "+",  "#",      None],
    ["9",   "6",  "3",      "."],
    ["8",   "5",  "2",      None],
    ["7",   "4",  "1",      "0"],
    ["S-",  "EX", "CE",     "CL"]
]
for c in _lookup:
    c.reverse()


help = '''
Keyboard (enter a sequence of keys and press enter):

                  a     d--------  r--
                              
                  S     7  8  9    -  #         CM   
                  EX    4  5  6    +  /    %    RM
                  CE    1  2  3       *    M+   M-
                  CL    0     .     =      M=+  M=-

a:  Paper feed button   d:  Decimal point selector   r:   Round off switch
S:  Minus sign                                       CM:  Clear memory
EX: Exchange                                         RM:  Recall memory
CE: Clear entry         M+:  Memory +                M-:  Memory -
CL: Clear               M=+: Memory equals +         M=-: Memory equals -

Status line:

    ### DP[0] RND[F] ( )( )( ):
           |      |   |  |  |
           |      |   |  |  ----> Memory light          
           |      |   |  -------> Negative light
           |      |   ----------> Overflow light
           |      --------------> Rounding mode (F:float, R:round, T:truncate)
           ---------------------> Decimal points (0-8) 
'''

class keyboard(sensor):
    def __init__(self, input, lights):
        sensor.__init__(self, input)
        self.input = input
        self.lights = lights
        self.output = pbus()
        self.advance = pwire()
        self.dp_sw = [0, 0, 0, 0]        # Digital point switch position
        self.rnd_sw = [0, 0, 0, 0]       # Rounding switch position
        self.buffer = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
            self.dp_sw, self.rnd_sw] 
        self.key_buffer = ""


    def always(self):
        for i in range(10):
            if self.input.pwire(i).v == 0:
                for j in range(4):
                    self.output.pwire(3-j).v = self.buffer[i][j]
                    if i < 8:   # Don't reset the switches!
                        self.buffer[i][j] = 0

    def getKeyBufferHead(self):
        head = None
        if len(self.key_buffer) == 0:
            return head
        for k in ['q', 'd', 'r', 'a', 'h']:
            if self.key_buffer.startswith(k):
                head = k
        if head is None:
            for c in range(8):
                for r in range(4):
                    s = _lookup[c][r]
                    if s is not None and self.key_buffer.startswith(s):
                        head = s
                        # break out of the 2 loops
        if head is None:
            head = self.key_buffer[0]
        # Remove head from key_buffer
        self.key_buffer = self.key_buffer[len(head):]
        return head

    def clearAdvance(self):
        self.advance.v = 0
        
    def readKey(self):
        if len(self.key_buffer) == 0:
            k = input("### {} {}: ".format(self.switches(), self.lights.display())).strip()
            self.appendKeyBuffer(k)
        k = self.getKeyBufferHead()
        if k is not None:
            if k == 'q':
                sys.exit()
            if k == 'd':
                self.incDP()
            elif k == 'r':
                self.incRND()
            elif k == 'a':
                self.advance.v = 1
            elif k == 'h':
                print(help)
            else:
                for c in range(8):
                    for r in range(4):
                        s = _lookup[c][r]
                        if s is not None and k == s:
                            self.buffer[c][r] = 1
                            return
                print("!!! ERROR: Unknown key '{}'! Use 'h' for help.".format(k), file=sys.stderr)

    def incDP(self):
        n = int("".join(map(str, self.dp_sw)), 2)
        n = (n + 1) % 9
        self.dp_sw[:] = list(map(int, list("{:04b}".format(n))))

    def incRND(self):
        n = int("".join(map(str, self.rnd_sw)), 2)
        if n == 0:
            n = 1
            desc = "round"
        elif n == 1:
            n = 8
            desc = "trunc"
        else:
            n = 0
            desc = "float"
        self.rnd_sw[:] = list(map(int, list("{:04b}".format(n))))
 */
