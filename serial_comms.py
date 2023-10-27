import serial
import serial.tools.list_ports as port_list
from numpy import float16


print(list(port_list.comports()))

# --- Init ---

_SER = serial.Serial()
_SER.port = 'COM3'
_SER.baudrate = 9600
_SER.bytesize = serial.EIGHTBITS
_SER.parity = serial.PARITY_EVEN
_SER.stopbits = serial.STOPBITS_ONE
_SER.timeout = 1



# --- Read & Write ---

def sendParameterDatatoPacemaker():
    pass

def _writeSerialData():
    pass

def receiveEgramDataFromPacemaker():
    pass

def _readSerialData():
    pass