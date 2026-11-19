
from abc import ABC, abstractmethod
import logging

from excepciones import ValidacionError


class Entidad(ABC):

    @abstractmethod
    def validar(self):
        pass


class Cliente(Entidad):

    def __init__(self, nombre, documento, correo, telefono):
        self.__nombre = nombre
        self.__documento = documento
        self.__correo = correo
        self.__telefono = telefono

        self.validar()

        logging.info(
            f"Cliente registrado: {self.__nombre} "
            f"(Doc: {self.__documento})"
        )

    def validar(self):

        if not isinstance(self.__nombre, str) or not self.__nombre.strip():
            raise ValidacionError(
                "El nombre del cliente no puede estar vacío."
            )

        if not str(self.__documento).strip():
            raise ValidacionError("El documento es obligatorio.")

        if "@" not in str(self.__correo) or "." not in str(self.__correo):
            raise ValidacionError(
                "El correo no tiene un formato válido."
            )

        if (
            not str(self.__telefono).isdigit()
            or len(str(self.__telefono)) < 7
        ):
            raise ValidacionError(
                "El teléfono debe ser numérico y mínimo de 7 dígitos."
            )

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
