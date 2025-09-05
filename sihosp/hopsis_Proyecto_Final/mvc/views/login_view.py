
# mvc/views/login_view.py
import tkinter as tk
from tkinter import messagebox
from mvc.utils.constants import COLOR_FONDO, COLOR_TITULO, COLOR_BOTON_PRIMARIO, COLOR_TEXTO_BOTON

class LoginView:
    def __init__(self, root, controller_callback):
        self.root = root
        self.controller_callback = controller_callback # To call controller's login method
        self.root.title("Login - HOPSIS")
        self.root.geometry("400x400")
        self.root.configure(bg=COLOR_FONDO)
        self.root.resizable(False, False)

        self._setup_ui()

    def _setup_ui(self):
        tk.Label(self.root, text="Inicio de Sesión HOPSIS", font=("Arial", 18, "bold"),
                 bg=COLOR_FONDO, fg=COLOR_TITULO).pack(pady=20)

        tk.Label(self.root, text="Usuario", bg=COLOR_FONDO, font=("Arial", 10)).pack()
        self.usuario_entry = tk.Entry(self.root, font=("Arial", 10))
        self.usuario_entry.pack(pady=5, padx=50, fill="x")

        tk.Label(self.root, text="Contraseña", bg=COLOR_FONDO, font=("Arial", 10)).pack()
        self.clave_entry = tk.Entry(self.root, show="*", font=("Arial", 10))
        self.clave_entry.pack(pady=5, padx=50, fill="x")
        
        tk.Label(self.root, text="contraseña para el usuario admin ", bg=COLOR_FONDO, font=("Arial", 8)).pack(pady=(10,0))
        tk.Label(self.root, text="(admin123)", bg=COLOR_FONDO, font=("Arial", 8, "italic")).pack()
        # para los demas usuarios 
        tk.Label(self.root, text="contraseña para el usuario doctor ", bg=COLOR_FONDO, font=("Arial", 8)).pack(pady=(10,0))
        tk.Label(self.root, text="(doctor123)", bg=COLOR_FONDO, font=("Arial", 8, "italic")).pack()
        tk.Label(self.root, text="contraseña para el usuario enfermera ", bg=COLOR_FONDO, font=("Arial", 8)).pack(pady=(10,0))
        tk.Label(self.root, text="(enfermera123)", bg=COLOR_FONDO, font=("Arial", 8, "italic")).pack()
        
        
        tk.Button(self.root, text="Ingresar", command=self._on_login_button_click,
                  bg=COLOR_BOTON_PRIMARIO, fg=COLOR_TEXTO_BOTON,
                  font=("Arial", 11, "bold"), relief=tk.FLAT, overrelief=tk.RIDGE).pack(pady=20, ipadx=10)
        
        self.usuario_entry.focus()

    def _on_login_button_click(self):
        username = self.usuario_entry.get().strip()
        password = self.clave_entry.get().strip()
        self.controller_callback(username, password) # Pass to controller

    def get_credentials(self):
        return self.usuario_entry.get().strip(), self.clave_entry.get().strip()

    def show_error(self, title, message):
        messagebox.showerror(title, message)

    def show_success(self, title, message):
        messagebox.showinfo(title, message)

    def close(self):
        self.root.destroy()
