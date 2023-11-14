import tkinter as tk
import global_vars
import GUI_helpers
import DCM_handler

_BUTTON_WIDTH = global_vars._BUTTON_WIDTH
_FONT_DEFAULT = global_vars._FONT_DEFAULT
_BUTTON_BG = global_vars._BUTTON_BG
_VERSION_NUMBER = global_vars._VERSION_NUMBER
_PAD_Y = global_vars._PAD_Y
_PAD_X = global_vars._PAD_X


root = global_vars.root

welcomeFrame = tk.Frame(root)

DCMFrame = global_vars.DCMFrame
lowerDCMFrame = global_vars.lowerDCMFrame
middleDCMFrame = global_vars.middleDCMFrame
upperDCMFrame = global_vars.upperDCMFrame

egramFrame = tk.Frame(root)

def openEgram():
    GUI_helpers.hideFrame(DCMFrame)
    egramFrame.grid(row=0, column=0, pady=25, padx=25, sticky="nsew")
    egramDCMButton = tk.Button(egramFrame, width=_BUTTON_WIDTH, text="DCM", font=_FONT_DEFAULT, bg=_BUTTON_BG, command=openDCM)
    egramDCMButton.grid(row=0, column=0)
    egramLogoutButton = tk.Button(egramFrame, width=_BUTTON_WIDTH, text="Logout", font=_FONT_DEFAULT, bg=_BUTTON_BG, command=DCM_handler.logout)
    egramLogoutButton.grid(row=1, column=0)
    institutionLabel = tk.Label(egramFrame, text="McMaster University", padx=_PAD_X*4, font=_FONT_DEFAULT)
    institutionLabel.grid(row=1, column=1, pady=(0,_PAD_Y))
    verNumLabel = tk.Label(egramFrame, text="Version " + _VERSION_NUMBER, padx=_PAD_X*4, font=_FONT_DEFAULT)
    verNumLabel.grid(row=0, column=1)
    egramLinkButton = tk.Button(egramFrame, width=_BUTTON_WIDTH, text="Link", font=_FONT_DEFAULT, pady=_PAD_Y*2, bg=_BUTTON_BG, command=link)
    egramLinkButton.grid(row=0, rowspan=2, column=2)
    egramSendDataButton = tk.Button(egramFrame, width=_BUTTON_WIDTH*2, text="Send Egram Data", pady=_PAD_Y, font=_FONT_DEFAULT, bg=_BUTTON_BG)
    egramSendDataButton.grid(row=2, columnspan=3, column=0,pady=(_PAD_Y*2,_PAD_Y))
    egramSendDataButton = tk.Button(egramFrame, width=_BUTTON_WIDTH*3, text="Recieve + Show Egram Data", pady=_PAD_Y, font=_FONT_DEFAULT, bg=_BUTTON_BG)
    egramSendDataButton.grid(row=3, columnspan=3, column=0,pady=_PAD_Y)


def openDCM():
    GUI_helpers.hideFrame(egramFrame)
    DCMFrame.grid(row=0, column=0, pady=25, padx=25, sticky="nsew")
    upperDCMFrame.grid(row=0,column=0)
    middleDCMFrame.grid(row=1,column=0)
    lowerDCMFrame.grid(row=2,column=0)

def link():
    return