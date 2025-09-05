import tkinter as tk
from tkinter import ttk, messagebox
import hashlib # Para hashear contraseñas (mejora de seguridad)

# --- Constantes y Configuración ---
COLOR_FONDO = "#E3F2FD"
COLOR_TITULO = "#1565C0"
COLOR_BOTON_PRIMARIO = "#1976D2"
COLOR_BOTON_SECUNDARIO = "#FFA000" # Naranja para Editar/Actualizar
COLOR_BOTON_PELIGRO = "#D32F2F"
COLOR_BOTON_NEUTRO = "#757575"
COLOR_TEXTO_BOTON = "white"
COLOR_TEXTO_ERROR = "red"

# Textos de UI (para facilitar cambios o internacionalización)
TEXTO_INICIO_SESION = "Inicio de Sesión HOPSIS"
TEXTO_USUARIO = "Usuario"
TEXTO_CLAVE = "Contraseña"
TEXTO_INGRESAR = "Ingresar"
TEXTO_AGREGAR = "Agregar"
TEXTO_ELIMINAR_SELECCIONADO = "Eliminar Seleccionado"
TEXTO_LIMPIAR_CAMPOS = "Limpiar Campos"
TEXTO_ACTUALIZAR = "Actualizar Cambios"
TEXTO_CARGAR_PARA_EDITAR = "Cargar para Editar"

# --- Gestión de Usuarios ---
# En una aplicación real, las contraseñas NUNCA deben estar en texto plano.
# Se usaría un hash. Ejemplo:
# def hash_password(password):
#     return hashlib.sha256(password.encode()).hexdigest()
# 'admin123_hashed': hash_password('admin123')

USUARIOS = {
    "admin": {"password_hash": hashlib.sha256("admin123".encode()).hexdigest(), "rol": "admin"},
    "doctor": {"password_hash": hashlib.sha256("doc2024".encode()).hexdigest(), "rol": "doctor"},
    "recepcion": {"password_hash": hashlib.sha256("rec123".encode()).hexdigest(), "rol": "recepcion"}
}

ROLES_MODULOS = {
    "admin": ["Pacientes", "Médicos", "Citas", "Historial Médico", "Recetas", "Facturación"],
    "doctor": ["Pacientes", "Médicos", "Citas", "Historial Médico", "Recetas"],
    "recepcion": ["Pacientes", "Médicos", "Citas", "Facturación"]
}

class EstilosApp:
    @staticmethod
    def configurar_estilos_globales():
        style = ttk.Style()
        style.theme_use('clam') # 'clam', 'alt', 'default', 'classic'

        # Estilo para Treeview Heading
        style.configure("Treeview.Heading",
                        font=("Arial", 10, "bold"),
                        background=COLOR_BOTON_PRIMARIO,
                        foreground=COLOR_TEXTO_BOTON,
                        relief=tk.FLAT)
        style.map("Treeview.Heading",
                  background=[('active', COLOR_TITULO)])

        # Estilo para Treeview Rows
        style.configure("Treeview",
                        font=("Arial", 10),
                        rowheight=25,
                        fieldbackground=COLOR_FONDO)
        style.map("Treeview",
                  background=[('selected', COLOR_BOTON_SECUNDARIO)],
                  foreground=[('selected', COLOR_TEXTO_BOTON)])

        # Estilo para Notebook Tabs
        style.configure("TNotebook.Tab",
                        font=("Arial", 10, "bold"),
                        padding=[10, 5],
                        background=COLOR_FONDO,
                        foreground=COLOR_TITULO)
        style.map("TNotebook.Tab",
                  background=[("selected", COLOR_BOTON_PRIMARIO)],
                  foreground=[("selected", COLOR_TEXTO_BOTON)])
        
        style.configure("TNotebook", background=COLOR_FONDO)
        style.configure("TFrame", background=COLOR_FONDO) # Para que los frames dentro del notebook hereden el color

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - HOPSIS")
        self.root.geometry("400x380") # Un poco más de alto para posible mensaje de error
        self.root.configure(bg=COLOR_FONDO)
        self.root.resizable(False, False)

        EstilosApp.configurar_estilos_globales() # Configurar estilos aquí también si se usan widgets ttk

        tk.Label(root, text=TEXTO_INICIO_SESION, font=("Arial", 18, "bold"),
                 bg=COLOR_FONDO, fg=COLOR_TITULO).pack(pady=20)

        tk.Label(root, text=TEXTO_USUARIO, bg=COLOR_FONDO, font=("Arial", 10)).pack()
        self.usuario_entry = ttk.Entry(root, font=("Arial", 10))
        self.usuario_entry.pack(pady=5, padx=50, fill="x")

        tk.Label(root, text=TEXTO_CLAVE, bg=COLOR_FONDO, font=("Arial", 10)).pack()
        self.clave_entry = ttk.Entry(root, show="*", font=("Arial", 10))
        self.clave_entry.pack(pady=5, padx=50, fill="x")
        
        self.mensaje_error_label = tk.Label(root, text="", font=("Arial", 9), bg=COLOR_FONDO, fg=COLOR_TEXTO_ERROR)
        self.mensaje_error_label.pack(pady=(0, 5))

        ttk.Button(root, text=TEXTO_INGRESAR, command=self._verificar_credenciales,
                   style="Primary.TButton").pack(pady=20, ipadx=10)
        
        # Definir estilos de botones ttk si no existen
        style = ttk.Style()
        style.configure("Primary.TButton", font=("Arial", 11, "bold"),
                        background=COLOR_BOTON_PRIMARIO, foreground=COLOR_TEXTO_BOTON)
        style.map("Primary.TButton", background=[('active', COLOR_TITULO)])


        self.usuario_entry.focus()
        self.root.bind('<Return>', lambda event: self._verificar_credenciales()) # Ingresar con Enter

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def _verificar_credenciales(self):
        usuario = self.usuario_entry.get().strip()
        clave = self.clave_entry.get().strip()
        self.mensaje_error_label.config(text="") # Limpiar mensaje de error previo

        if not usuario or not clave:
            self.mensaje_error_label.config(text="Usuario y contraseña son requeridos.")
            return

        user_data = USUARIOS.get(usuario)
        if user_data and user_data["password_hash"] == self._hash_password(clave):
            rol = user_data["rol"]
            messagebox.showinfo("Acceso Concedido", f"Bienvenido {usuario.capitalize()} ({rol.capitalize()})")
            self.root.destroy()
            self._abrir_app_principal(usuario, rol)
        else:
            self.mensaje_error_label.config(text="Usuario o contraseña incorrectos.")
            self.clave_entry.delete(0, tk.END)
            self.clave_entry.focus()

    def _abrir_app_principal(self, usuario, rol):
        root_app = tk.Tk()
        App(root_app, usuario, rol)
        root_app.mainloop()

