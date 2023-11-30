from time import sleep  #TODO: REMOVE IF NOT NEEDED
import serial
import serial.tools.list_ports as port_list
import struct
import numpy
from pacemaker_parameters import Parameters
from pacemaker_pacingmodes import PacingModes


# --- Constants ---

_SER_BAUDRATE = 115200                  # units of bits/sec
_SER_BYTESIZE = serial.EIGHTBITS
_SER_PARTITY = serial.PARITY_NONE
_SER_STOPBITS = serial.STOPBITS_ONE
_SER_TIMEOUT = 5                        # units of seconds
_SER_WRITE_TIMEOUT = 0                  # units of seconds
_SER_MAX_READ_BYTE_LEN = 32000          # units of bytes

_pacemakerCommPortName = ''             # Active pacemaker comm ports, as required for PySerial connection
_PACEMAKER_COMM_PORT_DESCP_WIN = 'JLink CDC UART Port'
_PACEMAKER_COMM_PORT_DESCP_MAC = 'J-Link'
_PACEMAKER_COMM_PORT_PREFIX_MAC = '/dev/'

_deviceType = ''                        # Recorded type of device - ie Windows, Mac, etc
_DEVICETYPE_WIN = "WIN"
_DEVICETYPE_MAC = "MAC"

_SYNC_CODE = 22                         # Function Codes for Serial Comms with Pacemaker - VALUES CANNOT CHANGE, AGREED COMMS BETWEEN PACEMAKER AND DCM
_PARAMS_FNCODE = 85
_PARAMS_SUCCESS_CODE = 76
_EGRAM_FNCODE = 34

_STRUCT_ENDIANNESS_CHAR = '<'           # Little Endian
_STRUCT_DATATYPE_CHAR = 'd'             # Double
_STRUCT_BYTESIZE_OF_DATATYPE = 8        # Double is 8 bytes
_STRUCT_FORMAT_STR = _STRUCT_ENDIANNESS_CHAR + _STRUCT_DATATYPE_CHAR

