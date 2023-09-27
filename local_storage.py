import json
from user import User, Parameters   # TODO: Remove parameters import

_USERS_FILEPATH = "users.json"
_USERNAME_KEY = "username"
_PASSWORD_KEY = "password"
_PARAMS_KEY = "parameters"

def readUsersFromFile() -> list[User]:
    users = []
    userDictList = _readFromJSONFile(_USERS_FILEPATH)
    for userDict in userDictList:
        username = userDict[_USERNAME_KEY]
        password = userDict[_PASSWORD_KEY]
        parameters = userDict[_PARAMS_KEY]
        user = User(username, password)
        user.setAllParameters(parameters)
        users.append(user)
    return users


def _readFromJSONFile(filepath: str) -> dict:
    with open(filepath, "r") as file:
        fileContents = json.load(file)
    return fileContents


def writeUsersToFile(users: list[User]) -> None:
    userDictList = []
    for user in users:
        userDict = {}
        userDict[_USERNAME_KEY] = user.getUsername()
        userDict[_PASSWORD_KEY] = user.getPassword()
        userDict[_PARAMS_KEY] = user.getAllParameters()
        userDictList.append(userDict)
    _writeToJSONFile(_USERS_FILEPATH, userDictList)


def _writeToJSONFile(filepath: str, fileContents: dict) -> None:
    with open(filepath, "w") as file:
        json.dump(fileContents, file)

# TODO: Remove Testing Code

users = readUsersFromFile()
users[1].setParameter(Parameters.ATRIAL_AMPLITUDE, 92.3)
users[1].setParameter(Parameters.VENTRICULAR_REFACTORY_PERIOD, 29.34)
writeUsersToFile(users)
print(users)

