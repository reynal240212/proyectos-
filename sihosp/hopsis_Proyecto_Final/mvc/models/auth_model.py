

from mvc.utils.constants import USUARIOS, ROLES_MODULOS

class AuthModel:
    def __init__(self):
        self.usuarios = USUARIOS
        self.roles_modulos = ROLES_MODULOS

    def verify_credentials(self, username, password):
        user_data = self.usuarios.get(username)
        if user_data and user_data["password"] == password:
            return user_data["rol"]
        return None

    def get_allowed_modules(self, rol):
        return self.roles_modulos.get(rol, [])
