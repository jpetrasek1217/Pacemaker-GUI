import re   #regex
import local_storage
import serial_comms
from pacemaker_pacingmodes import PacingModes
from pacemaker_parameters import Parameters
from user import User


_MAX_USERS_SAVED = int(10)
_REGEX_VALID_CHARS = "^[a-zA-Z0-9]*$"


# --- Init ---

_users: list[User] = local_storage.readUsersFromFile()
_activeUser: User | None = None
for user in _users:
    user.addMissingParameters(Parameters.getNominalValues())


# --- Login, Register, Delete Users ---

def loginUser(username: str, password: str) -> tuple[bool, str]:
    '''Attempts to login the User with the given Username and Password strings.
    Returns a tuple of (isSuccessful: bool, ErrorMessage: str).
    '''
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
    '''Attempts to register a new User with the given Username and Password strings.
    Returns a tuple of (isSuccessful: bool, ErrorMessage: str).
    '''
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


def logoutUser() -> tuple[bool, str]:
    '''Attempts to logout the active User.
    Returns a tuple of (isSuccessful: bool, ErrorMessage: str).
    '''
    global _activeUser
    _activeUser = None
    return True, ""


def deleteUser(username: str) -> tuple[bool, str]:
    '''Attempts to delete the User with the given Username string.
    Returns a tuple of (isSuccessful: bool, ErrorMessage: str).
    '''
    user = _findUser(username)                          # Checks that user exists
    userExists = isinstance(user, User)
    if not userExists:                                  
        return False, f"Cannot delete user \'{username}\', user does not exist."
    
    _users.remove(user)                                 # If user exists, remove from list and save updates locally
    local_storage.writeUsersToFile(_users)
    return True, ""


def _findUser(username: str) -> User | None:         # Finds user with matching username, returns user
    '''Returns a User with the matching given Username string,
    returns None if a User is not found.
    '''
    for user in _users:
        if not isinstance(user, User):
            raise TypeError
        if user.getUsername() == username:
            return user
    return None


def _validateUsernamePasswordInputs(username: str, password: str) -> tuple[bool, str]:
    '''Validates that the given Username and Password strings only contain the desired characters.
    Returns a tuple of (isSuccessful: bool, ErrorMessage: str).
    '''
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
    '''Returns the Active User's Username.'''
    return _activeUser.getUsername()


def getPacingMode() -> str:
    '''Returns the Active User's Pacing Mode.'''
    return _activeUser.getPacingMode()


def getAllPacingModes() -> list[str]:
    '''Returns a list of all the pacing modes.'''
    pacingModeList = []
    for pacingMode in PacingModes:
        pacingModeList.append(pacingMode.getName())
    return pacingModeList


def savePacingMode(pacingMode: str | PacingModes) -> tuple[bool, str]:
    '''Updates and saves the given Pacing Mode to the Active User.'''
    if isinstance(pacingMode, PacingModes):     # Checks if given type is a PacingModes
        pacingMode = pacingMode.getName()       # If so, get the str of the PacingMode

    _activeUser.setPacingMode(pacingMode)
    local_storage.writeUsersToFile(_users)
    return True, ""


def getSavedParameterValue(param: str | Parameters) -> float:
    '''Returns the value of the specified Parameter from the Active User.'''
    if isinstance(param, Parameters):
        param = param.getName()
    return _activeUser.getParameterValue(param)


def getAllSavedParametersAndVisibilityFromSavedPacingMode() -> list[tuple[str, str, float, bool]]:
    '''Get all saved Parameters from the Active User that correspond to either Atrial or Ventricular pacing modes.
    Returns a list of tuples of (parameterName: str, parameterTitle: str, parameterValue: float, isParamaterVisibleAndEditable: bool).'''
    # Returns list of (Param Name, Param Title, Saved Param Value, is Param Visible)
    listOfParamObjs = PacingModes.getAllVisibleParameters(_activeUser.getPacingMode())  # Returns all Atrial or Ventricular parameters
    listOfParams = []
    for paramObj in listOfParamObjs:
        paramObjName = paramObj.getName()
        listOfParams.append((paramObjName,
                             paramObj.getTitle() + '\n[' + paramObj.getUnits() + ']',   # Formatting for the GUI
                            _activeUser.getParameterValue(paramObjName),
                            _isParameterVisible(paramObjName),
                            ))
    return listOfParams

    
def _isParameterVisible(param: str) -> bool:
    '''Returns if the passed Parameter is in the subset of the Active User's Pacing Mode Parameters.'''
    if isinstance(param, Parameters):
        param = param.getName()
    listOfParamObjs = PacingModes[_activeUser.getPacingMode()].getParameters()  # Ger subset of parameters
    for paramObj in listOfParamObjs:
        if param == paramObj.getName():     # If given parameter is in the subset (Parameter should be visible & editable)
            return True
    return False


def saveParameterValue(param: str | Parameters, value: float) -> tuple[bool, str]:
    '''Updates the specified Parameter from the Active User with the given value.'''
    if isinstance(param, Parameters):
        param = param.getName()

    isValidParamValue, errorMsg = _validateParameterValue(param, value)
    if(not isValidParamValue):
        return False, errorMsg
    
    _activeUser.setParameterValue(param, float(value))
    local_storage.writeUsersToFile(_users)
    return True, ""


def _validateParameterValue(param: str, value: float) -> tuple[bool, str]:
    '''Validates that the passed Parameter value is within the Parameter's acceptable range.'''
    paramObj = Parameters[param]
    if not isinstance(value, float):    # Verify if value is a float
        try:
            value = float(value)        # Checks if passed value was an integer or numeric string
        except ValueError:
                return False, f"Please enter a floating point number for Parameter \'{paramObj.getTitleNoFormatting()}\'."
    
    if not paramObj.isAcceptableValue(value):     # Checks that the parameter is an acceptable value
        return False, f"Invalid value of \'{value}\' for Parameter \'{paramObj.getTitleNoFormatting()}\'.\n{paramObj.getAcceptableValuesString()}"
    else:
        return True, ""
    

# TODO: Remove Testing Code

byteArray = serial_comms.sendParameterDataToPacemaker(_users[0].getAllParameterValues(), _users[0].getPacingMode())
serial_comms.receiveParameterDataFromPacemaker(byteArray)