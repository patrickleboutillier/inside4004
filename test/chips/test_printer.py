import unittest
from hdl import *
import chips.printer as printer

'''
;
;	Sector	Hex	binary (msb-lsb)	meaning (1.4142135623730 SQ)
;	---------------------------------------------------------------------------------------------------------------------------
;	0	20000	00100000000000000000                           0	;one digit 0 is used
;	1	00248	00000000001001001000             1  1  1        	;three digit 1 are used
;	2	02100	00000010000100000000                  2    2    	;two digit 2 are used
;	3	14400   00010100010000000000                    3   3 3 	;three digit 3 are used
;	4	000A0	00000000000010100000               4 4          	;two digit 4 are used
;	5	00800   00000000100000000000                     5      	;one digit 5 is used
;   6   01000   00000001000000000000                      6		;one digit 6 is used
;   7   08000	00001000000000000000                         7		;one digit 7 is used
;	8	00000	00000000000000000000                                    ;digit 8 is not used
;	9   00001	00000000000000000001                             SQ	;digit 9 is not used, square root character is used
;   10	00010	00000000000000010000		  .			;digit point
;	11	00000	00000000000000000000                                    ;no character is used from this row
'''

class TestPrinter(unittest.TestCase):

    def test_printer(self):
        p = printer.printer(pwire(), pwire(), pwire())

        p.input().v(0x20000) ; p.fireHammers()
        self.assertEqual(p.peekLine(), "              0       ") ; p.nextSector()
        p.input().v(0x00248) ; p.fireHammers()
        self.assertEqual(p.peekLine(), "1  1  1       0       ") ; p.nextSector()
        p.input().v(0x02100) ; p.fireHammers()
        self.assertEqual(p.peekLine(), "1  1 21   2   0       ") ; p.nextSector()
        p.input().v(0x14400) ; p.fireHammers()
        self.assertEqual(p.peekLine(), "1  1 213  23 30       ") ; p.nextSector()
        p.input().v(0x000A0) ; p.fireHammers()
        self.assertEqual(p.peekLine(), "1 414213  23 30       ") ; p.nextSector()
        p.input().v(0x00800) ; p.fireHammers()
        self.assertEqual(p.peekLine(), "1 4142135 23 30       ") ; p.nextSector()
        p.input().v(0x01000) ; p.fireHammers()
        self.assertEqual(p.peekLine(), "1 4142135623 30       ") ; p.nextSector()
        p.input().v(0x08002) ; p.fireHammers()
        self.assertEqual(p.peekLine(), "1 4142135623730    T  ") ; p.nextSector()
        p.input().v(0x00000) ; p.fireHammers()
        self.assertEqual(p.peekLine(), "1 4142135623730    T  ") ; p.nextSector()
        p.input().v(0x00001) ; p.fireHammers()
        self.assertEqual(p.peekLine(), "1 4142135623730 SQ T  ") ; p.nextSector()
        p.input().v(0x00010) ; p.fireHammers()
        self.assertEqual(p.peekLine(), "1.4142135623730 SQ T  ") ; p.nextSector()
        p.input().v(0x00000) ; p.fireHammers()
        self.assertEqual(p.peekLine(), "1.4142135623730 SQ T  ") ; 
        s = p.nextSector()
        self.assertEqual(s, 12) ; 
        p.input().v(0x00000) ; p.fireHammers()
        self.assertEqual(p.peekLine(), "1.4142135623730 SQ T  ") ; 
        s = p.nextSector()
        self.assertEqual(s, 0) ; 

if __name__ == '__main__':
    unittest.main()