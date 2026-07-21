"""
Módulo de citas: Gestión de programación y seguimiento de citas de práctica
"""
from datetime import datetime
from persistencia import cargar_datos, guardar_datos, obtener_proximo_id
from utilidades import (
    validar_fecha, validar_hora, es_fecha_futura, limpiar_entrada,
    obtener_entrada_segura
)
import clientes
import instructores
import vehiculos


ARCHIVO = "citas"
DURACIONES_VALIDAS = [30, 45, 60, 90, 120]  # minutos


@staticmethod
def programar_cita(id_cliente: int, id_instructor: int, id_vehiculo: int,
                    fecha: str, hora: str, duracion: int, observaciones: str = "") -> dict:
        
        # Validaciones de existencia
        cliente = clientes.obtener_cliente(id_cliente)
        if not cliente:
            print("❌ Cliente no encontrado.")
            return None
        
        instructor = instructores.obtener_instructor(id_instructor)
        if not instructor:
            print("❌ Instructor no encontrado.")
            return None
        
        vehiculo = vehiculos.obtener_vehiculo(id_vehiculo)
        if not vehiculo:
            print("❌ Vehículo no encontrado.")
            return None
        
        # Validar disponibilidad del vehículo
        if not vehiculo.get("disponible"):
            print("❌ El vehículo no está disponible.")
            return None
        
        # Validar que especialidad del instructor coincida con tipo de vehículo
        especialidad_instructor = instructor.get("especialidad")
        tipo_vehiculo = vehiculo.get("tipo")
        
        if especialidad_instructor != tipo_vehiculo:
            print(f"❌ El instructor está especializado en {especialidad_instructor}, no en {tipo_vehiculo}.")
            return None
        
        # Validar duración
        if duracion not in citas.DURACIONES_VALIDAS:
            print(f"❌ Duración inválida. Opciones: {citas.DURACIONES_VALIDAS}")
            return None
        
        citas = cargar_datos(citas.ARCHIVO)
        if not isinstance(citas, list):
            citas = []
        
        # Generar ID
        nuevo_id = obtener_proximo_id(citas.ARCHIVO, "id_cita")
        
        cita = {
            "id_cita": nuevo_id,
            "id_cliente": id_cliente,
            "id_instructor": id_instructor,
            "id_vehiculo": id_vehiculo,
            "fecha": fecha,
            "hora": hora,
            "duracion": duracion,
            "estado": "programada",
            "asistencia": None,  # None: pendiente, True: asistió, False: no asistió
            "observaciones": limpiar_entrada(observaciones)
        }
        
        citas.append(cita)
        
        # Marcar vehículo como no disponible
        vehiculos.actualizar_disponibilidad(id_vehiculo, False)
        
        guardar_datos(citas.ARCHIVO, citas)
        print(f"✅ Cita programada exitosamente con ID {nuevo_id}.")
        return cita
@staticmethod
def obtener_cita(id_cita: int) -> dict:
    def obtener_cita(id_cita: int) -> dict:
        
        citas = cargar_datos(citas.ARCHIVO)
        
        if not isinstance(citas, list):
            return None
        
        for cita in citas:
            if cita.get("id_cita") == id_cita:
                return cita
        
        return None
@staticmethod
def registrar_asistencia(id_cita: int, asistio: bool, observaciones_practica: str = "") -> bool:
        
        citas = cargar_datos(citas.ARCHIVO)
        
        if not isinstance(citas, list):
            return False
        
        for cita in citas:
            if cita.get("id_cita") == id_cita:
                cita["asistencia"] = asistio
                cita["observaciones"] = limpiar_entrada(observaciones_practica)
                
                if asistio:
                    cita["estado"] = "completada"
                else:
                    cita["estado"] = "no_presentado"
                
                # Liberar vehículo
                id_vehiculo = cita.get("id_vehiculo")
                vehiculos.actualizar_disponibilidad(id_vehiculo, True)
                
                guardar_datos(citas.ARCHIVO, citas)
                print("✅ Asistencia registrada exitosamente.")
                return True
        
        return False
@staticmethod
def listar_citas(id_cliente: int = None, fecha: str = None) -> list:
        
        citas = cargar_datos(citas.ARCHIVO)
        
        if not isinstance(citas, list):
            citas = []
        
        lista = []
        for c in citas:
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
@staticmethod

def historial_cliente(id_cliente: int) -> list:
        """
        Obtiene el historial de prácticas de un cliente
        
        Args:
            id_cliente: ID del cliente
            
        Returns:
            Lista de citas del cliente
        """
        return listar_citas(id_cliente=id_cliente)
@staticmethod
def menu_citas():
        """Menú interactivo para gestión de citas"""
        while True:
            print("\n" + "="*60)
            print("📅 GESTIÓN DE CITAS")
            print("="*60)
            print("1. Programar nueva cita")
            print("2. Consultar cita por ID")
            print("3. Listar todas las citas")
            print("4. Registrar asistencia")
            print("5. Historial de cliente")
            print("6. Citas por fecha")
            print("7. Volver al menú principal")
            print("="*60)
            
            opcion = input("Seleccione una opción: ").strip()
            
            if opcion == "1":
                print("\n--- PROGRAMAR NUEVA CITA ---")
                try:
                    id_cliente = int(input("ID del cliente: "))
                    id_instructor = int(input("ID del instructor: "))
                    id_vehiculo = int(input("ID del vehículo: "))
                    
                    fecha = obtener_entrada_segura(
                        "Fecha (DD/MM/YYYY): ",
                        validador=lambda x: validar_fecha(x) and es_fecha_futura(x)
                    )
                    
                    hora = obtener_entrada_segura(
                        "Hora (HH:MM): ",
                        validador=validar_hora
                    )
                    
                    print(f"\nDuraciones disponibles (minutos): {cita.DURACIONES_VALIDAS}")
                    duracion = int(input("Duración: "))
                    
                    observaciones = input("Observaciones (opcional): ").strip()
                    
                    programar_cita(
                        id_cliente, id_instructor, id_vehiculo,
                        fecha, hora, duracion, observaciones
                    )
                except ValueError:
                    print("❌ Datos inválidos.")
            
            elif opcion == "2":
                print("\n--- CONSULTAR CITA ---")
                try:
                    id_cita = int(input("ID de la cita: "))
                    cita = cita.obtener_cita(id_cita)
                    
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
                    cita.listar_citas(),
                    "Todas las Citas Programadas"
                )
            
            elif opcion == "4":
                print("\n--- REGISTRAR ASISTENCIA ---")
                try:
                    id_cita = int(input("ID de la cita: "))
                    
                    print("¿Asistió el cliente?")
                    print("1. Sí")
                    print("2. No")
                    respuesta = input("Respuesta: ").strip()
                    
                    asistio = respuesta == "1"
                    observaciones = input("Observaciones de la práctica: ").strip()
                    
                    if cita.registrar_asistencia(id_cita, asistio, observaciones):
                        print("✅ Asistencia registrada.")
                    else:
                        print("❌ Cita no encontrada.")
                except ValueError:
                    print("❌ Datos inválidos.")
            
            elif opcion == "5":
                print("\n--- HISTORIAL DE CLIENTE ---")
                try:
                    id_cliente = int(input("ID del cliente: "))
                    from utilidades import formatear_lista
                    formatear_lista(
                        cita.historial_cliente(id_cliente),
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
                    cita.listar_citas(fecha=fecha),
                    f"Citas del {fecha}"
                )
            
            elif opcion == "7":
                break
            
            else:
                print("❌ Opción inválida.")
