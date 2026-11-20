"""
Clase abstracta Servicio y tres servicios especializados:
ReservaSalas, AlquilerEquipos y AsesoriasEspecializadas.
"""
from abc import abstractmethod
import logging

from entidades import Entidad
from excepciones import ValidacionError


class Servicio(Entidad):
    """Clase abstracta base de todos los servicios de Software FJ."""

    def __init__(self, id_servicio, nombre_servicio, tarifa_base, disponible=True):
        # Atributos protegidos: accesibles por las clases hijas
        self._id_servicio = id_servicio
        self._nombre_servicio = nombre_servicio
        self._tarifa_base = tarifa_base
        self._disponible = disponible

        self.validar()

    def validar(self):
        """Valida los datos comunes a todos los servicios."""

        if not str(self._id_servicio).strip():
            raise ValidacionError("El ID del servicio no puede estar vacío.")

        if not isinstance(self._nombre_servicio, str) or not self._nombre_servicio.strip():
            raise ValidacionError("El nombre del servicio no puede estar vacío.")

        if not isinstance(self._tarifa_base, (int, float)) or self._tarifa_base <= 0:
            raise ValidacionError("La tarifa base debe ser mayor a cero.")

    # ---------- Métodos abstractos (polimorfismo) ----------
    @abstractmethod
    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        """Cada servicio calcula su costo de forma distinta."""
        pass

    @abstractmethod
    def descripcion_servicio(self):
        """Cada servicio se describe de forma distinta."""
        pass

    # ---------- Métodos de apoyo comunes ----------
    def _validar_calculo(self, duracion, descuento, impuesto, unidad="horas"):
        """Valida los parámetros del cálculo de costos (cálculos inconsistentes)."""

        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise ValidacionError(
                f"La duración debe ser mayor a 0 {unidad}."
            )

        if not isinstance(descuento, (int, float)) or not 0 <= descuento <= 100:
            raise ValidacionError(
                "El descuento debe estar entre 0 y 100."
            )

        if not isinstance(impuesto, (int, float)) or impuesto < 0:
            raise ValidacionError(
                "El impuesto no puede ser negativo."
            )

    @staticmethod
    def _aplicar_descuento_impuesto(costo, descuento, impuesto):
        """Aplica descuento y luego impuesto (porcentajes) sobre un costo."""
        if descuento > 0:
            costo -= costo * (descuento / 100)

        if impuesto > 0:
            costo += costo * (impuesto / 100)

        return round(costo, 2)

    # ---------- Variantes del cálculo (sobrecarga simulada) ----------
    # Python no tiene sobrecarga real; se simula con parámetros opcionales
    # y con variantes que reciben distintos parámetros.
    def costo_simple(self, duracion):
        """Variante 1: solo duración (sin descuento ni impuesto)."""
        return self.calcular_costo(duracion)

    def costo_con_descuento(self, duracion, descuento):
        """Variante 2: duración y descuento."""
        return self.calcular_costo(duracion, descuento=descuento)

    def costo_con_impuesto(self, duracion, impuesto):
        """Variante 3: duración e impuesto."""
        return self.calcular_costo(duracion, impuesto=impuesto)

    # ---------- Disponibilidad y accesos ----------
    def esta_disponible(self):
        return self._disponible

    def cambiar_disponibilidad(self, estado: bool):
        """Activa o desactiva el servicio y lo registra en el log."""
        self._disponible = estado
        logging.info(
            f"Servicio '{self._nombre_servicio}' disponible: {estado}"
        )

    def obtener_nombre(self):
        return self._nombre_servicio

    def obtener_id(self):
        return self._id_servicio


class ReservaSalas(Servicio):
    """Servicio de reserva de salas (costo por hora)."""

    def __init__(
        self,
        id_servicio,
        nombre_servicio,
        tarifa_base,
        capacidad_personas,
        incluye_proyector=True,
        disponible=True
    ):
        # Se asignan antes de super().__init__ porque validar() los usa
        self.__capacidad = capacidad_personas
        self.__incluye_proyector = incluye_proyector

        super().__init__(
            id_servicio,
            nombre_servicio,
            tarifa_base,
            disponible
        )

    def validar(self):
        """Sobrescribe validar(): añade la validación de capacidad."""
        super().validar()

        if not isinstance(self.__capacidad, int) or self.__capacidad <= 0:
            raise ValidacionError(
                "La capacidad de la sala debe ser un entero positivo."
            )

    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        """Costo = tarifa * horas (+ recargo si capacidad > 20), con descuento e impuesto."""
        self._validar_calculo(duracion, descuento, impuesto, "horas")

        costo = self._tarifa_base * duracion

        # Recargo fijo para salas grandes
        if self.__capacidad > 20:
            costo += 50.0

        return self._aplicar_descuento_impuesto(costo, descuento, impuesto)

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
    """Servicio de alquiler de equipos (costo por equipo y por día)."""

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
        """Sobrescribe validar(): añade la validación de cantidad de equipos."""
        super().validar()

        if not isinstance(self.__cantidad, int) or self.__cantidad <= 0:
            raise ValidacionError(
                "La cantidad de equipos debe ser mayor a cero."
            )

    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        """Costo = tarifa * cantidad de equipos * días, con descuento e impuesto."""
        self._validar_calculo(duracion, descuento, impuesto, "días")

        costo = self._tarifa_base * self.__cantidad * duracion

        return self._aplicar_descuento_impuesto(costo, descuento, impuesto)

    def descripcion_servicio(self):
        return (
            f"[Alquiler Equipos] {self._nombre_servicio} "
            f"(Cant: {self.__cantidad} unid. | "
            f"Depósito: ${self.__deposito})"
        )


class AsesoriasEspecializadas(Servicio):
    """Servicio de asesorías (costo por hora según nivel del consultor)."""

    NIVELES = {
        "Junior": 1.0,
        "Semi-Senior": 1.3,
        "Senior": 1.6
    }

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
        """Sobrescribe validar(): añade la validación del nivel del consultor."""
        super().validar()

        if self.__nivel_consultor not in self.NIVELES:
            raise ValidacionError("Nivel de consultor inválido.")

    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        """Costo = tarifa * horas * multiplicador del nivel, con descuento e impuesto."""
        self._validar_calculo(duracion, descuento, impuesto, "horas")

        costo = (
            self._tarifa_base
            * duracion
            * self.NIVELES[self.__nivel_consultor]
        )

        return self._aplicar_descuento_impuesto(costo, descuento, impuesto)

    def descripcion_servicio(self):
        return (
            f"[Asesoría Técnica] {self._nombre_servicio} "
            f"(Consultor: {self.__nivel_consultor})"
        )
