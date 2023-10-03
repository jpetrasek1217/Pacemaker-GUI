from enum import Enum
from pacemaker_parameters import Parameters

_ATRIAL_KEY = "A"
_VENTRICULAR_KEY = "V"

class PacingModes(Enum):
    AOO = [
        Parameters.LOWER_RATE_LIMIT,
        Parameters.UPPER_RATE_LIMIT,
        Parameters.ATRIAL_AMPLITUDE,
        Parameters.ATRIAL_PULSE_WIDTH,
    ]

    AAI = [
        Parameters.LOWER_RATE_LIMIT,
        Parameters.UPPER_RATE_LIMIT,
        Parameters.ATRIAL_AMPLITUDE,
        Parameters.ATRIAL_PULSE_WIDTH,
        Parameters.ATRIAL_SENSITIVITY,
        Parameters.ATRIAL_REFACTORY_PERIOD,
        Parameters.PVARP,
        Parameters.HYSTERESIS,
        Parameters.RATE_SMOOTHING,
    ]

    AOOR = [
        Parameters.LOWER_RATE_LIMIT,
        Parameters.UPPER_RATE_LIMIT,
        Parameters.ATRIAL_AMPLITUDE,
        Parameters.ATRIAL_PULSE_WIDTH,
        Parameters.MAX_SENSOR_RATE,
    ]

    AAIR = [
        Parameters.LOWER_RATE_LIMIT,
        Parameters.UPPER_RATE_LIMIT,
        Parameters.ATRIAL_AMPLITUDE,
        Parameters.ATRIAL_PULSE_WIDTH,
        Parameters.ATRIAL_SENSITIVITY,
        Parameters.ATRIAL_REFACTORY_PERIOD,
        Parameters.PVARP,
        Parameters.HYSTERESIS,
        Parameters.RATE_SMOOTHING,
        Parameters.MAX_SENSOR_RATE,
    ]

    AXXX = AAIR.copy()

    VOO = [
        Parameters.LOWER_RATE_LIMIT,
        Parameters.UPPER_RATE_LIMIT,
        Parameters.VENTRICULAR_AMPLITUDE,
        Parameters.VENTRICULAR_PULSE_WIDTH,
    ]

    VVI = [
        Parameters.LOWER_RATE_LIMIT,
        Parameters.UPPER_RATE_LIMIT,
        Parameters.VENTRICULAR_AMPLITUDE,
        Parameters.VENTRICULAR_PULSE_WIDTH,
        Parameters.VENTRICULAR_SENSITIVITY,
        Parameters.VENTRICULAR_REFACTORY_PERIOD,
        Parameters.HYSTERESIS,
        Parameters.RATE_SMOOTHING,
    ]

    VOOR = [
        Parameters.LOWER_RATE_LIMIT,
        Parameters.UPPER_RATE_LIMIT,
        Parameters.VENTRICULAR_AMPLITUDE,
        Parameters.VENTRICULAR_PULSE_WIDTH,
        Parameters.MAX_SENSOR_RATE,
    ]

    VVIR = [
        Parameters.LOWER_RATE_LIMIT,
        Parameters.UPPER_RATE_LIMIT,
        Parameters.VENTRICULAR_AMPLITUDE,
        Parameters.VENTRICULAR_PULSE_WIDTH,
        Parameters.VENTRICULAR_SENSITIVITY,
        Parameters.VENTRICULAR_REFACTORY_PERIOD,
        Parameters.HYSTERESIS,
        Parameters.RATE_SMOOTHING,
        Parameters.MAX_SENSOR_RATE,
    ]

    VXXX = VVIR.copy()

    def __init__(self, listOfParameters: list[Parameters]) -> None:
        super().__init__()
        self._params = listOfParameters
        self._checkValues()

    def _checkValues(self) -> None:
        if any(not isinstance(param, Parameters) for param in self._params):
            raise TypeError(f"Pacing Mode \'{self.name}\' has objects that are not a Parameter.")
        
    def getName(self) -> str:
        return self.name

    def getParameters(self) -> list[Parameters]:
        return self._params
    
    
    @classmethod
    def getInitialPacingMode(cls) -> str:
        return PacingModes.AOO.name
    
            
    @classmethod
    def getAllVisibleParameters(cls, pacingMode: str) -> list[Parameters]:
        if not isinstance(pacingMode, str):
            raise TypeError("Must Pass String to getAllVisibleParameters()")
        
        if PacingModes._pacingModeIsAtrial(pacingMode):
            return PacingModes.AXXX.getParameters()
        elif PacingModes._pacingModeIsVentricular(pacingMode):
            return PacingModes.VXXX.getParameters()
        else:
            raise TypeError("Unknown Pacing Mode.")


    @classmethod
    def _pacingModeIsAtrial(cls, pacingMode: str) -> bool:
        if not isinstance(pacingMode, str):
            raise TypeError()
        pacingModeKey = pacingMode[0]
        if pacingModeKey == _ATRIAL_KEY:
            return True
        else:
            return False

        
    @classmethod
    def _pacingModeIsVentricular(cls, pacingMode: str) -> bool:
        if not isinstance(pacingMode, str):
            raise TypeError()
        pacingModeKey = pacingMode[0]
        if pacingModeKey == _VENTRICULAR_KEY:
            return True
        else:
            return False