_PARAMS_NAMES_ORDERED_LIST = [          # Ordered List of Parameters to send - VALUES CANNOT CHANGE, AGREED COMMS BETWEEN PACEMAKER AND DCM
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
_PACKET_BYTESIZE = (len(_PARAMS_NAMES_ORDERED_LIST) + 5) * _STRUCT_BYTESIZE_OF_DATATYPE    # plus 5 from: SYNC, FNCODE, PACINGMODE, THRESHOLD, CHECKSUM


# --- Send & Receive Data ---

def sendParameterDataToPacemaker(params: dict[str, float], pacingMode: str | PacingModes, threshold: float) -> bool:
    # Construct byte array - Reference Docs for structure and order of data
    byteArrayToWrite = bytearray(struct.pack(_STRUCT_FORMAT_STR, _SYNC_CODE))
    byteArrayToWrite.extend(bytearray(struct.pack(_STRUCT_FORMAT_STR, _PARAMS_FNCODE)))
    byteArrayToWrite.extend(bytearray(struct.pack(_STRUCT_FORMAT_STR, _getPacingModeByte(pacingMode))))

    for param in _PARAMS_NAMES_ORDERED_LIST:
        if param in params:
            byteArrayToWrite.extend((bytearray(struct.pack(_STRUCT_FORMAT_STR, params[param]))))
        else:
            raise KeyError(f"Unrecognized parameter \'{param}\' in serial communication stream when writing data.")

    byteArrayToWrite.extend(bytearray(struct.pack(_STRUCT_FORMAT_STR, threshold)))
    byteArrayToWrite.extend(bytearray(struct.pack(_STRUCT_FORMAT_STR, _calculateChecksum(byteArrayToWrite))))
    
    # Send Param Data
    _writeSerialData(byteArrayToWrite)

    # Read Success Message
    byteArrayFromRead = _readSerialData()
    if len(byteArrayFromRead) % _STRUCT_BYTESIZE_OF_DATATYPE != 0:
        return False
    successCode = _unpackByteArray(byteArrayFromRead)
    try:
        successCode = int(successCode)
    except TypeError:
        try:
            successCode = successCode[0]
        except:
            return False
    return successCode == _PARAMS_SUCCESS_CODE


def receiveEgramDataFromPacemaker() -> tuple[list[float], list[float]]:
    # Construct byte array - Reference Docs for structure and order of data
    byteArrayToWrite = bytearray(struct.pack(_STRUCT_FORMAT_STR, _SYNC_CODE))
    byteArrayToWrite.extend(bytearray(struct.pack(_STRUCT_FORMAT_STR, _EGRAM_FNCODE)))
    
	# Send Egram Request Code
    _writeSerialData(byteArrayToWrite)

    # Read Egram Data
    byteArrayFromRead = _readSerialData()
    if len(byteArrayFromRead) % _STRUCT_BYTESIZE_OF_DATATYPE != 0:
        return False
    egramDataTuple = _unpackByteArray(byteArrayFromRead)
    return egramDataTuple[0::2], egramDataTuple[1::2]


# --- Read & Write ---

def _writeSerialData(byteArray: bytearray):
    # Check that pacemaker comm port is plugged in
    if not isPacemakerConnected():
        raise ValueError(f"Pacemaker cannot be found.")
    
    while len(byteArray) < _PACKET_BYTESIZE:
        byteArray.extend((bytearray(struct.pack(_STRUCT_FORMAT_STR, 0.0))))

    if len(byteArray) > _PACKET_BYTESIZE:
        raise ValueError(f"Size of packet being sent to pacemaker is too large.")
    
    # Adjust comm port for PySerial based on type of device
    serPort = _pacemakerCommPortName
    if _deviceType == _DEVICETYPE_MAC:
        serPort = _PACEMAKER_COMM_PORT_PREFIX_MAC + _pacemakerCommPortName

    # Write to port
    with serial.Serial(port=serPort, 
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
        print(f"WROTE: {_unpackByteArray(byteArray)}")


def _readSerialData() -> bytearray:
    # Check that pacemaker comm port is plugged in
    if not isPacemakerConnected():
        raise ValueError(f"Pacemaker cannot be found.")
    
    # Adjust comm port for PySerial based on type of device
    serPort = _pacemakerCommPortName
    if _deviceType == _DEVICETYPE_MAC:
        serPort = _PACEMAKER_COMM_PORT_PREFIX_MAC + _pacemakerCommPortName

    # Read from Port
    with serial.Serial(port=serPort, 
                       baudrate=_SER_BAUDRATE, 
                       bytesize=_SER_BYTESIZE, 
                       parity=_SER_PARTITY, 
                       stopbits=_SER_STOPBITS, 
                       timeout=_SER_TIMEOUT, 
                       write_timeout=_SER_WRITE_TIMEOUT
                      ) as ser:  
        print(f"READING...")
        byteArray = ser.read(_SER_MAX_READ_BYTE_LEN)
        print(f"SIZE OF READ: {len(byteArray)}")
        print(f"READ: {_unpackByteArray(byteArray)}")
    return byteArray


# --- Helper Functions ---

def _getPacingModeByte(pacingMode: str | PacingModes) -> int:
    '''Returns an integer value corresponding to each pacing mode.
    The values are agreed upon between the DCM and the Pacemaker.'''
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
    floatArray = _unpackByteArray(byteArray)
    checksum = numpy.double(0.0)
    for i in range(len(floatArray)):
        checksum += numpy.double(floatArray[i] * (i + 1))
    return checksum


def _unpackByteArray(byteArray: bytearray) -> tuple[any]:
    unpackStr = _STRUCT_ENDIANNESS_CHAR + _STRUCT_DATATYPE_CHAR * (len(byteArray) // _STRUCT_BYTESIZE_OF_DATATYPE)
    return struct.unpack(unpackStr, byteArray)

# --- Pacemaker Connection Status ---

def connectToPacemaker() -> None:
    '''Connects to the Pacemaker comm port.'''
    global _pacemakerCommPortName, _deviceType
    portDict = {port.description: port.name for port in port_list.comports()}
    for descp in portDict.keys():
        if descp.startswith(_PACEMAKER_COMM_PORT_DESCP_WIN) or descp.startswith(_PACEMAKER_COMM_PORT_DESCP_MAC):
            _pacemakerCommPortName = portDict[descp]
            if descp.startswith(_PACEMAKER_COMM_PORT_DESCP_WIN):
                _deviceType = _DEVICETYPE_WIN
            elif descp.startswith(_PACEMAKER_COMM_PORT_DESCP_MAC):
                _deviceType = _DEVICETYPE_MAC
            break
    else:
        _pacemakerCommPortName = ''


def disconnectFromPacemaker() -> None:
    '''Disconnects from the saved Pacemaker comm port.'''
    global _pacemakerCommPortName
    _pacemakerCommPortName = ''


def isPacemakerConnected() -> bool:
    '''Returns a boolean value of if the saved Pacemaker is detected.'''
    return _pacemakerCommPortName in list(port.name for port in port_list.comports()) and _onlyOnePacemakerConnected()


def _onlyOnePacemakerConnected() -> bool:
    '''Returns a boolean value if only 1 Pacemaker is detected.'''
    amountOfPacemakersDetected = 0
    portDict = {port.description: port.name for port in port_list.comports()}
    for descp in portDict.keys():
        if descp.startswith(_PACEMAKER_COMM_PORT_DESCP_WIN) or descp.startswith(_PACEMAKER_COMM_PORT_DESCP_MAC):
            amountOfPacemakersDetected += 1
    if amountOfPacemakersDetected == 1:
        return True
    else:
        return False