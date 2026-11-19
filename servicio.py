
from abc import abstractmethod
import logging

from entidades import Entidad
from excepciones import ValidacionError


class Servicio(Entidad):

    def __init__(self, id_servicio, nombre_servicio, tarifa_base, disponible=True):
        self._id_servicio = id_servicio
        self._nombre_servicio = nombre_servicio
        self._tarifa_base = tarifa_base
        self._disponible = disponible

        self.validar()

    def validar(self):

        if not str(self._id_servicio).strip():
            raise ValidacionError("El ID del servicio no puede estar vacío.")

        if not isinstance(self._nombre_servicio, str) or not self._nombre_servicio.strip():
            raise ValidacionError("El nombre del servicio no puede estar vacío.")

        if not isinstance(self._tarifa_base, (int, float)) or self._tarifa_base <= 0:
            raise ValidacionError("La tarifa base debe ser mayor a cero.")

    @abstractmethod
    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        pass

    @abstractmethod
    def descripcion_servicio(self):
        pass

    def esta_disponible(self):
        return self._disponible

    def cambiar_disponibilidad(self, estado: bool):
        self._disponible = estado
        logging.info(
            f"Servicio '{self._nombre_servicio}' disponible: {estado}"
        )

    def obtener_nombre(self):
        return self._nombre_servicio


class ReservaSalas(Servicio):

    def __init__(
        self,
        id_servicio,
        nombre_servicio,
        tarifa_base,
        capacidad_personas,
        incluye_proyector=True,
        disponible=True
    ):
        self.__capacidad = capacidad_personas
        self.__incluye_proyector = incluye_proyector

        super().__init__(
            id_servicio,
            nombre_servicio,
            tarifa_base,
            disponible
        )

    def validar(self):
        super().validar()

        if not isinstance(self.__capacidad, int) or self.__capacidad <= 0:
            raise ValidacionError(
                "La capacidad de la sala debe ser un entero positivo."
            )

    def calcular_costo(self, duracion, descuento=0, impuesto=0):

        if duracion <= 0:
            raise ValidacionError(
                "La duración debe ser mayor a 0 horas."
            )

        costo = self._tarifa_base * duracion

        if self.__capacidad > 20:
            costo += 50.0

        if descuento > 0:
            costo -= costo * (descuento / 100)

        if impuesto > 0:
            costo += costo * (impuesto / 100)

        return round(costo, 2)

    def descripcion_servicio(self):

        proyector = (
            "Con proyector"
            if self.__incluye_proyector
            else "Sin proyector"
        )

        return (
            f"[Reserva de Sala] {self._nombre_servicio} "
            f"(Capacidad: {self.__capacidad} pers. | {proyector})"
        )


class AlquilerEquipos(Servicio):

    def __init__(
        self,
        id_servicio,
        nombre_servicio,
        tarifa_base,
        cantidad_equipos,
        deposito_garantia=100.0,
        disponible=True
    ):
        self.__cantidad = cantidad_equipos
        self.__deposito = deposito_garantia

        super().__init__(
            id_servicio,
            nombre_servicio,
            tarifa_base,
            disponible
        )

    def validar(self):
        super().validar()

        if not isinstance(self.__cantidad, int) or self.__cantidad <= 0:
            raise ValidacionError(
                "La cantidad de equipos debe ser mayor a cero."
            )

    def calcular_costo(self, duracion, descuento=0, impuesto=0):

        if duracion <= 0:
            raise ValidacionError(
                "La duración del alquiler debe ser mayor a 0 días."
            )

        costo = (
            self._tarifa_base * self.__cantidad * duracion
        )

        if descuento > 0:
            costo -= costo * (descuento / 100)

        if impuesto > 0:
            costo += costo * (impuesto / 100)

        return round(costo, 2)

    def descripcion_servicio(self):

        return (
            f"[Alquiler Equipos] {self._nombre_servicio} "
            f"(Cant: {self.__cantidad} unid. | "
            f"Depósito: ${self.__deposito})"
        )


class AsesoriasEspecializadas(Servicio):

    def __init__(
        self,
        id_servicio,
        nombre_servicio,
        tarifa_base,
        nivel_consultor="Senior",
        disponible=True
    ):
        self.__nivel_consultor = nivel_consultor

        super().__init__(
            id_servicio,
            nombre_servicio,
            tarifa_base,
            disponible
        )

    def validar(self):
        super().validar()

        if self.__nivel_consultor not in [
            "Junior",
            "Semi-Senior",
            "Senior"
        ]:
            raise ValidacionError("Nivel de consultor inválido.")

    def calcular_costo(self, duracion, descuento=0, impuesto=0):

        if duracion <= 0:
            raise ValidacionError(
                "La duración debe ser mayor a 0 horas."
            )

        multiplicadores = {
            "Junior": 1.0,
            "Semi-Senior": 1.3,
            "Senior": 1.6
        }

        costo = (
            self._tarifa_base
            * duracion
            * multiplicadores[self.__nivel_consultor]
        )

        if descuento > 0:
            costo -= costo * (descuento / 100)

        if impuesto > 0:
            costo += costo * (impuesto / 100)

        return round(costo, 2)

    def descripcion_servicio(self):

        return (
            f"[Asesoría Técnica] {self._nombre_servicio} "
            f"(Consultor: {self.__nivel_consultor})"
        )
