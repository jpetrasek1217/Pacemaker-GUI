import re
import local_storage
from user import User
from typing import Optional
from GUI_helpers import throwErrorPopup


_MAX_USERS_SAVED = int(10)
_REGEX_VALID_CHARS = "^[a-zA-Z0-9]*$"

_users: list[User] = local_storage.readUsersFromFile()
_activeUser: Optional[User] = None


def getActiveUser() -> Optional[User]:
    return _activeUser


def loginUser(username: str, password: str) -> tuple(bool, str):
    usernameFormatted = username.strip()
    passwordFormatted = password.strip()

    returnSuccess, errorMsg = _validateUsernamePasswordInputs(usernameFormatted, passwordFormatted)
    if(not returnSuccess):
        return False, errorMsg
    
    user = _findUser(usernameFormatted)     # Checks that user exists
    userExists = isinstance(user, User)
    if not userExists or user.getPassword() != passwordFormatted:   
        return False, "Incorrect credentials."
    
    global _activeUser          # If user exists and passwords match, set as active user
    _activeUser = user
    return True, ""


def registerUser(username: str, password: str) -> tuple(bool, str):
    if len(_users) >= _MAX_USERS_SAVED:                 # Check that the amount of saved users is not maxed
        return False, "Maximum amount of users created."
    
    usernameFormatted = username.strip()
    passwordFormatted = password.strip()

    returnSuccess, errorMsg = _validateUsernamePasswordInputs(usernameFormatted, passwordFormatted)
    if(not returnSuccess):
        return False, errorMsg
    
    usernameAvaliable = not isinstance(_findUser(usernameFormatted), User)   # Check if username is avaliable
    if not usernameAvaliable:                               
        return False, f"Username \'{usernameFormatted}\' already exists."
    
    newUser = User(usernameFormatted, passwordFormatted)    # If username is avaliable, create new user and save user locally
    _users.append(newUser)
    local_storage.writeUsersToFile(_users)
    return True, ""


def deleteUser(username: str) -> tuple(bool, str):
    user = _findUser(username)                          # Checks that user exists
    userExists = isinstance(user, User)
    if not userExists:                                  
        return False, f"Cannot delete user \'{username}\', user does not exist."
    
    _users.remove(user)                                 # If user exists, remove from list and save updates locally
    local_storage.writeUsersToFile(_users)


def _findUser(username: str) -> Optional[User]:         # Finds user with matching username, returns user
    for user in _users:
        if not isinstance(user, User):
            raise TypeError
        if user.getUsername() == username:
            return user
    return None


def _validateUsernamePasswordInputs(username: str, password: str) -> tuple(bool, str):
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