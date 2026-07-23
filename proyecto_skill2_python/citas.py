"""
Módulo de citas: Gestión de programación y seguimiento de citas de práctica
"""
from datetime import datetime
import clientes
import instructores
import vehiculos
from persistencia import cargar_datos, guardar_datos, obtener_proximo_id, importar_json
from utilidades import (validar_fecha, validar_hora, es_fecha_futura,es_hora_laboral,)
from utilidades import(limpiar_entrada,obtener_entrada_segura,validar_estado,esta_activo)
def importar_citas_desde_json(ruta_archivo: str, reemplazar: bool = False) -> bool:
    return importar_json(ARCHIVO, ruta_archivo, reemplazar=reemplazar)

ARCHIVO = "citas"
DURACIONES_VALIDAS = [30, 45, 60, 90, 120]  # Duraciones válidas en minutos

def programar_cita(id_cliente: int, id_instructor: int, id_vehiculo: int,
                    fecha: str, hora: str, duracion: int, observaciones: str = "") -> dict:
    cliente = clientes.obtener_cliente(id_cliente)
    if not cliente:
        print("❌ Cliente no encontrado.")
        return None

    instructor = instructores.obtener_instructor(id_instructor)
    if not instructor:
        print("❌ Instructor no encontrado.")
        return None

    estado_instructor = instructor.get("estado", "")
    if not validar_estado(estado_instructor) or not esta_activo(estado_instructor):
        print("❌ El instructor no está activo.")
        return None

    vehiculo = vehiculos.obtener_vehiculo(id_vehiculo)
    if not vehiculo:
        print("❌ Vehículo no encontrado.")
        return None

    estado_vehiculo = vehiculo.get("estado", "")
    if not validar_estado(estado_vehiculo) or not esta_activo(estado_vehiculo):
        print("❌ El vehículo no está activo.")
        return None

    if not vehiculo.get("disponible"):
        print("❌ El vehículo no está disponible.")
        return None

    especialidad_instructor = instructor.get("especialidad")
    tipo_vehiculo = vehiculo.get("tipo")

    if especialidad_instructor != tipo_vehiculo:
        print(f"❌ El instructor está especializado en {especialidad_instructor}, no en {tipo_vehiculo}.")
        return None


    datos_citas = cargar_datos(ARCHIVO)
    if not isinstance(datos_citas, list):
        datos_citas = []

    # Generar ID
    nuevo_id = obtener_proximo_id(ARCHIVO, "id_cita")

    cita = {
        "id_cita": nuevo_id,
        "id_cliente": id_cliente,
        "id_instructor": id_instructor,
        "id_vehiculo": id_vehiculo,
        "fecha": fecha,
        "hora": hora,
        "duracion": duracion,
        "estado": "programada",
        "asistencia": None,
        "observaciones": limpiar_entrada(observaciones)
    }

    datos_citas.append(cita)

    # Marcar vehículo como no disponible
    vehiculos.actualizar_disponibilidad(id_vehiculo, False)

    guardar_datos(ARCHIVO, datos_citas)
    print(f"✅ Cita programada exitosamente con ID {nuevo_id}.")
    return cita
def obtener_cita(id_cita: int) -> dict:
    datos_citas = cargar_datos(ARCHIVO)

    if not isinstance(datos_citas, list):
        return None

    for cita in datos_citas:
        if cita.get("id_cita") == id_cita:
            return cita

    return None
def registrar_asistencia(id_cita: int, asistio=None, observaciones_practica: str = "") -> bool:
    datos_citas = cargar_datos(ARCHIVO)

    if not isinstance(datos_citas, list):
        return False

    for cita in datos_citas:
        if cita.get("id_cita") == id_cita:
            cita["asistencia"] = asistio
            cita["observaciones"] = limpiar_entrada(observaciones_practica)

            if asistio is True:
                cita["estado"] = "completada"
            elif asistio is False:
                cita["estado"] = "no_presentado"
            else:
                cita["estado"] = "en_curso"

            if cita.get("estado") != "en_curso":
                id_vehiculo = cita.get("id_vehiculo")
                vehiculos.actualizar_disponibilidad(id_vehiculo, True)

            guardar_datos(ARCHIVO, datos_citas)
            if cita.get("estado") == "en_curso":
                print("✅ Cita marcada como en curso.")
            else:
                print("✅ Asistencia registrada exitosamente.")
            return True

    return False
