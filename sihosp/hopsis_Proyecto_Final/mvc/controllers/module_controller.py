

from mvc.views.module_view import ModuleView 

class ModuleController:
    def __init__(self, data_model, module_name, campos, parent_notebook_for_view):
        self.data_model = data_model
        self.module_name = module_name
        self.campos = campos 

        self.view = ModuleView(parent_notebook_for_view, self.module_name, self.campos, self)

    def load_initial_data(self):
        registros = self.data_model.get_registros(self.module_name)
        self.view.populate_table(registros)

    def handle_add_registro(self):
        valores_actuales = self.view.get_form_data()
        if not all(valores_actuales): 
            self.view.show_message("Campos incompletos", "Por favor complete todos los campos.", type="warning")
            return

        success, message = self.data_model.agregar_registro(self.module_name, valores_actuales)
        
        if success:
            self.view.clear_form_fields()
            self.load_initial_data() 
            self.view.show_message("Éxito", message)
        else:
            self.view.show_message("Error al Agregar", message, type="error")

    def handle_delete_registros(self):
        selected_values_list = self.view.get_selected_item_values()
        if not selected_values_list:
            self.view.show_message("Seleccionar", "Seleccione uno o más registros para eliminar.", type="warning")
            return

        if not self.view.confirm_action("Confirmar Eliminación",
                                       f"¿Está seguro de que desea eliminar {len(selected_values_list)} registro(s)?"):
            return

        success, message = self.data_model.eliminar_registros(self.module_name, selected_values_list)

        if success:
            self.load_initial_data() 
            self.view.show_message("Eliminado", message)
        else:
            self.view.show_message("Atención", message, type="warning")
            
    def handle_clear_fields(self): 
        self.view.clear_form_fields()
