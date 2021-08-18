from chips.modules.timing import *
from hdl import *


# This class implements the behaviour of the 4001 ROM chip.


class i4001():
    def __init__(self, chipnum, io_cfg, ph1, ph2, sync, data, cm):
        self.chipnum = chipnum                          # The chip number or identifier (0-15), normally burnt right into the chip.
        self.data = data                                # The data bus
        self.cm = cm                                    # The command line
        self.io = bus()                                 # The I/O bus to which other devices can connect
        self.addrh = 0                                  # The high nibble of the ROPM address
        self.addrl = 0                                  # The low nibble of the ROM address
        self.rom = [0] * 256                            # The actual ROM cells
        self.rom_select = 0                             # 1 if this chip is selected (during A3) to return instructions to the CPU
        self.io_select = 0                              # 1 if this chip is selected (by SRC during X2) for I/O instructions
        self.src = 0                                    # 1 if we are currently processing a SRC instruction
        self.io_inst = 0                                # 1 if we are currently processing an I/O instruction
        self.rdr = 0                                    # 1 if the current instruction is RDR
        self.wrr = 0                                    # 1 if the current instruction is wwr

        self.timing = timing(ph1, ph2, sync)            # The timing module and associated callback functions

        @A1ph2
        def _():
            # Record addrl
            self.addrl = self.data._v

        @A2ph2
        def _():
            # Record addrh
            self.addrh = self.data._v

        @A3ph2
        def _():
            # If cm is on, we are the selected ROM chip for instructions if self.chipnum == self.data._v
            if self.cm.v():
                self.rom_select = 1 if self.chipnum == self.data._v else 0

        @M1ph1
        def _():
            # If we are the selected chip for instructions, send out opr
            if self.rom_select:
                opr = self.rom[self.addrh << 4 | self.addrl] >> 4
                self.data.v(opr)

        @M1ph2
        def _():
            # opr is on the bus, no matter who put it there (us or another ROM chip). Check if an I/O instruction is in progress
            self.io_inst = 1 if self.data._v == 0b1110 else 0

        @M2ph1
        def _():
            # If we are the selected chip for instructions, send out opr
            if self.rom_select:
                self.opa = self.rom[self.addrh << 4 | self.addrl] & 0xF
                self.data.v(self.opa)

        @M2ph2
        def _():
            # opa is on the bus, no matter who put it there (us or another ROM chip). Check if a RDR or WRR I/O instruction is in progress
            self.rdr = 1 if self.io_inst and self.data._v == 0b1010 else 0
            self.wrr = 1 if self.io_inst and self.data._v == 0b0010 else 0

        @X2ph1
        def _():
            # Send data for RDR
            if self.io_select and self.rdr:
                self.data.v(self.io._v)

        @X2ph2
        def _():
            if self.cm.v():
                # A SRC instruction is in progress
                if self.chipnum == self.data._v:
                    # If cm is on, we are the selected ROM chip for I/O if self.chipnum == self.data._v
                    self.src = 1
                    self.io_select = 1
                else:
                    self.io_select = 0
            else:
                self.src = 0
                if self.io_select and self.wrr:
                    # Grab data for WRR
                    self.io.v(self.data._v)

        @X3ph2
        def _():
            if self.src:
                # Data @ X3 is ignored
                pass


    # This method is used to "program" the ROM from a filehandle.
    def program(self, fi):
        addr = 0
        for line in fi:
            inst = line[0:8]
            if inst[0] in ['0', '1']:
                self.rom[addr] = int(inst, 2)
                addr += 1
                if addr == 256:
                    break
        # Finish of with NOPs
        for x in range(addr, 256):
            self.rom[x] = 0
        return addr


    # Dump the ROM info.
    def dump(self):
        print("ROM {:2}: IO:{:04b}  ".format(self.chipnum, self.io._v), end = "")
