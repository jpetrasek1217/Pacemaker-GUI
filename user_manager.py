from typing import Optional
from user import User
import local_storage


_MAX_USERS_SAVED = int(10)
_users: list[User] = local_storage.readUsersFromFile()
_activeUser: Optional[User] = None


def getActiveUser() -> Optional[User]:
    return _activeUser


def loginUser(username: str, password: str) -> None:
    user = _findUser(username)                          # Checks that user exists
    userExists = isinstance(user, User)
    
    if userExists and user.getPassword() == password:   # If user exists and passwords match, set as active user
        global _activeUser
        _activeUser = user


def registerUser(username: str, password: str) -> None:
    if len(_users) >= _MAX_USERS_SAVED:                 # Check that the amount of saved users is not maxed
        return
    usernameAvaliable = not isinstance(_findUser(username), User)   # Check if username is avaliable
    if usernameAvaliable:                               # If username is avaliable, create new user and save user locally
        newUser = User(username, password)
        _users.append(newUser)
        local_storage.writeUsersToFile(_users)


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

# TODO: Remove Testing Code