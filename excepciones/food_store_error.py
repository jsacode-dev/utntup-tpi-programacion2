class FoodStoreError(Exception):
    """Excepción base para errores del sistema."""

    pass

class EntidadNoEncontradaError(FoodStoreError):
    """Se lanza cuando no se encuentra una entidad solicitada."""

    pass

class DatoInvalidoError(FoodStoreError):
    """Se lanza cuando un dato no cumple con las validaciones requeridas."""

    pass

class PrecioInvalidoError(FoodStoreError):
    """Se lanza cuando el precio de un producto es inválido."""

    pass

class StockInsuficienteError(FoodStoreError):
    """Se lanza cuando no hay stock suficiente para una operación."""

    pass

class DuplicadoError(FoodStoreError):
    """Se lanza cuando se intenta crear una entidad que ya existe."""

    pass

class OperacionNoPermitidaError(FoodStoreError):
    """Se lanza cuando se intenta ejecutar una operación no permitida."""

    pass

class CredencialesInvalidasError(FoodStoreError):
    """Se lanza cuando las credenciales de autenticación son incorrectas."""

    pass
