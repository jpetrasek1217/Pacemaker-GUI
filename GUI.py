import tkinter as tk
import user_manager 
import GUI_helpers

# Constants
_VERSION_NUMBER = "1.0.7"
_ICON_BITMAP_FILEPATH = "assets/pacemaker_icon.ico"
_WINDOW_TITLE = "Pacemaker Device Controller Monitor " + _VERSION_NUMBER
_PAD_X = 10
_PAD_Y = 5
_BUTTON_WIDTH = 8
_BUTTON_BG = "white"
_ENTRY_WIDTH = 20
_ENTRY_BG = "white"
_ENTRY_FG = "black"

root = tk.Tk()
root.title(_WINDOW_TITLE)
root.minsize(width=100, height=200)
root.iconbitmap(_ICON_BITMAP_FILEPATH)

welcomeFrame = tk.Frame(root)

DCMFrame = tk.Frame(root)
lowerDCMFrame = tk.Frame(DCMFrame)
middleDCMFrame = tk.Frame(DCMFrame)
upperDCMFrame = tk.Frame(DCMFrame)


# parameterEntryAndLabelList is made up of sublists: [paramName: str, paramEntry: tk.Entry, paramLabel: tk.Label]
parameterEntryAndLabelList = []


def Start():
    createAndShowWelcome()
    return

def createAndShowWelcome():   
    welcomeLabel = tk.Label(welcomeFrame, text="Welcome!",  font=("Montserrat", 16, "bold"))
    promptLabel = tk.Label(welcomeFrame, text="Please login or create a new user")
    usernameLabel = tk.Label(welcomeFrame, text="Username")
    global usernameInput 
    usernameInput = tk.Entry(welcomeFrame, width=_ENTRY_WIDTH, bg=_ENTRY_BG, fg=_ENTRY_FG)
    passwordLabel = tk.Label(welcomeFrame, text="Password")
    global passwordInput 
    passwordInput = tk.Entry(welcomeFrame, width=_ENTRY_WIDTH, bg=_ENTRY_BG, fg=_ENTRY_FG, show="*")
    loginButton = tk.Button(welcomeFrame, text="Login", padx=_PAD_X, pady=_PAD_Y, bg=_BUTTON_BG, command=onLogin)
    createUserButton = tk.Button(welcomeFrame, text="Create New User", padx=_PAD_X, pady=_PAD_Y, bg=_BUTTON_BG, command= onRegisterUser) 
    welcomeFrame.grid(row=0, column=0, pady=25, padx=25, sticky="nsew")
    welcomeLabel.grid(pady=_PAD_Y, row=0,column=0, columnspan=2)
    promptLabel.grid(row=1, column=0, columnspan=2, pady=_PAD_Y)
    usernameLabel.grid(pady=_PAD_Y,row=2, column=0, columnspan=2)
    usernameInput.grid(row=3, column=0, padx=_PAD_X, pady=_PAD_Y, columnspan=2)
    passwordLabel.grid(pady=_PAD_Y,row=4, column=0, columnspan=2)
    passwordInput.grid(row=5, column=0, padx=_PAD_X, pady=_PAD_Y, columnspan=2)
    loginButton.grid(row=6, column=0, padx=_PAD_X, pady=_PAD_Y)
    createUserButton.grid(row=6, column=1, padx=_PAD_X, pady=_PAD_Y)

def onLogin():
    isSuccessfulLogin, errorMsg = user_manager.loginUser(usernameInput.get(), passwordInput.get())
    if not isSuccessfulLogin:
         GUI_helpers.throwErrorPopup(errorMsg)
         return
    for widget in welcomeFrame.winfo_children():
        widget.grid_forget()
    welcomeFrame.grid_forget()

    DCMFrame.grid(row=0, column=0, pady=25, padx=25, sticky="nsew")
    upperDCMFrame.grid(row=0,column=0)
    middleDCMFrame.grid(row=1,column=0)
    lowerDCMFrame.grid(row=2,column=0)


    createAndShowDCM(user_manager.getPacingMode())

