from tkinter import *



#Create a label widget
#myLabel1 = Label(root, text="Hello World")
#myLabel2 = Label(root, text="SUKA BEEYAT")
#shoving widget onto screen

#myLabel1.grid(row=0, column=0)
#myLabel2.grid(row=1, column=0)

#def myClick():
 #   hello ="I am in your walls " + e.get()
  #  myLabel = Label(root, text=hello)
   # myLabel.pack()

#e.pack()
#e.insert(0, "Enter Your Name")

#myButton = Button(root, text="Enter Your Name", padx=5, pady=3, fg="blue", bg="pink")
#myButton.pack()

"""
root = Tk()
root.title("Simple Calculator")
e = Entry(root, width=50, bg="white", fg="blue")
e.grid(row=0, column=0, columnspan=3, padx=10, pady=10)



def button_click(number):
    current = e.get()
    e.delete(0, END)
    e.insert(0, str(current) + str(number))

def button_clear():
    e.delete(0, END)

def button_add():
    global prev
    prev = int(e.get())
    e.delete(0,END)

def button_equate():
    next = int(e.get())
    e.delete(0, END)
    e.insert(0, prev + next)
    

button_1 = Button(root, text="1", padx=40, pady=20, command=lambda: button_click(1))
button_2 = Button(root, text="2", padx=40, pady=20, command=lambda: button_click(2))
button_3 = Button(root, text="3", padx=40, pady=20, command=lambda: button_click(3))
button_4 = Button(root, text="4", padx=40, pady=20, command=lambda: button_click(4))
button_5 = Button(root, text="5", padx=40, pady=20, command=lambda: button_click(5))
button_6 = Button(root, text="6", padx=40, pady=20, command=lambda: button_click(6))
button_7 = Button(root, text="7", padx=40, pady=20, command=lambda: button_click(7))
button_8 = Button(root, text="8", padx=40, pady=20, command=lambda: button_click(8))
button_9 = Button(root, text="9", padx=40, pady=20, command=lambda: button_click(9))
button_0 = Button(root, text="0", padx=40, pady=20, command=lambda: button_click(0))
button_plus = Button(root, text="+", padx=40, pady=20, command=button_add)
button_equal = Button(root, text="=", padx=90, pady=20, command=button_equate)
button_gone = Button(root, text="Clear", padx=80, pady=20, command=button_clear)
#put buttons on screen

button_1.grid(row=3, column=2)
button_2.grid(row=3, column=1)
button_3.grid(row=3, column=0)
button_4.grid(row=2, column=2)
button_5.grid(row=2, column=1)
button_6.grid(row=2, column=0)
button_7.grid(row=1, column=2)
button_8.grid(row=1, column=1)
button_9.grid(row=1, column=0)
button_0.grid(row=4, column=0)
button_plus.grid(row=5, column=0)
button_equal.grid(row=4, column=1, columnspan=2)
button_gone.grid(row=5, column=1, columnspan=2)

"""

root = Tk()
root.title="peepeeaafs]vsdvssoo"
root.iconbitmap=("#")

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

ARP_input = Entry(frame_stats, width=10, bg="white", fg="blue")
ARP_input.grid(row=3, column=0, columnspan=1, padx=10, pady=0)
ARP_Label = Label(frame_stats, text="ARP").grid( pady=(10,25),row=4, column=0)

PVARP_input = Entry(frame_stats, width=10, bg="white", fg="blue")
PVARP_input.grid(row=3, column=1, columnspan=1, padx=10, pady=0)

H_input = Entry(frame_stats, width=10, bg="white", fg="blue")
H_input.grid(row=3, column=2, columnspan=1, padx=10, pady=0)

RS_input = Entry(frame_stats, width=10, bg="white", fg="blue")
RS_input.grid(row=3, column=3, columnspan=1, padx=10, pady=0)

MSR_input = Entry(frame_stats, width=10, bg="white", fg="blue")
MSR_input.grid(row=3, column=4, columnspan=1, padx=10, pady=0)



button_AOO = Button(frame_parameters, text="AOO", padx=10, pady=5)
button_AAI = Button(frame_parameters, text="AAI", padx=10, pady=5)
button_VOO = Button(frame_parameters, text="VOO", padx=10, pady=5)
button_VVI = Button(frame_parameters, text="VVI", padx=10, pady=5)
button_AOOR = Button(frame_parameters, text="AOOR", padx=10, pady=5)
button_AAIR = Button(frame_parameters, text="AAIR", padx=10, pady=5)
button_VOOR = Button(frame_parameters, text="VOOR", padx=10, pady=5)
button_VVIR = Button(frame_parameters, text="VVIR", padx=10, pady=5)

button_AOO.grid(row=2, column=0)
button_AAI.grid(row=2, column=1)
button_VOO.grid(row=2, column=2)
button_VVI.grid(row=2, column=3)
button_AOOR.grid(row=2, column=4)
button_AAIR.grid(row=2, column=5)
button_VOOR.grid(row=2, column=6)
button_VVIR.grid(row=2, column=7)

root.mainloop()
