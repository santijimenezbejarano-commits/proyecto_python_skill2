
import json
import os
from persistencia import cargar_datos, guardar_datos, obtener_proximo_id, importar_json
from utilidades import validar_documento_inicio, validar_si_no, validar_nombre
from utilidades import limpiar_entrada, obtener_entrada_segura, esta_activo, esta_inactivo,validar_si
#import utilidades as util
ARCHIVO = "instructores"
ESPECIALIDADES_VALIDAS = ["moto", "carro"]


def importar_intructores_desde_json(ruta_archivo: str, reemplazar: bool = False) -> bool:
    """Importa clientes desde un archivo JSON."""
    return importar_json(ARCHIVO, ruta_archivo, reemplazar=reemplazar)


def leer_instructores_en_lectura(ruta_archivo: str = None) -> list:
    """Lee la lista de instructores desde un archivo JSON en modo lectura."""
    ruta = ruta_archivo or os.path.join("datos", f"{ARCHIVO}.json")

    if not os.path.exists(ruta):
        print(f"❌ No se encontró el archivo: {ruta}")
        return []

    with open(ruta, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    if isinstance(datos, dict):
        return list(datos.values())
    if isinstance(datos, list):
        return datos

    return []

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
        for inst in leer_instructores_en_lectura():
            if isinstance(inst, dict):
                key = str(inst.get("id_instructor", len(instructores) + 1))
                instructores[key] = inst

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
        print("\n" + "="*50)
        print(" "*10 + "👨‍🏫 GESTIÓN DE INSTRUCTORES")
        print("="*50)
        print("1. Registrar nuevo instructor")
        print("2. Consultar instructor por ID")
        print("3. Listar todos los instructores")
        print("4. Listar por especialidad")
        print("5. Volver al menú principal")
        print("="*50)
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            print("\n--- REGISTRAR NUEVO INSTRUCTOR ---")
            nombre = obtener_entrada_segura(
                "Nombre del instructor: ",
                validador = validar_nombre
            )
            documento = obtener_entrada_segura(
                "Documento (6-12 dígitos): ",
                validador=validar_documento_inicio
            )
                
            print("\nEspecialidades disponibles: moto, carro, ambos")
            especialidad = obtener_entrada_segura(
                "Especialidad: ",
                validador=lambda x: x.lower() in ESPECIALIDADES_VALIDAS
            )
            
            registrar_instructor(nombre, documento, especialidad)
            


        elif opcion == "2":
            print("\n--- CONSULTAR INSTRUCTOR ---")
            ver_antes = input("¿Deseas ver la lista de instructores activos antes de buscar? (S/N): ").strip().lower()
            validador=validar_si_no
            if ver_antes == "s":
                from utilidades import formatear_lista
                formatear_lista(
                    listar_instructores(),"Instructores Activos","Clientes",
                )
            entrada = input("📝ID del instructor (enter para cancelar_O_SI para continuar): ").strip()
            if entrada == "":
                    print("\n"+"="*22)
                    print("❌Operación cancelada.")
                    print("="*22)
                    continue
            
            try:
                id_instructor = int(entrada)
                instructor = obtener_instructor(id_instructor)

                if instructor:
                    estado = instructor.get("estado", "desconocido")
                    print(f"\n✅ Instructor encontrado:")
                    print(f"   ID: {instructor['id_instructor']}")
                    print(f"   Nombre: {instructor['nombre']}")
                    print(f"   Documento: {instructor['documento']}")
                    print(f"   Especialidad: {instructor['especialidad']}")
                    print(f"   Estado: {estado}")
                    activo_txt = "Sí" if esta_activo(estado) else ("No" if esta_inactivo(estado) else "Desconocido")
                    print(f"   ¿Está activo?: {activo_txt}")
                else:
                    print("❌ Instructor no encontrado.")
            except ValueError:
                print("="*22)
                print("❌ Operación cancelada")
                print("="*22)

        
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