"""
ACADEMIA DRIVESAFE - Sistema de Gestión de Citas de Práctica
Aplicación principal - Menú de navegación
"""
from clientes import Clientes
from instructores import Instructores
from vehiculos import Vehiculos
from citas import Citas
from pagos import Pagos
from persistencia import inicializar_datos

def mostrar_banner():
    """Muestra el banner de bienvenida"""
    print("\n" + "="*70)
    print(" "*15 + "🏁 ACADEMIA DRIVESAFE 🏁")
    print(" "*10 + "Sistema de Gestión de Citas de Práctica")
    print("="*70 + "\n")

def menu_principal():
    """Menú principal de la aplicación"""
    mostrar_banner()
    
    while True:
        print("\n" + "="*70)
        print("📋 MENÚ PRINCIPAL")
        print("="*70)
        print("1. 👤 Gestionar Clientes")
        print("2. 👨‍🏫 Gestionar Instructores")
        print("3. 🚗 Gestionar Vehículos")
        print("4. 📅 Gestionar Citas")
        print("5. � Gestionar Pagos")
        print("6. 📊 Reportes y Consultas")
        print("7. 🚪 Salir")
        print("="*70)
        
        opcion = input("\nSeleccione una opción: ").strip()
        
        if opcion == "1":
            Clientes.menu_clientes()
        
        elif opcion == "2":
            Instructores.menu_instructores()
        
        elif opcion == "3":
            Vehiculos.menu_vehiculos()
        
        elif opcion == "4":
            Citas.menu_citas()
        
        elif opcion == "5":
            Pagos.menu_pagos()
        
        elif opcion == "6":
            menu_reportes()
        
        elif opcion == "7":
            print("\n" + "="*70)
            print("👋 ¡Gracias por usar DriveSafe! ¡Conducir seguro!")
            print("="*70 + "\n")
            break
        
        else:
            print("❌ Opción inválida. Intente de nuevo.")

def menu_reportes():
    """Menú de reportes y consultas"""
    while True:
        print("\n" + "="*70)
        print("📊 REPORTES Y CONSULTAS")
        print("="*70)
        print("1. Resumen de cliente")
        print("2. Citas próximas (7 días)")
        print("3. Instructores por especialidad")
        print("4. Vehículos disponibles")
        print("5. Historial de prácticas por cliente")
        print("6. Volver al menú principal")
        print("="*70)
        
        opcion = input("\nSeleccione una opción: ").strip()
        
        if opcion == "1":
            reporte_cliente()
        
        elif opcion == "2":
            reporte_proximas_citas()
        
        elif opcion == "3":
            reporte_instructores_especialidad()
        
        elif opcion == "4":
            reporte_vehiculos_disponibles()
        
        elif opcion == "5":
            reporte_historial_cliente()
        
        elif opcion == "6":
            break
        
        else:
            print("❌ Opción inválida.")

def reporte_cliente():
    """Genera un reporte completo de un cliente"""
    print("\n--- REPORTE DE CLIENTE ---")
    try:
        id_cliente = int(input("ID del cliente: "))
        cliente = Clientes.obtener_cliente(id_cliente)
        
        if not cliente:
            print("❌ Cliente no encontrado.")
            return
        
        print(f"\n{'='*70}")
        print(f"DATOS PERSONALES")
        print(f"{'='*70}")
        print(f"ID: {cliente['id_cliente']}")
        print(f"Nombre: {cliente['nombre']}")
        print(f"Documento: {cliente['documento']}")
        print(f"Tipo de Vehículo: {cliente['tipo_vehiculo']}")
        print(f"Estado: {cliente['estado']}")
        
        print(f"\n{'='*70}")
        print(f"HISTORIAL DE CITAS")
        print(f"{'='*70}")
        
        historial = Citas.historial_cliente(id_cliente)
        if historial:
            for i, cita in enumerate(historial, 1):
                print(f"{i}. {cita}")
        else:
            print("No hay citas registradas.")
        
        print(f"{'='*70}\n")
        
    except ValueError:
        print("❌ ID inválido.")

