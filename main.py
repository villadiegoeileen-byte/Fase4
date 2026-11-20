"""
UNAD - Programación (213023)
Fase 4 - Prácticas Simuladas
Software FJ

Integrantes:
- NEIFER ALEXANDER CASTRO SÁNCHEZ
- EILEEN KATERINE VILLADIEGO ARGEL
"""

import logging

from excepciones import SistemaError
from entidades import Cliente
from servicio import (
    ReservaSalas,
    AlquilerEquipos,
    AsesoriasEspecializadas
)
from reserva import Reserva
from gestor import GestorSistema


def ejecutar_simulacion():
    """Ejecuta las operaciones simuladas sin detener el sistema ante errores."""

    print("=" * 70)
    print(" SOFTWARE FJ - SISTEMA INTEGRAL DE GESTIÓN Y RESERVAS")
    print("=" * 70)

    # Gestor con las listas internas (sin base de datos)
    gestor = GestorSistema()

    def operacion(num, titulo, accion):
        """Ejecuta una operación con try/except/else/finally."""

        print(f"\n--- Operación {num}: {titulo} ---")

        try:
            accion()

        except SistemaError as e:
            # Excepciones propias del sistema (errores controlados)
            print(f"❌ Excepción Controlada [{type(e).__name__}]: {e}")
            mensaje = f"Operación {num} fallida: {e}"

            # Si la excepción está encadenada, se muestra la causa original
            if e.__cause__ is not None:
                print(
                    f"   ↳ Causa original "
                    f"[{type(e.__cause__).__name__}]: {e.__cause__}"
                )
                mensaje += f" | Causa original: {e.__cause__}"

            logging.error(mensaje)

        except Exception as e:
            # Cualquier error no previsto: se registra y el sistema continúa
            print(f"💥 Error Inesperado: {e}")
            logging.exception(f"Error inesperado en operación {num}")

        else:
            # Se ejecuta solo si no hubo ninguna excepción
            print(f"✅ Operación {num} ejecutada correctamente.")

        finally:
            # Se ejecuta siempre, haya o no error
            logging.info(f"Finalización de operación {num}")

    # OPERACIÓN 1: Registro de cliente válido
    def op1():
        cliente = Cliente(
            "Neifer Castro",
            "1098765432",
            "neifer@softwarefj.com",
            "3001234567"
        )
        gestor.registrar_cliente(cliente)
        print(f"Registrado: {cliente}")

    operacion(1, "Registro de cliente válido", op1)

    # OPERACIÓN 2: Correo inválido
    def op2():
        gestor.registrar_cliente(Cliente(
            "Cristian Chala",
            "1012345678",
            "correo_sin_arroba",
            "3119876543"
        ))

    operacion(2, "Registro de cliente con correo inválido", op2)

    # OPERACIÓN 3: Teléfono incorrecto
    def op3():
        gestor.registrar_cliente(Cliente(
            "Eileen Villadiego",
            "1055544433",
            "eileen@softwarefj.com",
            "123"
        ))

    operacion(3, "Registro de cliente con teléfono insuficiente", op3)

    # OPERACIÓN 4: Creación de sala válida
    def op4():
        servicio = ReservaSalas(
            "SALA-01",
            "Sala de Audiencias Exec",
            tarifa_base=80.0,
            capacidad_personas=25
        )
        gestor.registrar_servicio(servicio)
        print(servicio.descripcion_servicio())

    operacion(4, "Creación de servicio de sala", op4)

    # OPERACIÓN 5: Servicio con tarifa negativa
    def op5():
        gestor.registrar_servicio(AlquilerEquipos(
            "EQ-01",
            "Laptops Dev",
            tarifa_base=-45.0,
            cantidad_equipos=5
        ))

    operacion(5, "Servicio con tarifa negativa", op5)

    # OPERACIÓN 6: Creación de servicios válidos
    def op6():
        equipos = AlquilerEquipos(
            "EQ-02",
            "Servidores Prueba",
            tarifa_base=120.0,
            cantidad_equipos=2
        )
        asesoria = AsesoriasEspecializadas(
            "ASE-01",
            "Arquitectura Cloud",
            tarifa_base=150.0,
            nivel_consultor="Senior"
        )
        gestor.registrar_servicio(equipos)
        gestor.registrar_servicio(asesoria)

        print(
            f"Servicios registrados. Total activos: "
            f"{len(gestor.servicios)}"
        )

    operacion(6, "Creación de servicios válidos", op6)

    # OPERACIÓN 7: Reserva y confirmación exitosa
    def op7():
        reserva = Reserva(
            "RES-001",
            gestor.obtener_cliente("1098765432"),
            gestor.obtener_servicio("SALA-01"),
            duracion=3
        )
        gestor.registrar_reserva(reserva)

        total = reserva.confirmar(descuento=10, impuesto=19)

        print(reserva)
        print(f"Monto total procesado: ${total}")

    operacion(7, "Reserva y confirmación válida", op7)

    # OPERACIÓN 8: Reservar un servicio inactivo
    def op8():
        sala = gestor.obtener_servicio("SALA-01")
        sala.cambiar_disponibilidad(False)

        reserva = Reserva(
            "RES-002",
            gestor.obtener_cliente("1098765432"),
            sala,
            duracion=2
        )
        gestor.registrar_reserva(reserva)

    operacion(8, "Reserva sobre servicio inactivo", op8)

    # OPERACIÓN 9: Confirmar nuevamente una reserva ya confirmada
    def op9():
        gestor.obtener_reserva("RES-001").confirmar()

    operacion(9, "Reconfirmación de reserva", op9)

    # OPERACIÓN 10: Doble cancelación
    def op10():
        sala = gestor.obtener_servicio("SALA-01")
        sala.cambiar_disponibilidad(True)

        reserva = Reserva(
            "RES-003",
            gestor.obtener_cliente("1098765432"),
            sala,
            duracion=4
        )
        gestor.registrar_reserva(reserva)

        reserva.cancelar()
        print(f"Cancelación inicial: {reserva.obtener_estado()}")

        print("Intentando cancelar nuevamente...")
        reserva.cancelar()

    operacion(10, "Doble cancelación de reserva", op10)

    # OPERACIÓN 11: Encadenamiento de excepciones (cálculo inconsistente)
    def op11():
        reserva = Reserva(
            "RES-004",
            gestor.obtener_cliente("1098765432"),
            gestor.obtener_servicio("SALA-01"),
            duracion=2
        )
        gestor.registrar_reserva(reserva)

        # Descuento de 150% -> ValidacionError encadenada como ReservaError
        reserva.confirmar(descuento=150)

    operacion(11, "Encadenamiento de excepciones en el cálculo", op11)

    # OPERACIÓN 12: Polimorfismo y variantes del cálculo de costos
    def op12():
        for servicio in gestor.servicios:
            print(servicio.descripcion_servicio())
            print(f"   Simple (2):            ${servicio.costo_simple(2)}")
            print(f"   Con descuento 10%:     ${servicio.costo_con_descuento(2, 10)}")
            print(f"   Con impuesto 19%:      ${servicio.costo_con_impuesto(2, 19)}")
            print(f"   Completo (10% y 19%):  ${servicio.calcular_costo(2, 10, 19)}")

    operacion(12, "Polimorfismo y cálculo de costos con variantes", op12)

    # OPERACIÓN 13: Cliente duplicado
    def op13():
        gestor.registrar_cliente(Cliente(
            "Neifer Duplicado",
            "1098765432",
            "otro@softwarefj.com",
            "3005557788"
        ))

    operacion(13, "Registro de cliente con documento duplicado", op13)

    # OPERACIÓN 14: Parámetros faltantes (cliente None)
    def op14():
        Reserva(
            "RES-005",
            None,
            gestor.obtener_servicio("EQ-02"),
            duracion=1
        )

    operacion(14, "Reserva con parámetros faltantes", op14)

    # OPERACIÓN 15: Procesamiento exitoso de una reserva
    def op15():
        reserva = Reserva(
            "RES-006",
            gestor.obtener_cliente("1098765432"),
            gestor.obtener_servicio("ASE-01"),
            duracion=2
        )
        gestor.registrar_reserva(reserva)

        total = reserva.procesar(descuento=5, impuesto=19)
        print(reserva)
        print(f"Total procesado: ${total}")

    operacion(15, "Procesamiento completo de una reserva", op15)

    print("\n" + "=" * 70)
    print(" SIMULACIÓN CONCLUIDA SIN DETENER EL SISTEMA")
    print(f" Clientes registrados: {len(gestor.clientes)}")
    print(f" Servicios registrados: {len(gestor.servicios)}")
    print(f" Reservas registradas: {len(gestor.reservas)}")
    print(" Historial guardado en logs.txt")
    print("=" * 70)


if __name__ == "__main__":
    ejecutar_simulacion()
