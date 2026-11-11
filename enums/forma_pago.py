from enum import Enum

class FormaPago(Enum):
    """Formas de pago disponibles."""

    TARJETA = "Tarjeta"
    TRANSFERENCIA = "Transferencia"
    EFECTIVO = "Efectivo"
