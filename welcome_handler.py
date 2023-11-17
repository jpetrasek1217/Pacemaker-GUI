import tkinter as tk
import GUI_helpers
import global_vars
import DCM_handler
import user_manager

_PAD_X = global_vars._PAD_X
_PAD_Y = global_vars._PAD_Y
_BUTTON_BG = global_vars._BUTTON_BG
_WELCOME_ENTRY_WIDTH = global_vars._WELCOME_ENTRY_WIDTH
_ENTRY_BG = global_vars._ENTRY_BG
_ENTRY_FG = global_vars._ENTRY_FG
_FONT_DEFAULT = global_vars._FONT_DEFAULT

root = global_vars.root

welcomeFrame = global_vars.welcomeFrame

DCMFrame = global_vars.DCMFrame
lowerDCMFrame = global_vars.lowerDCMFrame
middleDCMFrame = global_vars.middleDCMFrame
upperDCMFrame = global_vars.upperDCMFrame

def createAndShowWelcome():   
    welcomeLabel = tk.Label(welcomeFrame, text="Welcome!",  font=("Montserrat", 22, "bold"))
    promptLabel = tk.Label(welcomeFrame, text="Please login or create a new user", font=_FONT_DEFAULT)
    usernameLabel = tk.Label(welcomeFrame, text="Username", font=_FONT_DEFAULT)
    global usernameInput
    usernameInput = tk.Entry(welcomeFrame, width=_WELCOME_ENTRY_WIDTH, font=_FONT_DEFAULT, bg=_ENTRY_BG, fg=_ENTRY_FG)
    passwordLabel = tk.Label(welcomeFrame, text="Password", font=_FONT_DEFAULT)
    global passwordInput
    passwordInput = tk.Entry(welcomeFrame, width=_WELCOME_ENTRY_WIDTH, font=_FONT_DEFAULT, bg=_ENTRY_BG, fg=_ENTRY_FG, show="*")
    loginButton = tk.Button(welcomeFrame, text="Login", padx=_PAD_X, pady=_PAD_Y, bg=_BUTTON_BG, font=_FONT_DEFAULT, command=onLogin)
    createUserButton = tk.Button(welcomeFrame, text="Create New User", padx=_PAD_X, pady=_PAD_Y, bg=_BUTTON_BG, font=_FONT_DEFAULT, command= onRegisterUser) 
    welcomeFrame.grid(row=0, column=0, pady=25, padx=25, sticky="nsew")
    welcomeLabel.grid(pady=_PAD_Y, row=0,column=0, columnspan=2)
    promptLabel.grid(row=1, column=0, columnspan=2, pady=(_PAD_Y/2,_PAD_Y*2))
    usernameLabel.grid(pady=(_PAD_Y*2,_PAD_Y),row=2, column=0, columnspan=2)
    usernameInput.grid(row=3, column=0, padx=_PAD_X, pady=_PAD_Y, columnspan=2)
    passwordLabel.grid(pady=_PAD_Y,row=4, column=0, columnspan=2)
    passwordInput.grid(row=5, column=0, padx=_PAD_X, pady=(_PAD_Y,_PAD_Y*4), columnspan=2)
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


    DCM_handler.createAndShowDCM(user_manager.getPacingMode())

def onRegisterUser():
    isSuccessfulRegister, errorMsg = user_manager.registerUser(usernameInput.get(), passwordInput.get())
    if isSuccessfulRegister:
         GUI_helpers.throwSuccessPopup(f"Successfully Created New User \'{usernameInput.get().strip()}\'")
    else:
         GUI_helpers.throwErrorPopup(errorMsg)