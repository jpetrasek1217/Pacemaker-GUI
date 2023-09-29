import re
import local_storage
from user import User
from typing import Optional
from GUI_components import throwErrorPopup


_MAX_USERS_SAVED = int(10)
_REGEX_VALID_CHARS = "^[a-zA-Z0-9]*$"

_users: list[User] = local_storage.readUsersFromFile()
_activeUser: Optional[User] = None


def getActiveUser() -> Optional[User]:
    return _activeUser


def loginUser(username: str, password: str) -> None:
    usernameFormatted = username.strip()
    passwordFormatted = password.strip()

    validInputs = _validateUsernamePasswordInputs(usernameFormatted, passwordFormatted)
    if(not validInputs):
        return
    
    user = _findUser(usernameFormatted)                          # Checks that user exists
    userExists = isinstance(user, User)
    if userExists and user.getPassword() == passwordFormatted:   # If user exists and passwords match, set as active user
        global _activeUser
        _activeUser = user
    else:
        throwErrorPopup("Incorrect credentials.")


def registerUser(username: str, password: str) -> None:
    if len(_users) >= _MAX_USERS_SAVED:                 # Check that the amount of saved users is not maxed
        throwErrorPopup("Maximum amount of users created.")
        return
    
    usernameFormatted = username.strip()
    passwordFormatted = password.strip()

    validInputs = _validateUsernamePasswordInputs(usernameFormatted, passwordFormatted)
    if(not validInputs):
        return
    
    usernameAvaliable = not isinstance(_findUser(usernameFormatted), User)   # Check if username is avaliable
    if usernameAvaliable:                               # If username is avaliable, create new user and save user locally
        newUser = User(usernameFormatted, passwordFormatted)
        _users.append(newUser)
        local_storage.writeUsersToFile(_users)
    else:
        throwErrorPopup(f"Username \'{usernameFormatted}\' already exists.")


def deleteUser(username: str) -> None:
    user = _findUser(username)                          # Checks that user exists
    userExists = isinstance(user, User)
    if userExists:                                      # If user exists, remove from list and save updates locally
        _users.remove(user)
        local_storage.writeUsersToFile(_users)


def _findUser(username: str) -> Optional[User]:         # Finds user with matching username, returns user
    for user in _users:
        if not isinstance(user, User):
            raise TypeError
        if user.getUsername() == username:
            return user
    return None


def _validateUsernamePasswordInputs(username: str, password: str) -> bool:
    if(len(username) <= 0):
        throwErrorPopup("Invalid username. Please fill in all required fields.")
        return False
    elif(not re.search(_REGEX_VALID_CHARS, username)):
        throwErrorPopup("Invalid username. Please only use charaters from A-Z, a-z and 0-9.")
        return False
    elif(len(password) <= 0):
        throwErrorPopup("Invalid password. Please fill in all required fields.")
        return False
    elif(not re.search(_REGEX_VALID_CHARS, password)):
        throwErrorPopup("Invalid password. Please only use charaters from A-Z, a-z and 0-9.")
        return False
    else:
        return True