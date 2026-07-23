"""
Módulo de vehículos: Gestión de vehículos disponibles
"""
import json
import os
from persistencia import cargar_datos, guardar_datos, obtener_proximo_id, importar_json
from utilidades import validar_placa, limpiar_entrada, obtener_entrada_segura,validar_si_no,validar_si

ARCHIVO = "vehiculos"
TIPOS_VALIDOS = ["moto","carro"]

def importar_clientes_desde_json(ruta_archivo: str, reemplazar: bool = False) -> bool:
    """Importa clientes desde un archivo JSON."""
    return importar_json(ARCHIVO, ruta_archivo, reemplazar=reemplazar)


def leer_vehiculos_en_lectura(ruta_archivo: str = None) -> list:
    """Lee la lista de vehículos desde un archivo JSON en modo lectura."""
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

def registrar_vehiculo(tipo: str, placa: str, modelo: str = "") -> dict:
    
        vehiculos_guardados = cargar_datos(ARCHIVO)
        
        if not isinstance(vehiculos_guardados, dict):
            vehiculos_guardados = {}
        
        # Validar placa única
        for vehiculo in vehiculos_guardados.values():
            if vehiculo.get("placa") == placa.upper():
                print("❌ La placa ya está registrada.")
                return None
        
        # Generar ID
        nuevo_id = obtener_proximo_id(ARCHIVO, "id_vehiculo")
        
        vehiculo_registrado = {
            "id_vehiculo": nuevo_id,
            "tipo": tipo.lower(),
            "placa": placa.upper(),
            "disponible": True,
            "estado": "activo"
        }
        
        vehiculos_guardados[str(nuevo_id)] = vehiculo_registrado
        guardar_datos(ARCHIVO, vehiculos_guardados)
        print(f"✅ Vehículo '{placa.upper()}' registrado exitosamente con ID {nuevo_id}.")
        return vehiculo_registrado
    
def obtener_vehiculo(id_vehiculo: int) -> dict:
    
        vehiculos_guardados = cargar_datos(ARCHIVO)
        
        if isinstance(vehiculos_guardados, dict):
            return vehiculos_guardados.get(str(id_vehiculo))
        
        return None
    
def listar_vehiculos(disponibles_solo: bool = False, tipo: str = None) -> list:
    
        vehiculos_guardados = cargar_datos(ARCHIVO)
        
        if not isinstance(vehiculos_guardados, dict):
            vehiculos_guardados = {}
        
        lista = []
        for v in vehiculos_guardados.values():
            if v.get("estado") == "activo":
                if disponibles_solo and not v.get("disponible"):
                    continue
                if tipo and v.get("tipo") != tipo.lower():
                    continue
                
                disponibilidad = "✅ Disponible" if v.get("disponible") else "❌ En uso"
                modelo = v.get("modelo", "Sin modelo")
                lista.append(
                    f"[ID: {v['id_vehiculo']}] {v['tipo'].upper()} | Placa: {v['placa']} | Modelo: {modelo} | {disponibilidad}"
                )
        
        return lista
    
def actualizar_disponibilidad(id_vehiculo: int, disponible: bool) -> bool:
    
        vehiculos_guardados = cargar_datos(ARCHIVO)
        
        if not isinstance(vehiculos_guardados, dict):
            vehiculos_guardados = {}
        
        vehiculo_actual = vehiculos_guardados.get(str(id_vehiculo))
        if vehiculo_actual:
            vehiculo_actual["disponible"] = disponible
            vehiculos_guardados[str(id_vehiculo)] = vehiculo_actual
            guardar_datos(ARCHIVO, vehiculos_guardados)
            return True
        
        return False
    

