from tkinter import messagebox

# GUI Popups

def throwErrorPopup(msg: str) -> None:
    if len(msg) <= 0:
        msg = "Opps! Something went wrong."
    messagebox.showerror("Error", f"Error: {msg}")

def throwSuccessPopup(msg: str) -> None:
    if len(msg) <= 0:
        msg = "Successfully completed the action."
    messagebox.showinfo("Success!", f"{msg}")

def hideFrame(frame):
    for widget in frame.winfo_children():
        widget.grid_forget()
    frame.grid_forget()