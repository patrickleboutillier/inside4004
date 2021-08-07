from hdl import *


class lights():
    def __init__(self, memory, overflow, negative):
        sensor.__init__(self, memory, overflow, negative)
        self._memory = memory
        self._overflow = overflow
        self._negative = negative
    

    def always(self):
        pass

    def display(self):
        return "({})({})({})".format(
            "O" if self._overflow.v() else " ",
            "-" if self._negative.v() else " ",
            "M" if self._memory.v() else " ")
