import tkinter as tk
import user_manager 
import GUI_helpers

_VERSION_NUMBER = "1.0.3"
root = tk.Tk()
root.title= "Title"
root.iconbitmap=("#")
root.minsize(width=100, height=200)

Welcome_Frame = tk.Frame(root)

DCM_Frame = tk.Frame(root)
Lower_DCM_Frame = tk.Frame(DCM_Frame)
Upper_DCM_Frame = tk.Frame(DCM_Frame)


# parameterEntryAndLabelList consists of sublists: [paramName, paramEntry, paramLabel]
parameterEntryAndLabelList = []


"""
def placeRequiredParameters():
    for num in range(5):
        Mode_input = Entry(frame_stats, width=10, bg="white", fg="blue")
        Mode_input.grid(row=3, column=0, columnspan=1, padx=10, pady=0)
        Mode_Label = Label(frame_stats, text="ARP").grid(pady=(10,25),row=4, column=0)

placeRequiredParameters()

button_PARAMETERS = Button(frame_parameters, text="TEST", padx=10, pady=5)

#button_MODE.grid(row=2, column=0)

"""



def SetInputState(param_list, set_state: str):
    for widget in param_list:
        widget.config(state=set_state)
    return


def Amnesia(param_list):
    for widget in param_list:
        widget.grid_forget()
    return


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
    #DCM_Frame.grid_forget()
    createAllDCMItems(mode)

    '''
    SetInputState(input_list, "normal")
    if mode == "AAIR" or mode == "AOOR" or mode == "VVIR" or mode == "VOOR":
        SetInputState(input_list, "disabled")
        return
    
    Title_Label = tk.Label(Upper_DCM_Frame, text="You are using Parameter " + mode + "  ")
    Title_Label.grid(row=0,column=0, columnspan=5, padx=10, pady=10, sticky="w")

    if mode=="AOO":
        Amnesia(V_only)
        AA_input.grid(row=1, column=2, columnspan=1, padx=10, pady=10)
        AA_Label.grid(row=2, column=2, columnspan=1, padx=10, pady=10)
        APW_input.grid(row=1, column=3, columnspan=1, padx=10, pady=10)
        APW_Label.grid(row=2, column=3, columnspan=1, padx=10, pady=10)
        AS_input.grid(row=3, column=0, columnspan=1, padx=10, pady=10)
        AS_Label.grid(row=4, column=0, columnspan=1, padx=10, pady=10)
        ARP_input.grid(row=3, column=1, columnspan=1, padx=10, pady=0)
        ARP_Label.grid(row=4, column=1, columnspan=1, padx=10, pady=0)
        RS_input.config(state="disabled")
        AS_input.config(state="disabled")
        MSR_input.config(state="disabled")
        ARP_input.config(state="disabled")
        PVARP_input.config(state="disabled")
        H_input.config(state="disabled")
        RS_input.config(state="disabled")
    elif mode=="AAI":
        Amnesia(V_only)
        AA_input.grid(row=1, column=2, columnspan=1, padx=10, pady=10)
        AA_Label.grid(row=2, column=2, columnspan=1, padx=10, pady=10)
        APW_input.grid(row=1, column=3, columnspan=1, padx=10, pady=10)
        APW_Label.grid(row=2, column=3, columnspan=1, padx=10, pady=10)
        AS_input.grid(row=3, column=0, columnspan=1, padx=10, pady=10)
        AS_Label.grid(row=4, column=0, columnspan=1, padx=10, pady=10)
        ARP_input.grid(row=3, column=1, columnspan=1, padx=10, pady=0)
        ARP_Label.grid(row=4, column=1, columnspan=1, padx=10, pady=0)
        MSR_input.config(state="disabled")
        VRP_input.config(state="disabled")
    elif mode=="VOO":
        Amnesia(A_only)
        VA_input.grid(row=1, column=2, columnspan=1, padx=10, pady=10)
        VA_Label.grid(row=2, column=2, columnspan=1, padx=10, pady=10)
        VPW_input.grid(row=1, column=3, columnspan=1, padx=10, pady=10)
        VPW_Label.grid(row=2, column=3, columnspan=1, padx=10, pady=10)
        VS_input.grid(row=3, column=0, columnspan=1, padx=10, pady=10)
        VS_Label.grid(row=4, column=0, columnspan=1, padx=10, pady=10)
        VRP_input.grid(row=3, column=1, columnspan=1, padx=10, pady=0)
        VRP_Label.grid(row=4, column=1, columnspan=1, padx=10, pady=0)
        VS_input.config(state="disabled")
        MSR_input.config(state="disabled")
        VRP_input.config(state="disabled")
        ARP_input.config(state="disabled")
        PVARP_input.config(state="disabled")
        H_input.config(state="disabled")
        RS_input.config(state="disabled")
    elif mode=="VVI":
        Amnesia(A_only)
        VA_input.grid(row=1, column=2, columnspan=1, padx=10, pady=10)
        VA_Label.grid(row=2, column=2, columnspan=1, padx=10, pady=10)
        VPW_input.grid(row=1, column=3, columnspan=1, padx=10, pady=10)
        VPW_Label.grid(row=2, column=3, columnspan=1, padx=10, pady=10)
        VS_input.grid(row=3, column=0, columnspan=1, padx=10, pady=10)
        VS_Label.grid(row=4, column=0, columnspan=1, padx=10, pady=10)
        VRP_input.grid(row=3, column=1, columnspan=1, padx=10, pady=0)
        VRP_Label.grid(row=4, column=1, columnspan=1, padx=10, pady=0)
        MSR_input.config(state="disabled")
        PVARP_input.config(state="disabled")
     '''


