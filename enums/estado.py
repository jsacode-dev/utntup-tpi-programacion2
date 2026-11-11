from enum import Enum

class Estado(Enum):
    """Estados posibles de un pedido."""

    PENDIENTE = "Pendiente"
    CONFIRMADO = "Confirmado"
    TERMINADO = "Terminado"
    CANCELADO = "Cancelado"
