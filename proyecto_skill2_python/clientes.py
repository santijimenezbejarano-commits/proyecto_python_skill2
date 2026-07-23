
import json
import os
from persistencia import cargar_datos, guardar_datos, obtener_proximo_id, importar_json
from utilidades import validar_documento_inicio, validar_nombre, limpiar_entrada, obtener_entrada_segura, validar_si,validar_si_no

TIPOS_VALIDOS = ["moto", "carro", "ambos"]
ARCHIVO = "clientes"


def importar_clientes_desde_json(ruta_archivo: str, reemplazar: bool = False) -> bool:
    """Importa clientes desde un archivo JSON."""
    return importar_json(ARCHIVO, ruta_archivo, reemplazar=reemplazar)


def leer_clientes_en_lectura(ruta_archivo: str = None) -> list:
    """Lee la lista de clientes desde un archivo JSON en modo lectura."""
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

def registrar_cliente(nombre: str, documento: str, tipo_vehiculo: str, correo: str = "") -> dict:
    datos_clientes = cargar_datos(ARCHIVO)

    if not isinstance(datos_clientes, dict):
        datos_clientes = {}

    # Validar documento único
    for cliente in datos_clientes.values():
        if cliente.get("documento") == documento:
            print("❌ El documento ya está registrado.")
            return None

    # Generar ID
    nuevo_id = obtener_proximo_id(ARCHIVO, "id_cliente")

    cliente = {
        "id_cliente": nuevo_id,
        "nombre": limpiar_entrada(nombre),
        "documento": documento,
        "correo": limpiar_entrada(correo),
        "tipo_vehiculo": tipo_vehiculo.lower(),
        "estado": "activo"
    }

    datos_clientes[str(nuevo_id)] = cliente

    guardar_datos(ARCHIVO, datos_clientes)
    print(f"✅ Cliente '{nombre}' registrado exitosamente con ID {nuevo_id}.")
    return cliente



def obtener_cliente(id_cliente: int) -> dict:
    """
    Obtiene un cliente por ID

    Args:
        id_cliente: ID del cliente

    Returns:
        Diccionario con datos del cliente o None
    """
    datos_clientes = cargar_datos(ARCHIVO)

    if isinstance(datos_clientes, dict):
        return datos_clientes.get(str(id_cliente))

    for cliente in datos_clientes:
        if cliente.get("id_cliente") == id_cliente:
            return cliente

    return None
    


def obtener_cliente_por_documento(documento: str) -> dict:
    """
    Obtiene un cliente por documento

    Args:
        documento: Documento del cliente

    Returns:
        Diccionario con datos del cliente o None
    """
    datos_clientes = cargar_datos(ARCHIVO)

    for cliente in datos_clientes.values() if isinstance(datos_clientes, dict) else datos_clientes:
        if cliente.get("documento") == documento:
            return cliente

    return None
    


def listar_clientes() -> list:
    """
    Lista todos los clientes

    Returns:
        Lista de clientes activos
    """
    datos_clientes = cargar_datos(ARCHIVO)

    if isinstance(datos_clientes, dict):
        datos_clientes = list(datos_clientes.values())

    activos = [c for c in datos_clientes if c.get("estado") == "activo"]

    return [
        f"[ID: {c['id_cliente']}] {c['nombre']} | Doc: {c['documento']} | Vehículo: {c['tipo_vehiculo']}"
        for c in activos
    ]
    


def actualizar_cliente(id_cliente: int, **kwargs) -> bool:
    datos_clientes = cargar_datos(ARCHIVO)

    if isinstance(datos_clientes, dict):
        cliente = datos_clientes.get(str(id_cliente))
        if cliente:
            cliente.update(kwargs)
            datos_clientes[str(id_cliente)] = cliente
    else:
        for cliente in datos_clientes:
            if cliente.get("id_cliente") == id_cliente:
                cliente.update(kwargs)
                break
        else:
            return False

    guardar_datos(ARCHIVO, datos_clientes)
    return True
    


def menu_clientes():
        """Menú interactivo para gestión de clientes"""
        while True:
            print("\n" + "="*50)
            print(" "*10 + "📋 GESTIÓN DE CLIENTES")
            print("="*50)
            print("1. Registrar nuevo cliente")
            print("2. Consultar cliente por ID")
            print("3. Listar todos los clientes")
            print("4. Volver al menú principal")
            print("="*50)
            
            opcion = input("Seleccione una opción: ").strip()
            
            if opcion == "1":
                print("\n--- REGISTRAR NUEVO CLIENTE ---")
                nombre = obtener_entrada_segura(
                    "Nombre del cliente: ",
                    validador = validar_nombre
                    )
                
                documento = obtener_entrada_segura(
                    "Documento (6-12 dígitos): ",
                    validador=validar_documento_inicio
                )
                

                print("\nTipos de vehículo disponibles: moto, carro, ambos")
                tipo_vehiculo = obtener_entrada_segura(
                    "Tipo de vehículo: ",
                    validador=lambda x: x.lower() in TIPOS_VALIDOS
                )

                registrar_cliente(nombre, documento, tipo_vehiculo)
            
            elif opcion == "2":
                print("\n--- CONSULTAR CLIENTE ---")
                ver_antes = input("¿Deseas ver la lista de clientes activos antes de buscar? (S/N): ").strip().lower()
                validador=validar_si_no
                if ver_antes == "s":
                    from utilidades import formatear_lista
                    formatear_lista(
                        listar_clientes(),
                        "Clientes Activos"
                    )
                if not ver_antes == "s":
                        print("\n"+"="*22)
                        print("❌Operación cancelada.")
                        print("="*22)
                        continue
                    
                entrada = input("📝 ID del cliente (enter para cancelar): ").strip()
                try:
                    id_cliente = int(input("📝 ID del cliente: "))
                    cliente_encontrado = obtener_cliente(id_cliente)

                    if cliente_encontrado:
                        print(f"\n✅ Cliente encontrado:")
                        print(f"   ID: {cliente_encontrado['id_cliente']}")
                        print(f"   Nombre: {cliente_encontrado['nombre']}")
                        print(f"   Documento: {cliente_encontrado['documento']}")
                        print(f"   Tipo de vehículo: {cliente_encontrado['tipo_vehiculo']}")
                        print(f"   Estado: {cliente_encontrado['estado']}")
                    else:
                        print("❌ Cliente no encontrado.")
                except ValueError:
                    print("❌ ID inválido.")

            elif opcion == "3":
                print("\n--- LISTADO DE CLIENTES ---")
                from utilidades import formatear_lista
                formatear_lista(listar_clientes(), "Clientes Activos")
            
            elif opcion == "4":
                break
            
            else:
                print("❌ Opción inválida.")
