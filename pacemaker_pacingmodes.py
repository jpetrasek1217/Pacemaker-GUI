from enum import Enum
from pacemaker_parameters import Parameters

_PACING_TYPE_ATRIAL = "ATRIAL"
_PACING_TYPE_VENTRICULAR = "VENTRICULAR"

class PacingModes(Enum):
    AOO = _PACING_TYPE_ATRIAL, [
        Parameters.LOWER_RATE_LIMIT,
        Parameters.UPPER_RATE_LIMIT,
        Parameters.ATRIAL_AMPLITUDE,
        Parameters.ATRIAL_PULSE_WIDTH,
    ]

    AAI = _PACING_TYPE_ATRIAL, [
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

    AOOR = _PACING_TYPE_ATRIAL, [
        Parameters.LOWER_RATE_LIMIT,
        Parameters.UPPER_RATE_LIMIT,
        Parameters.ATRIAL_AMPLITUDE,
        Parameters.ATRIAL_PULSE_WIDTH,
        Parameters.MAX_SENSOR_RATE,
    ]

    AAIR = _PACING_TYPE_ATRIAL, [
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

    _AXXX = _PACING_TYPE_ATRIAL, [
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

    VOO = _PACING_TYPE_VENTRICULAR, [
        Parameters.LOWER_RATE_LIMIT,
        Parameters.UPPER_RATE_LIMIT,
        Parameters.VENTRICULAR_AMPLITUDE,
        Parameters.VENTRICULAR_PULSE_WIDTH,
    ]

    VVI = _PACING_TYPE_VENTRICULAR, [
        Parameters.LOWER_RATE_LIMIT,
        Parameters.UPPER_RATE_LIMIT,
        Parameters.VENTRICULAR_AMPLITUDE,
        Parameters.VENTRICULAR_PULSE_WIDTH,
        Parameters.VENTRICULAR_SENSITIVITY,
        Parameters.VENTRICULAR_REFACTORY_PERIOD,
        Parameters.HYSTERESIS,
        Parameters.RATE_SMOOTHING,
    ]

    VOOR = _PACING_TYPE_VENTRICULAR, [
        Parameters.LOWER_RATE_LIMIT,
        Parameters.UPPER_RATE_LIMIT,
        Parameters.VENTRICULAR_AMPLITUDE,
        Parameters.VENTRICULAR_PULSE_WIDTH,
        Parameters.MAX_SENSOR_RATE,
    ]

    VVIR = _PACING_TYPE_VENTRICULAR, [
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

    _VXXX = _PACING_TYPE_VENTRICULAR, [
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

    def __init__(self, pacingType: str, listOfParameters: list[Parameters]) -> None:
        super().__init__()
        self._pacingType = pacingType # Atrial or Ventricular
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
        
        if PacingModes[pacingMode]._pacingType == _PACING_TYPE_ATRIAL:
            return PacingModes._AXXX.getParameters()
        elif PacingModes[pacingMode]._pacingType == _PACING_TYPE_VENTRICULAR:
            return PacingModes._VXXX.getParameters()
        else:
            raise TypeError("Unknown Pacing Mode.")