from entidades.base import Base
from enums.rol import Rol
from excepciones.food_store_error import *

class Usuario(Base):
    def __init__(self, nombre: str, apellido: str, mail: str, celular: str, contrasenia: str, rol: Rol):
        super().__init__()
        self.nombre = nombre
        self.apellido = apellido
        self.mail = mail
        self.celular = celular
        self.__contrasenia = contrasenia
        self.rol = rol

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor.strip():
            raise DatoInvalidoError("El nombre no puede estar vacío.")
        self.__nombre = valor.strip()

    @property
    def apellido(self) -> str:
        return self.__apellido

    @apellido.setter
    def apellido(self, valor: str) -> None:
        if not valor.strip():
            raise DatoInvalidoError("El apellido no puede estar vacío.")
        self.__apellido = valor.strip()

    @property
    def mail(self) -> str:
        return self.__mail

    @mail.setter
    def mail(self, valor: str) -> None:
        if not valor.strip():
            raise DatoInvalidoError("El mail no puede estar vacío.")
        if "@" not in valor or "." not in valor:
            raise DatoInvalidoError("El mail debe tener formato válido (contener '@' y '.').")
        self.__mail = valor.strip()

    @property
    def celular(self) -> str:
        return self.__celular

    @celular.setter
    def celular(self, valor: str) -> None:
        if not valor.strip():
            raise DatoInvalidoError("El celular no puede estar vacío.")
        self.__celular = valor.strip()

    @property
    def rol(self) -> Rol:
        return self.__rol

    @rol.setter
    def rol(self, valor: Rol) -> None:
        if not isinstance(valor, Rol):
            raise DatoInvalidoError("El rol debe ser una instancia de Rol.")
        self.__rol = valor

    def verificar_contrasenia(self, contrasenia: str) -> bool:
        return self.__contrasenia == contrasenia

    def __str__(self) -> str:
        return f"[{self.rol}] {self.nombre} {self.apellido} - {self.mail} - {self.celular}"
