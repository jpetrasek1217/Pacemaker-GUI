import json
from user import User

_USERS_FILEPATH = "local_storage/users.json"
_USERNAME_KEY = "USERNAME"
_PASSWORD_KEY = "PASSWORD"
_PACINGMODE_KEY = "PACING_MODE"
_PARAMS_KEY = "PARAMETERS"

def readUsersFromFile() -> list[User]:
    '''Reads all the saved User data from file, returns a list of User Objects.'''
    users = []
    userDictList = _readFromJSONFile(_USERS_FILEPATH)
    for userDict in userDictList:
        usernameStr = userDict[_USERNAME_KEY]
        passwordStr = userDict[_PASSWORD_KEY]
        pacingModeStr = userDict[_PACINGMODE_KEY]
        parametersDict = userDict[_PARAMS_KEY]
        user = User(usernameStr, passwordStr, pacingModeStr, parametersDict)
        users.append(user)
    return users


def _readFromJSONFile(filepath: str) -> dict:
    '''Reads a dicitionary from the specified JSON file.'''
    with open(filepath, "r") as file:
        fileContents = json.load(file)
    return fileContents


def writeUsersToFile(users: list[User]) -> None:
    '''Saves and writes a list of User Objects to the User data file.'''
    userDictList = []
    for user in users:
        userDict = {}
        userDict[_USERNAME_KEY] = user.getUsername()
        userDict[_PASSWORD_KEY] = user.getPassword()
        userDict[_PACINGMODE_KEY] = user.getPacingMode()
        userDict[_PARAMS_KEY] = user.getAllParameterValues()
        userDictList.append(userDict)
    _writeToJSONFile(_USERS_FILEPATH, userDictList)


def _writeToJSONFile(filepath: str, fileContents: dict) -> None:
    '''Writes a dicitionary to the specified JSON file.'''
    with open(filepath, "w") as file:
        json.dump(fileContents, file)