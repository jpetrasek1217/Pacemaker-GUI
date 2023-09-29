from tkinter import messagebox


# GUI Error Popup

def throwErrorPopup(msg: str) -> None:
    messagebox.showerror("Error", f"Error: {msg}")
