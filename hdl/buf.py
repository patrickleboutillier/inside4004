from hdl import *


class pbuf(sensor):
    def __init__(self, i, o):
        sensor.__init__(self, i)
        self.i = i
        self.o = o


    def always(self, signal):
        self.o.v = self.i.v