def listar_citas(id_cliente: int = None, fecha: str = None) -> list:
    datos_citas = cargar_datos(ARCHIVO)

    if not isinstance(datos_citas, list):
        datos_citas = []

    lista = []
    for c in datos_citas:
        if id_cliente and c.get("id_cliente") != id_cliente:
            continue
        if fecha and c.get("fecha") != fecha:
            continue

        cliente = clientes.obtener_cliente(c.get("id_cliente"))
        instructor = instructores.obtener_instructor(c.get("id_instructor"))
        vehiculo = vehiculos.obtener_vehiculo(c.get("id_vehiculo"))

        cliente_nombre = cliente.get("nombre") if cliente else "Desconocido"
        instructor_nombre = instructor.get("nombre") if instructor else "Desconocido"
        vehiculo_placa = vehiculo.get("placa") if vehiculo else "Desconocido"

        estado_asistencia = ""
        if c.get("asistencia") is None:
            estado_asistencia = "[Pendiente]"
        elif c.get("asistencia"):
            estado_asistencia = "[✅ Asistió]"
        else:
            estado_asistencia = "[❌ No asistió]"

        lista.append(
            f"[ID: {c['id_cita']}] {c['fecha']} {c['hora']} | Cliente: {cliente_nombre} | "
            f"Instructor: {instructor_nombre} | Vehículo: {vehiculo_placa} | "
            f"Duración: {c['duracion']}min | Estado: {c['estado']} {estado_asistencia}"
        )

    return lista
def historial_cliente(id_cliente: int) -> list:
        return listar_citas(id_cliente=id_cliente)