def menu_vehiculos():
        """Menú interactivo para gestión de vehículos"""
        while True:
            print("\n" + "="*50)
            print(" "*10 + "🚗 GESTIÓN DE VEHÍCULOS")
            print("="*50)
            print("1. Registrar nuevo vehículo")
            print("2. Consultar vehículo por ID")
            print("3. Listar todos los vehículos")
            print("4. Listar vehículos disponibles")
            print("5. Listar vehículos no disponibles")
            print("6. Listar por tipo")
            print("7. Volver al menú principal")
            print("="*50)
            
            opcion = input("Seleccione una opción: ").strip()
            
            if opcion == "1":
                print("\n--- REGISTRAR NUEVO VEHÍCULO ---")
                
                print("Tipos disponibles: moto,carro")
                tipo = obtener_entrada_segura(
                    "Tipo de vehículo: ",
                    validador=lambda x: x.lower() in TIPOS_VALIDOS
                )
                
                if tipo.lower() == "moto":
                    placa = obtener_entrada_segura(
                        "Placa de moto (Ejemplo: ABC12D): ",
                        validador=lambda x: validar_placa(x, tipo_vehiculo="moto")
                    )
                else:
                    placa = obtener_entrada_segura(
                        "Placa de carro (ejemplo: BTB213): ",
                        validador=lambda x: validar_placa(x, tipo_vehiculo="carro")
                    )
                
                registrar_vehiculo(tipo, placa)
            
            elif opcion == "2":
                print("\n--- CONSULTAR VEHÍCULO ---")
                ver_antes = input("¿Deseas ver la lista de vehículos activos antes de buscar? (S/N): ").strip().lower()
                validador=validar_si_no
                if ver_antes == "s":
                    from utilidades import formatear_lista
                    formatear_lista(
                        listar_vehiculos(),"Vehículos Activos"
                    )
                entrada = input("📝🚗ID del instructor (enter para cancelar_O_SI para continuar): ").strip()
                validador=validar_si
                
                try:
                    id_vehiculo = int(input("ID del vehículo: "))
                    vehiculo_encontrado = obtener_vehiculo(id_vehiculo)
                    
                    if vehiculo_encontrado:
                        disponibilidad = "✅ Disponible" if vehiculo_encontrado.get("disponible") else "❌ En uso"
                        print(f"\n✅ Vehículo encontrado:")
                        print(f"   ID: {vehiculo_encontrado['id_vehiculo']}")
                        print(f"   Tipo: {vehiculo_encontrado['tipo']}")
                        print(f"   Placa: {vehiculo_encontrado['placa']}")
                        print(f"   {disponibilidad}")
                        print(f"   Estado: {vehiculo_encontrado['estado']}")
                    else:
                        print("❌ Vehículo no encontrado.")
                except ValueError:
                    print("❌ ID inválido.")
            
            elif opcion == "3":
                print("\n--- LISTADO DE VEHÍCULOS ---")
                from utilidades import formatear_lista
                formatear_lista(
                    listar_vehiculos(),
                    "Vehículos Activos"
                )
            
            elif opcion == "4":
                print("\n--- VEHÍCULOS DISPONIBLES ---")
                from utilidades import formatear_lista
                formatear_lista(
                    listar_vehiculos(disponibles_solo=True),
                    "Vehículos Disponibles"
                )
            elif opcion == "5":
                print("\n--- VEHÍCULOS NO DISPONIBLES ---")
                from utilidades import formatear_lista
                formatear_lista(
                    listar_vehiculos(disponibles_solo=False),
                    "Vehículos No Disponibles"
                )
            
            elif opcion == "6":
                print("\n--- FILTRAR POR TIPO ---")
                print("Tipos: moto, automóvil")
                tipo = input("Tipo: ").lower().strip()
                
                if tipo in TIPOS_VALIDOS:
                    from utilidades import formatear_lista
                    formatear_lista(
                        listar_vehiculos(tipo=tipo),
                        f"Vehículos tipo {tipo}"
                    )
                else:
                    print("❌ Tipo inválido.")
            
            elif opcion == "7":
                break
            
            else:
                print("❌ Opción inválida.")