import hdl


class sensor:
    def __init__(self, *buses):
        for b in buses:
            bus = b
            filter = None
            if type(b) is hdl.wire:
                bus = b._bus
                filter = 1 << b._bit
            bus.connect(self, filter)


class bus:
    def __init__(self, n=4, v=0):
        self._n = n
        self._v = v
        self._sensors = {}
        self._wires = {}

    def len(self):
        return self._n

    def v(self, v=None):
        if v != None:   # set
            if v != self._v:
                changed = v ^ self._v
                self._v = v
                for (sensor, filters) in self._sensors.items():
                    for f in filters:
                        if f is None or f & changed:    # The sensor is impacted by the change
                            sensor.always()
        else:   # get
            return self._v

    def bit(self, n, v=None):
        if v != None:   # set
            v = (self._v & ~(1 << n)) | v << n
            self.v(v)
        else:   # get
            return (self._v >> n) & 1            

    def wire(self, bit):
        if bit not in self._wires:
            self._wires[bit] = hdl.wire(None, self, bit)
        return self._wires[bit]

    def connect(self, sensor, filter):
        if not sensor in self._sensors:
            self._sensors[sensor] = [] 
        self._sensors[sensor].append(filter)
