from enum import Enum

class Thresholds(Enum):
    VERY_LOW = 'Very Low', 25.0
    LOW = 'Low', 30.0
    MED_LOW = 'Medium Low', 35.0
    MED = 'Medium', 40.0
    MED_HIGH = 'Medium High', 45.0
    HIGH = 'High', 50.0
    VERY_HIGH = 'Very High', 55.0


    def __init__(self, title: str, value: float) -> None:
        super().__init__()
        self._title = str(title)
        self._value = float(value)
    

    def getName(self) -> str:
        '''Returns the Threshold's name.  Used as the key for dictionaries containing Thresholds.'''
        return self.name


    def getTitle(self) -> str:
        '''Returns the Threshold Title. Note that this includes formatting characters for display on the GUI.'''
        return self._title
    

    def getValue(self) -> float:
        '''Returns the Threshold numerical value used by the Pacemaker.'''
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
        '''Returns the default Threshold name.'''
        return Thresholds.MED.getName()