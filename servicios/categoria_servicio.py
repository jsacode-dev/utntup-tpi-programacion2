from entidades.categoria import Categoria
from excepciones.food_store_error import (
    EntidadNoEncontradaError,
    DuplicadoError,
    OperacionNoPermitidaError,
)

class CategoriaServicio:
    def __init__(self) -> None:
        self.categorias: list[Categoria] = []

    def listar(self) -> list[Categoria]: #devuelve solo las categorías que no están eliminadas
        return [c for c in self.__categorias if not c.eliminado]

    def buscar_por_id(self, id_categoria: int) -> Categoria:
        for categoria in self.__categorias:
            if categoria.id == id_categoria and not categoria.eliminado:
                return categoria
        raise EntidadNoEncontradaError(f"No existe una categoría con id {id_categoria}")

    def crear(self, nombre: str, descripcion: str) -> Categoria: 
        self.__validar_nombre_unico(nombre)
        categoria = Categoria(nombre, descripcion)
        self.__categorias.append(categoria)
        return categoria

    def editar(self, id_categoria: int, nombre: str, descripcion: str) -> Categoria: #si el usuario no escribe nada, se mantiene el valor anterior
        categoria = self.buscar_por_id(id_categoria)
        self.__validar_nombre_unico(nombre, id_categoria)
        categoria.nombre = nombre
        categoria.descripcion = descripcion
        return categoria

    def eliminar(self, id_categoria: int) -> None:
        categoria = self.buscar_por_id(id_categoria)
        activos = len([p for p in categoria.productos if not p.eliminado]) #devuelve la cantidad de productos activos que tiene la categoría
        if activos > 0:
            raise OperacionNoPermitidaError(
                f"No se puede eliminar: la categoría tiene {activos} producto(s) activo(s)"
            )
        categoria.eliminado = True

    def __validar_nombre_unico(self, nombre: str, id_excluido: int = 0) -> None: #El id excluido es para cuando se edita una categoría, para que no se compare con ella misma
        for categoria in self.listar():
            if categoria.nombre.lower() == nombre.strip().lower() and categoria.id != id_excluido:
                raise DuplicadoError(f"Ya existe una categoría llamada {categoria.nombre}") 