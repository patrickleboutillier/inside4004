import sys


WIRES = []
WIRE_NAMES = {}
BUSES = []
BUS_NAMES = {}


class sensor:
    def __init__(self, name, *wires):
        self._name = name
        for w in wires:
            w.connect(self)

    def name():
        return self._name


class wire(sensor):
    def __init__(self, name="", v=0):
        self._v = v
        self._name = name
        self._sensors = []
        WIRES.append(self)
        if self._name != "": 
            if name in WIRE_NAMES: 
                sys.exit("A wire with name '{}' already exists!".format(name))
            WIRE_NAMES[name] = self

    def v(self, v=None):
        if v != None and self._v != v:
            self._v = int(bool(v))
            for s in self._sensors:
                if type(s) is wire:
                    s.v(self._v)
                else:
                    s.always()
        return self._v

    def connect(self, sensor):
        self._sensors.append(sensor)

    def drive(self, sensor):
        self.connect(sensor)

    def find(name):
        return WIRE_NAMES[name]


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
        BUSES.append(self)
        if self._name != "": 
            if name in BUS_NAMES: 
                sys.exit("A bus with name '{}' already exists!".format(name))
            BUS_NAMES[name] = self

    def len(self):
        return self._n

    def wire(self, n):  # LSB is 0
        idx = len(self._wires) - 1 - n
        return self._wires[idx]

    def make(wires):
        that = bus("", 0)
        that._n = len(wires)
        that._wires = wires
        return that

    def v(self, v=None):
        if v != None:
            for w in self._wires[::-1]:
                w.v(v & 0x1)
                v = v >> 1
        v = 0 
        for w in self._wires:
            v = v << 1
            v = v | w.v()
        return v

    def connect(self, sensor):
        for w in self._wires:
            w.connect(sensor)

    def find(name):
        return BUS_NAMES[name]




wire.GND = wire("GND")
wire.VCC = wire("VCC", 1)
