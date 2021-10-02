import serial

COM = "COM4"
port = None
try:
    port = serial.Serial(COM, baudrate=500000)    
except:
  print("Can't open serial connection to {}".format(COM))


def ready():
    if port is not None:
        port.read()

def toByte(byte):
    return byte.to_bytes(1, byteorder='big')

def wireOn(id):
    port.write(toByte((id & 0b111) << 4 | 1))

def wireOff(id):
    port.write(toByte((id & 0b111) << 4))

def busRead(id):
    port.write(toByte(1 << 7 | (id & 0b11) << 5))
    data = int.from_bytes(port.read(), byteorder='big')
    return data & 0xF

def busZ(id):
    port.write(toByte(1 << 7 | (id & 0b11) << 5 | 1))

def busWrite(id, data):
    port.write(toByte(1 << 7 | (id & 0b11) << 5 | 1 << 4 | data & 0xF))