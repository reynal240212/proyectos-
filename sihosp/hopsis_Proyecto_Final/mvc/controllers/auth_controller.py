
from mvc.models.auth_model import AuthModel
from mvc.views.login_view import LoginView
from mvc.controllers.app_controller import AppController # To launch main app
import tkinter as tk

class AuthController:
    def __init__(self, root):
        self.root = root
        self.auth_model = AuthModel()
        self.login_view = LoginView(self.root, self.handle_login_attempt)


    def handle_login_attempt(self, username, password):

        
        if not username or not password:
            self.login_view.show_error("Error de Login", "Usuario y contraseña son requeridos.")
            return

        rol = self.auth_model.verify_credentials(username, password)

        if rol:
            self.login_view.show_success("Acceso Concedido", f"Bienvenido {username.capitalize()} ({rol.capitalize()})")
            self.login_view.close()
            self._launch_main_app(username, rol)
        else:
            self.login_view.show_error("Error de Acceso", "Usuario o contraseña incorrectos.")

    def _launch_main_app(self, username, rol):
        main_app_root = tk.Tk()

        app_controller = AppController(main_app_root, (username, rol), self.auth_model, self) 
        main_app_root.mainloop()
    
    def show_login_view(self):
        self.root = tk.Tk()
        self.login_view = LoginView(self.root, self.handle_login_attempt)
        self.root.mainloop()

