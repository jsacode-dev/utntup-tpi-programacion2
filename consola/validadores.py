import math
import re

from consola.presentacion import mostrar_error
from excepciones.food_store_error import DatoInvalidoError

def es_email_valido(valor: str) -> bool:
    patron_email = re.compile(r"[\w.-]+@[\w.-]+\.\w+")
    return patron_email.fullmatch(valor.strip()) is not None

def validar_texto(m_entrada: str, m_salida: str | None = None, salto_valor: bool = False) -> str | None:
    while True:
        try:
            valor = input(m_entrada)
            if salto_valor and not valor.strip():
                return None
            if not valor.strip():
                raise DatoInvalidoError("No se permite un valor vacío.")
            if m_salida is not None:
                print(m_salida)
            return valor.strip()
        except DatoInvalidoError as e:
            mostrar_error(str(e))

def validar_numero(m_entrada: str, m_salida: str | None = None, decimal: bool = False, no_negativo: bool = False, cero_incluido: bool = True, minimo: int | float | None = None, maximo: int | float | None = None, salto_valor: bool = False) -> int | float | None:
    while True:
        try:
            valor = input(m_entrada).strip().replace(",", ".")
            if salto_valor and not valor:
                return None
            if not valor:
                raise DatoInvalidoError("No se permite un valor vacío.")
            try:
                numero: int | float = float(valor) if decimal else int(valor)
            except ValueError:
                raise DatoInvalidoError("Debe ingresar un número válido.") from None
            if isinstance(numero, float) and not math.isfinite(numero): # Se usa math.isfinite para verificar que el número sea finito (no infinito[inf, -inf] ni NaN[nan])
                raise DatoInvalidoError("Debe ingresar un número válido.")
            if no_negativo and numero < 0:
                raise DatoInvalidoError("No se permiten números negativos.")
            if not cero_incluido and numero == 0:
                raise DatoInvalidoError("No se permite el cero.")
            validar_numero_rango(numero, minimo, maximo)
            if m_salida is not None:
                print(m_salida)
            return numero
        except DatoInvalidoError as e:
            mostrar_error(str(e))

def validar_email(m_entrada: str, m_salida: str | None = None, salto_valor: bool = False) -> str | None:
    while True:
        try:
            valor = input(m_entrada).strip()
            if salto_valor and not valor:
                return None
            if not valor:
                raise DatoInvalidoError("No se permite un valor vacío.")
            if not es_email_valido(valor):
                raise DatoInvalidoError("Debe ingresar un email válido.")
            if m_salida is not None:
                print(m_salida)
            return valor
        except DatoInvalidoError as e:
            mostrar_error(str(e))

def validar_numero_rango(numero: int | float, minimo: int | float | None = None, maximo: int | float | None = None) -> None:
    if minimo is not None and numero < minimo:
        raise DatoInvalidoError(f"El valor debe ser mayor o igual a {minimo}.")
    if maximo is not None and numero > maximo:
        raise DatoInvalidoError(f"El valor debe ser menor o igual a {maximo}.")