def onSaveParameters():
    for paramEntryAndLabel in parameterEntryAndLabelList:
        paramName = paramEntryAndLabel[0]
        paramEntry = paramEntryAndLabel[1]

        isSuccessfulSave, errorMsg = user_manager.saveParameterValue(paramName, paramEntry.get())
        if not isSuccessfulSave:
            GUI_helpers.throwErrorPopup(errorMsg)
            return


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
    Institution_Label.grid(row=2, column=1, columnspan=3, pady=(10,0))
    
    """
    LRL_input.grid(row=1, column=0, columnspan=1, padx=10, pady=10)
    LRL_Label.grid(row=2, column=0, columnspan=1, padx=10, pady=10)
    URL_input.grid(row=1, column=1, columnspan=1, padx=10, pady=10)
    URL_Label.grid(row=2, column=1, columnspan=1, padx=10, pady=10)
    AA_input.grid(row=1, column=2, columnspan=1, padx=10, pady=10)
    AA_Label.grid(row=2, column=2, columnspan=1, padx=10, pady=10)
    APW_input.grid(row=1, column=3, columnspan=1, padx=10, pady=10)
    APW_Label.grid(row=2, column=3, columnspan=1, padx=10, pady=10)
    MSR_input.grid(row=1, column=4, columnspan=1, padx=10, pady=10)
    MSR_Label.grid(row=2, column=4, columnspan=1, padx=10, pady=10)
    AS_input.grid(row=3, column=0, columnspan=1, padx=10, pady=10)
    AS_Label.grid(row=4, column=0, columnspan=1, padx=10, pady=10)
    ARP_input.grid(row=3, column=1, columnspan=1, padx=10, pady=0)
    ARP_Label.grid(row=4, column=1, columnspan=1, padx=10, pady=0)
    PVARP_input.grid(row=3, column=2, columnspan=1, padx=10, pady=0)
    PVARP_Label.grid(row=4, column=2, columnspan=1, padx=10, pady=0)
    H_Label.grid(row=4, column=3, columnspan=1, padx=10, pady=0)
    H_input.grid(row=3, column=3, columnspan=1, padx=10, pady=0)
    RS_input.grid(row=3, column=4, columnspan=1, padx=10, pady=0)
    RS_Label.grid(row=4, column=4, columnspan=1, padx=10, pady=0)
    """

    createAllDCMItems(user_manager.getPacingMode())

    

    #Change_Parameters("AOO")

    # VA_input.grid(row=0, column=3, columnspan=1, padx=10, pady=10)
    # VA_Label.grid(row=1, column=3, columnspan=1, padx=10, pady=10)
    # VPW_input.grid(row=0, column=4, columnspan=1, padx=10, pady=10)
    # VPW_Label.grid(row=1, column=4, columnspan=1, padx=10, pady=10)
    # AS_input.grid(row=2, column=0, columnspan=1, padx=10, pady=10)
    # AS_Label.grid(row=3, column=0, columnspan=1, padx=10, pady=10)
    # ARP_input.grid(row=2, column=1, columnspan=1, padx=10, pady=0)
    # ARP_Label.grid(row=3, column=1, columnspan=1, padx=10, pady=0)
    # PVARP_input.grid(row=2, column=1, columnspan=1, padx=10, pady=0)
    # PVARP_Label.grid(row=3, column=1, columnspan=1, padx=10, pady=0)
    # H_Label.grid(row=3, column=2, columnspan=1, padx=10, pady=0)
    # H_input.grid(row=2, column=2, columnspan=1, padx=10, pady=0)
    # RS_input.grid(row=2, column=3, columnspan=1, padx=10, pady=0)
    # RS_Label.grid(row=3, column=3, columnspan=1, padx=10, pady=0)
    # MSR_input.grid(row=2, column=4, columnspan=1, padx=10, pady=0)
    # MSR_Label.grid(row=3, column=4, columnspan=1, padx=10, pady=0)



