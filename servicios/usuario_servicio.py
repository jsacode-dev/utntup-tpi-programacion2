from entidades.usuario import Usuario
from enums.rol import Rol
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

    def listar(self) -> list[Usuario]:
        return [u for u in self.__usuarios if not u.eliminado]

    def buscar_por_id(self, id_usuario: int) -> Usuario:
        for usuario in self.__usuarios:
            if usuario.id == id_usuario and not usuario.eliminado:
                return usuario
        raise EntidadNoEncontradaError(f"Usuario con ID {id_usuario} no encontrado.")

    def mail_disponible(self, mail: str) -> bool:
        return self.__buscar_por_mail(mail) is None

    def crear(self, nombre: str, apellido: str, mail: str, celular: str, contrasenia: str, rol: Rol) -> Usuario:
        usuario = Usuario(nombre, apellido, mail, celular, contrasenia, rol)
        self.agregar(usuario)
        return usuario

    def editar(self, id_usuario: int, id_sesion: int, nombre: str, apellido: str, mail: str, celular: str, rol: Rol) -> Usuario:
        usuario = self.buscar_por_id(id_usuario)
        if id_usuario == id_sesion and rol != usuario.rol: # Regla propia, no figura en la consigna
            raise OperacionNoPermitidaError("No puede cambiar su propio rol.")
        existente = self.__buscar_por_mail(mail)
        if existente is not None and existente is not usuario:
            raise DuplicadoError("Ya existe un usuario con ese mail.")
        usuario.nombre = nombre
        usuario.apellido = apellido
        usuario.mail = mail
        usuario.celular = celular
        usuario.rol = rol
        return usuario

    def eliminar(self, id_usuario: int, id_sesion: int) -> None:
        if id_usuario == id_sesion:
            raise OperacionNoPermitidaError("No puede eliminarse a sí mismo.")
        usuario = self.buscar_por_id(id_usuario)
        usuario.eliminado = True

    def __buscar_por_mail(self, mail: str) -> Usuario | None:
        for usuario in self.__usuarios:
            if usuario.mail.lower() == mail.strip().lower() and not usuario.eliminado:
                return usuario
        return None
