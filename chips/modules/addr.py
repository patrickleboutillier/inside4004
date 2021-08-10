from hdl import *


class addr(sensor):
    def __init__(self, data, ph1, ph2, stepper):
        sensor.__init__(self, data, ph1, ph2, stepper.output())
        self._data = data 
        self._stepper = stepper
        self.sp = 0
        self.stack = [{'h':0, 'm':0, 'l':0}, {'h':0, 'm':0, 'l':0}, {'h':0, 'm':0, 'l':0}, {'h':0, 'm':0, 'l':0}]

    # Here we mostly handle what happens in a1, a2 and a3.
    def always(self):
        if self._stepper.ph1().v():
            if self._stepper.a1():
                self._data.v(self.getPL())
            elif self._stepper.a2():
                self._data.v(self.getPM())
            elif self._stepper.a3(): 
                # TODO: Set cm_rom and checkit in ROM
                self._data.v(self.getPH())
        elif self._stepper.ph2().v():
            if self._stepper.a3(): 
                # TODO: This must happen only once, should be moved where data is not on the sensivity list.  
                self.incPC()

    def getPH(self):
        return self.stack[self.sp]['h']

    def getPM(self):
        return self.stack[self.sp]['m']

    def getPL(self):
        return self.stack[self.sp]['l']

    def getPC(self):        # For debugging
        return self.stack[self.sp]['h'] << 8 | self.stack[self.sp]['m'] << 4 | self.stack[self.sp]['l']

    def setPH(self, ph):
        self.stack[self.sp]['h'] = ph

    def setPM(self, pm):
        self.stack[self.sp]['m'] = pm

    def setPL(self, pl):
        self.stack[self.sp]['l'] = pl

    def incPC(self):
        pc = self.stack[self.sp]['h'] << 8 | self.stack[self.sp]['m'] << 4 | self.stack[self.sp]['l']
        pc = pc + 1
        self.stack[self.sp]['h'] = pc >> 8
        self.stack[self.sp]['m'] = pc >> 4 & 0xF
        self.stack[self.sp]['l'] = pc & 0xF

    def incSP(self):
        self.sp = (self.sp + 1) & 0b11

    def decSP(self):
        self.sp = (self.sp - 1) & 0b11