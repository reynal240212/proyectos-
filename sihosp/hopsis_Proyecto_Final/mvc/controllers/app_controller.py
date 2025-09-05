
# mvc/controllers/app_controller.py
import tkinter as tk
from tkinter import messagebox
from mvc.views.main_app_view import MainAppView
from mvc.models.data_model import DataModel
from mvc.controllers.module_controller import ModuleController
from mvc.views.module_view import ModuleView

class AppController:
    def __init__(self, root, user_info, auth_model, auth_controller):
        self.root = root
        self.user_info = user_info  
        self.auth_model = auth_model 
        self.data_model = DataModel() 
        self.auth_controller = auth_controller 

        self.main_app_view = MainAppView(self.root, self.user_info, self.handle_logout, self.handle_app_close)
        self.module_controllers = {}

        self._load_modules()

    def _load_modules(self):
        username, rol = self.user_info
        allowed_modules_names = self.auth_model.get_allowed_modules(rol)

        for module_name in allowed_modules_names:
            campos = self.data_model.get_campos(module_name)
            if not campos:
                print(f"Advertencia: Campos no definidos para el módulo '{module_name}' en constants.py")
                continue
         
            module_ctrl = ModuleController(self.data_model, module_name, campos, self.main_app_view.notebook)
            self.module_controllers[module_name] = module_ctrl
      
            self.main_app_view.add_module_tab(module_name, module_ctrl.view.get_frame())
            
            module_ctrl.load_initial_data() 

    def handle_logout(self):
        if messagebox.askokcancel("Cerrar Sesión", "¿Está seguro de que desea cerrar sesión?"):
            self.main_app_view.close() 
            self.auth_controller.show_login_view() 

    def handle_app_close(self):
       
        self.root.quit() 
      