def reporte_proximas_citas():
    """Muestra citas programadas para los próximos 7 días"""
    from datetime import datetime, timedelta
    from persistencia import cargar_datos
    
    print("\n--- CITAS PRÓXIMAS (7 DÍAS) ---")
    
    citas = cargar_datos("citas")
    if not isinstance(citas, list):
        citas = []
    
    hoy = datetime.now().date()
    proximos_7_dias = hoy + timedelta(days=7)
    
    citas_proximas = []
    for cita in citas:
        try:
            fecha_cita = datetime.strptime(cita.get("fecha"), "%d/%m/%Y").date()
            if hoy <= fecha_cita <= proximos_7_dias and cita.get("estado") == "programada":
                citas_proximas.append(cita)
        except:
            continue
    
    if citas_proximas:
        citas_proximas.sort(key=lambda x: datetime.strptime(x["fecha"], "%d/%m/%Y"))
        
        print(f"\n{'='*70}")
        for cita in citas_proximas:
            cliente = Clientes.obtener_cliente(cita.get("id_cliente"))
            instructor = Instructores.obtener_instructor(cita.get("id_instructor"))
            vehiculo = Vehiculos.obtener_vehiculo(cita.get("id_vehiculo"))
            
            print(f"Fecha: {cita['fecha']} | Hora: {cita['hora']}")
            print(f"  Cliente: {cliente.get('nombre') if cliente else 'Desconocido'}")
            print(f"  Instructor: {instructor.get('nombre') if instructor else 'Desconocido'}")
            print(f"  Vehículo: {vehiculo.get('placa') if vehiculo else 'Desconocido'}")
            print("-" * 70)
        print(f"{'='*70}\n")
    else:
        print("\n✅ No hay citas programadas en los próximos 7 días.\n")

def reporte_instructores_especialidad():
    """Muestra instructores disponibles por especialidad"""
    print("\n--- INSTRUCTORES POR ESPECIALIDAD ---")
    
    especialidades = ["moto", "carro"]
    
    for especialidad in especialidades:
        print(f"\n📋 Instructores de {especialidad.upper()}:")
        print("=" * 70)
        
        instructores_list = Instructores.listar_instructores(especialidad)
        if instructores_list:
            for inst in instructores_list:
                print(f"  {inst}")
        else:
            print(f"  No hay instructores de {especialidad}.")
    
    print("\n")

def reporte_vehiculos_disponibles():
    """Muestra vehículos disponibles"""
    print("\n--- VEHÍCULOS DISPONIBLES ---")
    print("=" * 70)
    
    vehiculos_list = Vehiculos.listar_vehiculos(disponibles_solo=True)
    if vehiculos_list:
        for v in vehiculos_list:
            print(f"  {v}")
    else:
        print("  No hay vehículos disponibles en este momento.")
    
    print("=" * 70 + "\n")

def reporte_historial_cliente():
    """Muestra el historial detallado de un cliente"""
    print("\n--- HISTORIAL DETALLADO DE CLIENTE ---")
    try:
        id_cliente = int(input("ID del cliente: "))
        cliente = Clientes.obtener_cliente(id_cliente)
        
        if not cliente:
            print("❌ Cliente no encontrado.")
            return
        
        historial = Citas.historial_cliente(id_cliente)
        
        print(f"\n{'='*70}")
        print(f"HISTORIAL DE {cliente['nombre'].upper()}")
        print(f"{'='*70}")
        
        if historial:
            completadas = 0
            no_presentadas = 0
            pendientes = 0
            
            for i, cita_str in enumerate(historial, 1):
                print(f"\n{i}. {cita_str}")
                
                cita = Citas.obtener_cita(int(cita_str.split(":")[1].split("]")[0]))
                if cita:
                    if cita.get("estado") == "completada":
                        completadas += 1
                    elif cita.get("estado") == "no_presentado":
                        no_presentadas += 1
                    else:
                        pendientes += 1
            
            print(f"\n{'='*70}")
            print(f"RESUMEN:")
            print(f"  - Prácticas completadas: {completadas}")
            print(f"  - No presentado: {no_presentadas}")
            print(f"  - Pendientes: {pendientes}")
            print(f"{'='*70}\n")
        else:
            print("\nEste cliente aún no tiene citas registradas.\n")
            
    except ValueError:
        print("❌ ID inválido.")

def main():
    """Punto de entrada de la aplicación"""
    inicializar_datos()
    menu_principal()

if __name__ == "__main__":
    main()
