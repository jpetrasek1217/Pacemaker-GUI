from datetime import datetime

'''
NOTE: This is not a complete implementation.
The raw data recieved from the communcations method from the pacemaker is not defined,
thus parsing the raw data cannot be completed. Placeholder values are in place to keep code operational.
'''

# List of data received from pacemaker
_receivedData: list[tuple[datetime, float]] = []


def getReceivedDataList() -> list[tuple[datetime, float]]:
    return _receivedData.copy()


def getReceivedDataAtTime(time: datetime) -> float:
    for datapoint in _receivedData:
        if datapoint[0] == time:
            return datapoint[1]
    # Time not found
    raise ValueError(f"Time {time} not found in egram received data.")


def receiveDataFromPacemaker(maxDatapointsCollected: int = 100) -> None:
    while _isCommsActiveWithPacemaker() and len(_receivedData) < maxDatapointsCollected:
        rawData = None # Read from communications from Pacemaker, # Placeholder until data datatype is defined by communications method
        parsedData = _parseData(rawData)
        _receivedData.append(parsedData)


def _parseData(data) -> tuple[datetime, float]:
    # Parses raw data from pacemaker comms into tuple of datetime, float
    datetimeData = datetime(year=2000, month=1, day=1, hour=1, minute=1, second=1, microsecond=1) 
    floatData = 0.0         # Placeholders until data datatype is defined by communications method
    return datetimeData, floatData


def _isCommsActiveWithPacemaker() -> bool:
    # Checks that comms is actively open with pacemaker by watching port activity
    return True    # Placeholder until communications method is defined
