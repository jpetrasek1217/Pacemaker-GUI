from tkinter import *
#from pacing_modes import Parameters
#from pacing_modes import PacingModes
import user_manager 


root = Tk()
root.title="Title"
root.iconbitmap=("#")
"""
frame_stats = Frame(root)
frame_stats.grid(row=0, column=0, padx=10, pady=20)

frame_parameters = Frame(root)
frame_parameters.grid(row=1, column=0, padx=10, pady=10)

LRL_input = Entry(frame_stats, width=10, bg="white", fg="blue")
LRL_input.grid(row=0, column=0, columnspan=1, padx=10, pady=0)
LRL_Label = Label(frame_stats, text="Lower\nRate Limit").grid( pady=(10,25),row=1, column=0)

URL_input = Entry(frame_stats, width=10, bg="white", fg="blue")
URL_input.grid(row=0, column=1, columnspan=1, padx=10, pady=0)
URL_Label = Label(frame_stats, text="Upper\nRate Limit").grid( pady=(10,25),row=1, column=1)

AA_input = Entry(frame_stats, width=10, bg="white", fg="blue")
AA_input.grid(row=0, column=2, columnspan=1, padx=10, pady=0)
AA_Label = Label(frame_stats, text="Atrial\nAmplitude").grid( pady=(10,25),row=1, column=2)

APW_input = Entry(frame_stats, width=10, bg="white", fg="blue")
APW_input.grid(row=0, column=3, columnspan=1, padx=10, pady=0)
APW_Label = Label(frame_stats, text="Atrial\nPulse Width").grid( pady=(10,25),row=1, column=3)

VA_input = Entry(frame_stats, width=10, bg="white", fg="blue")
VA_input.grid(row=0, column=2, columnspan=1, padx=10, pady=0)
VA_Label = Label(frame_stats, text="Ventricular\nAmplitude").grid( pady=(10,25),row=1, column=2)

VPW_input = Entry(frame_stats, width=10, bg="white", fg="blue")
VPW_input.grid(row=0, column=3, columnspan=1, padx=10, pady=0)
VPW_Label = Label(frame_stats, text="Ventricular\nPulse Width").grid( pady=(10,25),row=1, column=3)

AS_input = Entry(frame_stats, width=10, bg="white", fg="blue")
AS_input.grid(row=0, column=4, columnspan=1, padx=10, pady=0)
AS_Label = Label(frame_stats, text="Atrial\nSensitivity").grid( pady=(10,25),row=1, column=4)



PVARP_input = Entry(frame_stats, width=10, bg="white", fg="blue")
PVARP_input.grid(row=3, column=1, columnspan=1, padx=10, pady=0)

H_input = Entry(frame_stats, width=10, bg="white", fg="blue")
H_input.grid(row=3, column=2, columnspan=1, padx=10, pady=0)

RS_input = Entry(frame_stats, width=10, bg="white", fg="blue")
RS_input.grid(row=3, column=3, columnspan=1, padx=10, pady=0)

MSR_input = Entry(frame_stats, width=10, bg="white", fg="blue")
MSR_input.grid(row=3, column=4, columnspan=1, padx=10, pady=0)




def placeRequiredParameters():
    for num in range(5):
        Mode_input = Entry(frame_stats, width=10, bg="white", fg="blue")
        Mode_input.grid(row=3, column=0, columnspan=1, padx=10, pady=0)
        Mode_Label = Label(frame_stats, text="ARP").grid(pady=(10,25),row=4, column=0)

placeRequiredParameters()

button_PARAMETERS = Button(frame_parameters, text="TEST", padx=10, pady=5)

#button_MODE.grid(row=2, column=0)
"""

def on_Login():
    user_manager.loginUser(Username_input.get(), Password_input.get())

def on_CreateUser():
    user_manager.registerUser(Username_input.get(), Password_input.get())

Welcome = Label(root, text="Welcome!")#.grid(pady=(10,25),row=0, column=0)

Prompt = Label(root, text="Please login or\ncreate a new user")#.grid(row=1, column=0, pady=(10,25))

Username_Label = Label(root, text="Username")#.grid(pady=(25,10),row=2, column=0)
Username_input = Entry(root, width=10, bg="white", fg="blue")#.grid(row=3, column=0, padx=10, pady=0)

Password_Label = Label(root, text="Password")#.grid(pady=(25,10),row=4, column=0)
Password_input = Entry(root, width=10, bg="white", fg="blue")#.grid(row=5, column=0, padx=10, pady=0)

Login_button = Button(root, text="LOGIN", padx=10, pady=5, command=on_Login)
CreateUser_button = Button(root, text="Create New User", padx=10, pady=5, command=on_CreateUser)

Welcome.pack()
Prompt.pack()
Username_Label.pack()
Username_input.pack()
Password_Label.pack()
Password_input.pack()
Login_button.pack()
CreateUser_button.pack()

root.mainloop()
