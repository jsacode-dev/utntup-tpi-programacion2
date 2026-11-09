from servicios.categoria_servicio import CategoriaServicio
from excepciones.food_store_error import FoodStoreError
from consola.validadores import validar_texto, validar_numero
from consola.presentacion import mostrar_error


def listar_categorias(servicio: CategoriaServicio) -> None:
    categorias = servicio.listar()
    if not categorias:
        print("No hay categorías cargadas")
        return
    for categoria in categorias:
        print(categoria)


def crear_categoria(servicio: CategoriaServicio) -> None:
    nombre = validar_texto("Nombre: ")
    descripcion = validar_texto("Descripción: ")
    categoria = servicio.crear(nombre, descripcion)
    print(f"Categoría creada con id {categoria.id}")


def editar_categoria(servicio: CategoriaServicio) -> None:
    listar_categorias(servicio)
    id_categoria = validar_numero("Id de la categoría a editar: ")
    categoria = servicio.buscar_por_id(id_categoria)
    print("(Enter para conservar el valor actual)")
    nombre = validar_texto(f"Nombre [{categoria.nombre}]: ", salto_valor=True) or categoria.nombre
    descripcion = validar_texto(f"Descripción [{categoria.descripcion}]: ", salto_valor=True) or categoria.descripcion
    servicio.editar(id_categoria, nombre, descripcion)
    print("Categoría actualizada")


def eliminar_categoria(servicio: CategoriaServicio) -> None:
    listar_categorias(servicio)
    id_categoria = validar_numero("Id de la categoría a eliminar: ")
    servicio.buscar_por_id(id_categoria)
    confirmacion = validar_texto("¿Confirma la eliminación? (S/N): ").upper()
    if confirmacion != "S":
        print("Eliminación cancelada")
        return
    servicio.eliminar(id_categoria)
    print("Categoría eliminada")


def menu_categorias(servicio: CategoriaServicio) -> None:
    while True:
        print("\n--- CATEGORÍAS ---")
        print("1. Listar")
        print("2. Crear")
        print("3. Editar")
        print("4. Eliminar")
        print("0. Volver")
        opcion = validar_numero("Seleccione: ", minimo=0, maximo=4)
        try:
            match opcion:
                case 1:
                    listar_categorias(servicio)
                case 2:
                    crear_categoria(servicio)
                case 3:
                    editar_categoria(servicio)
                case 4:
                    eliminar_categoria(servicio)
                case 0:
                    return
        except FoodStoreError as e:
            mostrar_error(str(e))