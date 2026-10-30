from abc import ABC, abstractmethod
from datetime import datetime

class Base(ABC):
    _contador: int = 0 #atributo de clase, para que no hayan dos objetos con el mismo id

    def __init__(self) -> None:
        Base._contador += 1
        self.__id: int = Base._contador #se leerían con las properties
        self.__eliminado: bool = False
        self.__creado_en: datetime = datetime.now()

    @property
    def id(self) -> int:
        return self.__id

    @property
    def eliminado(self) -> bool:
        return self.__eliminado

    @eliminado.setter #solo este tendría setter porque es el único atributo que puede cambiar su valor
    def eliminado(self, valor: bool) -> None:
        self.__eliminado = valor

    @property
    def creado_en(self) -> datetime:
        return self.__creado_en

    def __eq__(self, otro: object) -> bool: #dos entidades son iguales si tienen el mismo id
        if not isinstance(otro, Base):
            return False
        return self.id == otro.id

    @abstractmethod #base no se puede instanciar, cada entidad debe implementar su propio __str__
    def __str__(self) -> str:
        ...