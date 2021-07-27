from asm import *

FIM(p7, 15)
LDM(15) ; CLC() ; XCH(r11)
JMS('assert:cy_clear')
LD(r11) ; JMS('assert:acc_eq_r15')
LDM(15) ; STC() ; XCH(r11)
JMS('assert:cy_set')
LD(r11) ; JMS('assert:acc_eq_r15')
LDM(15) ; CLC() ; XCH(r11)
JMS('assert:cy_clear')
LD(r11) ; JMS('assert:acc_eq_r15')
# Carry is now clear
LDM(15) ; CMC() ; XCH(r11)
JMS('assert:cy_set')
LD(r11) ; JMS('assert:acc_eq_r15')
LDM(15) ; CMC() ; XCH(r11)
JMS('assert:cy_clear')
LD(r11) ; JMS('assert:acc_eq_r15')

HLT()

from test import *