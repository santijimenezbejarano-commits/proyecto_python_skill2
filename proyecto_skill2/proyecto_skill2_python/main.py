import clientes
import instructores 
import vehiculos
import citas
from persistencia import inicializar_datos

def mostrar_banner(): 
    print("\n" + "="*50)
    print("="*10 + "🏁 ACADEMIA DRIVESAFE 🏁"+"="*16)
    print(" "*6 + "Sistema de Gestión de Citas de Práctica")
    print("="*50 + "\n")

def menu_principal():
    
    mostrar_banner()
    
    while True:
        print("\n" + "="*50)
        print(" "*15+ "📋 MENU PRINCIPAL")
        print("="*50)
        print("1. 👤 Gestionar Clientes")
        print("2. 👨‍🏫 Gestionar Instructores")
        print("3. 🚗 Gestionar Vehiculos")
        print("4. 📅 Gestionar Citas")
        print("5. 📊 Reportes y Consultas")
        print("6. 🚪 Salir")
        print("="*50)
        
        opcion = input("\nSeleccione una opcion: ").strip()
        
        if opcion == "1":
            clientes.menu_clientes()
        
        elif opcion == "2":
            instructores.menu_instructores()
        
        elif opcion == "3":
            vehiculos.menu_vehiculos()
        
        elif opcion == "4":
            citas.menu_citas()
        
        elif opcion == "5":
            menu_reportes()
        
        elif opcion == "6":
            print("\n" + "="*50)
            print("👋 ¡Gracias por usar DriveSafe! ¡Conducir seguro!")
            print("="*50 + "\n")
            break
        
        else:
            print("❌ Opcion invalida. Intente de nuevo.")

def menu_reportes():
    
    while True:
        print("\n" + "="*50)
        print("📊 REPORTES Y CONSULTAS")
        print("="*50)
        print("1. Resumen de cliente")
        print("2. Citas proximas (7 dias)")
        print("3. Instructores por especialidad")
        print("4. Vehiculos disponibles")
        print("5. Historial de practicas por cliente")
        print("6. Volver al menu principal")
        print("="*50)
        
        opcion = input("\nSeleccione una opcion: ").strip()
        
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
            print("❌ Opcion invalida.")

def reporte_cliente():
    
    print("\n--- REPORTE DE CLIENTE ---")
    ver_antes = input("¿Deseas ver la lista de clientes activos antes de buscar? (S/N): ").strip().lower()
    if ver_antes == "s":
        from utilidades import formatear_lista
        formatear_lista(
            clientes.listar_clientes(),
            "Clientes Activos"
        )
    entrada = input("📝 ID del cliente (enter para cancelar): ").strip()
    if entrada == "":
        print("Operación cancelada.")
        return
    try:
        id_cliente = int(entrada)
        cliente = clientes.obtener_cliente(id_cliente)

        if not cliente:
            print("❌ Cliente no encontrado.")
            return

        print(f"\n{'='*50}")
        print(f"DATOS PERSONALES")
        print(f"{'='*50}")
        print(f"ID: {cliente['id_cliente']}")
        print(f"Nombre: {cliente['nombre']}")
        print(f"Documento: {cliente['documento']}")
        print(f"Tipo de Vehiculo: {cliente['tipo_vehiculo']}")
        print(f"Estado: {cliente['estado']}")

        print(f"\n{'='*50}")
        print(f"HISTORIAL DE CITAS")
        print(f"{'='*50}")

        historial = citas.historial_cliente(id_cliente)
        if historial:
            for i, cita in enumerate(historial, 1):
                print(f"{i}. {cita}")
        else:
            print("No hay citas registradas.")

        print(f"{'='*50}\n")

    except ValueError:
        print("❌ ID invalido.")

