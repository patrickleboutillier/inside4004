from hdl import *


class lights:
    def __init__(self, memory, overflow, negative):
        self.memory = memory
        self.overflow = overflow
        self.negative = negative
        

    def display(self):
        return "({})({})({})".format(
            "O" if self.overflow.v else " ",
            "-" if self.negative.v else " ",
            "M" if self.memory.v else " ")
