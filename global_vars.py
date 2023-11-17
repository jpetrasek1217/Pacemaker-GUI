import tkinter as tk
import tkinter.font as tkFont

# Constants
_VERSION_NUMBER = "2.0.8"
_ICON_BITMAP_FILEPATH = "assets/pacemaker_icon.ico"
_WINDOW_TITLE = "Pacemaker Device Controller Monitor " + _VERSION_NUMBER
_PAD_X = 20
_PAD_Y = 10
_BUTTON_WIDTH = 10
_BUTTON_BG = "white"
_WELCOME_ENTRY_WIDTH = 25
_DCM_ENTRY_WIDTH = 15
_ENTRY_HEIGHT = 5
_ENTRY_BG = "white"
_ENTRY_FG = "black"
_FONT_DEFAULT = ("Arial", 16)


root = tk.Tk()
root.title(_WINDOW_TITLE)
root.minsize(width=100, height=200)
root.iconbitmap(_ICON_BITMAP_FILEPATH)
_TKFONT_DEFAULT = tkFont.Font(family='Arial', size=16)
_SELECTED_OPTION = tk.StringVar()

welcomeFrame = tk.Frame(root)

DCMFrame = tk.Frame(root)
lowerDCMFrame = tk.Frame(DCMFrame)
middleDCMFrame = tk.Frame(DCMFrame)
upperDCMFrame = tk.Frame(DCMFrame)

# parameterEntryAndLabelList is made up of sublists: [paramName: str, paramEntry: tk.Entry, paramLabel: tk.Label]
parameterEntryAndLabelList = []