class ModuloBase:
    def __init__(self, notebook, nombre, campos, app_principal):
        self.nombre = nombre
        self.campos = campos
        self.datos = [] # base de datos en memoria
        self.app_principal = app_principal # Referencia a la app principal para la barra de estado
        self.id_campo_principal = campos[0] # Asumimos que el primer campo es el ID principal

        self.frame = ttk.Frame(notebook, padding=10) # Usar ttk.Frame para heredar estilos
        notebook.add(self.frame, text=nombre)
        
        self.entradas = {}
        self.id_registro_seleccionado_para_edicion = None # Para saber qué item del treeview se está editando

        self._crear_interfaz_formulario()
        self._crear_interfaz_tabla()
        self._configurar_botones_estilo_ttk()

    def _configurar_botones_estilo_ttk(self):
        style = ttk.Style()
        common_opts = {"font": ("Arial", 10, "bold"), "padding": 5}
        
        style.configure("Primary.TButton", **common_opts,
                        background=COLOR_BOTON_PRIMARIO, foreground=COLOR_TEXTO_BOTON)
        style.map("Primary.TButton", background=[('active', '#1E88E5')]) # Un poco más claro al activar

        style.configure("Danger.TButton", **common_opts,
                        background=COLOR_BOTON_PELIGRO, foreground=COLOR_TEXTO_BOTON)
        style.map("Danger.TButton", background=[('active', '#E53935')])

        style.configure("Neutral.TButton", **common_opts,
                        background=COLOR_BOTON_NEUTRO, foreground=COLOR_TEXTO_BOTON)
        style.map("Neutral.TButton", background=[('active', '#8D8D8D')])
        
        style.configure("Warning.TButton", **common_opts,
                        background=COLOR_BOTON_SECUNDARIO, foreground=COLOR_TEXTO_BOTON)
        style.map("Warning.TButton", background=[('active', '#FFB300')])


    def _crear_interfaz_formulario(self):
        form_frame = tk.LabelFrame(self.frame, text=f"Gestión de {self.nombre}",
                                   bg=COLOR_FONDO, fg=COLOR_TITULO, font=("Arial", 14, "bold"), padx=15, pady=15)
        form_frame.pack(fill="x", padx=5, pady=5)

        for i, campo_nombre in enumerate(self.campos):
            tk.Label(form_frame, text=f"{campo_nombre}:", bg=COLOR_FONDO, font=("Arial", 10)).grid(
                row=i, column=0, padx=5, pady=5, sticky="w")
            var = tk.StringVar()
            self.entradas[campo_nombre] = var
            entry = ttk.Entry(form_frame, textvariable=var, font=("Arial", 10), width=40)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            if i == 0: # El primer campo (ID) podría ser no editable en actualización
                self.entry_id_principal = entry

        form_frame.columnconfigure(1, weight=1)

        botones_frame = ttk.Frame(form_frame) # Usar ttk.Frame
        botones_frame.grid(row=len(self.campos), column=0, columnspan=2, pady=10, sticky="ew")
        
        # Configurar pesos para que los botones se distribuyan
        for i in range(4): # Número de botones principales
            botones_frame.columnconfigure(i, weight=1)

        ttk.Button(botones_frame, text=TEXTO_AGREGAR, style="Primary.TButton",
                   command=self.agregar_registro).grid(row=0, column=0, padx=5, sticky="ew")
        
        self.btn_actualizar = ttk.Button(botones_frame, text=TEXTO_ACTUALIZAR, style="Warning.TButton",
                                         command=self.actualizar_registro, state=tk.DISABLED)
        self.btn_actualizar.grid(row=0, column=1, padx=5, sticky="ew")

        ttk.Button(botones_frame, text=TEXTO_ELIMINAR_SELECCIONADO, style="Danger.TButton",
                   command=self.eliminar_registro).grid(row=0, column=2, padx=5, sticky="ew")

        ttk.Button(botones_frame, text=TEXTO_LIMPIAR_CAMPOS, style="Neutral.TButton",
                   command=self.limpiar_formulario).grid(row=0, column=3, padx=5, sticky="ew")

    def _crear_interfaz_tabla(self):
        tabla_frame = ttk.Frame(self.frame)
        tabla_frame.pack(fill="both", expand=True, padx=5, pady=10)

        self.tabla = ttk.Treeview(tabla_frame, columns=self.campos, show="headings", height=10)
        
        scrollbar_y = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tabla.yview)
        scrollbar_x = ttk.Scrollbar(tabla_frame, orient="horizontal", command=self.tabla.xview)
        self.tabla.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        
        for campo in self.campos:
            self.tabla.heading(campo, text=campo, anchor="w")
            self.tabla.column(campo, width=150, anchor="w", minwidth=100)
        
        self.tabla.pack(side="left", fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self._al_seleccionar_item)

    def _al_seleccionar_item(self, event=None):
        seleccion = self.tabla.selection()
        if seleccion:
            self.id_registro_seleccionado_para_edicion = seleccion[0] # Guardar el item ID del treeview
            valores = self.tabla.item(self.id_registro_seleccionado_para_edicion, "values")
            for i, campo_nombre in enumerate(self.campos):
                self.entradas[campo_nombre].set(valores[i])
            self.btn_actualizar.config(state=tk.NORMAL)
            self.entry_id_principal.config(state="readonly") # No permitir editar el ID principal
            self.app_principal.mostrar_mensaje_status(f"Registro '{valores[0]}' cargado para editar.")
        else:
            self.id_registro_seleccionado_para_edicion = None
            self.btn_actualizar.config(state=tk.DISABLED)
            self.entry_id_principal.config(state="normal")
            self.app_principal.mostrar_mensaje_status("")


    def limpiar_formulario(self, limpiar_status=True):
        for campo_nombre in self.campos:
            self.entradas[campo_nombre].set("")
        self.tabla.selection_remove(self.tabla.selection()) # Deseleccionar
        self.id_registro_seleccionado_para_edicion = None
        self.btn_actualizar.config(state=tk.DISABLED)
        self.entry_id_principal.config(state="normal")
        if limpiar_status:
            self.app_principal.mostrar_mensaje_status(f"Campos del formulario '{self.nombre}' limpiados.")
        self.entradas[self.campos[0]].get() # Poner foco en el primer campo (si es visible)

    def _validar_campos(self, es_actualizacion=False):
        valores_actuales = {}
        for campo in self.campos:
            valor = self.entradas[campo].get().strip()
            if not valor:
                messagebox.showwarning("Campo Vacío", f"El campo '{campo}' no puede estar vacío.")
                return None
            valores_actuales[campo] = valor
        
        # Validar unicidad del ID principal (excepto si estamos actualizando el mismo registro)
        id_principal_valor = valores_actuales[self.id_campo_principal]
        for i, registro_existente_lista in enumerate(self.datos):
            registro_existente_dict = dict(zip(self.campos, registro_existente_lista))
            if registro_existente_dict[self.id_campo_principal] == id_principal_valor:
                # Si estamos actualizando y el ID coincide con el registro que estamos editando, está bien.
                # Necesitamos comparar con el ID original del registro que se cargó para editar.
                if es_actualizacion and self.id_registro_seleccionado_para_edicion:
                    item_original_valores = self.tabla.item(self.id_registro_seleccionado_para_edicion, "values")
                    if item_original_valores and item_original_valores[0] == id_principal_valor:
                        continue # Es el mismo registro que estamos editando
                
                messagebox.showwarning("ID Duplicado", f"El {self.id_campo_principal} '{id_principal_valor}' ya existe.")
                return None
        return valores_actuales

    def agregar_registro(self):
        valores_dict = self._validar_campos()
        if not valores_dict:
            return

        valores_lista = [valores_dict[c] for c in self.campos]

        self.datos.append(valores_lista)
        self.tabla.insert("", "end", values=valores_lista, tags=('added',))
        self.limpiar_formulario(limpiar_status=False)
        self.app_principal.mostrar_mensaje_status(f"Registro '{valores_lista[0]}' agregado a '{self.nombre}'.")
        messagebox.showinfo("Éxito", f"Registro agregado al módulo '{self.nombre}'.")


    def actualizar_registro(self):
        if not self.id_registro_seleccionado_para_edicion:
            messagebox.showwarning("No Seleccionado", "Ningún registro seleccionado para actualizar.")
            return

        valores_dict_nuevos = self._validar_campos(es_actualizacion=True) # Permitir el mismo ID si es el item actual
        if not valores_dict_nuevos:
            return
        
        valores_lista_nuevos = [valores_dict_nuevos[c] for c in self.campos]

        # Actualizar en self.datos
        # Encontrar el índice del registro original en self.datos para actualizarlo
        valores_originales_tabla = self.tabla.item(self.id_registro_seleccionado_para_edicion, "values")
        try:
            # Convertir la tupla de valores del Treeview a lista para buscar en self.datos
            indice_en_datos = self.datos.index(list(valores_originales_tabla))
            self.datos[indice_en_datos] = valores_lista_nuevos
        except ValueError:
            # Esto podría pasar si los datos se desincronizan, lo cual no debería ocurrir con este flujo
            messagebox.showerror("Error", "No se pudo encontrar el registro original en los datos internos para actualizar.")
            return

        # Actualizar en el Treeview
        self.tabla.item(self.id_registro_seleccionado_para_edicion, values=valores_lista_nuevos)
        
        self.limpiar_formulario(limpiar_status=False)
        self.app_principal.mostrar_mensaje_status(f"Registro '{valores_lista_nuevos[0]}' actualizado en '{self.nombre}'.")
        messagebox.showinfo("Éxito", f"Registro actualizado en '{self.nombre}'.")


    def eliminar_registro(self):
        seleccionados_ids_treeview = self.tabla.selection()
        if not seleccionados_ids_treeview:
            messagebox.showwarning("Seleccionar", "Seleccione uno o más registros para eliminar.")
            return

        confirmar = messagebox.askyesno("Confirmar Eliminación",
                                       f"¿Está seguro de que desea eliminar {len(seleccionados_ids_treeview)} registro(s)?")
        if not confirmar:
            return

        registros_eliminados_count = 0
        for item_id_treeview in seleccionados_ids_treeview:
            # Obtener valores del Treeview para buscar y eliminar en self.datos
            valores_tupla_tabla = self.tabla.item(item_id_treeview, "values")
            valores_lista_tabla = list(valores_tupla_tabla) # Convertir tupla a lista

            if valores_lista_tabla in self.datos:
                self.datos.remove(valores_lista_tabla)
                self.tabla.delete(item_id_treeview) # Eliminar de la vista
                registros_eliminados_count += 1
            else:
                # Si no está en self.datos pero sí en la tabla (raro, pero por si acaso)
                self.tabla.delete(item_id_treeview)
                print(f"Advertencia: El registro {valores_lista_tabla} estaba en la tabla pero no en self.datos.")


        if registros_eliminados_count > 0:
            self.app_principal.mostrar_mensaje_status(f"{registros_eliminados_count} registro(s) eliminado(s) de '{self.nombre}'.")
            messagebox.showinfo("Eliminado", f"{registros_eliminados_count} registro(s) eliminado(s) correctamente.")
        else:
            messagebox.showwarning("Atención", "No se eliminaron registros. Podrían haber sido eliminados previamente o no encontrados.")
        
        self.limpiar_formulario(limpiar_status=False) # Limpiar por si algo estaba cargado

