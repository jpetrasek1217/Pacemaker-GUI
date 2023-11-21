from time import sleep
import serial
import serial.tools.list_ports as port_list
import struct
import numpy
from pacemaker_parameters import Parameters
from pacemaker_pacingmodes import PacingModes


# --- Constants ---

_SER_BAUDRATE = 9600
_SER_BYTESIZE = serial.EIGHTBITS
_SER_PARTITY = serial.PARITY_NONE
_SER_STOPBITS = serial.STOPBITS_ONE
_SER_TIMEOUT = 1
_SER_WRITE_TIMEOUT = 0

_PACEMAKER_COMM_PORT_DESCP = "JLink CDC UART Port"
_pacemakerCommPort = ''

_BYTE_SYNC = 0x16   # 22 Decimal
_BYTE_PARAMS_FNCODE = 0x55  # 85 Decimal, 'U' ASCII

# THIS ORDER CANNOT CHANGE -- AGREED COMMS BETWEEN PACEMAKER AND DCM
_paramDataToSend = [
    Parameters.LOWER_RATE_LIMIT.getName(),
    Parameters.UPPER_RATE_LIMIT.getName(),
    Parameters.ATRIAL_AMPLITUDE.getName(),
    Parameters.ATRIAL_PULSE_WIDTH.getName(),
    Parameters.ATRIAL_SENSITIVITY.getName(),
    Parameters.ATRIAL_REFACTORY_PERIOD.getName(),
    Parameters.VENTRICULAR_AMPLITUDE.getName(),
    Parameters.VENTRICULAR_PULSE_WIDTH.getName(),
    Parameters.VENTRICULAR_SENSITIVITY.getName(),
    Parameters.VENTRICULAR_REFACTORY_PERIOD.getName(),
    Parameters.MAX_SENSOR_RATE.getName(),
    Parameters.REACTION_TIME.getName(),
    Parameters.RESPONSE_FACTOR.getName(),
    Parameters.RECOVERY_TIME.getName(),
]

# --- Read & Write ---

def sendParameterDataToPacemaker(params: dict[str, float], pacingMode: str | PacingModes, threshold: float):
    # Byte Array of all Parameter Data - Reference docs for order of data
    byteArray = bytearray(struct.pack('>H', _BYTE_SYNC))
    byteArray.extend(bytearray(struct.pack('>H', _BYTE_PARAMS_FNCODE)))
    byteArray.extend(bytearray(struct.pack('>H', _getPacingModeByte(pacingMode))))

    for param in _paramDataToSend:
        if param in params:
            byteArray.extend((bytearray(struct.pack('>H', numpy.ushort((params[param]*100))))))
        else:
            raise KeyError(f"Unrecognized parameter \'{param}\' in serial communication stream when writing data.")
        
    byteArray.extend(bytearray(struct.pack('>H', numpy.ushort((threshold*100)))))

    # Checksum
    # The sum of all the bytes including checksum should equal 0xFF, so checksum = ~(sum of all other bytes)
    bytesum = sum(byteArray) & 0xFFFF
    checksum = (~bytesum & 0xFFFF)
    byteArray.extend(bytearray(struct.pack('>H', checksum)))
    print(f"FIRST BYTE: {byteArray[0]}")

    print(f"BYTE DATA: {byteArray}, SUM OF BYTES: {sum(byteArray) & 0xFF}, SIZE OF PACKET: {len(byteArray)}")
    #_writeSerialData(byteArray)
    print(receiveParameterDataFromPacemaker(byteArray))


def _writeSerialData(port: str, byteArray: bytearray):
    # Check that pacemaker comm port is plugged in
    if not isPacemakerConnected():
        raise ValueError(f"Invalid Comm Port \'{port}\'.")
    
    # Write to port
    with serial.Serial(port=_pacemakerCommPort, 
                       baudrate=_SER_BAUDRATE, 
                       bytesize=_SER_BYTESIZE, 
                       parity=_SER_PARTITY, 
                       stopbits=_SER_STOPBITS, 
                       timeout=_SER_TIMEOUT, 
                       write_timeout=_SER_WRITE_TIMEOUT
                      ) as ser:  
        #ser.reset_input_buffer()   #TODO: remove if not needed
        #ser.reset_output_buffer()
        #sleep(1)
        ser.write(byteArray)
            

def receiveParameterDataFromPacemaker(byteArray: bytearray):
    unpackStr = '>HHH' + 'H'*(len(_paramDataToSend)) + 'HH'
    return struct.unpack(unpackStr, byteArray)


def receiveEgramDataFromPacemaker():
    pass


def _readSerialData(port: str) -> bytearray:
    # Check that pacemaker comm port is plugged in
    if not isPacemakerConnected():
        raise ValueError(f"Invalid Comm Port \'{port}\'.")
    
    # Read from Port
    with serial.Serial(port=_pacemakerCommPort, 
                       baudrate=_SER_BAUDRATE, 
                       bytesize=_SER_BYTESIZE, 
                       parity=_SER_PARTITY, 
                       stopbits=_SER_STOPBITS, 
                       timeout=_SER_TIMEOUT, 
                       write_timeout=_SER_WRITE_TIMEOUT
                      ) as ser:  
        print(f"READING...")
        byteArray = ser.read(50)
        print(f"READ: {byteArray}")
    return byteArray


# --- Helper Functions ---

def _getPacingModeByte(pacingMode: str | PacingModes) -> bytes:
    if pacingMode == PacingModes.AOO.getName():
        return 0x00
    elif pacingMode == PacingModes.AAI.getName():
        return 0x01
    elif pacingMode == PacingModes.AOOR.getName():
        return 0x02
    elif pacingMode == PacingModes.AAIR.getName():
        return 0x03
    elif pacingMode == PacingModes.VOO.getName():
        return 0x04
    elif pacingMode == PacingModes.VVI.getName():
        return 0x05
    elif pacingMode == PacingModes.VOOR.getName():
        return 0x06
    elif pacingMode == PacingModes.VVIR.getName():
        return 0x07
    else:
        raise ValueError("Given parameter is not a Pacing Mode.")


def connectToPacemaker() -> None:
    global _pacemakerCommPort
    portDict = {port.description: port.name for port in port_list.comports()}
    for descp in portDict.keys():
        if descp.startswith(_PACEMAKER_COMM_PORT_DESCP):
            _pacemakerCommPort = portDict[descp]
            break
    else:
        _pacemakerCommPort = ''
    print(f"COMM PORT: {_pacemakerCommPort}")

def disconnectFromPacemaker() -> None:
    global _pacemakerCommPort
    _pacemakerCommPort = ''


def isPacemakerConnected() -> bool:
    return _pacemakerCommPort in list(port.name for port in port_list.comports())


# print(len(port_list.comports()))
# print(port_list.comports()[0].description)