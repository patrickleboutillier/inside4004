import sys
import chips.i4001 as i4001, chips.i4002 as i4002, chips.i4004 as i4004
import chips.clock as clock
from hdl import *


import argparse
parser = argparse.ArgumentParser()
parser.add_argument("ROM_FILE")
parser.add_argument("-d", "--debug", help="output debug information",
                    action="store_true")      
parser.add_argument("-o", "--optimize", help="optimize for speed",
                    action="store_true")             


class MCS4:
    def __init__(self):
        global parser
        self.ram_chip = 0                   # This represents the currently active RAM chip

        self.clock = clock.clock()
 
        self.data = bus()
        self.cm_rom = pwire()
        self.cm_ram = pbus()
        self.test = pwire()
        self.CPU = i4004.i4004(self.clock, self.data, self.cm_rom, self.cm_ram, self.test)

        self.PROM = []
        self.RAM = [None, [], [], None, [], None, None, None, []]
        self.SR = []
      
        self.args = parser.parse_args()

    def addROM(self, rom):
        self.PROM.append(rom)

    def addRAM(self, bank, ram):
        idx = 1 << bank
        self.RAM[idx].append(ram)

    def addSR(self, sr):
        self.SR.append(sr)

    def program(self):
        fh = open(self.args.ROM_FILE, 'r')
        if self.PROM[0].program(fh) == 0:
            sys.exit("ERROR: No instructions loaded!") 
        elif len(self.PROM) > 1:
            for p in self.PROM[1:]:
                p.program(fh)
        # TODO: Make sure stdin is empty
        fh.close()

    def run(self, callback=None):
        dump = self.args.debug
        nb = 0
        while (True):
            if callback is not None:
                callback(nb)
            for i in range(8):
                self.clock.tick()
                if i == 4 and dump:
                    self.dump(nb)
            nb += 1

    def dump(self, nb):
        self.CPU.dump(nb)
        self.RAM[1][0].dump()
        self.RAM[1][1].dump()
        for r in self.PROM:
            r.dump()
        print()
        if len(self.SR):
            for s in self.SR:
                s.dump()
            print()