# --- Módulos Específicos ---
class ModuloPacientes(ModuloBase):
    def __init__(self, notebook, app_principal):
        campos = ["ID Paciente", "Nombre", "Apellido", "Fecha Nac.", "Género", "Teléfono", "Dirección"]
        super().__init__(notebook, "Pacientes", campos, app_principal)

class ModuloMedicos(ModuloBase):
    def __init__(self, notebook, app_principal):
        campos = ["ID Médico", "Nombre", "Apellido", "Especialidad", "Teléfono"]
        super().__init__(notebook, "Médicos", campos, app_principal)

class ModuloCitas(ModuloBase):
    def __init__(self, notebook, app_principal):
        campos = ["ID Cita", "ID Paciente", "ID Médico", "Fecha", "Hora", "Motivo", "Estado"]
        super().__init__(notebook, "Citas", campos, app_principal)

class ModuloHistorial(ModuloBase):
    def __init__(self, notebook, app_principal):
        campos = ["ID Historial", "ID Paciente", "ID Cita", "Diagnóstico", "Tratamiento", "Notas", "Fecha"]
        super().__init__(notebook, "Historial Médico", campos, app_principal)

class ModuloRecetas(ModuloBase):
    def __init__(self, notebook, app_principal):
        campos = ["ID Receta", "ID Paciente", "ID Médico", "Medicamento", "Dosis", "Indicaciones", "Fecha Emisión"]
        super().__init__(notebook, "Recetas", campos, app_principal)

