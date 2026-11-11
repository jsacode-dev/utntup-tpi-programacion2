from enums.rol import Rol
from entidades.base import Base
from excepciones.food_store_error import DatoInvalidoError

class Usuario(Base):
    """Representa un usuario del sistema con rol y datos personales."""

    def __init__(self, nombre: str, apellido: str, mail: str, celular: str, contrasenia: str, rol: Rol) -> None:
        super().__init__()
        self.nombre = nombre
        self.apellido = apellido
        self.mail = mail
        self.celular = celular
        self.__contrasenia = contrasenia
        self.rol = rol

    @property
    def nombre(self) -> str:
        """Retorna el nombre del usuario."""
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        """Establece el nombre, validando que no esté vacío."""
        if not valor.strip():
            raise DatoInvalidoError("El nombre no puede estar vacío.")
        self.__nombre = valor.strip()

    @property
    def apellido(self) -> str:
        """Retorna el apellido del usuario."""
        return self.__apellido

    @apellido.setter
    def apellido(self, valor: str) -> None:
        """Establece el apellido, validando que no esté vacío."""
        if not valor.strip():
            raise DatoInvalidoError("El apellido no puede estar vacío.")
        self.__apellido = valor.strip()

    @property
    def mail(self) -> str:
        """Retorna el mail del usuario."""
        return self.__mail

    @mail.setter
    def mail(self, valor: str) -> None:
        """Establece el mail, validando formato y que no esté vacío."""
        if not valor.strip():
            raise DatoInvalidoError("El mail no puede estar vacío.")
        if "@" not in valor or "." not in valor:
            raise DatoInvalidoError("El mail debe tener formato válido (contener '@' y '.').")
        self.__mail = valor.strip()

    @property
    def celular(self) -> str:
        """Retorna el celular del usuario."""
        return self.__celular

    @celular.setter
    def celular(self, valor: str) -> None:
        """Establece el celular, validando que no esté vacío."""
        if not valor.strip():
            raise DatoInvalidoError("El celular no puede estar vacío.")
        self.__celular = valor.strip()

    @property
    def rol(self) -> Rol:
        """Retorna el rol del usuario."""
        return self.__rol

    @rol.setter
    def rol(self, valor: Rol) -> None:
        """Establece el rol, validando que sea una instancia válida."""
        if not isinstance(valor, Rol):
            raise DatoInvalidoError("El rol debe ser una instancia de Rol.")
        self.__rol = valor

    def verificar_contrasenia(self, contrasenia: str) -> bool:
        """Verifica si la contraseña ingresada coincide con la almacenada."""
        return self.__contrasenia == contrasenia

    def __str__(self) -> str:
        """Retorna una representación en cadena del usuario."""
        return f"[{self.rol}] {self.nombre} {self.apellido} - {self.mail} - {self.celular}"