def Start():
    Welcome_Frame.grid(row=0, column=0, pady=25, padx=25)
    Welcome_Label.grid(pady=(10,0), row=0,column=0, columnspan=2)
    #Welcome_Label.pack(pady=10)
    Prompt_Label.grid(row=1, column=0, columnspan=2, pady=(0,10))
    #Prompt_Label.pack(pady=10)
    Username_Label.grid(pady=(10,5),row=2, column=0, columnspan=2)
    #Username_Label.pack(pady=10)
    Username_input.grid(row=3, column=0, padx=(5,10), pady=0, columnspan=2)
    #Username_input.pack(pady=10)
    Password_Label.grid(pady=(10,5),row=4, column=0, columnspan=2)
    #Password_Label.pack(pady=10)
    Password_input.grid(row=5, column=0, padx=10, pady=(5,30), columnspan=2)
    #Password_input.pack(pady=10)
    Login_button.grid(row=6, column=0, padx=10, pady=0)
    #Login_button.pack(pady=10)
    CreateUser_button.grid(row=6, column=1, padx=10, pady=0)
    #CreateUser_button.pack(pady=10)
    return

def on_registerUser():
    isSuccessfulRegister, errorMsg = user_manager.registerUser(Username_input.get(), Password_input.get())
    if isSuccessfulRegister:
         GUI_helpers.throwSuccessPopup(f"Successfully Created New User \'{Username_input.get().strip()}\'")
    else:
         GUI_helpers.throwErrorPopup(errorMsg)

Welcome_Label = tk.Label(Welcome_Frame, text="Welcome!",  font=("Montserrat", 16, "bold"))
Prompt_Label = tk.Label(Welcome_Frame, text="Please login or create a new user")
Username_Label = tk.Label(Welcome_Frame, text="Username")
Username_input = tk.Entry(Welcome_Frame, width=20, bg="white", fg="black")
Password_Label = tk.Label(Welcome_Frame, text="Password")
Password_input = tk.Entry(Welcome_Frame, width=20, bg="white", fg="black", show="*")
Login_button = tk.Button(Welcome_Frame, text="Login", padx=10, pady=5, bg="white", command=on_Login)
CreateUser_button = tk.Button(Welcome_Frame, text="Create New User", padx=10, pady=5, bg="white", command= on_registerUser)






    
        




        
    
