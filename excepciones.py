"""
Módulo de excepciones personalizadas y configuración del registro de logs.
Software FJ - Fase 4 (Programación 213023, UNAD).
"""
import logging

# Configuración del archivo de registros (eventos y errores del sistema)
logging.basicConfig(
    filename="logs.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)


class SistemaError(Exception):
    """Clase base para todas las excepciones del sistema Software FJ."""
    pass


class ValidacionError(SistemaError):
    """Errores en datos de entrada (datos inválidos o faltantes)."""
    pass


class ReservaError(SistemaError):
    """Errores en el flujo o estados de una reserva (operaciones no permitidas)."""
    pass


class ServicioNoDisponibleError(SistemaError):
    """Se intenta reservar un servicio que está inactivo."""
    pass

