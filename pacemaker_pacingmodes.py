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
        Parameters.ATRIAL_REFACTORY_PERIOD,
    ], False

    AAI = _PACING_TYPE_ATRIAL, [
        Parameters.LOWER_RATE_LIMIT,
        Parameters.UPPER_RATE_LIMIT,
        Parameters.ATRIAL_AMPLITUDE,
        Parameters.ATRIAL_PULSE_WIDTH,
        Parameters.ATRIAL_REFACTORY_PERIOD,
        Parameters.ATRIAL_SENSITIVITY,
    ], False

    AOOR = _PACING_TYPE_ATRIAL, [
        Parameters.LOWER_RATE_LIMIT,
        Parameters.UPPER_RATE_LIMIT,
        Parameters.ATRIAL_AMPLITUDE,
        Parameters.ATRIAL_PULSE_WIDTH,
        Parameters.ATRIAL_REFACTORY_PERIOD,
        Parameters.MAX_SENSOR_RATE,
        Parameters.REACTION_TIME,
        Parameters.RESPONSE_FACTOR,
        Parameters.RECOVERY_TIME,
    ], True

    AAIR = _PACING_TYPE_ATRIAL, [
        Parameters.LOWER_RATE_LIMIT,
        Parameters.UPPER_RATE_LIMIT,
        Parameters.ATRIAL_AMPLITUDE,
        Parameters.ATRIAL_PULSE_WIDTH,
        Parameters.ATRIAL_REFACTORY_PERIOD,
        Parameters.ATRIAL_SENSITIVITY,
        Parameters.MAX_SENSOR_RATE,
        Parameters.REACTION_TIME,
        Parameters.RESPONSE_FACTOR,
        Parameters.RECOVERY_TIME,
    ], True

    # Generic Object for all Atrial Parameters
    _AXXX = _PACING_TYPE_ATRIAL, [
        Parameters.LOWER_RATE_LIMIT,
        Parameters.UPPER_RATE_LIMIT,
        Parameters.ATRIAL_AMPLITUDE,
        Parameters.ATRIAL_PULSE_WIDTH,
        Parameters.ATRIAL_REFACTORY_PERIOD,
        Parameters.ATRIAL_SENSITIVITY,
        Parameters.MAX_SENSOR_RATE,
        Parameters.REACTION_TIME,
        Parameters.RESPONSE_FACTOR,
        Parameters.RECOVERY_TIME,
    ], True

    VOO = _PACING_TYPE_VENTRICULAR, [
        Parameters.LOWER_RATE_LIMIT,
        Parameters.UPPER_RATE_LIMIT,
        Parameters.VENTRICULAR_AMPLITUDE,
        Parameters.VENTRICULAR_PULSE_WIDTH,
        Parameters.VENTRICULAR_REFACTORY_PERIOD,
    ], False

    VVI = _PACING_TYPE_VENTRICULAR, [
        Parameters.LOWER_RATE_LIMIT,
        Parameters.UPPER_RATE_LIMIT,
        Parameters.VENTRICULAR_AMPLITUDE,
        Parameters.VENTRICULAR_PULSE_WIDTH,
        Parameters.VENTRICULAR_REFACTORY_PERIOD,
        Parameters.VENTRICULAR_SENSITIVITY,
    ], False

    VOOR = _PACING_TYPE_VENTRICULAR, [
        Parameters.LOWER_RATE_LIMIT,
        Parameters.UPPER_RATE_LIMIT,
        Parameters.VENTRICULAR_AMPLITUDE,
        Parameters.VENTRICULAR_PULSE_WIDTH,
        Parameters.VENTRICULAR_REFACTORY_PERIOD,
        Parameters.MAX_SENSOR_RATE,
        Parameters.REACTION_TIME,
        Parameters.RESPONSE_FACTOR,
        Parameters.RECOVERY_TIME,
    ], True

    VVIR = _PACING_TYPE_VENTRICULAR, [
        Parameters.LOWER_RATE_LIMIT,
        Parameters.UPPER_RATE_LIMIT,
        Parameters.VENTRICULAR_AMPLITUDE,
        Parameters.VENTRICULAR_PULSE_WIDTH,
        Parameters.VENTRICULAR_REFACTORY_PERIOD,
        Parameters.VENTRICULAR_SENSITIVITY,
        Parameters.MAX_SENSOR_RATE,
        Parameters.REACTION_TIME,
        Parameters.RESPONSE_FACTOR,
        Parameters.RECOVERY_TIME,
    ], True

    # Generic Object for all Ventricular Parameters
    _VXXX = _PACING_TYPE_VENTRICULAR, [
        Parameters.LOWER_RATE_LIMIT,
        Parameters.UPPER_RATE_LIMIT,
        Parameters.VENTRICULAR_AMPLITUDE,
        Parameters.VENTRICULAR_PULSE_WIDTH,
        Parameters.VENTRICULAR_REFACTORY_PERIOD,
        Parameters.VENTRICULAR_SENSITIVITY,
        Parameters.MAX_SENSOR_RATE,
        Parameters.REACTION_TIME,
        Parameters.RESPONSE_FACTOR,
        Parameters.RECOVERY_TIME,
    ], True


    def __init__(self, pacingType: str, listOfParameters: list[Parameters], isThresholdVisible: bool) -> None:
        super().__init__()
        self._pacingType = str(pacingType) # Atrial or Ventricular
        self._params = list(listOfParameters)
        self._isThresholdVisible = bool(isThresholdVisible)
        self._checkValues()


    def _checkValues(self) -> None:
        '''Verifies that all the items in the Parameter list are Parameter Objects.'''
        if any(not isinstance(param, Parameters) for param in self._params):
            raise TypeError(f"Pacing Mode \'{self.name}\' has objects that are not a Parameter.")
        

    def getName(self) -> str:
        '''Returns the Pacing Mode's name.  Used as the key for dictionaries containing Pacing Modes.'''
        return self.name


    def getParameters(self) -> list[Parameters]:
        '''Returns a list of the Pacing Mode's Parameters as Pacing Mode Parameter objects.'''
        return self._params
    

    def isThresholdVisible(self) -> bool:
        '''Returns a boolean value of if the threshold should be editable for a given pacing mode.'''
        return self._isThresholdVisible
    

    def isAtrialPacingType(self) -> bool:
        '''Returns a boolean value of if the given pacing mode is Atrial.'''
        return self._pacingType == _PACING_TYPE_ATRIAL
    

    def isVentricularPacingType(self) -> bool:
        '''Returns a boolean value of if the given pacing mode is Ventricular.'''
        return self._pacingType == _PACING_TYPE_VENTRICULAR
    
    
    @classmethod
    def getInitialPacingMode(cls) -> str:
        '''Returns the default Pacing Mode name.'''
        return PacingModes.AOO.getName()
    

    @classmethod
    def getAllVisibleParameters(cls, pacingMode: str) -> list[Parameters]:
        '''Returns all Pacing Mode Parameters for either the Atrial or Ventricular Pacing Types.'''
        if not isinstance(pacingMode, str):
            raise TypeError("Must Pass String to getAllVisibleParameters()")
        
        if PacingModes[pacingMode].isAtrialPacingType():
            return PacingModes._AXXX.getParameters()
        elif PacingModes[pacingMode].isVentricularPacingType():
            return PacingModes._VXXX.getParameters()
        else:
            raise TypeError("Unknown Pacing Mode.")