def menu_citas():
        """Menú interactivo para gestión de citas"""
        while True:
            print("\n" + "="*50)
            print(" "*10 + "📅 GESTIÓN DE CITAS")
            print("="*50)
            print("1. Programar nueva cita")
            print("2. Consultar cita por ID")
            print("3. Listar todas las citas")
            print("4. Registrar asistencia")
            print("5. Historial de cliente")
            print("6. Citas por fecha")
            print("7. Volver al menú principal")
            print("="*50)
            
            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                print("\n--- PROGRAMAR NUEVA CITA ---")
                try:
                    clientes_disponibles = clientes.listar_clientes()
                    if clientes_disponibles:
                        print("\nClientes disponibles:")
                        for item in clientes_disponibles:
                            print(f"  {item}")
                    else:
                        print("❌ No hay clientes registrados.")
                        continue

                    id_cliente = int(obtener_entrada_segura(
                        "📝 ID del cliente: ",
                        validador=lambda x: x.isdigit() and any(
                            str(cliente.get("id_cliente")) == x
                            for cliente in clientes.leer_clientes_en_lectura()
                            if isinstance(cliente, dict)
                        )
                    ))

                    instructores_activos = instructores.listar_instructores()
                    if instructores_activos:
                        print("\nInstructores disponibles:")
                        for item in instructores_activos:
                            print(f"  {item}")
                    else:
                        print("❌ No hay instructores activos disponibles.")
                        continue

                    id_instructor = int(obtener_entrada_segura(
                        "ID del instructor: ",
                        validador=lambda x: x.isdigit() and any(
                            str(instructor.get("id_instructor")) == x
                            for instructor in instructores.leer_instructores_en_lectura()
                            if isinstance(instructor, dict) and instructor.get("estado") == "activo"
                        )
                    ))
                    vehiculos_disponibles = vehiculos.listar_vehiculos(disponibles_solo=True)
                    if vehiculos_disponibles:
                        print("\nVehículos disponibles:")
                        for item in vehiculos_disponibles:
                            print(f"  {item}")
                    else:
                        print("❌ No hay vehículos disponibles para asignar.")
                        continue

                    id_vehiculo = int(obtener_entrada_segura(
                        "ID del vehículo: ",
                        validador=lambda x: x.isdigit() and any(
                            str(vehiculo.get("id_vehiculo")) == x
                            for vehiculo in vehiculos.leer_vehiculos_en_lectura()
                            if isinstance(vehiculo, dict) and vehiculo.get("estado") == "activo" and vehiculo.get("disponible") is True
                        )
                    ))
                    fecha = obtener_entrada_segura(
                        "Fecha (DD/MM/YYYY): ",
                        validador=lambda x: validar_fecha(x) and es_fecha_futura(x)
                    )

                    hora = obtener_entrada_segura(
                        "Hora (HH:MM): ",
                        validador=lambda x: validar_hora(x) and es_hora_laboral(x) 
                    )
                    print(f"hora valida: {hora}")

                    print(f"\nDuraciones disponibles (minutos): {DURACIONES_VALIDAS}")
                    while True:
                        try:
                            duracion = int(input("Duración (en minutos): "))
                            if duracion in DURACIONES_VALIDAS:
                                break
                            else:
                                print(f"❌ Duración inválida. Opciones válidas: {DURACIONES_VALIDAS}")
                        except ValueError:
                            print("❌ Entrada inválida. Por favor, ingrese un número entero.")

                    observaciones = input("Observaciones (opcional): ").strip()

                    programar_cita(
                        id_cliente, id_instructor, id_vehiculo,
                        fecha, hora, duracion, observaciones
                    )
                except ValueError:
                    print("❌ Datos inválidos.")

            elif opcion == "2":
                print("\n--- CONSULTAR CITA ---")
                ver_antes = input("¿Deseas ver la lista de citas antes de buscar? (S/N): ").strip().lower()
                if ver_antes == "s":
                    from utilidades import formatear_lista
                    formatear_lista(
                        listar_citas(),
                        "Citas Programadas"
                    )
                entrada = input("ID de la cita (enter para cancelar): ").strip()
                if entrada == "":
                    print("\n"+"="*22)
                    print("❌Operación cancelada.")
                    print("="*22)
                    continue
                try:
                    id_cita = int(entrada)
                    cita = obtener_cita(id_cita)
                    if cita:
                        cliente = clientes.obtener_cliente(cita.get("id_cliente"))
                        instructor = instructores.obtener_instructor(cita.get("id_instructor"))
                        vehiculo = vehiculos.obtener_vehiculo(cita.get("id_vehiculo"))

                        print(f"\n✅ Cita encontrada:")
                        print(f"   ID: {cita['id_cita']}")
                        print(f"   Cliente: {cliente.get('nombre') if cliente else 'Desconocido'}")
                        print(f"   Instructor: {instructor.get('nombre') if instructor else 'Desconocido'}")
                        print(f"   Vehículo: {vehiculo.get('placa') if vehiculo else 'Desconocido'}")
                        print(f"   Fecha: {cita['fecha']}")
                        print(f"   Hora: {cita['hora']}")
                        print(f"   Duración: {cita['duracion']} minutos")
                        print(f"   Estado: {cita['estado']}")
                        print(f"   Observaciones: {cita['observaciones']}")

                    else:
                        print("❌ Cita no encontrada.")
                except ValueError:
                    print("❌ ID inválido.")

            elif opcion == "3":
                print("\n--- LISTADO DE CITAS ---")
                from utilidades import formatear_lista
                formatear_lista(
                    listar_citas(),
                    "Todas las Citas Programadas"
                )

            elif opcion == "4":
                print("\n--- REGISTRAR ASISTENCIA ---")
                try:
                    citas_disponibles = listar_citas()
                    if citas_disponibles:
                        print("\nCitas disponibles:")
                        for item in citas_disponibles:
                            print(f"  {item}")
                    else:
                        print("❌ No hay citas registradas.")
                        continue

                    id_cita = int(obtener_entrada_segura(
                        "ID de la cita: ",
                        validador=lambda x: x.isdigit() and any(
                            str(cita.get("id_cita")) == x
                            for cita in cargar_datos(ARCHIVO)
                            if isinstance(cita, dict)
                        )
                    ))

                    print("¿Asistió el cliente?")
                    print("1. Sí")
                    print("2. No")
                    print("3. En curso")
                    respuesta = input("Respuesta: ").strip()

                    if respuesta == "1":
                        asistio = True
                    elif respuesta == "2":
                        asistio = False
                    elif respuesta == "3":
                        asistio = None
                    else:
                        print("❌ Opción inválida.")
                        continue

                    observaciones = input("Observaciones de la práctica: ").strip()

                    if registrar_asistencia(id_cita, asistio, observaciones):
                        if asistio is None:
                            print("✅ Cita marcada como en curso.")
                        else:
                            print("✅ Asistencia registrada.")
                    else: 
                        print("❌ Cita no encontrada.")
                except ValueError:
                    print("❌ Datos inválidos.")

            elif opcion == "5":
                print("\n--- HISTORIAL DE CLIENTE ---")
                ver_antes = input("¿Deseas ver la lista de clientes activos antes de buscar? (S/N): ").strip().lower()
                if ver_antes == "s":
                    from utilidades import formatear_lista
                    formatear_lista(
                        clientes.listar_clientes(),
                        "Clientes Activos"
                    )

                try:
                    id_cliente = int(input("📝 ID del cliente: "))
                    from utilidades import formatear_lista
                    formatear_lista(
                        historial_cliente(id_cliente),
                        f"Historial de Citas del Cliente {id_cliente}"
                    )
                except ValueError:
                    print("❌ ID inválido.")

            elif opcion == "6":
                print("\n--- CITAS POR FECHA ---")
                fecha = obtener_entrada_segura(
                    "Fecha (DD/MM/YYYY): ",
                    validador=validar_fecha
                )
                from utilidades import formatear_lista
                formatear_lista(
                    listar_citas(fecha=fecha),
                    f"Citas del {fecha}"
                )

            elif opcion == "7":
                return

            else:
                print("❌ Opción inválida.")