
"""
UNAD - Programación (213023)
Fase 4 - Prácticas Simuladas: Software FJ

Integrantes Activos:
- NEIFER ALEXANDER CASTRO SÁNCHEZ
- EILEEN KATERINE VILLADIEGO ARGEL
"""

import logging

from excepciones import SistemaError
from entidades import Cliente
from servicios import (
    ReservaSalas,
    AlquilerEquipos,
    AsesoriasEspecializadas
)
from reservas import Reserva


def ejecutar_simulacion():

    print("=" * 70)
    print(" SOFTWARE FJ - SISTEMA INTEGRAL DE GESTIÓN Y RESERVAS")
    print("=" * 70 + "\n")

    clientes = []
    servicios = []
    reservas = []

    def operacion(num, titulo, accion):

        print(f"--- Operación {num}: {titulo} ---")

        try:
            accion()

        except SistemaError as e:
            print(
                f" ❌ Excepción Controlada "
                f"[{type(e).__name__}]: {e}"
            )
            logging.error(f"Operación {num} fallida: {e}")

        except Exception as e:
            print(f" 💥 Error Inesperado: {e}")
            logging.critical(f"Error crítico en Op {num}: {e}")

        print()

    # 1. Cliente válido
    def op1():

        c1 = Cliente(
            "Neifer Castro",
            "1098765432",
            "neifer@softwarefj.com",
            "3001234567"
        )

        clientes.append(c1)

        print(f" ✅ Registrado: {c1}")

    operacion(1, "Registro de cliente válido", op1)

    # 2. Correo inválido
    def op2():

        c2 = Cliente(
            "Cristian Chala",
            "1012345678",
            "correo_sin_arroba",
            "3119876543"
        )

        clientes.append(c2)

    operacion(2, "Registro de cliente con correo inválido", op2)

    # 3. Teléfono corto
    def op3():

        c3 = Cliente(
            "Eileen Villadiego",
            "1055544433",
            "eileen@softwarefj.com",
            "123"
        )

        clientes.append(c3)

    operacion(3, "Registro de cliente con teléfono insuficiente", op3)

    # 4. Servicio Sala
    def op4():

        s1 = ReservaSalas(
            "SALA-01",
            "Sala de Audiencias Exec",
            tarifa_base=80.0,
            capacidad_personas=25
        )

        servicios.append(s1)

        print(f" ✅ Creado: {s1.descripcion_servicio()}")

    operacion(4, "Creación de Servicio de Sala", op4)

    # 5. Tarifa negativa
    def op5():

        s2 = AlquilerEquipos(
            "EQ-01",
            "Laptops Dev",
            tarifa_base=-45.0,
            cantidad_equipos=5
        )

        servicios.append(s2)

    operacion(5, "Servicio con tarifa negativa", op5)

    # 6. Varios Servicios Válidos
    def op6():

        s3 = AlquilerEquipos(
            "EQ-02",
            "Servidores Prueba",
            tarifa_base=120.0,
            cantidad_equipos=2
        )

        s4 = AsesoriasEspecializadas(
            "ASE-01",
            "Arquitectura Cloud",
            tarifa_base=150.0,
            nivel_consultor="Senior"
        )

        servicios.extend([s3, s4])

        print(
            f" ✅ Servicios registrados. "
            f"Total activos: {len(servicios)}"
        )

    operacion(6, "Creación de servicios válidos", op6)

    # 7. Reserva y Confirmación Exitosa
    def op7():

        r1 = Reserva(
            "RES-001",
            clientes[0],
            servicios[0],
            duracion=3
        )

        total = r1.confirmar(
            descuento=10,
            impuesto=19
        )

        reservas.append(r1)

        print(f" ✅ {r1}")
        print(f" 💰 Monto total procesado: ${total}")

    operacion(7, "Reserva y confirmación válida", op7)

    # 8. Servicio Inactivo
    def op8():

        servicios[0].cambiar_disponibilidad(False)

        r2 = Reserva(
            "RES-002",
            clientes[0],
            servicios[0],
            duracion=2
        )

        reservas.append(r2)

    operacion(8, "Reserva sobre servicio inactivo", op8)

    # 9. Re-confirmar Reserva
    def op9():

        reservas[0].confirmar()

    operacion(9, "Re-confirmación de reserva activa", op9)

    # 10. Doble Cancelación
    def op10():

        servicios[0].cambiar_disponibilidad(True)

        r3 = Reserva(
            "RES-003",
            clientes[0],
            servicios[0],
            duracion=4
        )

        r3.cancelar()

        print(
            f" ✅ Cancelación inicial procesada: "
            f"{r3.obtener_estado()}"
        )

        print(" ▶️ Re-intentando cancelar...")

        r3.cancelar()

    operacion(10, "Doble cancelación de reserva", op10)

    print("=" * 70)
    print(" SIMULACIÓN CONCLUIDA SIN DETENER EL SISTEMA")
    print(" Historial completo guardado en 'logs.txt'")
    print("=" * 70)


if __name__ == "__main__":
    ejecutar_simulacion()
