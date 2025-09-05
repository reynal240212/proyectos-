

from mvc.utils.constants import CAMPOS_MODULOS

class DataModel:
    def __init__(self):
        self.datos_modulos = {module_name: [] for module_name in CAMPOS_MODULOS}


    def get_campos(self, module_name):
        return CAMPOS_MODULOS.get(module_name, [])

    def get_registros(self, module_name):
        return self.datos_modulos.get(module_name, [])

    def agregar_registro(self, module_name, registro_valores):
        if module_name in self.datos_modulos:

            if registro_valores not in self.datos_modulos[module_name]:
                self.datos_modulos[module_name].append(registro_valores)
                return True, "Registro agregado exitosamente."
            else:
                return False, "Este registro ya existe."
        return False, f"Módulo '{module_name}' no encontrado."

    def eliminar_registros(self, module_name, registros_a_eliminar_valores):
        if module_name in self.datos_modulos:
            eliminados_count = 0
            for reg_valores in registros_a_eliminar_valores:
                if reg_valores in self.datos_modulos[module_name]:
                    self.datos_modulos[module_name].remove(reg_valores)
                    eliminados_count += 1
            
            if eliminados_count > 0:
                return True, f"{eliminados_count} registro(s) eliminado(s)."
            else:
                return False, "No se encontraron los registros seleccionados para eliminar en los datos."
        return False, f"Módulo '{module_name}' no encontrado."