def createAndShowDCM(mode):
    verNumLabel = tk.Label(upperDCMFrame, text="Version " + _VERSION_NUMBER)
    logoutButton = tk.Button(upperDCMFrame, width=_BUTTON_WIDTH, text="Logout", bg="white", command=Logout)

    updateParameters(mode)

    global pacingModeButtonList
    pacingModeButtonList = []
    for pacingMode in user_manager.getAllPacingModes():
        pacingModeButton = tk.Button(lowerDCMFrame, text=pacingMode, padx=_PAD_X, pady=_PAD_Y, width=_BUTTON_WIDTH, bg=_BUTTON_BG, command= lambda: updateParameters(pacingMode))
        pacingModeButtonList.append(pacingModeButton)
    currentPacingModeButton = 0
    for ro in range(2):
        for col in range(4):
            pacingModeButtonList[currentPacingModeButton].grid(row=ro, column=col)
            currentPacingModeButton += 1
    saveButton = tk.Button(lowerDCMFrame, text="Save", width=_BUTTON_WIDTH, height=4, bg="white", command=onSaveParameters)
    sendButton =  tk.Button(lowerDCMFrame, text="Send", padx=_PAD_X, pady=_PAD_Y, width=_BUTTON_WIDTH, height=1, bg="white", command= OpenEgram())
    institutionLabel = tk.Label(lowerDCMFrame, text="McMaster University")
    
    DCMFrame.grid(row=0, column=0, pady=25, padx=25, sticky="nsew")
    upperDCMFrame.grid(row=0,column=0)
    middleDCMFrame.grid(row=1,column=0)
    lowerDCMFrame.grid(row=2,column=0)

    verNumLabel.grid(row=0, column=2)
    logoutButton.grid(row=0,column=4, columnspan=1, padx=_PAD_X, pady=_PAD_Y)
    
    saveButton.grid(row=0, column=4, rowspan=2)
    sendButton.grid(row=3, column=0)
    institutionLabel.grid(row=2, column=1, columnspan=3, pady=_PAD_Y)


            
def updateParameters(mode):
    user_manager.savePacingMode(mode)
    hideFrame(middleDCMFrame)
    Title_Label = tk.Label(upperDCMFrame, text="Mode: " + mode, font=("Montserrat", 14, "bold"))
    Title_Label.grid(row=0,column=0, columnspan=5, padx=10, pady=10, sticky="w")
    parameterEntryAndLabelList = []
    for parameter in user_manager.getAllSavedParametersAndVisibilityFromSavedPacingMode():
        paramName = parameter[0]
        paramTitle = parameter[1]
        paramValue = parameter[2]
        paramVisibility = parameter[3]

        entry = tk.Entry(middleDCMFrame, width=10, bg="white", fg="black")
        entry.insert(0, paramValue)
        if not paramVisibility:
            entry.config(state="disabled")

        label = tk.Label(middleDCMFrame, text=paramTitle)
      
        parameterEntryAndLabelList.append([paramName, entry, label])

    for row in range(2):
        for col in range(5):
            index = row * 5 + col
            if index >= len(parameterEntryAndLabelList):
                break
            parameterEntryAndLabelList[index][1].grid(row = 2*row + 1, column=col, padx=10, pady=(15,5))
            parameterEntryAndLabelList[index][2].grid(row = 2*row + 2, column=col, padx=10, pady=(5,15))
        else:
            continue    # only executed if the inner loop did NOT break
        break           # only executed if the inner loop DID break


def Logout():
    user_manager.logoutUser()
    hideFrame(DCMFrame)
    createAndShowWelcome()
    return
    
def hideFrame(frame):
    for widget in frame.winfo_children():
        widget.grid_forget()
    frame.grid_forget()

def onSaveParameters():
    for paramEntryAndLabel in parameterEntryAndLabelList:
        paramName = paramEntryAndLabel[0]
        paramEntry = paramEntryAndLabel[1]

        isSuccessfulSave, errorMsg = user_manager.saveParameterValue(paramName, paramEntry.get())
        if not isSuccessfulSave:
            GUI_helpers.throwErrorPopup(errorMsg)
            return
    GUI_helpers.throwSuccessPopup("Successfully saved all parameters.")

def onRegisterUser():
    isSuccessfulRegister, errorMsg = user_manager.registerUser(usernameInput.get(), passwordInput.get())
    if isSuccessfulRegister:
         GUI_helpers.throwSuccessPopup(f"Successfully Created New User \'{usernameInput.get().strip()}\'")
    else:
         GUI_helpers.throwErrorPopup(errorMsg)

egramSend = tk.Frame(root)

def OpenEgram():
    for widget in welcomeFrame.winfo_children():
        widget.grid_forget()
    welcomeFrame.grid_forget()


Start()

root.mainloop()