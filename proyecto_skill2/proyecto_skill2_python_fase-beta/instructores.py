
from persistencia import cargar_datos, guardar_datos, obtener_proximo_id
from utilidades import validar_documento, limpiar_entrada, obtener_entrada_segura

ARCHIVO = "instructores"
ESPECIALIDADES_VALIDAS = ["moto", "carro"]

def registrar_instructor(nombre: str, documento: str, especialidad: str) -> dict:
    
    instructores = cargar_datos(ARCHIVO)
    
    if not isinstance(instructores, dict):
        instructores = {}
    
    
    for instructor in instructores.values():
        if instructor.get("documento") == documento:
            print("❌ El documento ya está registrado como instructor.")
            return None
    
    
    nuevo_id = obtener_proximo_id(ARCHIVO, "id_instructor")
    
    instructor = {
        "id_instructor": nuevo_id,
        "nombre": limpiar_entrada(nombre),
        "documento": documento,
        "especialidad": especialidad.lower(),
        "estado": "activo"
    }
    
    instructores[str(nuevo_id)] = instructor
    guardar_datos(ARCHIVO, instructores)
    print(f"✅ Instructor '{nombre}' registrado exitosamente con ID {nuevo_id}.")
    return instructor

def obtener_instructor(id_instructor: int) -> dict:

    instructores = cargar_datos(ARCHIVO)
    return instructores.get(str(id_instructor))

def listar_instructores(especialidad: str = None) -> list:
    
    instructores = cargar_datos(ARCHIVO)
    
    if not isinstance(instructores, dict):
        instructores = {}
    
    lista = []
    for inst in instructores.values():
        if inst.get("estado") == "activo":
            if especialidad is None or inst.get("especialidad") == especialidad.lower():
                lista.append(
                    f"[ID: {inst['id_instructor']}] {inst['nombre']} | Especialidad: {inst['especialidad']}"
                )
    
    return lista

def actualizar_instructor(id_instructor: int, **kwargs) -> bool:
    
    instructores = cargar_datos(ARCHIVO)
    
    if not isinstance(instructores, dict):
        instructores = {}
    
    instructor = instructores.get(str(id_instructor))
    if instructor:
        instructor.update(kwargs)
        instructores[str(id_instructor)] = instructor
        guardar_datos(ARCHIVO, instructores)
        return True
    
    return False

def menu_instructores():
    """Menú interactivo para gestión de instructores"""
    while True:
        print("\n" + "="*60)
        print("👨‍🏫 GESTIÓN DE INSTRUCTORES")
        print("="*60)
        print("1. Registrar nuevo instructor")
        print("2. Consultar instructor por ID")
        print("3. Listar todos los instructores")
        print("4. Listar por especialidad")
        print("5. Volver al menú principal")
        print("="*60)
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            print("\n--- REGISTRAR NUEVO INSTRUCTOR ---")
            nombre = obtener_entrada_segura("Nombre del instructor: ")
            documento = obtener_entrada_segura(
                "Documento (6-12 dígitos): ",
                validador=validar_documento
            )
            
            print("\nEspecialidades disponibles: moto, carro")
            especialidad = obtener_entrada_segura(
                "Especialidad: ",
                validador=lambda x: x.lower() in ESPECIALIDADES_VALIDAS
            )
            
            registrar_instructor(nombre, documento, especialidad)
        
        elif opcion == "2":
            print("\n--- CONSULTAR INSTRUCTOR ---")
            try:
                id_instructor = int(input("ID del instructor: "))
                instructor = obtener_instructor(id_instructor)
                
                if instructor:
                    print(f"\n✅ Instructor encontrado:")
                    print(f"   ID: {instructor['id_instructor']}")
                    print(f"   Nombre: {instructor['nombre']}")
                    print(f"   Documento: {instructor['documento']}")
                    print(f"   Especialidad: {instructor['especialidad']}")
                    print(f"   Estado: {instructor['estado']}")
                else:
                    print("❌ Instructor no encontrado.")
            except ValueError:
                print("❌ ID inválido.")
        
        elif opcion == "3":
            print("\n--- LISTADO DE INSTRUCTORES ---")
            from utilidades import formatear_lista
            formatear_lista(
                listar_instructores(),
                "Instructores Activos"
            )
        
        elif opcion == "4":
            print("\n--- FILTRAR POR ESPECIALIDAD ---")
            print("Especialidades: moto, carro")
            especialidad = input("Especialidad: ").lower().strip()
            
            if especialidad in ESPECIALIDADES_VALIDAS:
                from utilidades import formatear_lista
                formatear_lista(
                    listar_instructores(especialidad),
                    f"Instructores de {especialidad}"
                )
            else:
                print("❌ Especialidad inválida.")
        
        elif opcion == "5":
            break
        
        else:
            print("❌ Opción inválida.")