# UTN TUP - TPI Programación 2 (Food Store)

## Descripción del programa

Este programa es una aplicación de consola orientada a la gestión integral de un negocio de comidas (**Food Store**). El sistema permite gestionar categorías, productos, usuarios y pedidos mediante un menú dinámico adaptado por roles (Administrador y Cliente). Incorpora autenticación de usuarios, manejo de excepciones propias, validación rigurosa de entradas y almacenamiento en memoria mediante colecciones.

## Credenciales del Administrador Inicial

Para ingresar por primera vez al sistema como administrador, utilice las siguientes credenciales predeterminadas cargadas al iniciar la aplicación:

- **Email:** `admin@foodstore.com`
- **Contraseña:** `admin123`

Los demás usuarios (administradores y clientes) se crean desde el menú **Usuarios** del administrador. Los IDs se asignan automáticamente desde `0`, en orden de creación, con un contador compartido por todas las entidades.

## Instrucciones de uso

### Requisitos previos

- Python 3.12.x o superior instalado en el sistema (Python 3.15.2 recomendado).

- Instalación de biblioteca externa:

```bash
pip install rich
```

> La libreria `rich` se emplea para mostrar tablas y otros elementos de forma más atractiva, también dando color y estilo a los mensajes en la consola.

> [!CAUTION]
> La instalación de esta libreria es obligatoria para el correcto funcionamiento del programa. Recomendamos utilizar un entorno virtual (`venv`) para instalar la dependencia y evitar conflictos con otras bibliotecas instaladas globalmente.

### Ejecución del programa

1. Clonar el repositorio o descargar los archivos del proyecto.

2. Navegar al directorio raíz del proyecto (`food_store`) en la terminal o línea de comandos.

3. Ejecutar el programa principal con el comando:

```bash
python main.py
```

4. Para ejecutar la suite de pruebas unitarias y de validación del modelo/servicios:

```bash
python pruebas.py
```

5. Seguir las instrucciones interactivas en pantalla e ingresar credenciales según el rol deseado.

## Ejemplos de entradas/salidas

Los ejemplos asumen que existen los datos necesarios (productos, usuarios y pedidos) cargados previamente.

### Ejemplo 1: Inicio de sesión exitoso como administrador

- **Entrada:**
  - Email: `admin@foodstore.com`
  - Contraseña: `admin123`
- **Salida:**

```text
Bienvenido/a Ana Pérez (Administrador).
```

Luego se muestra el menú principal: Categorías, Productos, Usuarios, Pedidos, Cerrar sesión y Salir.

### Ejemplo 2: Credenciales incorrectas

- **Entrada:**
  - Email: `admin@foodstore.com`
  - Contraseña: `clave_incorrecta`
- **Salida:**

```text
Mail o contraseña incorrectos.
```

Tras 3 intentos fallidos se muestra `Ha agotado todos los intentos para iniciar sesión.` y el programa finaliza.

### Ejemplo 3: Alta de usuario con mail repetido

- **Entrada** (Usuarios > Crear): Mail `admin@foodstore.com`
- **Salida:**

```text
Ya existe un usuario con ese mail.
```

El sistema vuelve a pedir el mail hasta que ingrese uno libre.

### Ejemplo 4: Pedido con stock insuficiente

- **Entrada** (Pedidos > Crear): ID de usuario `1`, forma de pago `1` (Tarjeta), ID de producto `2` (Jugo, con stock 5), cantidad `10`.
- **Salida:**

```text
Stock insuficiente de Jugo. Disponible: 5.
```

El pedido no se guarda y el stock no se modifica.

### Ejemplo 5: Cliente consulta el detalle de un pedido propio

- **Entrada:** inicio de sesión como cliente, opción Mis pedidos, ID de pedido `1`.
- **Salida:** una tabla con el detalle, por ejemplo:

```text
       Detalle del pedido 1
┏━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┓
┃ Producto ┃ Cantidad ┃ Subtotal ┃
┡━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━┩
│ Jugo     │ 2        │ 1600.0   │
└──────────┴──────────┴──────────┘
Total: $1600.0
```

### Ejemplo 6: Cliente intenta ver un pedido de otro usuario

- **Entrada:** inicio de sesión como cliente, opción Mis pedidos, ID de un pedido ajeno `3`.
- **Salida:**

```text
Pedido con ID 3 no encontrado.
```

## Participación de los integrantes

### Juan Santiago Arango ([@jsacode-dev](https://github.com/jsacode-dev))

- Épica 0 (Acceso al sistema): Entidad Usuario, servicio de autenticación y sistema de menús polimórficos.
- Ëpica 2 (Gestión de productos): Entidad Producto, servicio de productos y su submenú con filtros
- Épica 3 (Gestión de usuarios): Gestión de usuarios en consola (ABM admin y "Ver mis datos" cliente).
- Épica 4 (Gestión de pedidos y detalles): Entidades Pedido y DetallePedido, lógica de stock/estados y menús de pedidos.
- Script de pruebas (pruebas.py).
- Edición del video de demostración.
- Repositorio de GitHub y README.MD.

### Romina Correa ([@Romi171](https://github.com/Romi171))

- Estructura de paquetes (entidades, servicios, consola, enums, excepciones) y main.py / pruebas.py.
- Jerarquía de excepciones propias (FoodStoreError y subclases).
- Enumerados (Rol, Estado, FormaPago).
- Clase abstracta Base e interfaz Calculable.
- Épica 1 (Gestión de categorías): Entidad Categoria, servicio de categorías y su submenú de consola.
- Informe técnico en PDF.

## Links útiles

- [Repositorio del proyecto en GitHub](https://github.com/jsacode-dev/utntup-tpi-programacion2)
- ~~Link del video explicativo / demostración~~ (Por el momento el video no está disponible)
