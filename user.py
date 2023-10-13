class User:
    def __init__(self, username: str, password: str, pacingMode: str, params: dict[str: float]) -> None:
        self._username = str(username)
        self._password = str(password)
        self._pacingMode = str(pacingMode)
        self._params = params

    def __repr__(self) -> str:
        s = f"\nuser.User object:\n\tUSERNAME: {self._username}\n\tPASSWORD: {self._password}\n"
        for key in self._params:
            s += f"\t{key}: {str(self._params[key])}\n"
        return s
    

    def __str__(self) -> str:
        return self.__repr__()[1:-1]  # Removes first and last newline chars, purely for formatting in terminal

   
    def getUsername(self) -> str:
        '''Returns the User's username.'''
        return self._username
    

    def getPassword(self) -> str:
        '''Returns the User's password.'''
        return self._password
    

    def getPacingMode(self) -> str:
        '''Returns the User's pacing mode.'''
        return self._pacingMode
    

    def setPacingMode(self, pacingMode: str) -> None:
        '''Sets the User's Pacing Mode.'''
        self._pacingMode = str(pacingMode)


    def getParameterValue(self, key: str) -> float:
        '''Returns the value of the specified Pacemaker Parameter.'''
        keyExists = isinstance(self._params.get(key), float)    # Check if key exists in user's parameters
        if keyExists:
            return self._params[key]
        else:
            raise KeyError(f"The key \'{key}\' is not in a valid Parameter key.")
    

    def getAllParameterValues(self) -> dict[str: float]:
        '''Returns a dictionary of all the User's Pacemaker Parameter values.'''
        return self._params
    

    def setParameterValue(self, key: str, value: float) -> None:
        '''Update the specified Pacemaker Parameter with the given value.'''
        keyExists = isinstance(self._params.get(key), float)    # Check if key exists in user's parameters
        valueIsFloat = isinstance(value, float)
        if keyExists and valueIsFloat:
            self._params[key] = value
        elif keyExists and not valueIsFloat:
            raise ValueError(f"Function user.setParameterValue(key, value) expected float, recieved \'{value}\'")
        else:
            raise KeyError(f"The key \'{key}\' is not in a valid Parameter key.")


    def setAllParameterValues(self, params: dict[str: float]) -> None:
        '''Updates values of the User's Pacemaker Parameters with the values in the given  dictionary.'''
        for key in self._params:            # Loop through user's parameter dictionary
            value = params.get(key)         # Get value from sent dict, if it does not exist get() returns None
            keyExistsInBoth = isinstance(value, float)  # Validates key exists in both and that the sent value is a float
            if keyExistsInBoth:             # If the key did exist, set user's param to sent param
                self._params[key] = value


    def addMissingParameters(self, params: dict[str: float]) -> None:
        '''Adds all missing items in given dictionary to the User's Pacemaker Parameters.'''
        for key in params:
            if key not in self._params:
                self._params[key] = params[key]