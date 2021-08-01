import sys

# A simple system of wires and sensors on which we will build a simple HDL:
# - Wires conduct values towards sensors, which react and may in turn send values through other wires.
# - Wires can have names, which must be unique, and can be looked-up by their name
# - Some wires are constants, i.e. VCC and GND. Their values cannot be changed
#   - This also means that their values cannot propagate, and they must be used directly when required. 


_WIRES = []
_NAMES = {}
_CONST = {}


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
        self._sensors = {}
        _WIRES.append(self)
        if self._name != "": 
            if name in _NAMES: 
                sys.exit("A wire with name '{}' already exists!".format(name))
            _NAMES[name] = self

    def v(self, v=None):
        if v != None and self._v != v and (not self in _CONST):
            self._v = int(bool(v))
            for s in self._sensors:
                if type(s) is wire:
                    s.v(self._v)
                else:
                    s.always()
        return self._v

    def connect(self, sensor):
        if not sensor in self._sensors: 
            self._sensors[sensor] = True
            if type(sensor) is wire:
                sensor.connect(self)

    def find(name):
        return _NAMES[name]



wire.GND = wire("GND", 0)
_CONST[wire.GND] = True
wire.VCC = wire("VCC", 1)
_CONST[wire.VCC] = True
