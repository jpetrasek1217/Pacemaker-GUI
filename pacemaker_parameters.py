from enum import Enum

class Parameters(Enum):
    # PARAMETER_NAME = "title", "units", nominalValue, lowerLimit, upperLimit, *additionalAcceptableValues
    LOWER_RATE_LIMIT = "Lower Rate\nLimit", "ppm", 60.0, 30.0, 175.0
    UPPER_RATE_LIMIT = "Upper Rate\nLimit", "ppm", 120.0, 50.0, 175.0
    ATRIAL_AMPLITUDE = "Atrial\nAmplitude", "V", 3.5, 0.5, 7.0, 0.0
    ATRIAL_PULSE_WIDTH = "Atrial\nPulse Width", "ms", 0.4, 0.1, 1.9, 0.05
    ATRIAL_REFACTORY_PERIOD = "Atrial\nRefractory Period", "ms", 250.0, 150.0, 500.0
    ATRIAL_SENSITIVITY = "Atrial\nSensitivity", "mV", 0.75, 1.0, 10.0, 0.25, 0.5, 0.75
    VENTRICULAR_AMPLITUDE = "Ventricular\nAmplitude", "V", 3.5, 0.5, 7.0, 0.0
    VENTRICULAR_PULSE_WIDTH = "Ventricular\nPulse Width", "ms", 0.4, 0.1, 1.9, 0.05
    VENTRICULAR_REFACTORY_PERIOD = "Ventricular\nRefractory Period", "ms", 320.0, 150.0, 500.0
    VENTRICULAR_SENSITIVITY = "Ventricular\nSensitivity", "mV", 2.5, 1.0, 10.0, 0.25, 0.5, 0.75
    HYSTERESIS = "Hysteresis", "ms", 0.0, 30.0, 175.0, 0.0
    RATE_SMOOTHING = "Rate\nSmoothing", "%", 0.0, 3.0, 25.0, 0.0
    MAX_SENSOR_RATE = "Max Sensor\nRate", "ppm", 120.0, 50.0, 175.0
    PVARP = "PVARP", "ms", 250.0, 150.0, 500.0

    def __init__(self, title: str, units: str, nominalValue: float, lowerLimit: float, upperLimit: float, *args: float) -> None:
        super().__init__()
        self._title = str(title)
        self._title_no_formatting = self._title.replace('\n', ' ') # Used for error messages
        self._units = str(units)
        self._nominalValue = float(nominalValue)
        self._lowerLimit = float(lowerLimit)
        self._upperLimit = float(upperLimit)
        self._additionalAcceptableValues = list(args)
        self._checkValues()

    def _checkValues(self) -> None:
        '''Verifies the Parameter's initialized values.'''
        if self._lowerLimit > self._upperLimit:
            raise ValueError(f"Parameter \'{self._title_no_formatting}\' has a Lower Limit higher than the Upper Limit.")
        if not self.isAcceptableValue(self._nominalValue):
            raise ValueError(f"Parameter \'{self._title_no_formatting}\' has a Nominal Value that is not an Accepted Value.")
        try:
            for i in range(len(self._additionalAcceptableValues)):
                self._additionalAcceptableValues[i] = float(self._additionalAcceptableValues[i])
        except ValueError:
            raise ValueError(f"Parameter \'{self._title_no_formatting}\' has Additional Acceptable Values that are not numbers.")

    def getName(self) -> str:
        '''Returns the Parameter's Name. Used as the key for dictionaries containing Parameters.'''
        return self.name

    def getTitle(self) -> str:
        '''Returns the Parameter Title. Note that this includes formatting characters for display on the GUI.'''
        return self._title
    
    def getTitleNoFormatting(self) -> str:
        '''Returns the Parameter's Title without any formatting.'''
        return self._title_no_formatting
    
    def getUnits(self) -> str:
        '''Returns the Parameter's Units.'''
        return self._units

    def getNominalValue(self) -> float:
        '''Returns the Parameter's Nominal Value.'''
        return self._nominalValue
    
    def getLowerLimit(self) -> float:
        '''Return's the Parameter's Lower Limit.'''
        return self._lowerLimit
    
    def getUpperLimit(self) -> float:
        '''Returns the Parameter;s Upper Limit.'''
        return self._upperLimit
    
    def getAcceptableValuesString(self) -> str:
        '''Returns a formatted string of all the acceptable values of the Parameter. Used for the GUI.'''
        s = f"{self._title_no_formatting} Acceptable Values: {self._lowerLimit}-{self._upperLimit} {self._units}"
        if self._additionalAcceptableValues:
            s += " or a value of "
            for acceptableVal in self._additionalAcceptableValues:
                s += f"{acceptableVal}, " 
            s = s[:-2]
            s += f" {self._units}"
        return s
    
    def isAcceptableValue(self, value: float) -> bool:
        '''Validates that the given value is an acceptable value for the Parameter.'''
        if value >= self._lowerLimit and value <= self._upperLimit:
            return True
        elif self._additionalAcceptableValues and any(value == acceptableVal for acceptableVal in self._additionalAcceptableValues):
            return True
        else:
            return False

    @classmethod
    def getNominalValues(cls) -> dict[str: float]:
        '''Returns a dictionary of {parameterName: parameterNominalValue}.'''
        return {param.getName(): param.getNominalValue() for param in Parameters}
            