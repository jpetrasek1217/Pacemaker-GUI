from tkinter import messagebox


# GUI Popups

def throwErrorPopup(msg: str) -> None:
    messagebox.showerror("Error", f"Error: {msg}")

def throwSuccessPopup(msg: str) -> None:
    messagebox.showinfo("Success!", f"{msg}")