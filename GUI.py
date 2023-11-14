import global_vars
import welcome_handler


def Start():
    welcome_handler.createAndShowWelcome()
    return

Start()

global_vars.root.mainloop()