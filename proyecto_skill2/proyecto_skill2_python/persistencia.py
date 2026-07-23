
import json
import os
from typing import Any, Dict

DATOS_DIR = "datos"

def inicializar_datos():
    """Crea el directorio de datos si no existe"""
    if not os.path.exists(DATOS_DIR):
        os.makedirs(DATOS_DIR)

def guardar_datos(nombre_archivo: str, datos: Any) -> bool:

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

    try:
        inicializar_datos()
        ruta = os.path.join(DATOS_DIR, f"{nombre_archivo}.json")

        if not os.path.exists(ruta):
            return {} if nombre_archivo != "citas" else []

        with open(ruta, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read().strip()

        if not contenido:
            return {} if nombre_archivo != "citas" else []

        return json.loads(contenido)
    except json.JSONDecodeError as e:
        print(f"⚠️ Archivo JSON inválido en {ruta}: {e}. Se usará un estado vacío.")
        return {} if nombre_archivo != "citas" else []
    except Exception as e:
        print(f"⚠️ Advertencia al cargar datos: {e}")
        return {} if nombre_archivo != "citas" else []

def importar_json(nombre_archivo: str, ruta_archivo: str, reemplazar: bool = False) -> bool:
    """Importa datos desde un archivo JSON al almacenamiento del proyecto."""
    try:
        if not os.path.exists(ruta_archivo):
            print(f"❌ No se encontró el archivo: {ruta_archivo}")
            return False

        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            datos_importados = json.load(archivo)

        if not isinstance(datos_importados, (dict, list)):
            print("❌ El contenido del archivo JSON debe ser un objeto o una lista.")
            return False

        if reemplazar:
            datos_finales = datos_importados
        else:
            datos_existentes = cargar_datos(nombre_archivo)

            if isinstance(datos_existentes, dict) and isinstance(datos_importados, dict):
                datos_finales = {**datos_existentes, **datos_importados}
            elif isinstance(datos_existentes, list) and isinstance(datos_importados, list):
                datos_finales = datos_existentes + datos_importados
            else:
                datos_finales = datos_importados

        return guardar_datos(nombre_archivo, datos_finales)
    except json.JSONDecodeError as e:
        print(f"❌ El archivo no es un JSON válido: {e}")
        return False
    except Exception as e:
        print(f"❌ Error al importar datos: {e}")
        return False

def obtener_proximo_id(nombre_archivo: str, clave_id: str = "id") -> int:
    
    datos = cargar_datos(nombre_archivo)
    
    if isinstance(datos, dict):
        datos = list(datos.values())
    
    if not datos:
        return 1
    
    ids = [item.get(clave_id, 0) for item in datos if isinstance(item, dict)]
    return max(ids) + 1 if ids else 1
