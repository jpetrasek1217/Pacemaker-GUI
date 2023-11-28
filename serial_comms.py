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
_pacemakerCommPort = '' # Active Comm Port that the pacemaker is connected to

_SYNC_CODE = 22
_PARAMS_FNCODE = 85 # 'U' ASCII
_PARAMS_SUCCESS_CODE = 76
_EGRAM_FNCODE = 34

_STRUCT_ENDIANNESS = '<' # Little Endian
_STRUCT_DATATYPE_CHAR = 'd' # Double
_STRUCT_BYTESIZE_DATATYPE = 8 # Double is 8 bytes
_STRUCT_FORMAT_STR = _STRUCT_ENDIANNESS + _STRUCT_DATATYPE_CHAR

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

def sendParameterDataToPacemaker(params: dict[str, float], pacingMode: str | PacingModes, threshold: float) -> bool:
    # Byte Array of all Parameter Data - Reference docs for order of data
    byteArrayToWrite = bytearray(struct.pack(_STRUCT_FORMAT_STR, _SYNC_CODE))
    byteArrayToWrite.extend(bytearray(struct.pack(_STRUCT_FORMAT_STR, _PARAMS_FNCODE)))
    byteArrayToWrite.extend(bytearray(struct.pack(_STRUCT_FORMAT_STR, _getPacingModeByte(pacingMode))))

    for param in _paramDataToSend:
        if param in params:
            byteArrayToWrite.extend((bytearray(struct.pack(_STRUCT_FORMAT_STR, params[param]))))
        else:
            raise KeyError(f"Unrecognized parameter \'{param}\' in serial communication stream when writing data.")

    byteArrayToWrite.extend(bytearray(struct.pack(_STRUCT_FORMAT_STR, threshold)))
    byteArrayToWrite.extend(bytearray(struct.pack(_STRUCT_FORMAT_STR, _calculateChecksum(byteArrayToWrite))))
    
    # Send Param Data
    print(f"BYTE DATA: {_unpackByteArray(byteArrayToWrite)}, BYTE SIZE OF PACKET: {len(byteArrayToWrite)}")
    _writeSerialData(byteArrayToWrite)

    # Read Success Message
    successCode = _unpackByteArray(_readSerialData())
    print(f"SUCCESS CODE: {successCode}")
    return successCode == _PARAMS_SUCCESS_CODE


def receiveEgramDataFromPacemaker() -> tuple[list[float], list[float]]:
    # Send Egram Request Code
    byteArrayToWrite = bytearray(struct.pack(_STRUCT_FORMAT_STR, _SYNC_CODE))
    byteArrayToWrite.extend(bytearray(struct.pack(_STRUCT_FORMAT_STR, _EGRAM_FNCODE)))
    print(f"BYTE DATA: {_unpackByteArray(byteArrayToWrite)}, BYTE SIZE OF PACKET: {len(byteArrayToWrite)}")
    _writeSerialData(byteArrayToWrite)

    # Read Egram Data
    egramDataTuple = _unpackByteArray(_readSerialData())
    return egramDataTuple, egramDataTuple


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
        print(f"WRITING...")
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
        return 0
    elif pacingMode == PacingModes.VOO.getName():
        return 1
    elif pacingMode == PacingModes.AAI.getName():
        return 2
    elif pacingMode == PacingModes.VVI.getName():
        return 3
    elif pacingMode == PacingModes.AOOR.getName():
        return 4
    elif pacingMode == PacingModes.VOOR.getName():
        return 5
    elif pacingMode == PacingModes.AAIR.getName():
        return 6
    elif pacingMode == PacingModes.VVIR.getName():
        return 7
    else:
        raise ValueError("Given parameter is not a Pacing Mode.")


def _calculateChecksum(byteArray: bytearray) -> int:
    # Checksum - Linear Combo of all data with coeffs of the index in the array (one-indexed)
    unpackStr = _STRUCT_ENDIANNESS + _STRUCT_DATATYPE_CHAR * (len(byteArray) // _STRUCT_BYTESIZE_DATATYPE)
    floatArray = struct.unpack(unpackStr, byteArray)

    checksum = numpy.double(0.0)
    for i in range(len(floatArray)):
        checksum += numpy.double(floatArray[i] * (i + 1))
    
    print(f"CHECKSUM: {checksum}")
    return checksum

def _packByteArray(data: any, *byteArray: bytearray):
    if byteArray:
        return byteArray.extend(bytearray(struct.pack(_STRUCT_FORMAT_STR, data)))
    else:
        return bytearray(struct.pack(_STRUCT_FORMAT_STR, data))


def _unpackByteArray(byteArray: bytearray):
    unpackStr = _STRUCT_ENDIANNESS + _STRUCT_DATATYPE_CHAR * (len(byteArray) // _STRUCT_BYTESIZE_DATATYPE)
    return struct.unpack(unpackStr, byteArray)

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