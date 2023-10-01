import tkinter as tk
#from pacing_modes import Parameters
#from pacing_modes import PacingModes
import user_manager 
from tkinter import messagebox


root = tk.Tk()
root.title= "Title"
root.iconbitmap=("#")
root.minsize(width=400, height=400)

Welcome_Frame = tk.Frame(root)
Welcome_Frame.grid(row=0, column=0)

DCM_Frame = tk.Frame(root)
Upper_DCM_Frame = tk.Frame(DCM_Frame)
Lower_DCM_Frame = tk.Frame(DCM_Frame)


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

def Change_Parameters(mode):
    if mode == "AAIR" or mode == "AOOR" or mode == "VVIR" or mode == "VOOR":
         return
    for widget in Upper_DCM_Frame.winfo_children():
            widget.grid_forget()
    Title_Label = tk.Label(Upper_DCM_Frame, text="You are using Parameter " + mode)
    Title_Label.grid(row=0,column=0, columnspan=5, padx=10, pady=10)
    if mode=="AOO":
        LRL_input.grid(row=1, column=0, columnspan=1, padx=10, pady=10)
        LRL_Label.grid(row=2, column=0, columnspan=1, padx=10, pady=10)
        URL_input.grid(row=1, column=1, columnspan=1, padx=10, pady=10)
        URL_Label.grid(row=2, column=1, columnspan=1, padx=10, pady=10)
        AA_input.grid(row=1, column=2, columnspan=1, padx=10, pady=10)
        AA_Label.grid(row=2, column=2, columnspan=1, padx=10, pady=10)
        APW_input.grid(row=1, column=3, columnspan=1, padx=10, pady=10)
        APW_Label.grid(row=2, column=3, columnspan=1, padx=10, pady=10)
    elif mode=="AAI":
        LRL_input.grid(row=1, column=0, columnspan=1, padx=10, pady=10)
        LRL_Label.grid(row=2, column=0, columnspan=1, padx=10, pady=10)
        URL_input.grid(row=1, column=1, columnspan=1, padx=10, pady=10)
        URL_Label.grid(row=2, column=1, columnspan=1, padx=10, pady=10)
        AA_input.grid(row=1, column=2, columnspan=1, padx=10, pady=10)
        AA_Label.grid(row=2, column=2, columnspan=1, padx=10, pady=10)
        APW_input.grid(row=1, column=3, columnspan=1, padx=10, pady=10)
        APW_Label.grid(row=2, column=3, columnspan=1, padx=10, pady=10)
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
    elif mode=="VOO":
        LRL_input.grid(row=1, column=0, columnspan=1, padx=10, pady=10)
        LRL_Label.grid(row=2, column=0, columnspan=1, padx=10, pady=10)
        URL_input.grid(row=1, column=1, columnspan=1, padx=10, pady=10)
        URL_Label.grid(row=2, column=1, columnspan=1, padx=10, pady=10)
        VA_input.grid(row=1, column=2, columnspan=1, padx=10, pady=10)
        VA_Label.grid(row=2, column=2, columnspan=1, padx=10, pady=10)
        VPW_input.grid(row=1, column=3, columnspan=1, padx=10, pady=10)
        VPW_Label.grid(row=2, column=3, columnspan=1, padx=10, pady=10)
    elif mode=="VVI":
        LRL_input.grid(row=1, column=0, columnspan=1, padx=10, pady=10)
        LRL_Label.grid(row=2, column=0, columnspan=1, padx=10, pady=10)
        URL_input.grid(row=1, column=1, columnspan=1, padx=10, pady=10)
        URL_Label.grid(row=2, column=1, columnspan=1, padx=10, pady=10)
        VA_input.grid(row=1, column=2, columnspan=1, padx=10, pady=10)
        VA_Label.grid(row=2, column=2, columnspan=1, padx=10, pady=10)
        VPW_input.grid(row=1, column=3, columnspan=1, padx=10, pady=10)
        VPW_Label.grid(row=2, column=3, columnspan=1, padx=10, pady=10)
        VS_input.grid(row=3, column=0, columnspan=1, padx=10, pady=10)
        VS_Label.grid(row=4, column=0, columnspan=1, padx=10, pady=10)
        VRP_input.grid(row=3, column=1, columnspan=1, padx=10, pady=0)
        VRP_Label.grid(row=4, column=1, columnspan=1, padx=10, pady=0)
        H_Label.grid(row=4, column=2, columnspan=1, padx=10, pady=0)
        H_input.grid(row=3, column=2, columnspan=1, padx=10, pady=0)
        RS_input.grid(row=3, column=3, columnspan=1, padx=10, pady=0)
        RS_Label.grid(row=4, column=3, columnspan=1, padx=10, pady=0)
    



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

