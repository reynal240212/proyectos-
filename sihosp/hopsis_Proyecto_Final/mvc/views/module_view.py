
# mvc/views/module_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from mvc.utils.constants import (COLOR_FONDO, COLOR_TITULO, COLOR_BOTON_PRIMARIO,
                                 COLOR_BOTON_PELIGRO, COLOR_TEXTO_BOTON, COLOR_BOTON_SECUNDARIO)

class ModuleView:
    def __init__(self, parent_notebook, module_name, campos_list, controller):
        self.module_name = module_name
        self.campos = campos_list
        self.controller = controller # To call controller methods for actions

        self.frame = ttk.Frame(parent_notebook, padding=10)
        # parent_notebook.add(self.frame, text=module_name) # MainAppView will add this

        self._setup_ui()

    def get_frame(self):
        return self.frame

    def _setup_ui(self):
        form_frame = tk.LabelFrame(self.frame, text=f"Gestión de {self.module_name}", bg=COLOR_FONDO,
                                   fg=COLOR_TITULO, font=("Arial", 14, "bold"), padx=15, pady=15)
        form_frame.pack(fill="x", padx=5, pady=5)
        self.entradas = {}

        num_campos = len(self.campos)
        for i, campo_nombre in enumerate(self.campos):
            tk.Label(form_frame, text=f"{campo_nombre}:", bg=COLOR_FONDO, font=("Arial", 10)).grid(
                row=i, column=0, padx=5, pady=5, sticky="w")
            var = tk.StringVar()
            self.entradas[campo_nombre] = var
            entry = tk.Entry(form_frame, textvariable=var, font=("Arial", 10), width=40)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")

        botones_frame = tk.Frame(form_frame, bg=COLOR_FONDO)
        botones_frame.grid(row=num_campos, column=0, columnspan=2, pady=10)

        tk.Button(botones_frame, text="Agregar", bg=COLOR_BOTON_PRIMARIO, fg=COLOR_TEXTO_BOTON,
                  font=("Arial", 10, "bold"), command=self._on_add_click,
                  relief=tk.FLAT, overrelief=tk.RIDGE).pack(side=tk.LEFT, padx=5)

        tk.Button(botones_frame, text="Eliminar Seleccionado", bg=COLOR_BOTON_PELIGRO, fg=COLOR_TEXTO_BOTON,
                  font=("Arial", 10, "bold"), command=self._on_delete_click,
                  relief=tk.FLAT, overrelief=tk.RIDGE).pack(side=tk.LEFT, padx=5)

        tk.Button(botones_frame, text="Limpiar Campos", bg=COLOR_BOTON_SECUNDARIO, fg=COLOR_TEXTO_BOTON,
                  font=("Arial", 10, "bold"), command=self.clear_form_fields,
                  relief=tk.FLAT, overrelief=tk.RIDGE).pack(side=tk.LEFT, padx=5)
        
        form_frame.columnconfigure(1, weight=1)

        self.tabla = ttk.Treeview(self.frame, columns=self.campos, show="headings", height=10)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        style.configure("Treeview", font=("Arial", 10), rowheight=25)

        for campo in self.campos:
            self.tabla.heading(campo, text=campo)
            self.tabla.column(campo, width=150, anchor="w")
        self.tabla.pack(fill="both", expand=True, padx=5, pady=10)

    def _on_add_click(self):
        self.controller.handle_add_registro()

    def _on_delete_click(self):
        self.controller.handle_delete_registros()

    def get_form_data(self):
        return [self.entradas[c].get().strip() for c in self.campos]

    def clear_form_fields(self):
        for campo_nombre in self.campos:
            self.entradas[campo_nombre].set("")

    def populate_table(self, data_list):
        for item in self.tabla.get_children(): # Clear existing items
            self.tabla.delete(item)
        for record_values in data_list:
            self.tabla.insert("", "end", values=record_values)

    def get_selected_item_values(self):
        selected_ids = self.tabla.selection()
        if not selected_ids:
            return []
        
        selected_values_list = []
        for item_id in selected_ids:
            values_tuple = self.tabla.item(item_id, "values")
            selected_values_list.append(list(values_tuple)) # Convert tuple to list
        return selected_values_list
        
    def show_message(self, title, message, type="info"):
        if type == "error":
            messagebox.showerror(title, message)
        elif type == "warning":
            messagebox.showwarning(title, message)
        else:
            messagebox.showinfo(title, message)

    def confirm_action(self, title, message):
        return messagebox.askyesno(title, message)
