from enum import Enum

class Estado(Enum):
    PENDIENTE = "Pendiente"
    CONFIRMADO = "Confirmado"
    TERMINADO = "Terminado"
    CANCELADO = "Cancelado"