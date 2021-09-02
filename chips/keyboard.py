import sys
from hdl import *

'''
;shifter	ROM1 bit0	    ROM1 bit1	ROM1 bit2	    ROM1 bit3
;----------------------------------------------------------------------------------------------------------------------------------
;bit0		CM (81)		    RM (82)		M- (83)		    M+ (84)
;bit1		SQRT (85)	    % (86)		M=- (87)	    M=+ (88)
;bit2		diamond (89)	/ (8a)		* (8b)		    = (8c)
;bit3		- (8d)		    + (8e)		diamond2 (8f)	000 (90)
;bit4		9 (91)		    6 (92)		3 (93)		    . (94)
;bit5		8 (95)		    5 (96)		2 (97)		    00 (98)
;bit6		7 (99)		    4 (9a)		1 (9b)		    0 (9c)
;bit7		Sign (9d)	    EX (9e)		CE (9f)		    C (a0)
;bit8		dp0		        dp1		    dp2		        dp3	(digit point switch, value 0,1,2,3,4,5,6,8 can be switched)
;bit9		sw1		        (unused)	(unused)	    sw2	(rounding switch, value 0,1,8 can be switched)
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

    def appendKeyBuffer(self, buffer):
        self.key_buffer += buffer.replace(",", "")

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

    def switches(self):
        dp = int("".join(map(str, self.dp_sw)), 2)
        rnd = int("".join(map(str, self.rnd_sw)), 2)
        if rnd == 0:
            r = "F"
        elif rnd == 1:
            r = "R"
        else:
            r = "T"
        return "DP[{}] RND[{}]".format(dp, r)