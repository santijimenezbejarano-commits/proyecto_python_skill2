"""
Módulo de vehículos: Gestión de vehículos disponibles
"""
from persistencia import cargar_datos, guardar_datos, obtener_proximo_id
from utilidades import validar_placa, limpiar_entrada, obtener_entrada_segura

ARCHIVO = "vehiculos"
TIPOS_VALIDOS = ["moto", "automóvil"]

@staticmethod
def registrar_vehiculo(tipo: str, placa: str, modelo: str = "") -> dict:
        """
        Registra un nuevo vehículo
        
        Args:
            tipo: Tipo de vehículo (moto o automóvil)
            placa: Placa del vehículo
            modelo: Modelo del vehículo (opcional)
            
        Returns:
            Diccionario con datos del vehículo registrado
        """
        vehiculos = cargar_datos(vehiculos.ARCHIVO)
        
        if not isinstance(vehiculos, dict):
            vehiculos = {}
        
        # Validar placa única
        for vehiculo in vehiculos.values():
            if vehiculo.get("placa") == placa.upper():
                print("❌ La placa ya está registrada.")
                return None
        
        # Generar ID
        nuevo_id = obtener_proximo_id(vehiculos.ARCHIVO, "id_vehiculo")
        
        vehiculo = {
            "id_vehiculo": nuevo_id,
            "tipo": tipo.lower(),
            "placa": placa.upper(),
            "modelo": limpiar_entrada(modelo),
            "disponible": True,
            "estado": "activo"
        }
        
        vehiculos[str(nuevo_id)] = vehiculo
        guardar_datos(vehiculos.ARCHIVO, vehiculos)
        print(f"✅ Vehículo '{placa.upper()}' registrado exitosamente con ID {nuevo_id}.")
        return vehiculo
    
@staticmethod
def obtener_vehiculo(id_vehiculo: int) -> dict:
        """
        Obtiene un vehículo por ID
        
        Args:
            id_vehiculo: ID del vehículo
            
        Returns:
            Diccionario con datos del vehículo o None
        """
        vehiculos = cargar_datos(vehiculos.ARCHIVO)
        
        if isinstance(vehiculos, dict):
            return vehiculos.get(str(id_vehiculo))
        
        return None
    
@staticmethod
def listar_vehiculos(disponibles_solo: bool = False, tipo: str = None) -> list:
        """
        Lista vehículos, opcionalmente filtrados
        
        Args:
            disponibles_solo: Si True, solo lista vehículos disponibles
            tipo: Filtrar por tipo (moto o automóvil)
            
        Returns:
            Lista de vehículos
        """
        vehiculos = cargar_datos(vehiculos.ARCHIVO)
        
        if not isinstance(vehiculos, dict):
            vehiculos = {}
        
        lista = []
        for v in vehiculos.values():
            if v.get("estado") == "activo":
                if disponibles_solo and not v.get("disponible"):
                    continue
                if tipo and v.get("tipo") != tipo.lower():
                    continue
                
                disponibilidad = "✅ Disponible" if v.get("disponible") else "❌ En uso"
                lista.append(
                    f"[ID: {v['id_vehiculo']}] {v['tipo'].upper()} | Placa: {v['placa']} | Modelo: {v['modelo']} | {disponibilidad}"
                )
        
        return lista
    
@staticmethod
def actualizar_disponibilidad(id_vehiculo: int, disponible: bool) -> bool:
        """
        Actualiza la disponibilidad de un vehículo
        
        Args:
            id_vehiculo: ID del vehículo
            disponible: True si está disponible, False si está en uso
            
        Returns:
            True si se actualizó, False si no existe
        """
        vehiculos = cargar_datos(vehiculos.ARCHIVO)
        
        if not isinstance(vehiculos, dict):
            vehiculos = {}
        
        vehiculo = vehiculos.get(str(id_vehiculo))
        if vehiculo:
            vehiculo["disponible"] = disponible
            vehiculos[str(id_vehiculo)] = vehiculo
            guardar_datos(vehiculos.ARCHIVO, vehiculos)
            return True
        
        return False
    

def menu_vehiculos():
        """Menú interactivo para gestión de vehículos"""
        while True:
            print("\n" + "="*60)
            print("🚗 GESTIÓN DE VEHÍCULOS")
            print("="*60)
            print("1. Registrar nuevo vehículo")
            print("2. Consultar vehículo por ID")
            print("3. Listar todos los vehículos")
            print("4. Listar vehículos disponibles")
            print("5. Listar por tipo")
            print("6. Volver al menú principal")
            print("="*60)
            
            opcion = input("Seleccione una opción: ").strip()
            
            if opcion == "1":
                print("\n--- REGISTRAR NUEVO VEHÍCULO ---")
                
                print("Tipos disponibles: moto, carro")
                tipo = obtener_entrada_segura(
                    "Tipo de vehículo: ",
                    validador=lambda x: x.lower() in vehiculo.TIPOS_VALIDOS
                )
                
                if tipo.lower()=="moto":
                    placa =obtener_entrada_segura("placa de moto (Ejemplo: ABC12D)",validador=lambda x: validar_placa(x,tipo_vehiculo="moto"))
                    
                else:
                    placa=obtener_entrada_segura("placa de carro (ejemplo:BTB213): ",validador=lambda x: validar_placa(x,tipo_vehiculo="carro"))
                    
                modelo = input("Modelo (opcional): ").strip()
                
                vehiculo.registrar_vehiculo(tipo, placa, modelo)
            
            elif opcion == "2":
                print("\n--- CONSULTAR VEHÍCULO ---")
                try:
                    id_vehiculo = int(input("ID del vehículo: "))
                    vehiculo = vehiculo.obtener_vehiculo(id_vehiculo)
                    
                    if vehiculo:
                        disponibilidad = "✅ Disponible" if vehiculo.get("disponible") else "❌ En uso"
                        print(f"\n✅ Vehículo encontrado:")
                        print(f"   ID: {vehiculo['id_vehiculo']}")
                        print(f"   Tipo: {vehiculo['tipo']}")
                        print(f"   Placa: {vehiculo['placa']}")
                        print(f"   Modelo: {vehiculo['modelo']}")
                        print(f"   {disponibilidad}")
                        print(f"   Estado: {vehiculo['estado']}")
                    else:
                        print("❌ Vehículo no encontrado.")
                except ValueError:
                    print("❌ ID inválido.")
            
            elif opcion == "3":
                print("\n--- LISTADO DE VEHÍCULOS ---")
                from utilidades import formatear_lista
                formatear_lista(
                    vehiculo.listar_vehiculos(),
                    "Vehículos Activos"
                )
            
            elif opcion == "4":
                print("\n--- VEHÍCULOS DISPONIBLES ---")
                from utilidades import formatear_lista
                formatear_lista(
                    vehiculo.listar_vehiculos(disponibles_solo=True),
                    "Vehículos Disponibles"
                )
            
            elif opcion == "5":
                print("\n--- FILTRAR POR TIPO ---")
                print("Tipos: moto, automóvil")
                tipo = input("Tipo: ").lower().strip()
                
                if tipo in vehiculo.TIPOS_VALIDOS:
                    from utilidades import formatear_lista
                    formatear_lista(
                        listar_vehiculos(tipo=tipo),
                        f"Vehículos tipo {tipo}"
                    )
                else:
                    print("❌ Tipo inválido.")
            
            elif opcion == "6":
                break
            
            else:
                print("❌ Opción inválida.")
