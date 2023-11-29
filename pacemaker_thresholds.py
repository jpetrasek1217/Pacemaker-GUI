from enum import Enum

class Thresholds(Enum):
    VERY_LOW = 'Very Low', 0.05
    LOW = 'Low', 1.15
    MED_LOW = 'Medium Low', 2.25
    MED = 'Medium', 3.35
    MED_HIGH = 'Medium High', 4.45
    HIGH = 'High', 5.55
    VERY_HIGH = 'Very High', 6.65


    def __init__(self, title: str, value: float) -> None:
        super().__init__()
        self._title = str(title)
        self._value = float(value)
    

    def getName(self) -> str:
        '''Returns the Threshold's name.  Used as the key for dictionaries containing Pacing Modes.'''
        return self.name


    def getTitle(self) -> str:
        '''Returns the Threshold Title. Note that this includes formatting characters for display on the GUI.'''
        return self._title
    

    def getValue(self) -> float:
        '''Returns the Threshold Value.'''
        return self._value


    @classmethod
    def getThresholdTitles(cls) -> dict[str: float]:
        '''Returns a dictionary of {thresholdName: ThresholdTitle}.'''
        return {thres.getName(): thres.getTitle() for thres in Thresholds}
    

    @classmethod
    def getThresholdValues(cls) -> dict[str: float]:
        '''Returns a dictionary of {thresholdName: ThresholdValue}.'''
        return {thres.getName(): thres.getValue() for thres in Thresholds}
    

    @classmethod
    def getNominalValue(cls) -> float:
        return Thresholds.MED.getValue()