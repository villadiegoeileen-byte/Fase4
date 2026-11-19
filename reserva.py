
import logging

from entidades import Entidad, Cliente
from servicios import Servicio
from excepciones import (
    ValidacionError,
    ReservaError,
    ServicioNoDisponibleError
)


class Reserva(Entidad):

    def __init__(self, id_reserva, cliente: Cliente, servicio: Servicio, duracion: int):
        self.__id_reserva = id_reserva
        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion
        self.__estado = "Pendiente"

        self.validar()

        logging.info(
            f"Reserva creada [ID: {self.__id_reserva}] "
            f"para {self.__cliente.obtener_nombre()}"
        )

    def validar(self):

        if not str(self.__id_reserva).strip():
            raise ValidacionError(
                "El ID de la reserva no puede estar vacío."
            )

        if not isinstance(self.__cliente, Cliente):
            raise ValidacionError(
                "Requiere un objeto Cliente válido."
            )

        if not isinstance(self.__servicio, Servicio):
            raise ValidacionError(
                "Requiere un objeto Servicio válido."
            )

        if not isinstance(self.__duracion, int) or self.__duracion <= 0:
            raise ValidacionError(
                "La duración debe ser un entero positivo."
            )

        if not self.__servicio.esta_disponible():
            raise ServicioNoDisponibleError(
                f"El servicio '{self.__servicio.obtener_nombre()}' "
                f"no está disponible."
            )

    def confirmar(self, descuento=0, impuesto=19):

        if self.__estado == "Confirmada":
            raise ReservaError(
                f"La reserva ID {self.__id_reserva} ya está confirmada."
            )

        if self.__estado == "Cancelada":
            raise ReservaError(
                f"No se puede confirmar la reserva ID "
                f"{self.__id_reserva} porque fue cancelada."
            )

        total = self.__servicio.calcular_costo(
            self.__duracion,
            descuento,
            impuesto
        )

        self.__estado = "Confirmada"

        logging.info(
            f"Reserva ID {self.__id_reserva} CONFIRMADA. "
            f"Total: ${total}"
        )

        return total

    def cancelar(self):

        if self.__estado == "Cancelada":
            raise ReservaError(
                f"La reserva ID {self.__id_reserva} ya estaba cancelada."
            )

        self.__estado = "Cancelada"

        logging.warning(
            f"Reserva ID {self.__id_reserva} CANCELADA."
        )

    def obtener_estado(self):
        return self.__estado

    def __str__(self):

        return (
            f"Reserva #{self.__id_reserva} | "
            f"{self.__cliente.obtener_nombre()} | "
            f"{self.__servicio.descripcion_servicio()} | "
            f"Estado: {self.__estado}"
        )
      
