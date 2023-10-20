import tkinter as tk
import user_manager 
import GUI_helpers

# Constants
_VERSION_NUMBER = "1.0.7"
_ICON_BITMAP_FILEPATH = "assets/pacemaker_icon.ico"
_WINDOW_TITLE = "Pacemaker Device Controller Monitor " + _VERSION_NUMBER

root = tk.Tk()
root.title(_WINDOW_TITLE)
root.minsize(width=100, height=200)
root.iconbitmap(_ICON_BITMAP_FILEPATH)

Welcome_Frame = tk.Frame(root)

DCM_Frame = tk.Frame(root)
Lower_DCM_Frame = tk.Frame(DCM_Frame)
Upper_DCM_Frame = tk.Frame(DCM_Frame)


# parameterEntryAndLabelList is made up of sublists: [paramName: str, paramEntry: tk.Entry, paramLabel: tk.Label]
parameterEntryAndLabelList = []


def Logout():
    user_manager.logoutUser()
    for widget in DCM_Frame.winfo_children():
        widget.grid_forget()
    DCM_Frame.grid_forget()

    Welcome_Frame.grid(row=0, column=0, pady=25, padx=25, sticky="nsew")
    Welcome_Label.grid(pady=10, row=0,column=0, columnspan=2)
    Prompt_Label.grid(row=1, column=0, columnspan=2, pady=10)
    Username_Label.grid(pady=10,row=2, column=0, columnspan=2)
    Username_input.grid(row=3, column=0, padx=10, pady=10, columnspan=2)
    Password_Label.grid(pady=10,row=4, column=0, columnspan=2)
    Password_input.grid(row=5, column=0, padx=10, pady=20, columnspan=2)
    Login_button.grid(row=6, column=0, padx=10, pady=10)
    CreateUser_button.grid(row=6, column=1, padx=10, pady=10)
    return
    

def Change_Parameters(mode):
    user_manager.savePacingMode(mode)
    for widget in Upper_DCM_Frame.winfo_children():
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


def createAllDCMItems(mode):
    global parameterEntryAndLabelList
    parameterEntryAndLabelList = []
    for parameter in user_manager.getAllSavedParametersAndVisibilityFromSavedPacingMode():
        paramName = parameter[0]
        paramTitle = parameter[1]
        paramValue = parameter[2]
        paramVisibility = parameter[3]

        entry = tk.Entry(Upper_DCM_Frame, width=10, bg="white", fg="black")
        entry.insert(0, paramValue)
        if not paramVisibility:
            entry.config(state="disabled")

        label = tk.Label(Upper_DCM_Frame, text=paramTitle)
      
        parameterEntryAndLabelList.append([paramName, entry, label])
    
    DCM_Frame.grid(row=0, column=0, pady=25, padx=25, sticky="nsew")
    Upper_DCM_Frame.grid(row=0,column=0)
    Title_Label = tk.Label(Upper_DCM_Frame, text="Mode: " + mode, font=("Montserrat", 14, "bold"))
    Title_Label.grid(row=0,column=0, columnspan=5, padx=10, pady=10, sticky="w")
    logout_button.grid(row=0,column=4, columnspan=1, padx=10, pady=10)
    Ver_Num_Label.grid(row=0, column=2)
    
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
            

def on_Login():
    isSuccessfulLogin, errorMsg = user_manager.loginUser(Username_input.get(), Password_input.get())
    if not isSuccessfulLogin:
         GUI_helpers.throwErrorPopup(errorMsg)
         return
    for widget in Welcome_Frame.winfo_children():
        widget.grid_forget()
    Welcome_Frame.grid_forget()

    DCM_Frame.grid(row=0, column=0, pady=25, padx=25, sticky="nsew")
    Upper_DCM_Frame.grid(row=0,column=0)
    Lower_DCM_Frame.grid(row=1,column=0)

    Save_Button.grid(row=0, column=4, rowspan=2)
    Ver_Num_Label.grid(row=0, column=2)
    logout_button.grid(row=0,column=4, columnspan=1, padx=10, pady=10)

    AOO_Button.grid(row=1, column=0)
    AAI_Button.grid(row=0, column=0)
    VOO_Button.grid(row=1, column=1)
    VVI_Button.grid(row=0, column=1)
    AOOR_Button.grid(row=1, column=2)
    AAIR_Button.grid(row=0, column=2)
    VOOR_Button.grid(row=1, column=3)
    VVIR_Button.grid(row=0, column=3)
    Send_Button.grid(row=2, column=0)
    Institution_Label.grid(row=2, column=1, columnspan=3, pady=(10,0))

    createAllDCMItems(user_manager.getPacingMode())


