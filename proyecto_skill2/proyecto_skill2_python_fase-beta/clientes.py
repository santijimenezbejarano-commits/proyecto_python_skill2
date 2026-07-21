
from io import open

# Removed incomplete 'with open:' statement
from persistencia import cargar_datos, guardar_datos, obtener_proximo_id
from utilidades import validar_documento, limpiar_entrada, obtener_entrada_segura

TIPOS_VALIDOS = ["moto", "automóvil", "ambos"]

@staticmethod
def registrar_cliente(nombre: str, documento: str, tipo_vehiculo: str) -> dict:
        
        
        clientes = cargar_datos(clientes.ARCHIVO)
        
        # Validar documento único
        for cliente in clientes.values() if isinstance(clientes, dict) else clientes:
            if cliente.get("documento") == documento:
                print("❌ El documento ya está registrado.")
                return None
        
        # Generar ID
        nuevo_id = obtener_proximo_id(clientes.ARCHIVO, "id_cliente")
        
        cliente = {
            "id_cliente": nuevo_id,
            "nombre": limpiar_entrada(nombre),
            "documento": documento,
            "tipo_vehiculo": tipo_vehiculo.lower(),
            "estado": "activo"
        }
        
        # Guardar
        if isinstance(clientes, dict):
            clientes[str(nuevo_id)] = cliente
        else:
            clientes.append(cliente)
        
        guardar_datos(clientes.ARCHIVO, clientes)
        print(f"✅ Cliente '{nombre}' registrado exitosamente con ID {nuevo_id}.")
        return cliente
    
@staticmethod
def obtener_cliente(id_cliente: int) -> dict:
        """
        Obtiene un cliente por ID
        
        Args:
            id_cliente: ID del cliente
            
        Returns:
            Diccionario con datos del cliente o None
        """
        clientes = cargar_datos(clientes.ARCHIVO)
        
        if isinstance(clientes, dict):
            return clientes.get(str(id_cliente))
        else:
            for cliente in clientes:
                if cliente.get("id_cliente") == id_cliente:
                    return cliente
        
        return None
    
@staticmethod
def obtener_cliente_por_documento(documento: str) -> dict:
        """
        Obtiene un cliente por documento
        
        Args:
            documento: Documento del cliente
            
        Returns:
            Diccionario con datos del cliente o None
        """
        clientes = cargar_datos(clientes.ARCHIVO)
        
        for cliente in clientes.values() if isinstance(clientes, dict) else clientes:
            if cliente.get("documento") == documento:
                return cliente
        
        return None
    
@staticmethod
def listar_clientes() -> list:
        """
        Lista todos los clientes
        
        Returns:
            Lista de clientes activos
        """
        clientes = cargar_datos(clientes.ARCHIVO)
        
        if isinstance(clientes, dict):
            clientes = list(clientes.values())
        
        activos = [c for c in clientes if c.get("estado") == "activo"]
        
        return [
            f"[ID: {c['id_cliente']}] {c['nombre']} | Doc: {c['documento']} | Vehículo: {c['tipo_vehiculo']}"
            for c in activos
        ]
    
@staticmethod
def actualizar_cliente(id_cliente: int, **kwargs) -> bool:
      
        clientes = cargar_datos(clientes.ARCHIVO)
        
        if isinstance(clientes, dict):
            cliente = clientes.get(str(id_cliente))
            if cliente:
                cliente.update(kwargs)
                clientes[str(id_cliente)] = cliente
        else:
            for cliente in clientes:
                if cliente.get("id_cliente") == id_cliente:
                    cliente.update(kwargs)
                    break
            else:
                return False
        
        guardar_datos(clientes.ARCHIVO, clientes)
        return True
    
@staticmethod
def menu_clientes():
        """Menú interactivo para gestión de clientes"""
        while True:
            print("\n" + "="*60)
            print("📋 GESTIÓN DE CLIENTES")
            print("="*60)
            print("1. Registrar nuevo cliente")
            print("2. Consultar cliente por ID")
            print("3. Listar todos los clientes")
            print("4. Volver al menú principal")
            print("="*60)
            
            opcion = input("Seleccione una opción: ").strip()
            
            if opcion == "1":
                print("\n--- REGISTRAR NUEVO CLIENTE ---")
                nombre = obtener_entrada_segura("Nombre del cliente: ")
                documento = obtener_entrada_segura(
                    "Documento (6-12 dígitos): ",
                    validador=validar_documento
                )
                
                print("\nTipos de vehículo disponibles: moto, automóvil, ambos")
                tipo_vehiculo = obtener_entrada_segura(
                    "Tipo de vehículo: ",
                    validador=lambda x: x.lower() in TIPOS_VALIDOS
                )
                
                (nombre, documento, tipo_vehiculo)
            
            elif opcion == "2":
                print("\n--- CONSULTAR CLIENTE ---")
                try:
                    id_cliente = int(input("ID del cliente: "))
                    cliente = cliente.obtener_cliente(id_cliente)
                    
                    if cliente:
                        print(f"\n✅ Cliente encontrado:")
                        print(f"   ID: {cliente['id_cliente']}")
                        print(f"   Nombre: {cliente['nombre']}")
                        print(f"   Documento: {cliente['documento']}")
                        print(f"   Tipo de vehículo: {cliente['tipo_vehiculo']}")
                        print(f"   Estado: {cliente['estado']}")
                    else:
                        print("❌ Cliente no encontrado.")
                except ValueError:
                    print("❌ ID inválido.")
            
            elif opcion == "3":
                print("\n--- LISTADO DE CLIENTES ---")
                from utilidades import formatear_lista
                formatear_lista(cliente.listar_clientes(), "Clientes Activos")
            
            elif opcion == "4":
                break
            
            else:
                print("❌ Opción inválida.")
