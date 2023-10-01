from pacing_modes import Parameters, ParameterKeyError

class User:
    def __init__(self, username: str, password: str) -> None:
        self._username = str(username)
        self._password = str(password)
        self._params = {param.value:0.0 for param in Parameters}    # Init dict of all parameters, default values to zero
       

    def __repr__(self) -> str:
        s = f"\nuser.User object:\n\tusername: {self._username}\n\tpassword: {self._password}\n"
        for key in self._params:
            s += f"\t{key}: {str(self._params[key])}\n"
        return s
    

    def __str__(self) -> str:
        return self.__repr__()[1:-1]  # Removes first and last newline chars, purely for formatting in terminal

   
    def getUsername(self) -> str:
        return self._username
    

    def getPassword(self) -> str:
        return self._password


    def getParameter(self, key: Parameters) -> float:
        keyExists = isinstance(self._params.get(key), float)    # Check if key exists in user's parameters
        if keyExists:
            return self._params[key]
        else:
            raise ParameterKeyError(key)
    

    def getAllParameters(self) -> dict[Parameters, float]:
        return self._params
    

    def setParameter(self, key: Parameters, value: float) -> None:
        keyExists = isinstance(self._params.get(key), float)    # Check if key exists in user's parameters
        if keyExists:
            self._params[key] = value
        else:
            raise ParameterKeyError(key)


    def setAllParameters(self, params: dict[Parameters, float]) -> None:
        for key in self._params:            # Loop through user's parameter dictonary
            value = params.get(key)         # Get value from sent dict, if it does not exist get() returns None
            keyExists = isinstance(value, float)
            if keyExists:                   # If the key did exist, set user's param to sent param
                self._params[key] = value
            else:
                raise ParameterKeyError(key)
