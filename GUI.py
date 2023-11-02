import tkinter as tk
import user_manager 
import GUI_helpers

# Constants
_VERSION_NUMBER = "1.0.7"
_ICON_BITMAP_FILEPATH = "assets/pacemaker_icon.ico"
_WINDOW_TITLE = "Pacemaker Device Controller Monitor " + _VERSION_NUMBER
_PAD_X = 10

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


def createAndShowWelcome():   
    welcomeLabel = tk.Label(welcomeFrame, text="Welcome!",  font=("Montserrat", 16, "bold"))
    promptLabel = tk.Label(welcomeFrame, text="Please login or create a new user")
    usernameLabel = tk.Label(welcomeFrame, text="Username")
    usernameInput = tk.Entry(welcomeFrame, width=20, bg="white", fg="black")
    passwordLabel = tk.Label(welcomeFrame, text="Password")
    passwordInput = tk.Entry(welcomeFrame, width=20, bg="white", fg="black", show="*")
    loginButton = tk.Button(welcomeFrame, text="Login", padx=_PAD_X, pady=5, bg="white", command=on_Login)
    createUserButton = tk.Button(welcomeFrame, text="Create New User", padx=10, pady=5, bg="white", command= on_registerUser) 

    welcomeFrame.grid(row=0, column=0, pady=25, padx=25, sticky="nsew")
    welcomeLabel.grid(pady=10, row=0,column=0, columnspan=2)
    promptLabel.grid(row=1, column=0, columnspan=2, pady=10)
    usernameLabel.grid(pady=10,row=2, column=0, columnspan=2)
    usernameInput.grid(row=3, column=0, padx=10, pady=10, columnspan=2)
    passwordLabel.grid(pady=10,row=4, column=0, columnspan=2)
    passwordInput.grid(row=5, column=0, padx=10, pady=20, columnspan=2)
    loginButton.grid(row=6, column=0, padx=10, pady=10)
    createUserButton.grid(row=6, column=1, padx=10, pady=10)

def createAndShowDCM(mode):
    saveButton = tk.Button(lowerDCMFrame, text="Save", width=10, height=4, bg="white", command=onSaveParameters)
    verNumLabel = tk.Label(upperDCMFrame, text="Version " + _VERSION_NUMBER)
    logoutButton = tk.Button(upperDCMFrame, text="Logout", bg="white", command=Logout)
    institutionLabel = tk.Label(lowerDCMFrame, text="McMaster University")

    for pacingMode in user_manager.getAllPacingModes():
        pacingModeButton = tk.Button(lowerDCMFrame, text=pacingMode, padx=_PAD_X, pady=_PAD_Y, width=_BUTTON_WIDTH, bg=_BUTTON_BG, command= lambda: Change_Parameters(pacingMode))

    sendButton =  tk.Button(lowerDCMFrame, text="Send", padx=10, pady=5, width=8, height=1, bg="white", command= lambda: EgramSend.grid(row=0, column=0, pady=25, padx=25, sticky="nsew"))
    
    DCMFrame.grid(row=0, column=0, pady=25, padx=25, sticky="nsew")
    upperDCMFrame.grid(row=0,column=0)
    middleDCMFrame.grid(row=1,column=0)
    lowerDCMFrame.grid(row=1,column=0)
    logoutButton.grid(row=0,column=4, columnspan=1, padx=10, pady=10)
    verNumLabel.grid(row=0, column=2)


            
def updateParameters(mode):
    Title_Label = tk.Label(upperDCMFrame, text="Mode: " + mode, font=("Montserrat", 14, "bold"))
    Title_Label.grid(row=0,column=0, columnspan=5, padx=10, pady=10, sticky="w")
    parameterEntryAndLabelList = []
    for parameter in user_manager.getAllSavedParametersAndVisibilityFromSavedPacingMode():
        paramName = parameter[0]
        paramTitle = parameter[1]
        paramValue = parameter[2]
        paramVisibility = parameter[3]

        entry = tk.Entry(upperDCMFrame, width=10, bg="white", fg="black")
        entry.insert(0, paramValue)
        if not paramVisibility:
            entry.config(state="disabled")

        label = tk.Label(upperDCMFrame, text=paramTitle)
      
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
    showWelcome()
    return
    
def hideFrame(frame):
    for widget in frame.winfo_children():
        widget.grid_forget()
    frame.grid_forget()

def Change_Parameters(mode):
    user_manager.savePacingMode(mode)
    for widget in upperDCMFrame.winfo_children():
        widget.grid_forget()
    createAllDCMItems(mode)

def onSaveParameters():
    for paramEntryAndLabel in parameterEntryAndLabelList:
        paramName = paramEntryAndLabel[0]
        paramEntry = paramEntryAndLabel[1]

        isSuccessfulSave, errorMsg = user_manager.saveParameterValue(paramName, paramEntry.get())
        if not isSuccessfulSave:
            GUI_helpers.throwErrorPopup(errorMsg)
            return
    GUI_helpers.throwSuccessPopup("Successfully saved all parameters.")



def on_Login():
    isSuccessfulLogin, errorMsg = user_manager.loginUser(Username_input.get(), Password_input.get())
    if not isSuccessfulLogin:
         GUI_helpers.throwErrorPopup(errorMsg)
         return
    for widget in welcomeFrame.winfo_children():
        widget.grid_forget()
    welcomeFrame.grid_forget()

    DCMFrame.grid(row=0, column=0, pady=25, padx=25, sticky="nsew")
    upperDCMFrame.grid(row=0,column=0)
    lowerDCMFrame.grid(row=1,column=0)

    saveButton.grid(row=0, column=4, rowspan=2)
    verNumLabel.grid(row=0, column=2)
    logoutButton.grid(row=0,column=4, columnspan=1, padx=10, pady=10)

    AOOButton.grid(row=1, column=0)
    AAIButton.grid(row=0, column=0)
    VOOButton.grid(row=1, column=1)
    VVIButton.grid(row=0, column=1)
    AOORButton.grid(row=1, column=2)
    AAIRButton.grid(row=0, column=2)
    VOORButton.grid(row=1, column=3)
    VVIRButton.grid(row=0, column=3)
    sendButton.grid(row=2, column=0)
    institutionLabel.grid(row=2, column=1, columnspan=3, pady=(10,0))

    createAllDCMItems(user_manager.getPacingMode())


def Start():
    showWelcome()
    return

def on_registerUser():
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
    
    


# Welcome Frame



# DCM Frame


Start()

root.mainloop()