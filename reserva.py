"""
Clase Reserva: integra cliente, servicio, duración y estado.
"""
import logging

from entidades import Entidad, Cliente
from servicio import Servicio
from excepciones import (
    ValidacionError,
    ReservaError,
    ServicioNoDisponibleError
)


class Reserva(Entidad):
    """Reserva de un servicio por parte de un cliente."""

    def __init__(
        self,
        id_reserva,
        cliente: Cliente,
        servicio: Servicio,
        duracion: int
    ):
        self.__id_reserva = id_reserva
        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion
        self.__estado = "Pendiente"   # Estados: Pendiente, Confirmada, Cancelada

        self.validar()

        logging.info(
            f"Reserva creada [ID: {self.__id_reserva}] "
            f"para {self.__cliente.obtener_nombre()}"
        )

    def validar(self):
        """Valida los datos de la reserva y la disponibilidad del servicio."""

        if self.__id_reserva is None or not str(self.__id_reserva).strip():
            raise ValidacionError(
                "El ID de la reserva no puede estar vacío."
            )

        # Parámetros faltantes o de tipo incorrecto
        if not isinstance(self.__cliente, Cliente):
            raise ValidacionError(
                "Requiere un objeto Cliente válido."
            )

        if not isinstance(self.__servicio, Servicio):
            raise ValidacionError(
                "Requiere un objeto Servicio válido."
            )

        if (
            not isinstance(self.__duracion, int)
            or self.__duracion <= 0
        ):
            raise ValidacionError(
                "La duración debe ser un entero positivo."
            )

        # No se puede reservar un servicio inactivo
        if not self.__servicio.esta_disponible():
            raise ServicioNoDisponibleError(
                f"El servicio '{self.__servicio.obtener_nombre()}' "
                f"no está disponible."
            )

    def confirmar(self, descuento=0, impuesto=19):
        """Confirma la reserva y devuelve el total a pagar."""

        if self.__estado == "Confirmada":
            raise ReservaError(
                f"La reserva ID {self.__id_reserva} "
                "ya está confirmada."
            )

        if self.__estado == "Cancelada":
            raise ReservaError(
                f"No se puede confirmar la reserva ID "
                f"{self.__id_reserva} porque fue cancelada."
            )

        try:
            total = self.__servicio.calcular_costo(
                self.__duracion,
                descuento,
                impuesto
            )
        except ValidacionError as e:
            # ENCADENAMIENTO DE EXCEPCIONES: la causa original queda
            # ligada a la nueva excepción mediante "from e"
            raise ReservaError(
                f"No se pudo confirmar la reserva ID "
                f"{self.__id_reserva}: cálculo de costo inválido."
            ) from e

        # Solo se cambia el estado si el cálculo fue exitoso
        self.__estado = "Confirmada"

        logging.info(
            f"Reserva ID {self.__id_reserva} CONFIRMADA. "
            f"Total: ${total}"
        )

        return total

    def cancelar(self):
        """Cancela la reserva (no se puede cancelar dos veces)."""

        if self.__estado == "Cancelada":
            raise ReservaError(
                f"La reserva ID {self.__id_reserva} "
                "ya estaba cancelada."
            )

        self.__estado = "Cancelada"

        logging.warning(
            f"Reserva ID {self.__id_reserva} CANCELADA."
        )

    def procesar(self, descuento=0, impuesto=19):
        """Procesa la reserva completa usando try/except/else/finally."""
        try:
            total = self.confirmar(descuento, impuesto)
        except ReservaError as e:
            logging.error(
                f"Procesamiento fallido de {self.__id_reserva}: {e}"
            )
            raise   # Se relanza para que el llamador decida qué hacer
        else:
            logging.info(
                f"Reserva {self.__id_reserva} procesada con éxito. "
                f"Total: ${total}"
            )
            return total
        finally:
            logging.info(
                f"Fin del procesamiento de la reserva {self.__id_reserva}"
            )

    def obtener_estado(self):
        return self.__estado

    def obtener_id(self):
        return self.__id_reserva

    def __str__(self):
        return (
            f"Reserva #{self.__id_reserva} | "
            f"{self.__cliente.obtener_nombre()} | "
            f"{self.__servicio.descripcion_servicio()} | "
            f"Estado: {self.__estado}"
        )
