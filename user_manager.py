import re   #regex
import local_storage
from pacemaker_pacingmodes import PacingModes
from pacemaker_parameters import Parameters
from user import User


_MAX_USERS_SAVED = int(10)
_REGEX_VALID_CHARS = "^[a-zA-Z0-9]*$"

_users: list[User] = local_storage.readUsersFromFile()
_activeUser: User | None = None


# --- Login, Register, Delete Users ---

def loginUser(username: str, password: str) -> tuple[bool, str]:
    usernameFormatted = username.strip()
    passwordFormatted = password.strip()

    isValidUsernamePassword, errorMsg = _validateUsernamePasswordInputs(usernameFormatted, passwordFormatted)
    if(not isValidUsernamePassword):
        return False, errorMsg
    
    user = _findUser(usernameFormatted)     # Checks that user exists
    userExists = isinstance(user, User)
    if not userExists or user.getPassword() != passwordFormatted:   
        return False, "Incorrect credentials."
    
    global _activeUser          # If user exists and passwords match, set as active user
    _activeUser = user
    return True, ""


def registerUser(username: str, password: str) -> tuple[bool, str]:
    if len(_users) >= _MAX_USERS_SAVED:                 # Check that the amount of saved users is not maxed
        return False, "Maximum amount of users created."
    
    usernameFormatted = username.strip()
    passwordFormatted = password.strip()

    isValidUsernamePassword, errorMsg = _validateUsernamePasswordInputs(usernameFormatted, passwordFormatted)
    if(not isValidUsernamePassword):
        return False, errorMsg
    
    usernameAvaliable = not isinstance(_findUser(usernameFormatted), User)   # Check if username is avaliable
    if not usernameAvaliable:                               
        return False, f"Username \'{usernameFormatted}\' already exists."
    
    newUser = User(usernameFormatted, passwordFormatted, PacingModes.getInitialPacingMode(), Parameters.getNominalValues())    # If username is avaliable, create new user and save user locally
    _users.append(newUser)
    local_storage.writeUsersToFile(_users)
    return True, ""


def deleteUser(username: str) -> tuple[bool, str]:
    user = _findUser(username)                          # Checks that user exists
    userExists = isinstance(user, User)
    if not userExists:                                  
        return False, f"Cannot delete user \'{username}\', user does not exist."
    
    _users.remove(user)                                 # If user exists, remove from list and save updates locally
    local_storage.writeUsersToFile(_users)


def _findUser(username: str) -> User | None:         # Finds user with matching username, returns user
    for user in _users:
        if not isinstance(user, User):
            raise TypeError
        if user.getUsername() == username:
            return user
    return None


def _validateUsernamePasswordInputs(username: str, password: str) -> tuple[bool, str]:
    if(len(username) <= 0):
        return False, "Invalid username. Please fill in all required fields."
    elif(not re.search(_REGEX_VALID_CHARS, username)):
        return False, "Invalid username. Please only use charaters from A-Z, a-z and 0-9."
    elif(len(password) <= 0):
        return False, "Invalid password. Please fill in all required fields."
    elif(not re.search(_REGEX_VALID_CHARS, password)):
        return False, "Invalid password. Please only use charaters from A-Z, a-z and 0-9."
    else:
        return True, ""
    

# --- Set & Get Parameters from Active User ---

def getActiveUserUsername() -> str:
    return _activeUser.getUsername()


def getPacingMode() -> str:
    return _activeUser.getPacingMode()


def savePacingMode(pacingMode: str | PacingModes) -> tuple[bool, str]:
    if isinstance(pacingMode, PacingModes):
        pacingMode = pacingMode.getName()

    _activeUser.setPacingMode(pacingMode)
    local_storage.writeUsersToFile(_users)
    return True, ""


def getSavedParameterValue(param: str | Parameters) -> float:
    if isinstance(param, Parameters):
        param = param.getName()
    return _activeUser.getParameterValue(param)


def getAllSavedParametersAndVisibilityFromSavedPacingMode() -> list[tuple[str, str, float, bool]]:
    # Returns list of (Param Name, Param Title, Saved Param Value, is Param Visible)
    listOfParamObjs = PacingModes.getAllVisibleParameters(_activeUser.getPacingMode())
    listOfParams = []
    for paramObj in listOfParamObjs:
        listOfParams.append((paramObj.getName(),
                             paramObj.getTitle(), 
                            _activeUser.getParameterValue(paramObj.getName()),
                            _isParameterVisible(paramObj.getName()),
                            ))
    return listOfParams

    
def _isParameterVisible(param: str) -> bool:
    if isinstance(param, Parameters):
        param = param.getName()
    listOfParamObjs = PacingModes[_activeUser.getPacingMode()].getParameters()
    for paramObj in listOfParamObjs:
        if param == paramObj.getName():
            return True
    return False


def saveParameterValue(param: str | Parameters, value: float) -> tuple[bool, str]:
    if isinstance(param, Parameters):
        param = param.getName()

    isValidParamValue, errorMsg = _validateParameterValue(param, value)
    if(not isValidParamValue):
        return False, errorMsg
    
    _activeUser.setParameterValue(param, float(value))
    local_storage.writeUsersToFile(_users)
    return True, ""


def _validateParameterValue(param: str, value: float) -> tuple[bool, str]:
    paramObj = Parameters[param]
    if not isinstance(value, float):
        try:
            float(value)
            return True, ""
        except ValueError:
                return False, f"Please enter a floating point number for Parameter \'{paramObj.getTitle()}\'."
    elif not paramObj.isAcceptableValue(value):
        return False, f"Invalid value of \'{value}\' for Parameter \'{paramObj.getTitle()}\'.\n{paramObj.getAcceptableValuesString()}"
    else:
        return True, ""