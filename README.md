# UTN TUP - TPI Programación 2 (Food Store)

## Descripción del programa

Este programa es una aplicación de consola orientada a la gestión integral de un negocio de comidas (**Food Store**). El sistema permite gestionar categorías, productos, usuarios y pedidos mediante un menú dinámico adaptado por roles (Administrador y Cliente). Incorpora autenticación de usuarios, manejo de excepciones propias, validación rigurosa de entradas y almacenamiento en memoria mediante colecciones.

## Credenciales del Administrador Inicial

Para ingresar por primera vez al sistema como administrador, utilice las siguientes credenciales predeterminadas cargadas al iniciar la aplicación:

- **Email:** `admin@foodstore.com`
- **Contraseña:** `admin123`

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

### Ejemplo 1: Inicio de sesión exitoso como Administrador

- **Entrada:**
  - Mail: `admin@foodstore.com`
  - Contraseña: `admin123`
- **Salida:** `"Bienvenido/a, Ana Pérez [ADMIN]"` seguido del menú completo de gestión (Categorías, Productos, Usuarios, Pedidos).

### Ejemplo 2: Intento fallido de autenticación

- **Entrada:**
  - Mail: `admin@foodstore.com`
  - Contraseña: `clave_incorrecta`
- **Salida:** `"Mail o contraseña incorrectos"` (Tras 3 intentos fallidos, el programa informa el bloqueo de sesión y finaliza la ejecución).

### Ejemplo 3: Creación de un pedido sin stock suficiente

- **Entrada:** Selección de un producto con stock insuficiente al armar el detalle de un pedido.
- **Salida:** `"Error: StockInsuficienteError - La cantidad solicitada supera el stock disponible del producto."` (El pedido se cancela sin modificar los datos guardados).

### Ejemplo 4: Intento de eliminación de una categoría con productos activos

- **Entrada:** Selección de la opción para eliminar una categoría asociada a productos no eliminados.
- **Salida:** `"Error: OperacionNoPermitidaError - No se puede eliminar la categoría porque contiene productos activos asociados."`

## Participación de los integrantes

### Juan Santiago Arango ([@jsacode-dev](https://github.com/jsacode-dev))

- Tarea 1
- Tarea 2
- Tarea 3

### Romina Correa ([@Romi171](https://github.com/Romi171))

- Tarea 1
- Tarea 2
- Tarea 3

## Links útiles

- [Repositorio del proyecto en GitHub](https://github.com/jsacode-dev/utntup-tpi-programacion2)
- [Link del video explicativo / demostración](https://drive.google.com/file/d/TU_ID_VIDEO_DEMO/view?usp=sharing)

# HACER PÚBLICO EL REPOSITORIO
