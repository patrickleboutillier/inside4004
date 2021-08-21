from chips.modules.timing import *
from hdl import * 


# This class implements the behaviour of the 4002 RAM chip.


class i4002:
    def __init__(self, bank, chip, ph1, ph2, sync, data, cm):
        self.bank = bank                            # The bank that this RAM belongs to. For dump purposes only.
        self.chip = chip                            # The chip number or identifier (0-3). Bit 1 is the model number (-1 or -2) and bit 0 is the P0 signal
        self.data = data                            # The data bus
        self.cm = cm                                # The command line
        self.output = pbus()                         # The output bus
        self.src = 0                                # 1 if we are currently processing a SRC instruction
        self.ram_select = 0                         # 1 if this chip is selected (by SRC during X2) for RAM/I/O instructions
        self.ram_inst = 0                           # 1 if we are currently processing an RAM/I/O instruction
        self.opa = 0                                # opa, saves during M2
        self.reg = 0                                # The selected (by SRC) RAM register
        self.char = 0                               # The selected (by SRC) RAM character
        self.ram = [[0] * 16, [0] * 16, [0] * 16, [0] * 16] # The actual RAM cells
        self.status = [[0] * 4, [0] * 4, [0] * 4, [0] * 4]  # The actual status cells                    
   
        self.timing = timing(ph1, ph2, sync)        # The timing module and associated callback functions
 
        @M2ph2
        def _():
            # Grab opa
            self.opa = self.data.v
            if self.ram_select and self.cm.v():
                # If we are the selected chip for RAM/I/O and cm is on, the CPU is telling us that we are processing a RAM/I/O instruction
                # NOTE: We could have just checked that opr == 0b1110 during M1...
                self.ram_inst = 1
            else:
                self.ram_inst = 0

        @X2ph1
        def _():
            if self.ram_inst:
                # A RAM/I/O instruction is on progress, execute the proper operation according to the value of opa
                if self.opa == 0b1000:
                    self.data.v = self.ram[self.reg][self.char]
                elif self.opa == 0b1001:
                    self.data.v = self.ram[self.reg][self.char]
                elif self.opa == 0b1011:
                    self.data.v = self.ram[self.reg][self.char]
                elif self.opa == 0b1100:
                    self.data.v = self.status[self.reg][0]
                elif self.opa == 0b1101:
                    self.data.v = self.status[self.reg][1]
                elif self.opa == 0b1110:
                    self.data.v = self.status[self.reg][2]
                elif self.opa == 0b1111:
                    self.data.v = self.status[self.reg][3]

        @X2ph2
        def _():
            if self.cm.v():
                # An SRC instruction is in progress
                if self.chip == (self.data.v >> 2):
                    # We are the selected RAM chip for RAM/I/O if self.chip == (self.data.v >> 2)
                    self.src = 1
                    self.ram_select = 1
                    # Grab the selected RAM register
                    self.reg = self.data.v & 0b0011
                else:
                    self.ram_select = 0
            else:
                self.src = 0                
            if self.ram_inst:
                # A RAM/I/O instruction is on progress, execute the proper operation according to the value of opa
                if self.opa == 0b0000:
                    self.ram[self.reg][self.char] = self.data.v
                elif self.opa == 0b0001:
                    self.output.v(self.data.v)
                elif self.opa == 0b0100:
                    self.status[self.reg][0] = self.data.v
                elif self.opa == 0b0101:
                    self.status[self.reg][1] = self.data.v
                elif self.opa == 0b0110:
                    self.status[self.reg][2] = self.data.v
                elif self.opa == 0b0111:
                    self.status[self.reg][3] = self.data.v

        @X3ph2
        def _():
            # If we are processing an SRC instruction, grab the selected RAM character
            if self.src:
                self.char = self.data.v


    def dump(self):
        ss = " ".join(["".join(["{:x}".format(x) for x in self.ram[i]]) + "/" + "".join(["{:x}".format(x) for x in self.status[i]]) for i in range(4)])
        print("RAM {:x}/{:x}:{} OUTPUT:{:04b}".format(self.bank, self.chip, ss, self.output._v))