
import tkinter as tk
from mvc.controllers.auth_controller import AuthController

if __name__ == "__main__":
    root_login = tk.Tk()
    auth_controller = AuthController(root_login)
    root_login.mainloop()
