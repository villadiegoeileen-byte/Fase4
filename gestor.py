"""
GestorSistema: administra las listas internas de clientes, servicios y
reservas (sin base de datos).
"""
import logging

from entidades import Cliente
from servicio import Servicio
from reserva import Reserva
from excepciones import ValidacionError


class GestorSistema:
    """Centraliza el manejo de las listas internas del sistema."""

    def __init__(self):
        # Listas privadas (encapsulación)
        self.__clientes = []
        self.__servicios = []
        self.__reservas = []

    # ---------- Registro ----------
    def registrar_cliente(self, cliente):
        """Agrega un cliente; no permite documentos repetidos."""
        if not isinstance(cliente, Cliente):
            raise ValidacionError("Solo se pueden registrar objetos Cliente.")

        for existente in self.__clientes:
            if existente.obtener_documento() == cliente.obtener_documento():
                raise ValidacionError(
                    f"Ya existe un cliente con documento "
                    f"{cliente.obtener_documento()}."
                )

        self.__clientes.append(cliente)
        logging.info(f"Cliente agregado al sistema: {cliente.obtener_nombre()}")

    def registrar_servicio(self, servicio):
        """Agrega un servicio; no permite IDs repetidos."""
        if not isinstance(servicio, Servicio):
            raise ValidacionError("Solo se pueden registrar objetos Servicio.")

        for existente in self.__servicios:
            if existente.obtener_id() == servicio.obtener_id():
                raise ValidacionError(
                    f"Ya existe un servicio con ID {servicio.obtener_id()}."
                )

        self.__servicios.append(servicio)
        logging.info(f"Servicio agregado al sistema: {servicio.obtener_nombre()}")

    def registrar_reserva(self, reserva):
        """Agrega una reserva a la lista interna."""
        if not isinstance(reserva, Reserva):
            raise ValidacionError("Solo se pueden registrar objetos Reserva.")

        self.__reservas.append(reserva)

    # ---------- Búsquedas ----------
    def obtener_cliente(self, documento):
        for c in self.__clientes:
            if c.obtener_documento() == documento:
                return c
        raise ValidacionError(f"No existe un cliente con documento {documento}.")

    def obtener_servicio(self, id_servicio):
        for s in self.__servicios:
            if s.obtener_id() == id_servicio:
                return s
        raise ValidacionError(f"No existe un servicio con ID {id_servicio}.")

    def obtener_reserva(self, id_reserva):
        for r in self.__reservas:
            if r.obtener_id() == id_reserva:
                return r
        raise ValidacionError(f"No existe una reserva con ID {id_reserva}.")

    # ---------- Consultas (devuelven copias para proteger las listas) ----------
    @property
    def clientes(self):
        return list(self.__clientes)

    @property
    def servicios(self):
        return list(self.__servicios)

    @property
    def reservas(self):
        return list(self.__reservas)
