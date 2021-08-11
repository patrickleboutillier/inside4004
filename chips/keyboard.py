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
    ["<>",  "/",  "*",      "="],
    ["-",   "+",  "#",      "000"],
    ["9",   "6",  "3",      "."],
    ["8",   "5",  "2",      "00"],
    ["7",   "4",  "1",      "0"],
    ["S",   "EX", "CE",     "C"]
]
for c in _lookup:
    c.reverse()


class keyboard(sensor):
    def __init__(self, input, lights):
        sensor.__init__(self, input)
        self._input = input
        self._lights = lights
        self._output = bus()
        self._advance = wire()
        self._dp_sw = [0, 0, 0, 0]        # Digital point switch position
        self._rnd_sw = [0, 0, 0, 0]       # Rounding switch position
        self._buffer = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
            self._dp_sw, self._rnd_sw] 
        self._key_buffer = []


    def output(self):
        return self._output

    def advance(self):
        return self._advance

    def always(self, signal):
        for i in range(10):
            if self._input.wire(i).v() == 0:
                for j in range(4):
                    self._output.wire(3-j).v(self._buffer[i][j])
                    if i < 8:   # Don't reset the switches!
                        self._buffer[i][j] = 0

    def setKeyBuffer(self, buffer):
        self._key_buffer += buffer.split(",")

    def clearAdvance(self):
        self._advance.v(0)
        
    def readKey(self):
        if len(self._key_buffer) == 0:
            k = input("### {} {}: ".format(self.switches(), self._lights.display())).strip()
            self._key_buffer += k.split(",")
        if len(self._key_buffer): 
            k = self._key_buffer.pop(0).strip()
            if k != "":
                if k == 'q':
                    sys.exit()
                if k == 'd':
                    self.incDP()
                elif k == 'r':
                    self.incRND()
                elif k == 'a':
                    self._advance.v(1)
                else:
                    for c in range(8):
                        for r in range(4):
                            s = _lookup[c][r]
                            if k == s:
                                self._buffer[c][r] = 1
                                return
                    print("!!! ERROR: Unknown key '{}'!".format(k), file=sys.stderr)

    def incDP(self):
        n = int("".join(map(str, self._dp_sw)), 2)
        n = (n + 1) % 9
        self._dp_sw[:] = list(map(int, list("{:04b}".format(n))))

    def incRND(self):
        n = int("".join(map(str, self._rnd_sw)), 2)
        if n == 0:
            n = 1
            desc = "round"
        elif n == 1:
            n = 8
            desc = "trunc"
        else:
            n = 0
            desc = "float"
        self._rnd_sw[:] = list(map(int, list("{:04b}".format(n))))

    def switches(self):
        dp = int("".join(map(str, self._dp_sw)), 2)
        rnd = int("".join(map(str, self._rnd_sw)), 2)
        if rnd == 0:
            r = "F"
        elif rnd == 1:
            r = "R"
        else:
            r = "T"
        return "DP[{}] RND[{}]".format(dp, r)