class ModuloFacturacion(ModuloBase):
    def __init__(self, notebook, app_principal):
        campos = ["ID Factura", "ID Paciente", "ID Cita", "Concepto", "Monto", "Fecha Emisión", "Estado Pago"]
        super().__init__(notebook, "Facturación", campos, app_principal)

# --- Aplicación Principal ---
class App:
    def __init__(self, root, usuario, rol):
        self.root = root
        self.usuario = usuario
        self.rol = rol
        root.title(f"HOPSIS - Gestión Médica ({self.usuario.capitalize()} - {self.rol.capitalize()})")
        root.geometry("1280x900") # Ajustar tamaño según necesidad
        root.config(bg=COLOR_FONDO)
        # root.state('zoomed') # Para iniciar maximizado

        EstilosApp.configurar_estilos_globales()

        tk.Label(root, text="HOPSIS - SISTEMA DE GESTIÓN HOSPITALARIA",
                 font=("Arial", 22, "bold"), bg=COLOR_FONDO, fg=COLOR_TITULO).pack(pady=15)

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)

        self.cargar_modulos_por_rol()

        # Barra de estado
        self.status_bar = tk.Label(root, text="Listo.", bd=1, relief=tk.SUNKEN, anchor=tk.W,
                                   bg=COLOR_FONDO, fg=COLOR_TITULO, font=("Arial", 9))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(0,5))

        self.root.protocol("WM_DELETE_WINDOW", self._al_cerrar_ventana)

    def mostrar_mensaje_status(self, mensaje, duracion_ms=5000):
        self.status_bar.config(text=mensaje)
        if hasattr(self, "_status_clear_job"):
            self.root.after_cancel(self._status_clear_job)
        if mensaje and mensaje != "Listo.": # No auto-limpiar "Listo."
            self._status_clear_job = self.root.after(duracion_ms, lambda: self.status_bar.config(text="Listo."))


    def cargar_modulos_por_rol(self):
        self.modulos_instanciados = {}
        modulos_disponibles_rol = ROLES_MODULOS.get(self.rol, [])

        clases_modulos = {
            "Pacientes": ModuloPacientes, "Médicos": ModuloMedicos, "Citas": ModuloCitas,
            "Historial Médico": ModuloHistorial, "Recetas": ModuloRecetas, "Facturación": ModuloFacturacion
        }

        for nombre_modulo in modulos_disponibles_rol:
            if nombre_modulo in clases_modulos:
                clase_modulo = clases_modulos[nombre_modulo]
                # Pasar 'self' (la instancia de App) a los módulos
                modulo_instancia = clase_modulo(self.notebook, self)
                self.modulos_instanciados[nombre_modulo] = modulo_instancia
            else:
                print(f"Advertencia: Clase para el módulo '{nombre_modulo}' no encontrada.")
    
    def _al_cerrar_ventana(self):
        if messagebox.askokcancel("Salir de HOPSIS", "¿Está seguro de que desea salir de la aplicación?"):
            # Aquí podrías añadir lógica para guardar datos si estuvieran persistidos
            self.root.destroy()

# --- Punto de Entrada ---
if __name__ == "__main__":
    root_login = tk.Tk()
    login_app = LoginApp(root_login)
    root_login.mainloop()