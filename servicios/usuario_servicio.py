from entidades.usuario import Usuario
from enums.rol import Rol
from excepciones.food_store_error import DuplicadoError, CredencialesInvalidasError, EntidadNoEncontradaError, OperacionNoPermitidaError

class UsuarioServicio:
    """Servicio de gestión de usuarios con autenticación y validación de roles."""

    def __init__(self) -> None:
        self.__usuarios: list[Usuario] = []

    def agregar(self, usuario: Usuario) -> None:
        """Agrega un nuevo usuario validando que el mail sea único."""
        if self.__buscar_por_mail(usuario.mail) is not None:
            raise DuplicadoError("Ya existe un usuario con ese mail.")
        self.__usuarios.append(usuario)

    def autenticar(self, mail: str, contrasenia: str) -> Usuario:
        """Autentica un usuario verificando credenciales."""
        usuario = self.__buscar_por_mail(mail)
        if usuario is None or not usuario.verificar_contrasenia(contrasenia):
            raise CredencialesInvalidasError("Mail o contraseña incorrectos.")
        return usuario

    def listar(self) -> list[Usuario]:
        """Retorna todos los usuarios activos."""
        return [u for u in self.__usuarios if not u.eliminado]

    def buscar_por_id(self, id_usuario: int) -> Usuario:
        """Busca un usuario por su ID."""
        for usuario in self.__usuarios:
            if usuario.id == id_usuario and not usuario.eliminado:
                return usuario
        raise EntidadNoEncontradaError(f"Usuario con ID {id_usuario} no encontrado.")

    def mail_disponible(self, mail: str) -> bool:
        """Verifica si un mail está disponible."""
        return self.__buscar_por_mail(mail) is None

    def crear(self, nombre: str, apellido: str, mail: str, celular: str, contrasenia: str, rol: Rol) -> Usuario:
        """Crea un nuevo usuario con el rol especificado."""
        usuario = Usuario(nombre, apellido, mail, celular, contrasenia, rol)
        self.agregar(usuario)
        return usuario

    def editar(self, id_usuario: int, id_sesion: int, nombre: str, apellido: str, mail: str, celular: str, rol: Rol) -> Usuario:
        """Edita los datos de un usuario con validaciones de permiso y unicidad."""
        usuario = self.buscar_por_id(id_usuario)
        if id_usuario == id_sesion and rol != usuario.rol:
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
        """Elimina un usuario con validación de permiso."""
        if id_usuario == id_sesion:
            raise OperacionNoPermitidaError("No puede eliminarse a sí mismo.")
        usuario = self.buscar_por_id(id_usuario)
        usuario.eliminado = True

    def __buscar_por_mail(self, mail: str) -> Usuario | None:
        """Busca un usuario activo por mail (sin distinguir mayúsculas)."""
        for usuario in self.__usuarios:
            if usuario.mail.lower() == mail.strip().lower() and not usuario.eliminado:
                return usuario
        return None
