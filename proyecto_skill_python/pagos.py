"""
Módulo de pagos: gestión de pagos de prácticas y servicios.
"""
from datetime import datetime
from persistencia import cargar_datos, guardar_datos, obtener_proximo_id
from clientes import Clientes
from citas import Citas
from utilidades import limpiar_entrada, obtener_entrada_segura


class Pagos:
    """Gestiona operaciones relacionadas con pagos."""

    ARCHIVO = "pagos"
    METODOS_VALIDOS = ["efectivo", "transferencia", "tarjeta", "qr"]
    ESTADOS_VALIDOS = ["pendiente", "pagado", "anulado"]

    @staticmethod
    def registrar_pago(id_cliente: int, monto: float, metodo_pago: str, id_cita: int = None,
                      fecha_pago: str = None, observaciones: str = "") -> dict:
        """
        Registra un nuevo pago asociado a un cliente y opcionalmente a una cita.
        """
        cliente = Clientes.obtener_cliente(id_cliente)
        if not cliente:
            print("❌ Cliente no encontrado.")
            return None

        if monto <= 0:
            print("❌ El monto debe ser mayor a cero.")
            return None

        metodo = metodo_pago.strip().lower()
        if metodo not in Pagos.METODOS_VALIDOS:
            print(f"❌ Método de pago inválido. Opciones: {Pagos.METODOS_VALIDOS}")
            return None

        if id_cita is not None:
            cita = Citas.obtener_cita(id_cita)
            if not cita:
                print("❌ La cita no existe.")
                return None

        pagos = cargar_datos(Pagos.ARCHIVO)
        if not isinstance(pagos, list):
            pagos = []

        if not fecha_pago:
            fecha_pago = datetime.now().strftime("%d/%m/%Y")

        nuevo_id = obtener_proximo_id(Pagos.ARCHIVO, "id_pago")

        pago = {
            "id_pago": nuevo_id,
            "id_cliente": id_cliente,
            "id_cita": id_cita,
            "monto": round(float(monto), 2),
            "metodo_pago": metodo,
            "fecha_pago": fecha_pago,
            "estado": "pagado",
            "observaciones": limpiar_entrada(observaciones),
        }

        pagos.append(pago)
        guardar_datos(Pagos.ARCHIVO, pagos)
        print(f"✅ Pago registrado correctamente con ID {nuevo_id}.")
        return pago

    @staticmethod
    def obtener_pago(id_pago: int) -> dict:
        """Obtiene un pago por su ID."""
        pagos = cargar_datos(Pagos.ARCHIVO)
        if not isinstance(pagos, list):
            return None

        for pago in pagos:
            if pago.get("id_pago") == id_pago:
                return pago
        return None

    @staticmethod
    def listar_pagos(id_cliente: int = None) -> list:
        """Lista los pagos, opcionalmente filtrados por cliente."""
        pagos = cargar_datos(Pagos.ARCHIVO)
        if not isinstance(pagos, list):
            pagos = []

        lista = []
        for pago in pagos:
            if id_cliente and pago.get("id_cliente") != id_cliente:
                continue

            cliente = Clientes.obtener_cliente(pago.get("id_cliente"))
            nombre_cliente = cliente.get("nombre") if cliente else "Desconocido"
            cita_texto = f" | Cita: {pago.get('id_cita')}" if pago.get("id_cita") else ""
            lista.append(
                f"[ID: {pago['id_pago']}] {nombre_cliente} | Monto: ${pago['monto']:.2f} | "
                f"Método: {pago['metodo_pago']} | Fecha: {pago['fecha_pago']} | Estado: {pago['estado']}{cita_texto}"
            )

        return lista

    @staticmethod
    def actualizar_estado(id_pago: int, estado: str) -> bool:
        """Cambia el estado de un pago."""
        pagos = cargar_datos(Pagos.ARCHIVO)
        if not isinstance(pagos, list):
            return False

        estado = estado.strip().lower()
        if estado not in Pagos.ESTADOS_VALIDOS:
            print("❌ Estado inválido.")
            return False

        for pago in pagos:
            if pago.get("id_pago") == id_pago:
                pago["estado"] = estado
                guardar_datos(Pagos.ARCHIVO, pagos)
                return True

        return False

    @staticmethod
    def menu_pagos():
        """Menú interactivo para gestionar pagos."""
        while True:
            print("\n" + "=" * 60)
            print("💳 GESTIÓN DE PAGOS")
            print("=" * 60)
            print("1. Registrar pago")
            print("2. Consultar pago por ID")
            print("3. Listar pagos")
            print("4. Cambiar estado de un pago")
            print("5. Volver al menú principal")
            print("=" * 60)

            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                print("\n--- REGISTRAR PAGO ---")
                try:
                    id_cliente = int(input("ID del cliente: "))
                    monto = float(input("Monto a pagar: "))
                    metodo = input("Método de pago (efectivo/transferencia/tarjeta/qr): ").strip().lower()
                    id_cita = input("ID de la cita (opcional, presione Enter si no aplica): ").strip()
                    observaciones = input("Observaciones (opcional): ").strip()

                    id_cita_int = int(id_cita) if id_cita else None
                    Pagos.registrar_pago(id_cliente, monto, metodo, id_cita_int, observaciones=observaciones)
                except ValueError:
                    print("❌ Datos inválidos.")

            elif opcion == "2":
                print("\n--- CONSULTAR PAGO ---")
                try:
                    id_pago = int(input("ID del pago: "))
                    pago = Pagos.obtener_pago(id_pago)
                    if pago:
                        cliente = Clientes.obtener_cliente(pago.get("id_cliente"))
                        nombre_cliente = cliente.get("nombre") if cliente else "Desconocido"
                        print(f"\n✅ Pago encontrado:")
                        print(f"   ID: {pago['id_pago']}")
                        print(f"   Cliente: {nombre_cliente}")
                        print(f"   Monto: ${pago['monto']:.2f}")
                        print(f"   Método: {pago['metodo_pago']}")
                        print(f"   Fecha: {pago['fecha_pago']}")
                        print(f"   Estado: {pago['estado']}")
                        if pago.get("id_cita"):
                            print(f"   Cita asociada: {pago['id_cita']}")
                    else:
                        print("❌ Pago no encontrado.")
                except ValueError:
                    print("❌ ID inválido.")

            elif opcion == "3":
                print("\n--- LISTADO DE PAGOS ---")
                try:
                    id_cliente = int(input("Filtrar por cliente (deje vacío para todos): ")) if input("Filtrar por cliente? (Ingrese ID o Enter para todos): ").strip() else None
                except ValueError:
                    id_cliente = None
                    print("⚠️ Filtro ignorado.")

                from utilidades import formatear_lista
                formatear_lista(Pagos.listar_pagos(id_cliente), "Pagos")

            elif opcion == "4":
                print("\n--- CAMBIAR ESTADO DE PAGO ---")
                try:
                    id_pago = int(input("ID del pago: "))
                    estado = input("Nuevo estado (pendiente/pagado/anulado): ").strip().lower()
                    if Pagos.actualizar_estado(id_pago, estado):
                        print("✅ Estado actualizado.")
                    else:
                        print("❌ No se pudo actualizar el estado.")
                except ValueError:
                    print("❌ ID inválido.")

            elif opcion == "5":
                break

            else:
                print("❌ Opción inválida.")
