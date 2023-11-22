from enum import Enum

class Parameters(Enum):
    # PARAMETER_NAME = "title", "units", nominalValue, lowerLimit, upperLimit, decimalPlaces
    LOWER_RATE_LIMIT = "Lower Rate\nLimit", "ppm", 60, 30, 175, 0
    UPPER_RATE_LIMIT = "Upper Rate\nLimit", "ppm", 120, 50, 175, 0
    ATRIAL_AMPLITUDE = "Atrial\nAmplitude", "V", 5.0, 0.1, 5.0, 1
    ATRIAL_PULSE_WIDTH = "Atrial\nPulse Width", "ms", 1.0, 1.0, 30.0, 1
    ATRIAL_SENSITIVITY = "Atrial\nSensitivity", "mV", 1.0, 0.0, 5.0, 1
    ATRIAL_REFACTORY_PERIOD = "Atrial\nRefractory Period", "ms", 250, 150, 500, -1
    VENTRICULAR_AMPLITUDE = "Ventricular\nAmplitude", "V", 5.0, 0.1, 5.0, 1
    VENTRICULAR_PULSE_WIDTH = "Ventricular\nPulse Width", "ms", 1.0, 1.0, 30.0, 1
    VENTRICULAR_SENSITIVITY = "Ventricular\nSensitivity", "mV", 3.5, 0.0, 5.0, 1
    VENTRICULAR_REFACTORY_PERIOD = "Ventricular\nRefractory Period", "ms", 320, 150, 500, -1
    MAX_SENSOR_RATE = "Max Sensor\nRate", "ppm", 120, 50, 175, 0
    REACTION_TIME = "Reaction\nTime", "sec", 30, 10, 50, -1
    RESPONSE_FACTOR = "Response\nFactor", "", 8, 1, 16, 0
    RECOVERY_TIME = "Recovery\nTime", "min", 5, 2, 16, 0


    def __init__(self, title: str, units: str, nominalValue: float, lowerLimit: float, upperLimit: float, decimalPlaces: int) -> None:
        super().__init__()
        self._title = str(title)
        self._titleNoFormatting = self._title.replace('\n', ' ') # Used for error messages
        self._units = str(units)
        self._nominalValue = float(nominalValue)
        self._lowerLimit = float(lowerLimit)
        self._upperLimit = float(upperLimit)
        self._decimalPlaces = int(decimalPlaces)
        self._checkValues()


    def _checkValues(self) -> None:
        '''Verifies the Parameter's initialized values.'''
        if self._lowerLimit > self._upperLimit:
            raise ValueError(f"Parameter \'{self._titleNoFormatting}\' has a Lower Limit higher than the Upper Limit.")
        if not self.isAcceptableValue(self._nominalValue):
            raise ValueError(f"Parameter \'{self._titleNoFormatting}\' has a Nominal Value that is not an Acceptable Value.")
 

    def getName(self) -> str:
        '''Returns the Parameter's Name. Used as the key for dictionaries containing Parameters.'''
        return self.name


    def getTitle(self) -> str:
        '''Returns the Parameter Title. Note that this includes formatting characters for display on the GUI.'''
        return self._title
    

    def getTitleNoFormatting(self) -> str:
        '''Returns the Parameter's Title without any formatting, including removal of newline characters.'''
        return self._titleNoFormatting


    def getUnits(self) -> str:
        '''Returns the Parameter's Units as a string.'''
        return self._units


    def getNominalValue(self) -> float:
        '''Returns the Parameter's Nominal Value.'''
        return self._nominalValue


    def getLowerLimit(self) -> float:
        '''Returns the Parameter's Lower Limit.'''
        return self._lowerLimit


    def getUpperLimit(self) -> float:
        '''Returns the Parameter's Upper Limit.'''
        return self._upperLimit


    def getDecimalPlaces(self) -> float:
        '''Returns the Parameter's number of decimal places, used for rounding.'''
        return self._decimalPlaces
    

    def getAcceptableValuesString(self) -> str:
        '''Returns a formatted string of all the acceptable values of the Parameter. Used for the GUI.'''
        return f"{self._titleNoFormatting} Acceptable Range: {self._lowerLimit}-{self._upperLimit} {self._units} with an precision of {self._decimalPlaces} decimal places."
    

    def isAcceptableValue(self, value: float) -> bool:
        '''Validates that the given value is an acceptable value for the Parameter.'''
        return value >= self._lowerLimit and value <= self._upperLimit


    @classmethod
    def getNominalValues(cls) -> dict[str: float]:
        '''Returns a dictionary of {parameterName: parameterNominalValue}.'''
        return {param.getName(): param.getNominalValue() for param in Parameters}
            