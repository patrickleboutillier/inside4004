from hdl import *


class arith:
    def __init__(self, data):
        self.data = data
        self.acc = 0
        self.cy = 0 


    def accZero(self):
        return 1 if self.acc == 0 else 0
