from getpass import getpass
from time import sleep

from servicios.usuario_servicio import UsuarioServicio
from servicios.categoria_servicio import CategoriaServicio
from servicios.pedido_servicio import PedidoServicio
from servicios.producto_servicio import ProductoServicio
from entidades.usuario import Usuario
from enums.rol import Rol
from excepciones.food_store_error import CredencialesInvalidasError
from consola.menu import Menu
from consola.menu_administrador import MenuAdministrador
from consola.menu_cliente import MenuCliente
from consola.presentacion import limpiar_consola, mostrar_encabezado, mostrar_error, mostrar_exito, mostrar_info, mostrar_sistema
from consola.validadores import validar_texto

def crear_menu(usuario: Usuario, usuario_servicio: UsuarioServicio, categoria_servicio: CategoriaServicio, producto_servicio: ProductoServicio, pedido_servicio: PedidoServicio) -> Menu:
    if usuario.rol == Rol.ADMIN:
        return MenuAdministrador(usuario, categoria_servicio, producto_servicio, usuario_servicio, pedido_servicio)
    elif usuario.rol == Rol.USUARIO:
        return MenuCliente(usuario, producto_servicio, pedido_servicio)
    else:
        raise ValueError("Rol de usuario no soportado.")

def login(servicio: UsuarioServicio) -> Usuario | None:
    intentos = 3
    while True:
        limpiar_consola()
        mostrar_encabezado("FOOD STORE", "INICIO DE SESIÓN")
        email = validar_texto("Ingrese su email: ")
        contrasenia = getpass("Ingrese su contraseña: ")
        try:
            usuario = servicio.autenticar(email, contrasenia)
            mostrar_exito(f"Bienvenido/a {usuario.nombre} {usuario.apellido} ({usuario.rol.value}).")
            sleep(1)
            limpiar_consola()
            return usuario
        except CredencialesInvalidasError as e:
            intentos -= 1
            mostrar_error(str(e))
            sleep(1)
            if intentos == 0:
                limpiar_consola()
                mostrar_encabezado("FOOD STORE", "INICIO DE SESIÓN")
                mostrar_error("Ha agotado todos los intentos para iniciar sesión.")
                return None

def main() -> None:
    usuario_servicio = UsuarioServicio()
    categoria_servicio = CategoriaServicio()
    producto_servicio = ProductoServicio(categoria_servicio)
    pedido_servicio = PedidoServicio(usuario_servicio, producto_servicio)
    usuario_admin = Usuario("Ana", "Pérez", "admin@foodstore.com", "+5491234567890", "admin123", Rol.ADMIN)
    usuario_servicio.agregar(usuario_admin)

    while True:
        usuario = login(usuario_servicio)
        if usuario is None:
            break
        menu = crear_menu(usuario, usuario_servicio, categoria_servicio, producto_servicio, pedido_servicio)
        if not menu.mostrar():
            break
    print()
    mostrar_sistema("Gracias por usar FOOD STORE.")

if __name__ == "__main__":
    main()

# Hacer prueba completa
# Hacer cambio de metodo para titulos en clase Menu, moviendolo a consola.presentacion
