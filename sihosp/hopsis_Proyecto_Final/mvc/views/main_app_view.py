
# mvc/views/main_app_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from mvc.utils.constants import COLOR_FONDO, COLOR_TITULO

class MainAppView:
    def __init__(self, root, user_info, logout_callback, close_callback):
        self.root = root
        self.user_info = user_info # Tuple (username, rol)
        self.logout_callback = logout_callback
        self.close_callback = close_callback

        username, rol = self.user_info
        self.root.title(f"HOPSIS - Gestión Médica ({username.capitalize()} - {rol.capitalize()})")
        self.root.geometry("1200x850")
        self.root.config(bg=COLOR_FONDO)
        # self.root.state('zoomed')

        self._setup_ui()

    def _setup_ui(self):
        tk.Label(self.root, text="HOPSIS - SISTEMA DE GESTIÓN HOSPITALARIA",
                 font=("Arial", 22, "bold"), bg=COLOR_FONDO, fg=COLOR_TITULO).pack(pady=15)
        
        user_status_frame = tk.Frame(self.root, bg=COLOR_FONDO)
        user_status_frame.pack(fill=tk.X, padx=10, pady=(0,10))

        username, rol = self.user_info
        tk.Label(user_status_frame, text=f"Usuario: {username.capitalize()} ({rol.capitalize()})",
                 font=("Arial", 10), bg=COLOR_FONDO, fg=COLOR_TITULO).pack(side=tk.LEFT)
        
        tk.Button(user_status_frame, text="Cerrar Sesión", command=self.logout_callback,
                  font=("Arial", 9), bg="#FFC107", fg="black").pack(side=tk.RIGHT, padx=5)


        self.notebook = ttk.Notebook(self.root)
        style = ttk.Style()
        style.configure("TNotebook.Tab", font=("Arial", 10, "bold"), padding=[10, 5])
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)

        self.root.protocol("WM_DELETE_WINDOW", self._on_close_window)

    def add_module_tab(self, module_name, module_frame):
        self.notebook.add(module_frame, text=module_name)

    def _on_close_window(self):
        if messagebox.askokcancel("Salir de HOPSIS", "¿Está seguro de que desea salir de la aplicación?"):
            self.close_callback() # Call controller's method for proper shutdown

    def close(self):
        self.root.destroy()
