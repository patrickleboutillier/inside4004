from hdl import *


class clock():
    def __init__(self):
        self._ph = bus(2)
        self._ph1 = self._ph.wire(1)
        self._ph2 = self._ph.wire(0)
        self._n = 0


    def ph1(self):
        return self._ph1

    def ph2(self):
        return self._ph2
        
    def tick(self, nb=1):
        for _ in range(nb):
            if self._n == 0:
                self._ph.v(0b00)
            elif self._n == 1:
                self._ph.v(0b10)
            elif self._n == 2:
                self._ph.v(0b00)
            else:   # n == 3
                self._ph.v(0b01)
            self._n = (self._n + 1) % 4
            # print("PH1:", self._ph1.v(), "PH2:", self._ph2.v())
