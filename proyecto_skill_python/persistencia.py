"""
Módulo de persistencia: Carga y guarda datos en archivos JSON
"""
import json
import os
from typing import Any, Dict

DATOS_DIR = "datos"

def inicializar_datos():
    """Crea el directorio de datos si no existe"""
    if not os.path.exists(DATOS_DIR):
        os.makedirs(DATOS_DIR)

def guardar_datos(nombre_archivo: str, datos: Any) -> bool:
    """
    Guarda datos en un archivo JSON
    
    Args:
        nombre_archivo: Nombre del archivo (sin extensión)
        datos: Datos a guardar
        
    Returns:
        True si se guardó exitosamente, False en caso contrario
    """
    try:
        inicializar_datos()
        ruta = os.path.join(DATOS_DIR, f"{nombre_archivo}.json")
        with open(ruta, 'w', encoding='utf-8') as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"❌ Error al guardar datos: {e}")
        return False

def cargar_datos(nombre_archivo: str) -> Dict | list:
    """
    Carga datos desde un archivo JSON
    
    Args:
        nombre_archivo: Nombre del archivo (sin extensión)
        
    Returns:
        Datos cargados o estructura vacía si no existe el archivo
    """
    try:
        inicializar_datos()
        ruta = os.path.join(DATOS_DIR, f"{nombre_archivo}.json")
        
        if not os.path.exists(ruta):
            return {} if nombre_archivo != "citas" else []
        
        with open(ruta, 'r', encoding='utf-8') as archivo:
            return json.load(archivo)
    except Exception as e:
        print(f"⚠️ Advertencia al cargar datos: {e}")
        return {} if nombre_archivo != "citas" else []

def obtener_proximo_id(nombre_archivo: str, clave_id: str = "id") -> int:
    """
    Obtiene el próximo ID disponible para una entidad
    
    Args:
        nombre_archivo: Nombre del archivo de datos
        clave_id: Nombre de la clave del ID
        
    Returns:
        Próximo ID disponible
    """
    datos = cargar_datos(nombre_archivo)
    
    if isinstance(datos, dict):
        datos = list(datos.values())
    
    if not datos:
        return 1
    
    ids = [item.get(clave_id, 0) for item in datos if isinstance(item, dict)]
    return max(ids) + 1 if ids else 1
