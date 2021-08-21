import sys
import hdl


class sensor:
    def __init__(self, *signals):
        for signal in signals:
            self.addSignal(signal)

    def addSignal(self, signal):
        bus = signal
        if type(signal) is hdl.pwire:
            bus = signal._bus
        bus.connect(self, signal)


class pbus:
    def __init__(self, n=4, v=0):
        self._n = n
        self._v = v
        self._sensors = {}
        self._wires = {}

    def len(self):
        return self._n

    def v(self, v):
        if v != self._v:
            changed = v ^ self._v
            self._v = v
            for (sensor, fss) in self._sensors.items():
                for (filter, signal) in fss:
                    if filter is None or filter & changed:    # The sensor is impacted by the change
                        sensor.always(signal)

    def pwire(self, bit):
        if bit not in self._wires:
            self._wires[bit] = hdl.pwire(None, self, bit)
        return self._wires[bit]

    def connect(self, sensor, signal):
        if not sensor in self._sensors:
            self._sensors[sensor] = [] 
        filter = None
        if type(signal) is hdl.pwire:
            filter = 1 << signal._bit
        self._sensors[sensor].append((filter, signal))


class bus:
    def __init__(self, n=4, v=0):
        self.n = n
        self.v = v

    def len(self):
        return self.n