'''

LRL_input = tk.Entry(Upper_DCM_Frame, width=10, bg="white", fg="blue")
LRL_Label = tk.Label(Upper_DCM_Frame, text="Lower\nRate Limit")

URL_input = tk.Entry(Upper_DCM_Frame, width=10, bg="white", fg="blue")
URL_Label = tk.Label(Upper_DCM_Frame, text="Upper\nRate Limit")

AA_input = tk.Entry(Upper_DCM_Frame, width=10, bg="white", fg="blue")
AA_Label = tk.Label(Upper_DCM_Frame, text="Atrial\nAmplitude")

APW_input = tk.Entry(Upper_DCM_Frame, width=10, bg="white", fg="blue")
APW_Label = tk.Label(Upper_DCM_Frame, text="Atrial\nPulse Width")

VA_input = tk.Entry(Upper_DCM_Frame, width=10, bg="white", fg="blue")
VA_Label = tk.Label(Upper_DCM_Frame, text="Ventricular\nAmplitude")

VPW_input = tk.Entry(Upper_DCM_Frame, width=10, bg="white", fg="blue")
VPW_Label = tk.Label(Upper_DCM_Frame, text="Ventricular\nPulse Width")

AS_input = tk.Entry(Upper_DCM_Frame, width=10, bg="white", fg="blue")
AS_Label = tk.Label(Upper_DCM_Frame, text="Atrial\nSensitivity")

VS_input = tk.Entry(Upper_DCM_Frame, width=10, bg="white", fg="blue")
VS_Label = tk.Label(Upper_DCM_Frame, text="Vetricular\nSensitivity")

ARP_input = tk.Entry(Upper_DCM_Frame, width=10, bg="white", fg="blue")
ARP_Label = tk.Label(Upper_DCM_Frame, text="ARP")

VRP_input = tk.Entry(Upper_DCM_Frame, width=10, bg="white", fg="blue")
VRP_Label = tk.Label(Upper_DCM_Frame, text="VRP")

PVARP_input = tk.Entry(Upper_DCM_Frame, width=10, bg="white", fg="blue")
PVARP_Label = tk.Label(Upper_DCM_Frame, text="PVARP")

H_input = tk.Entry(Upper_DCM_Frame, width=10, bg="white", fg="blue")
H_Label = tk.Label(Upper_DCM_Frame, text="Hysteresis")

RS_input = tk.Entry(Upper_DCM_Frame, width=10, bg="white", fg="blue")
RS_Label = tk.Label(Upper_DCM_Frame, text="Rate\nSmoothing")

MSR_input = tk.Entry(Upper_DCM_Frame, width=10, bg="white", fg="blue")
MSR_Label = tk.Label(Upper_DCM_Frame, text="Maximum\nSensor Rate")

'''

Save_Button = tk.Button(Lower_DCM_Frame, text="Save", width=10, height=4, bg="white", command=onSaveParameters)
Ver_Num_Label = tk.Label(Upper_DCM_Frame, text="Version " + _VERSION_NUMBER)
logout_button = tk.Button(Upper_DCM_Frame, text="Logout", bg="white", command=Logout)

AOO_Button = tk.Button(Lower_DCM_Frame, text="AOO", padx=10, pady=5, width=8, height=1, bg="white", command= lambda: Change_Parameters("AOO"))
AAI_Button = tk.Button(Lower_DCM_Frame, text="AAI", padx=10, pady=5, width=8, height=1, bg="white", command= lambda: Change_Parameters("AAI"))
VOO_Button = tk.Button(Lower_DCM_Frame, text="VOO", padx=10, pady=5, width=8, height=1, bg="white", command= lambda: Change_Parameters("VOO"))
VVI_Button = tk.Button(Lower_DCM_Frame, text="VVI", padx=10, pady=5, width=8, height=1, bg="white", command= lambda: Change_Parameters("VVI"))

AOOR_Button = tk.Button(Lower_DCM_Frame, text="AOOR", padx=10, pady=5, width=8, height=1, bg="white", command= lambda: Change_Parameters("AOOR"))
AAIR_Button = tk.Button(Lower_DCM_Frame, text="AAIR", padx=10, pady=5, width=8, height=1, bg="white", command= lambda: Change_Parameters("AAIR"))
VOOR_Button = tk.Button(Lower_DCM_Frame, text="VOOR", padx=10, pady=5, width=8, height=1, bg="white", command= lambda: Change_Parameters("VOOR"))
VVIR_Button = tk.Button(Lower_DCM_Frame, text="VVIR", padx=10, pady=5, width=8, height=1, bg="white", command= lambda: Change_Parameters("VVIR"))
Institution_Label = tk.Label(Lower_DCM_Frame, text="McMaster University")

'''
input_list = [LRL_input,
                URL_input,
                AA_input,
                APW_input,
                VA_input,
                VPW_input,
                AS_input,   
                VS_input,
                ARP_input,
                VRP_input,
                PVARP_input,
                H_input,
                RS_input,
                MSR_input]

A_only = [AA_input, AA_Label, APW_input, APW_Label, AS_input, AS_Label, ARP_input, ARP_Label]

V_only = [VA_input, VA_Label, VPW_input, VPW_Label, VS_input, VS_Label, VRP_input, VRP_Label]
'''

Start()


root.mainloop()