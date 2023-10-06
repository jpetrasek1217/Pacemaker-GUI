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
        self._title = title
        self._title_no_newline = self._title.replace('\n', ' ')
        self._units = units
        self._nominalValue = nominalValue
        self._lowerLimit = lowerLimit
        self._upperLimit = upperLimit
        self._additionalAcceptableValues = args
        self._checkValues()

    def _checkValues(self) -> None:
        if self._lowerLimit > self._upperLimit:
            raise ValueError(f"Parameter \'{self._title_no_newline}\' has a Lower Limit higher than the Upper Limit.")
        if not self.isAcceptableValue(self._nominalValue):
            raise ValueError(f"Parameter \'{self._title_no_newline}\' has a Nominal Value that is not an Accepted Value.")

    def getName(self) -> str:
        return self.name

    def getTitle(self) -> str:
        return self._title
    
    def getTitleNoNewline(self) -> str:
        return self._title_no_newline
    
    def getUnits(self) -> str:
        return self._units

    def getNominalValue(self) -> float:
        return self._nominalValue
    
    def getLowerLimit(self) -> float:
        return self._lowerLimit
    
    def getUpperLimit(self) -> float:
        return self._upperLimit
    
    def getAcceptableValuesString(self) -> str:
        s = f"{self._title_no_newline} Acceptable Values: {self._lowerLimit}-{self._upperLimit} {self._units}"
        if self._additionalAcceptableValues:
            s += " or a value of "
            for acceptableVal in self._additionalAcceptableValues:
                s += f"{acceptableVal}, " 
            s = s[:-2]
            s += f" {self._units}"
        return s
    
    def isAcceptableValue(self, value: float) -> bool:
        if value >= self._lowerLimit and value <= self._upperLimit:
            return True
        elif self._additionalAcceptableValues and any(value == acceptableVal for acceptableVal in self._additionalAcceptableValues):
            return True
        else:
            return False

    @classmethod
    def getNominalValues(cls) -> dict[str: float]:
        return {param.getName(): param.getNominalValue() for param in Parameters}
            