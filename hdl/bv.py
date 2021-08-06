# Implements a simple bit vector class with shadowing.


class bv:
    def __init__(self, n, v=0):
        self._master = None
        self._n = n
        self._v = 0 

    def v(self, n, v=None):
        if self._master is None:
            if v is None:
                return self._v
            else:
                self._v = v

    def bit(self, n, v=None):
        if self._master is None:
            if v is None:
                return (self._v >> n) & 1
            else:
                self._v = (self._v & ~(1 << n)) | v << n
