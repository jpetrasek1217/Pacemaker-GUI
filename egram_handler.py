import tkinter as tk
import global_vars
import GUI_helpers
import DCM_handler
import user_manager
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np

_BUTTON_WIDTH = global_vars._BUTTON_WIDTH
_FONT_DEFAULT = global_vars._FONT_DEFAULT
_BUTTON_BG = global_vars._BUTTON_BG
_VERSION_NUMBER = global_vars._VERSION_NUMBER
_PAD_Y = global_vars._PAD_Y
_PAD_X = global_vars._PAD_X
_LINK_BG = "CadetBlue1"
_UNLINK_BG = "misty rose"
_FONT_DICT_DEFAULT = global_vars._FONT_DICT_DEFAULT

root = global_vars.root

welcomeFrame = global_vars.welcomeFrame

DCMFrame = global_vars.DCMFrame
lowerDCMFrame = global_vars.lowerDCMFrame
middleDCMFrame = global_vars.middleDCMFrame
upperDCMFrame = global_vars.upperDCMFrame
egramFrame = global_vars.egramFrame
plotFrame = global_vars.plotFrame

def openEgram():
    DCM_handler.onSaveParameters()
    GUI_helpers.hideFrame(DCMFrame)
    egramFrame.grid(row=0, column=0, pady=25, padx=25, sticky="nsew")
    upperEgramFrame = tk.Frame(egramFrame)
    upperEgramFrame.grid(row=0, column=0, sticky="nsew")
    egramDCMButton = tk.Button(upperEgramFrame, width=_BUTTON_WIDTH, text="DCM", font=_FONT_DEFAULT, bg=_BUTTON_BG, command=openDCM)
    egramDCMButton.grid(row=0, column=0)
    egramLogoutButton = tk.Button(upperEgramFrame, width=_BUTTON_WIDTH, text="Logout", font=_FONT_DEFAULT, bg=_BUTTON_BG, command=DCM_handler.logout)
    egramLogoutButton.grid(row=1, column=0)
    institutionLabel = tk.Label(upperEgramFrame, text="McMaster University", padx=_PAD_X*4, font=_FONT_DEFAULT)
    institutionLabel.grid(row=1, column=1, pady=(0,_PAD_Y))
    verNumLabel = tk.Label(upperEgramFrame, text="Version " + _VERSION_NUMBER, padx=_PAD_X*4, font=_FONT_DEFAULT)
    verNumLabel.grid(row=0, column=1)

    global egramLinkButton 
    egramLinkButton = tk.Button(upperEgramFrame, width=_BUTTON_WIDTH, text="Link", font=_FONT_DEFAULT, pady=_PAD_Y*2, bg=_LINK_BG, command=link)
    global egramUnlinkButton
    egramUnlinkButton = tk.Button(upperEgramFrame, width=_BUTTON_WIDTH, text="Unlink", font=_FONT_DEFAULT, pady=_PAD_Y*2, bg=_UNLINK_BG, command=unlink)
       
    global egramSendDataButton
    egramSendDataButton = tk.Button(upperEgramFrame, width=_BUTTON_WIDTH*2, text="Send Egram Data", pady=_PAD_Y, font=_FONT_DEFAULT, bg=_BUTTON_BG, command=egramSendData)
    egramSendDataButton.grid(row=2, columnspan=3, column=0,pady=(_PAD_Y*2,_PAD_Y))
    global egramRecieveDataButton
    egramRecieveDataButton = tk.Button(upperEgramFrame, width=_BUTTON_WIDTH*3, text="Recieve + Show Egram Data", pady=_PAD_Y, font=_FONT_DEFAULT, bg=_BUTTON_BG, command=egramRecieveData)
    egramRecieveDataButton.grid(row=3, columnspan=3, column=0,pady=_PAD_Y)
    
    if user_manager.connectToPacemaker()[0]:
        egramUnlinkButton.grid(row=0, rowspan=2, column=2)
    else:
        egramLinkButton.grid(row=0, rowspan=2, column=2)
        egramSendDataButton.config(state="disabled")
        egramRecieveDataButton.config(state="disabled")

def link():
    isSuccessfullLink, errorMsg = user_manager.connectToPacemaker()
    if isSuccessfullLink:
        egramLinkButton.grid_forget()
        egramUnlinkButton.grid(row=0, rowspan=2, column=2)
        GUI_helpers.throwSuccessPopup("Successfully Connected!")
        egramSendDataButton.config(state="normal")
        egramRecieveDataButton.config(state="normal")
    else:
         GUI_helpers.throwErrorPopup(errorMsg)


def unlink():
    isSuccessfulUnlink, errorMsg = user_manager.disconnectFromPacemaker()
    if isSuccessfulUnlink:
        egramUnlinkButton.grid_forget()
        egramLinkButton.grid(row=0, rowspan=2, column=2)
        egramSendDataButton.config(state="disabled")
        egramRecieveDataButton.config(state="disabled")
        GUI_helpers.throwSuccessPopup("Successfully Disconnected!")
    else:
         GUI_helpers.throwErrorPopup(errorMsg)


def openDCM():
    GUI_helpers.hideFrame(egramFrame)
    DCMFrame.grid(row=0, column=0, pady=25, padx=25, sticky="nsew")
    upperDCMFrame.grid(row=0,column=0)
    middleDCMFrame.grid(row=1,column=0)
    lowerDCMFrame.grid(row=2,column=0)

def egramSendData():
    user_manager.sendParameterDataToPacemaker()

def egramRecieveData():
    fig, ax = plt.subplots()

    plotCanvas = FigureCanvasTkAgg(fig, plotFrame)
    plotToolbar = NavigationToolbar2Tk(plotCanvas, plotFrame, pack_toolbar=False)
    ax.clear()

    plotFrame.grid(row=4,column=0)
    plotCanvas.get_tk_widget().grid(row=1, column=0, columnspan=3, pady=_PAD_Y)
    ax.set_title(f"Display from Pacing Mode {user_manager.getPacingMode()}", font=_FONT_DICT_DEFAULT)
    ax.set_xlabel('Time [s]', font=_FONT_DICT_DEFAULT)
    ax.set_ylabel('Voltage [mV]', font=_FONT_DICT_DEFAULT)
    x = np.random.randint(0,100,10)
    y = np.random.randint(0,100,10)
    ax.plot(x,y)
    ax.set_xlim(0, max(x))
    ax.set_ylim(0, max(y))
    plotCanvas.draw()
    plotToolbar.update()
    plotToolbar.grid(row=2, column=0, sticky="w")
    plt.close(fig)
