import tkinter as tk
import global_vars
import user_manager
import egram_handler
import GUI_helpers
import welcome_handler

_PAD_X = global_vars._PAD_X
_PAD_Y = global_vars._PAD_Y
_BUTTON_BG = global_vars._BUTTON_BG
_BUTTON_WIDTH = global_vars._BUTTON_WIDTH
_VERSION_NUMBER = global_vars._VERSION_NUMBER
_DCM_ENTRY_WIDTH = global_vars._DCM_ENTRY_WIDTH
_FONT_DEFAULT = global_vars._FONT_DEFAULT
_MAX_ROW = 3
_MAX_COL = 4
_TKFONT_DEFAULT = global_vars._TKFONT_DEFAULT
_SELECTED_OPTION = global_vars._SELECTED_OPTION


root = global_vars.root

welcomeFrame = tk.Frame(root)

DCMFrame = global_vars.DCMFrame
lowerDCMFrame = global_vars.lowerDCMFrame
middleDCMFrame = global_vars.middleDCMFrame
upperDCMFrame = global_vars.upperDCMFrame

parameterEntryAndLabelList = global_vars.parameterEntryAndLabelList

def createAndShowDCM(mode):
    DCMFrame.grid(row=0, column=0, pady=25, padx=25, sticky="nsew")
    upperDCMFrame.grid(row=0,column=0)
    middleDCMFrame.grid(row=1,column=0)
    lowerDCMFrame.grid(row=2,column=0)

    global pacingModeButtonList
    pacingModeButtonList = []
    
    for pacingMode in user_manager.getAllPacingModes():
        pacingModeButton = tk.Button(lowerDCMFrame, text=pacingMode, padx=_PAD_X, pady=_PAD_Y, width=_BUTTON_WIDTH, bg=_BUTTON_BG, font=_FONT_DEFAULT, command= lambda pacingMode=pacingMode: updateParameters(pacingMode))
        pacingModeButtonList.append(pacingModeButton)
    currentPacingModeButton = 0
    for ro in range(2):
        for col in range(4):
            pacingModeButtonList[currentPacingModeButton].grid(row=ro, column=col)
            currentPacingModeButton += 1
    
    saveButton = tk.Button(global_vars.lowerDCMFrame, text="Save", padx=_PAD_X, pady=_PAD_Y, width=_BUTTON_WIDTH, bg=_BUTTON_BG, font=_FONT_DEFAULT, command=onSaveParameters)
    sendButton =  tk.Button(global_vars.lowerDCMFrame, text="Send", padx=_PAD_X, pady=_PAD_Y, width=_BUTTON_WIDTH, height=1, bg=_BUTTON_BG, font=_FONT_DEFAULT, command=egram_handler.openEgram)
    institutionLabel = tk.Label(lowerDCMFrame, text="McMaster University", font=_FONT_DEFAULT)
    
    saveButton.grid(row=0, column=4)
    sendButton.grid(row=1, column=4)
    institutionLabel.grid(row=2, column=1, columnspan=3, pady=_PAD_Y)
    updateParameters(mode)
    

def updateParameters(mode):
    user_manager.savePacingMode(mode)
    for widget in upperDCMFrame.winfo_children():
        widget.grid_forget()
    Title_Label = tk.Label(upperDCMFrame, text="Mode: " + mode, font=("Montserrat", 22, "bold"))
    verNumLabel = tk.Label(upperDCMFrame, text="Version " + _VERSION_NUMBER, font=_FONT_DEFAULT)
    logoutButton = tk.Button(upperDCMFrame, width=_BUTTON_WIDTH, text="Logout", font=_FONT_DEFAULT, bg=_BUTTON_BG, command=logout)
    Title_Label.grid(row=0,column=0, columnspan=1, padx=(0,_PAD_X*8), pady=_PAD_Y)
    verNumLabel.grid(row=0, column=1, columnspan=1)
    logoutButton.grid(row=0,column=2, columnspan=1, padx=(_PAD_X*8,0), pady=_PAD_Y)

    for widget in middleDCMFrame.winfo_children():
        widget.grid_forget()
    
    parameterEntryAndLabelList = []
    for parameter in user_manager.getAllSavedParametersAndVisibilityFromSavedPacingMode():
        paramName = parameter[0]
        paramTitle = parameter[1]
        paramValue = parameter[2]
        paramVisibility = parameter[3]

        entry = tk.Entry(middleDCMFrame, width=_DCM_ENTRY_WIDTH, font=_FONT_DEFAULT, bg=_BUTTON_BG, fg="black")
        entry.insert(0, paramValue)
        if not paramVisibility:
            entry.config(state="disabled")

        label = tk.Label(middleDCMFrame, text=paramTitle, font=_FONT_DEFAULT)
      
        parameterEntryAndLabelList.append([paramName, entry, label])
    row = 0
    col = 0
    for row in range(_MAX_ROW):
        for col in range(_MAX_COL):
            index = row * 4 + col
            if index >= len(parameterEntryAndLabelList):
                break
            parameterEntryAndLabelList[index][1].grid(row = 2*row + 1, column=col, padx=_PAD_X, pady=(_PAD_Y*3,_PAD_Y))
            parameterEntryAndLabelList[index][2].grid(row = 2*row + 2, column=col, padx=_PAD_X, pady=(_PAD_Y,_PAD_Y*3))
        else:
            continue    # only executed if the inner loop did NOT break
        break           # only executed if the inner loop DID break
    
    _SELECTED_OPTION.set(user_manager.getThresholdTitle())
    threshold_dropdown = tk.OptionMenu(middleDCMFrame, _SELECTED_OPTION, *user_manager.getThresholdTitles())
    threshold_dropdown.grid(row=_MAX_ROW*2-1, column=_MAX_COL-2, padx=_PAD_X, pady=(_PAD_Y*2,0))
    if user_manager.isThresholdVisible():
        threshold_dropdown.config(font=_FONT_DEFAULT,  width=_DCM_ENTRY_WIDTH-1, bg=_BUTTON_BG, fg="black")
    else:
        threshold_dropdown.config(font=_FONT_DEFAULT,  width=_DCM_ENTRY_WIDTH-1, bg=_BUTTON_BG, fg="black", state="disabled")
    threshold_label = tk.Label(middleDCMFrame, text="Threshold", font=_FONT_DEFAULT)
    threshold_label.grid(row=_MAX_ROW*2, column=_MAX_COL-2, padx=_PAD_X, pady=_PAD_Y)


def logout():
    user_manager.logoutUser()
    GUI_helpers.hideFrame(DCMFrame)
    GUI_helpers.hideFrame(egram_handler.egramFrame)
    welcome_handler.createAndShowWelcome()
    return

def onSaveParameters():
    for paramEntryAndLabel in global_vars.parameterEntryAndLabelList:
        paramName = paramEntryAndLabel[0]
        paramEntry = paramEntryAndLabel[1]
        isSuccessfulSave, errorMsg = user_manager.saveParameterValue(paramName, paramEntry.get())
        if not isSuccessfulSave:
            GUI_helpers.throwErrorPopup(errorMsg)
            return
    user_manager.setThresholdValueFromTitle(_SELECTED_OPTION.get())
    GUI_helpers.throwSuccessPopup("Successfully saved all parameters.")