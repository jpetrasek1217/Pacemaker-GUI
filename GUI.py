import GUI_global_vars as global_vars
import GUI_welcome_handler as welcome_handler

def Start():
    welcome_handler.createAndShowWelcome()
    return

Start()

global_vars.root.mainloop()