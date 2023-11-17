import global_vars
import welcome_handler


def Start():
    welcome_handler.createAndShowWelcome()
    return

Start()

"""


import tkinter as tk

def on_option_select(event):
    selected_option.set(event)

# Create the main application window
root = tk.Tk()
root.title("User Input from Dropdown List")
root.geometry("400x200")

# Create a StringVar to hold the selected option
selected_option = tk.StringVar()

# Create a label to instruct the user
instruction_label = tk.Label(root, text="Select an option:")
instruction_label.pack(pady=10)

# Create the dropdown menu with options
options = ["Option 1", "Option 2", "Option 3", "Option 4"]
dropdown = tk.OptionMenu(root, selected_option, *options)
dropdown.pack()

# Add a button to show the selected option
show_button = tk.Button(root, text="Show Selected Option", command=lambda: on_option_select(selected_option.get()))
show_button.pack(pady=10)

# Create a label to display the selected option
result_label = tk.Label(root, text="")
result_label.pack()
root.mainloop()
"""

global_vars.root.mainloop()