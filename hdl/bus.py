import sys
from hdl import *


_BUSES = []
_NAMES = {}


class bus:
    def __init__(self, name="", n=4):
        self._name = name
        self._n = n
        self._wires = []
        for i in range(n-1, -1, -1):
            wname = name
            if wname != "":
                wname = wname + "[" + str(i) + "]"
            self._wires.append(wire(wname))
        _BUSES.append(self)
        if self._name != "": 
            if name in _NAMES: 
                sys.exit("A bus with name '{}' already exists!".format(name))
            _NAMES[name] = self

    def len(self):
        return self._n

    def wire(self, n):  # LSB is 0
        idx = len(self._wires) - 1 - n
        return self._wires[idx]

    def wires(self):
        return self._wires
        
    def make(wires):
        that = bus("", 0)
        that._n = len(wires)
        that._wires = wires
        return that

    def v(self, v=None):
        if v != None:
            for w in self._wires[::-1]:
                w.v(v & 0x1, False)
                v = v >> 1
            for w in self._wires[::-1]:
                w.propagate()
        v = 0
        for w in self._wires:
            v = v << 1
            v = v | w.v()
        return v

    def connect(self, sensor):
        if type(sensor) is bus:
            for i in range(sensor.len()):
                sensor._wires[i].connect(self._wires[i])
        else:
            for w in self._wires:
                w.connect(sensor)

    def find(name):
        return _NAMES[name]
