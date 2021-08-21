from hdl import *


_specialChars = [
    ["<>",  "+ ",  "- ",  "X ",  "/ ",  "M+",  "M-",  "^ ",  "= ",  "SQ",  "% ",  "C ",  "R "],
    ["#  ", "*  ", "I  ", "II ", "III", "M+ ", "M- ", "T  ", "K  ", "E  ", "Ex ", "C  ", "M  "]
]

# Units are CPU cycles
_sector_pulse =  int((5 * 1000) / 22)
_sector_period = int((28 * 1000) / 22)


class printer(sensor):
    def __init__(self, fire, advance, color):
        sensor.__init__(self, fire, advance, color)
        self._input = pbus(n=20)
        self._sector = pwire()
        self._index = pwire()
        self._fire = fire
        self._advance = advance
        self._color = color

        self.initLine()
        self._cur_sector = 0 
        self._cycle = 0
        self._cur_color = ' '


    def input(self):
        return self._input

    def sector(self):
        return self._sector

    def index(self):
        return self._index

    def always(self, signal):
        if self._fire.v:
            self.fireHammers()
        if self._advance.v:
            self.advanceLine()
            self._cur_color = ' '   # Reset line color
        if self._color.v:
            self._cur_color = '-'   # Set color to "red", meaning negative value.

    # Called by the MCS-4 before each cycle.
    def cycle(self):
        if self._cycle == 0:
            self.startSectorPulse()
            return
        elif self._cycle == _sector_pulse:
            self.endSectorPulse()
            return
        elif self._cycle == _sector_period:
            self.endSectorPeriod()
            return
        else:
            self._cycle += 1

    def startSectorPulse(self):
        self._cycle = 0
        self._sector.v = 1
        if self._cur_sector == 0:
            self._index.v = 1
        self._cycle += 1

    def endSectorPulse(self):
        self._cycle = _sector_pulse
        self._sector.v = 0
        self._cycle += 1

    def endSectorPeriod(self):
        self._cycle = _sector_period
        if self._cur_sector == 0:
            self._index.v = 0
        self.nextSector()
        self._cycle = 0

    def nextSector(self):
        self._cur_sector += 1
        self._cur_sector = self._cur_sector % 13
        return self._cur_sector

    def fireHammers(self):
        # print("{:020b}".format(self._input.v))
        for i in range(20):
            if self._input.pwire(i).v:
                self.punchChar(i)

    def initLine(self):
        self._line = [' '] * 22

    def peekLine(self):
        return "".join(self._line)

    def advanceLine(self):
        # print previous line
        line = self.peekLine()
        print(">>> {}|{}|".format(self._cur_color, line))
        self.initLine()

    def punchChar(self, bit):
        (s, pos) = self.getChar(self._cur_sector, bit)
        if s is not None:
            self._line[pos:(pos+len(s))] = list(s)

    def getChar(self, sector, bit):
        if bit == 0:
            return (_specialChars[bit][self._cur_sector], 16)
        elif bit == 1:
            return (_specialChars[bit][self._cur_sector], 19)
        elif bit <= 17 and bit >= 3:
            if sector <= 9:
                return (str(self._cur_sector), bit-3)
            elif self._cur_sector == 10 or self._cur_sector == 11:
                return('.', bit-3)
            else:
                return('-', bit-3)
        return (None, -1)


'''
;   sector	    column 1-15	    column 17	    column 18
;	0		    0		        diamond		    #
;	1		    1		        +		        *
;	2	    	2		        -		        I
;	3		    3		        X		        II
;	4		    4		        /		        III
;	5		    5		        M+		        M+
;	6		    6		        M-		        M-
;	7		    7		        ^		        T
;	8		    8		        =		        K
;	9		    9		        SQRT		    E
;	10		    .		        %		        Ex
;	11		    .		        C		        C
;	12		    -		        R		        M

;bit00		column 17	special characters
;bit01		column 18	special characters
;bit02		-		not used
;bit03		column 1	digit or digit point
;bit04		column 2	digit or digit point
;bit05		column 3	digit or digit point
;bit06		column 4	digit or digit point
;bit07		column 5	digit or digit point
;bit08		column 6	digit or digit point
;bit09		column 7	digit or digit point
;bit10		column 8	digit or digit point
;bit11		column 9	digit or digit point
;bit12		column 10	digit or digit point
;bit13		column 11	digit or digit point
;bit14		column 12	digit or digit point
;bit15		column 13	digit or digit point
;bit16		column 14	digit or digit point
;bit17		column 15	digit or digit point
;bit18		-		not used
;bit19		-		not used
'''