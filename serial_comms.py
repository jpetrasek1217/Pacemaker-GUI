from time import sleep  #TODO: REMOVE IF NOT NEEDED
import serial
import serial.tools.list_ports as port_list
import struct
import numpy
from pacemaker_parameters import Parameters
from pacemaker_pacingmodes import PacingModes


# --- Constants ---

_SER_BAUDRATE = 115200
_SER_BYTESIZE = serial.EIGHTBITS
_SER_PARTITY = serial.PARITY_NONE
_SER_STOPBITS = serial.STOPBITS_ONE
_SER_TIMEOUT = 1
_SER_WRITE_TIMEOUT = 0

_PACEMAKER_COMM_PORT_DESCP = "JLink CDC UART Port"
_pacemakerCommPort = ''

_BYTE_SYNC = 22
_BYTE_PARAMS_FNCODE = 85 # 'U' ASCII

_ENDIANNESS = '<' # Little Endian
_DATATYPE = 'd' # Double
_BYTE_FORMAT = _ENDIANNESS + _DATATYPE

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


# --- Send & Receive Data ---

def sendParameterDataToPacemaker(params: dict[str, float], pacingMode: str | PacingModes, threshold: float):
    # Byte Array of all Parameter Data - Reference docs for order of data
    byteArray = bytearray(struct.pack(_BYTE_FORMAT, _BYTE_SYNC))
    byteArray.extend(bytearray(struct.pack(_BYTE_FORMAT, _BYTE_PARAMS_FNCODE)))
    byteArray.extend(bytearray(struct.pack(_BYTE_FORMAT, _getPacingModeByte(pacingMode))))

    for param in _paramDataToSend:
        if param in params:
            byteArray.extend((bytearray(struct.pack(_BYTE_FORMAT, params[param]))))
        else:
            raise KeyError(f"Unrecognized parameter \'{param}\' in serial communication stream when writing data.")

    byteArray.extend(bytearray(struct.pack(_BYTE_FORMAT, threshold)))

    # Checksum - The sum of all the bytes including checksum should equal 0xFF, so checksum = ~(sum of all other bytes)
    checksum = ~(numpy.uint64(sum(byteArray)))
    byteArray.extend(bytearray(struct.pack('<Q', checksum)))
    print(f"BYTESUM: {~checksum}, CHECKSUM: {checksum}, COMBINED: {sum(byteArray)}")
    print(f"BYTESUM: {bin(~checksum)}, CHECKSUM: {bin(checksum)}, COMBINED: {bin(sum(byteArray))}")

    print(f"BYTE DATA: {byteArray}, SIZE OF PACKET: {len(byteArray)}")
    print(receiveParameterDataFromPacemaker(byteArray))
    _writeSerialData(byteArray)


def receiveParameterDataFromPacemaker(byteArray: bytearray):
    unpackStr = _ENDIANNESS + _DATATYPE*(len(_paramDataToSend) + 4) + 'Q'
    return struct.unpack(unpackStr, byteArray)


def receiveEgramDataFromPacemaker():
    pass


# --- Read & Write ---

def _writeSerialData(byteArray: bytearray):
    # Check that pacemaker comm port is plugged in
    if not isPacemakerConnected():
        raise ValueError(f"Pacemaker cannot be found.")
    
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


def _readSerialData() -> bytearray:
    # Check that pacemaker comm port is plugged in
    if not isPacemakerConnected():
        raise ValueError(f"Pacemaker cannot be found.")
    
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


# --- Pacemaker Connection Status ---

def connectToPacemaker() -> None:
    global _pacemakerCommPort
    portDict = {port.description: port.name for port in port_list.comports()}
    for descp in portDict.keys():
        if descp.startswith(_PACEMAKER_COMM_PORT_DESCP):
            _pacemakerCommPort = portDict[descp]
            break
    else:
        _pacemakerCommPort = ''


def disconnectFromPacemaker() -> None:
    global _pacemakerCommPort
    _pacemakerCommPort = ''


def isPacemakerConnected() -> bool:
    return _pacemakerCommPort in list(port.name for port in port_list.comports())