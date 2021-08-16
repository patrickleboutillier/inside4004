from hdl import *


class clock():
    def __init__(self):
        self.phx = bus(2)
        self.ph1 = self.phx.wire(1)
        self.ph2 = self.phx.wire(0)
        self.n = 0

        
    def tick(self, nb=1):
        for _ in range(nb):
            if self.n == 0:
                self.phx.v(0b10)
            elif self.n == 1:
                self.phx.v(0b00)
            elif self.n == 2:
                self.phx.v(0b01)
            else:   # n == 3
                self.phx.v(0b00)
            self.n = (self.n + 1) % 4