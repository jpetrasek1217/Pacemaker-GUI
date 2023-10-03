from enum import Enum
from pacemaker_parameters import Parameters


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
    def getInitialPacingMode(self) -> str:
        return PacingModes.AOO.name