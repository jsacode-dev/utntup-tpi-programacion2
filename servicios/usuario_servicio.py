from entidades.usuario import Usuario
from excepciones.food_store_error import *

class UsuarioServicio:
    def __init__(self) -> None:
        self.__usuarios: list[Usuario] = []

    def agregar(self, usuario: Usuario) -> None:
        if self.__buscar_por_mail(usuario.mail) is not None:
            raise DuplicadoError("Ya existe un usuario con ese mail.")
        self.__usuarios.append(usuario)

    def autenticar(self, mail: str, contrasenia: str) -> Usuario:
        usuario = self.__buscar_por_mail(mail)
        if usuario is None or not usuario.verificar_contrasenia(contrasenia):
            raise CredencialesInvalidasError("Mail o contraseña incorrectos.")
        return usuario

    def __buscar_por_mail(self, mail: str) -> Usuario | None:
        for usuario in self.__usuarios:
            if usuario.mail.lower() == mail.strip().lower() and not usuario.eliminado:
                return usuario
        return None