Save_Button = tk.Button(Lower_DCM_Frame, text="Save", width=10, height=4 )#command=Save_Parameters)

AOO_Button = tk.Button(Lower_DCM_Frame, text="AOO", padx=10, pady=5, width=8, height=1, command= lambda: Change_Parameters("AOO"))
AAI_Button = tk.Button(Lower_DCM_Frame, text="AAI", padx=10, pady=5, width=8, height=1, command= lambda: Change_Parameters("AAI"))
VOO_Button = tk.Button(Lower_DCM_Frame, text="VOO", padx=10, pady=5, width=8, height=1, command= lambda: Change_Parameters("VOO"))
VVI_Button = tk.Button(Lower_DCM_Frame, text="VVI", padx=10, pady=5, width=8, height=1, command= lambda: Change_Parameters("VVI"))

AOOR_Button = tk.Button(Lower_DCM_Frame, text="AOOR", padx=10, pady=5, width=8, height=1, command= lambda: Change_Parameters("AOOR"))
AAIR_Button = tk.Button(Lower_DCM_Frame, text="AAIR", padx=10, pady=5, width=8, height=1, command= lambda: Change_Parameters("AAIR"))
VOOR_Button = tk.Button(Lower_DCM_Frame, text="VOOR", padx=10, pady=5, width=8, height=1, command= lambda: Change_Parameters("VOOR"))
VVIR_Button = tk.Button(Lower_DCM_Frame, text="VVIR", padx=10, pady=5, width=8, height=1, command= lambda: Change_Parameters("VVIR"))




def on_Login():
    user_manager.loginUser(Username_input.get(), Password_input.get())
    for widget in Welcome_Frame.winfo_children():
        widget.grid_forget()
    DCM_Frame.grid(row=0, column=0)
    Upper_DCM_Frame.grid(row=0,column=0)
    Lower_DCM_Frame.grid(row=1,column=0)
    Change_Parameters("AOO")
    Save_Button.grid(row=0, column=4, rowspan=2)
    AOO_Button.grid(row=1, column=0)
    AAI_Button.grid(row=0, column=0)
    VOO_Button.grid(row=1, column=1)
    VVI_Button.grid(row=0, column=1)
    AOOR_Button.grid(row=1, column=2)
    AAIR_Button.grid(row=0, column=2)
    VOOR_Button.grid(row=1, column=3)
    VVIR_Button.grid(row=0, column=3)
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


Welcome_Label = tk.Label(Welcome_Frame, text="Welcome!").grid(pady=10, row=0,column=0,  columnspan=2)
#Welcome_Label.pack(pady=10)

Prompt_Label = tk.Label(Welcome_Frame, text="Please login or create a new user").grid(row=1, column=0, columnspan=2, pady=10)
#Prompt_Label.pack(pady=10)

Username_Label = tk.Label(Welcome_Frame, text="Username").grid(pady=10,row=2, column=0, columnspan=2)
#Username_Label.pack(pady=10)
Username_input = tk.Entry(Welcome_Frame, width=20, bg="white", fg="blue")
Username_input.grid(row=3, column=0, padx=10, pady=0, columnspan=2)
#Username_input.pack(pady=10)

Password_Label = tk.Label(Welcome_Frame, text="Password").grid(pady=10,row=4, column=0, columnspan=2)
#Password_Label.pack(pady=10)
Password_input = tk.Entry(Welcome_Frame, width=20, bg="white", fg="blue", show="*")
Password_input.grid(row=5, column=0, padx=10, pady=(0,10), columnspan=2)
#Password_input.pack(pady=10)

Login_button = tk.Button(Welcome_Frame, text="LOGIN", padx=10, pady=5, command=on_Login).grid(row=6, column=0, padx=10, pady=0)
#Login_button.pack(pady=10)
CreateUser_button = tk.Button(Welcome_Frame, text="Create New User", padx=10, pady=5, command=lambda: user_manager.registerUser(Username_input.get(), Password_input.get())).grid(row=6, column=1, padx=10, pady=0)
#CreateUser_button.pack(pady=10)



root.mainloop()