import serial
import serial.tools.list_ports as port_list
from numpy import float16
import struct
from pacemaker_parameters import Parameters
from pacemaker_pacingmodes import PacingModes


print(f"COM PORTS: {list(port_list.comports())}")

# --- Init ---

_SER = serial.Serial()
_SER.port = 'COM3'
_SER.baudrate = 9600
_SER.bytesize = serial.EIGHTBITS
_SER.parity = serial.PARITY_EVEN
_SER.stopbits = serial.STOPBITS_ONE
_SER.timeout = 1

_BYTE_SYNC = 0x16
_BYTE_PARAMS_FNCODE = 0x55

# THIS ORDER CANNOT CHANGE -- AGREED COMMS BETWEEN PACEMAKER AND DCM
_paramDataStreamOrder = [
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
    "THRES",
    "REACTION",
    "RESPONSE_FACTOR",
    "RECOVERY",
    "CHECKSUM"
]

# --- Read & Write ---

def sendParameterDataToPacemaker(params: dict[str, float], pacingMode: str | PacingModes):
    byteArray = bytearray(struct.pack('>B', _BYTE_SYNC))
    byteArray.extend(bytearray(struct.pack('>B', _BYTE_PARAMS_FNCODE)))
    byteArray.extend(bytearray(struct.pack('>B', _getPacingModeByte(pacingMode))))

    tempCount = 0
    for param in _paramDataStreamOrder:
        if param in params:
            tempCount += 1
            byteArray.extend((bytearray(struct.pack('>f', params[param]))))
        else:
            continue #TODO: REMOVE
            raise KeyError(f"Unrecognized parameter {param} in serial communication stream when writing data.")

    # Checksum
    # The sum of all the bytes including checksum should equal 0xFF, so checksum = ~(sum of all other bytes)
    bytesum = sum(byteArray) & 0xFF
    checksum = (~bytesum & 0xFF)
    byteArray.extend(bytearray(struct.pack('>B', checksum)))

    print(f"BYTE DATA: {byteArray}, SUM OF BYTES: {sum(byteArray) & 0xFF}, SIZE OF PACKET: {len(byteArray)}")
    return byteArray #TODO REMOVE
    _writeSerialData(byteArray)


def _writeSerialData(byteArray: bytearray):
    with _SER:
        _SER.write(byteArray)


def receiveParameterDataFromPacemaker(byteArray: bytearray):
    unpackStr = '>BBB' + 'f'*(len(_paramDataStreamOrder)-5) + 'B'
    print(byteArray)
    print(struct.unpack(unpackStr, byteArray))


def receiveEgramDataFromPacemaker():
    pass


def _readSerialData():
    pass


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
