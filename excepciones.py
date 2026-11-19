
import logging

# Configuración del archivo de registros
logging.basicConfig(
    filename="logs.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)


class SistemaError(Exception):
    """Clase base para las excepciones del sistema Software FJ."""
    pass


class ValidacionError(SistemaError):
    """Excepción para errores en datos de entrada."""
    pass


class ReservaError(SistemaError):
    """Excepción para errores en flujo o estados de reserva."""
    pass


class ServicioNoDisponibleError(SistemaError):
    """Excepción cuando se intenta reservar un servicio inactivo."""
    pass