def reporte_proximas_citas():
    
    from datetime import datetime, timedelta
    from persistencia import cargar_datos
    
    print("\n--- CITAS PROXIMAS (7 DIAS) ---")
    
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
            cliente = clientes.obtener_cliente(cita.get("id_cliente"))
            instructor = instructores.obtener_instructor(cita.get("id_instructor"))
            vehiculo = vehiculos.obtener_vehiculo(cita.get("id_vehiculo"))
            
            print(f"Fecha: {cita['fecha']} | Hora: {cita['hora']}")
            print(f"  Cliente: {cliente.get('nombre') if cliente else 'Desconocido'}")
            print(f"  Instructor: {instructor.get('nombre') if instructor else 'Desconocido'}")
            print(f"  Vehiculo: {vehiculo.get('placa') if vehiculo else 'Desconocido'}")
            print("-" * 70)
        print(f"{'='*70}\n")
    else:
        print("\n✅ No hay citas programadas en los priximos 7 dias.\n")

def reporte_instructores_especialidad():
    
    print("\n--- INSTRUCTORES POR ESPECIALIDAD ---")
    
    especialidades = ["moto", "carro"]
    
    for especialidad in especialidades:
        print(f"\n📋 Instructores de {especialidad.upper()}:")
        print("=" * 50)
        
        instructores_list = instructores.listar_instructores(especialidad)
        if instructores_list:
            for inst in instructores_list:
                print(f"  {inst}")
        else:
            print(f"  No hay instructores de {especialidad}.")
    
    print("\n")

def reporte_vehiculos_disponibles():
    
    print("\n--- VEHICULOS DISPONIBLES ---")
    print("=" * 70)
    
    vehiculos_list = vehiculos.listar_vehiculos(disponibles_solo=True)
    if vehiculos_list:
        for v in vehiculos_list:
            print(f"  {v}")
    else:
        print("  No hay vehiculos disponibles en este momento.")
    
    print("=" * 70 + "\n")

def reporte_historial_cliente():
    print("\n--- HISTORIAL DETALLADO DE CLIENTE ---")
    ver_antes = input("¿Deseas ver la lista de clientes activos antes de buscar? (S/N): ").strip().lower()
    if ver_antes == "s":
        from utilidades import formatear_lista
        formatear_lista(
            clientes.listar_clientes(),
            "Clientes Activos"
        )

    entrada = input("📝 ID del cliente (enter para cancelar): ").strip()
    if entrada == "":
        print("\n" + "=" * 22)
        print("❌Operación cancelada.")
        print("=" * 22)
        return

    try:
        id_cliente = int(entrada)
        cliente = clientes.obtener_cliente(id_cliente)

        if not cliente:
            print("❌ Cliente no encontrado.")
            return

        historial = citas.historial_cliente(id_cliente)

        print(f"\n{'=' * 70}")
        print(f"HISTORIAL DE {cliente['nombre'].upper()}")
        print(f"{'=' * 70}")

        if historial:
            completadas = 0
            no_presentadas = 0
            pendientes = 0

            for i, cita_str in enumerate(historial, 1):
                print(f"\n{i}. {cita_str}")

                # Extraer id de la cita dentro del string guardado
                try:
                    cita_id = int(cita_str.split(":")[1].split("]")[0])
                except Exception:
                    cita_id = None

                if cita_id is not None:
                    cita = citas.obtener_cita(cita_id)
                    if cita:
                        estado = cita.get("estado")
                        if estado == "completada":
                            completadas += 1
                        elif estado == "no_presentado":
                            no_presentadas += 1
                        else:
                            pendientes += 1

            print(f"\n{'=' * 70}")
            print("RESUMEN:")
            print(f"  - Practicas completadas: {completadas}")
            print(f"  - No presentado: {no_presentadas}")
            print(f"  - Pendientes: {pendientes}")
            print(f"{'=' * 70}\n")
        else:
            print("\nEste cliente aun no tiene citas registradas.\n")

    except ValueError:
        print("❌ ID invalido.")

def main():
    
    inicializar_datos()
    menu_principal()

if __name__ == "__main__":
    main()