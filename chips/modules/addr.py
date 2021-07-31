

class addr:
    def __init__(self, data):
        self.data = data 
        self.sp = 0
        self.stack = [{'h':0, 'm':0, 'l':0}, {'h':0, 'm':0, 'l':0}, {'h':0, 'm':0, 'l':0}, {'h':0, 'm':0, 'l':0}]

    def getPH(self):
        return self.stack[self.sp]['h']

    def getPM(self):
        return self.stack[self.sp]['m']

    def getPL(self):
        return self.stack[self.sp]['l']

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