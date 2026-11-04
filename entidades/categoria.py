from entidades.base import Base
from excepciones.food_store_error import DatoInvalidoError

class Categoria(Base):
    def __init__(self, nombre: str, descripcion: str) -> None:
        super().__init__() #llama al constructor de Base
        self.nombre = nombre #Pasa por el setter, que valida que no esté vacío para guardar el valor en el atributo privado __nombre
        self.descripcion = descripcion
        self.__productos: list['Producto'] = [] #lista de productos que pertenecen a esta categoría

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre (self, valor: str) -> None:
        if not valor.strip():
            raise DatoInvalidoError("El nombre no puede estar vacío.")
        self.__nombre: str = valor.strip()

    @property
    def descripcion(self) -> str:
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, valor: str) -> None:
        if not valor.strip():
            raise DatoInvalidoError("La descripción no puede estar vacía.")
        self.__descripcion: str = valor.strip()


    #Acá no importé Producto porque Producto importa a Categoria, y eso genera un error de importación circular. 
    #Por eso usé 'Producto' entre comillas, para que Python lo interprete como un string y no intente importar la clase.
    @property
    def productos(self) -> tuple['Producto', ...]: #retorna una tupla de productos, para que no se pueda modificar la lista desde afuera
        return tuple(self.__productos)

    def agregar_producto(self, producto: 'Producto') -> None:
        self.__productos.append(producto)

    def quitar_producto(self, producto: 'Producto') -> None: #Para cuando se elimina un producto, se quita de la lista de productos de la categoría
        self.__productos.remove(producto)

    def __str__(self) -> str:
        return f"{self.id} - {self.nombre}: {self.descripcion}"