def Start():
    Welcome_Frame.grid(row=0, column=0, pady=25, padx=25)
    Welcome_Label.grid(pady=(10,0), row=0,column=0, columnspan=2)
    Prompt_Label.grid(row=1, column=0, columnspan=2, pady=(0,10))
    Username_Label.grid(pady=(10,5),row=2, column=0, columnspan=2)
    Username_input.grid(row=3, column=0, padx=(5,10), pady=0, columnspan=2)
    Password_Label.grid(pady=(10,5),row=4, column=0, columnspan=2)
    Password_input.grid(row=5, column=0, padx=10, pady=(5,30), columnspan=2)
    Login_button.grid(row=6, column=0, padx=10, pady=0)
    CreateUser_button.grid(row=6, column=1, padx=10, pady=0)
    return

def on_registerUser():
    isSuccessfulRegister, errorMsg = user_manager.registerUser(Username_input.get(), Password_input.get())
    if isSuccessfulRegister:
         GUI_helpers.throwSuccessPopup(f"Successfully Created New User \'{Username_input.get().strip()}\'")
    else:
         GUI_helpers.throwErrorPopup(errorMsg)

EgramSend = tk.Frame(root)

def OpenEgram():
    for widget in Welcome_Frame.winfo_children():
        widget.grid_forget()
    Welcome_Frame.grid_forget()
    
    


# Welcome Frame
Welcome_Label = tk.Label(Welcome_Frame, text="Welcome!",  font=("Montserrat", 16, "bold"))
Prompt_Label = tk.Label(Welcome_Frame, text="Please login or create a new user")
Username_Label = tk.Label(Welcome_Frame, text="Username")
Username_input = tk.Entry(Welcome_Frame, width=20, bg="white", fg="black")
Password_Label = tk.Label(Welcome_Frame, text="Password")
Password_input = tk.Entry(Welcome_Frame, width=20, bg="white", fg="black", show="*")
Login_button = tk.Button(Welcome_Frame, text="Login", padx=10, pady=5, bg="white", command=on_Login)
CreateUser_button = tk.Button(Welcome_Frame, text="Create New User", padx=10, pady=5, bg="white", command= on_registerUser)


# DCM Frame
Save_Button = tk.Button(Lower_DCM_Frame, text="Save", width=10, height=4, bg="white", command=onSaveParameters)
Ver_Num_Label = tk.Label(Upper_DCM_Frame, text="Version " + _VERSION_NUMBER)
logout_button = tk.Button(Upper_DCM_Frame, text="Logout", bg="white", command=Logout)
Institution_Label = tk.Label(Lower_DCM_Frame, text="McMaster University")

AOO_Button = tk.Button(Lower_DCM_Frame, text="AOO", padx=10, pady=5, width=8, height=1, bg="white", command= lambda: Change_Parameters("AOO"))
AAI_Button = tk.Button(Lower_DCM_Frame, text="AAI", padx=10, pady=5, width=8, height=1, bg="white", command= lambda: Change_Parameters("AAI"))
VOO_Button = tk.Button(Lower_DCM_Frame, text="VOO", padx=10, pady=5, width=8, height=1, bg="white", command= lambda: Change_Parameters("VOO"))
VVI_Button = tk.Button(Lower_DCM_Frame, text="VVI", padx=10, pady=5, width=8, height=1, bg="white", command= lambda: Change_Parameters("VVI"))
AOOR_Button = tk.Button(Lower_DCM_Frame, text="AOOR", padx=10, pady=5, width=8, height=1, bg="white", command= lambda: Change_Parameters("AOOR"))
AAIR_Button = tk.Button(Lower_DCM_Frame, text="AAIR", padx=10, pady=5, width=8, height=1, bg="white", command= lambda: Change_Parameters("AAIR"))
VOOR_Button = tk.Button(Lower_DCM_Frame, text="VOOR", padx=10, pady=5, width=8, height=1, bg="white", command= lambda: Change_Parameters("VOOR"))
VVIR_Button = tk.Button(Lower_DCM_Frame, text="VVIR", padx=10, pady=5, width=8, height=1, bg="white", command= lambda: Change_Parameters("VVIR"))

Send_Button =  tk.Button(Lower_DCM_Frame, text="Send", padx=10, pady=5, width=8, height=1, bg="white", command= lambda: EgramSend.grid(row=0, column=0, pady=25, padx=25, sticky="nsew"))

Start()

root.mainloop()