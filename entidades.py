"""
Entidades base del sistema: clase abstracta Entidad y clase Cliente.
"""
from abc import ABC, abstractmethod
import logging

from excepciones import ValidacionError


class Entidad(ABC):
    """Clase abstracta que representa cualquier entidad general del sistema."""

    @abstractmethod
    def validar(self):
        """Cada entidad debe validar sus propios datos."""
        pass


class Cliente(Entidad):
    """Cliente de Software FJ. Sus datos personales están encapsulados."""

    def __init__(self, nombre, documento, correo, telefono):
        # Atributos privados (encapsulación)
        self.__nombre = nombre
        self.__documento = documento
        self.__correo = correo
        self.__telefono = telefono

        # Si algún dato es inválido, validar() lanza ValidacionError
        self.validar()

        logging.info(
            f"Cliente registrado: {self.__nombre} "
            f"(Doc: {self.__documento})"
        )

    def validar(self):
        """Valida nombre, documento, correo y teléfono del cliente."""

        # El nombre debe ser texto no vacío
        if not isinstance(self.__nombre, str) or not self.__nombre.strip():
            raise ValidacionError(
                "El nombre del cliente no puede estar vacío."
            )

        # El documento es obligatorio
        if self.__documento is None or not str(self.__documento).strip():
            raise ValidacionError("El documento es obligatorio.")

        # Validación básica de correo: debe tener '@' y '.'
        if "@" not in str(self.__correo) or "." not in str(self.__correo):
            raise ValidacionError(
                "El correo no tiene un formato válido."
            )

        # Teléfono numérico de mínimo 7 dígitos
        if (
            not str(self.__telefono).isdigit()
            or len(str(self.__telefono)) < 7
        ):
            raise ValidacionError(
                "El teléfono debe ser numérico y mínimo de 7 dígitos."
            )

    # Métodos de acceso (getters)
    def obtener_nombre(self):
        return self.__nombre

    def obtener_documento(self):
        return self.__documento

    def __str__(self):
        return (
            f"Cliente: {self.__nombre} | "
            f"Doc: {self.__documento} | "
            f"Correo: {self.__correo}"
        )
