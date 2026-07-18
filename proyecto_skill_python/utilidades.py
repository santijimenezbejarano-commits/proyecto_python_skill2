"""
Módulo de utilidades: Funciones auxiliares y validaciones
"""
from datetime import datetime
import re

def validar_documento(documento: str) -> bool:
    """
    Valida formato de documento (solo números, 6-12 dígitos)
    
    Args:
        documento: Documento a validar
        
    Returns:
        True si es válido, False en caso contrario
    """
    return bool(re.match(r'^\d{6,12}$', documento.strip()))

def validar_placa(placa: str, tipo_vehiculo: str = None) -> bool:
    """
    Valida el formato de placa según el tipo de vehículo.
    
    - Carro/automóvil: ABC123
    - Moto: ABC12 o ABC12D
    
    Args:
        placa: Placa a validar
        tipo_vehiculo: Tipo de vehículo (moto o automóvil)
        
    Returns:
        True si es válida, False en caso contrario
    """
    placa_limpia = placa.strip().upper()
    if not placa_limpia:
        return False

    tipo = (tipo_vehiculo or "").strip().lower()

    if tipo in {"moto", "motocicleta"}:
        return bool(re.match(r'^[A-Z]{3}\d{2}[A-Z]?$', placa_limpia))

    if tipo in {"automóvil", "carro", "auto", "car"}:
        return bool(re.match(r'^[A-Z]{3}\d{3}$', placa_limpia))

    return bool(re.match(r'^(?:[A-Z]{3}\d{3}|[A-Z]{3}\d{2}[A-Z]?)$', placa_limpia))

def validar_fecha(fecha_str: str, formato: str = "%d/%m/%Y") -> bool:
    """
    Valida formato de fecha
    
    Args:
        fecha_str: Fecha en formato string
        formato: Formato esperado
        
    Returns:
        True si es válida, False en caso contrario
    """
    try:
        datetime.strptime(fecha_str.strip(), formato)
        return True
    except ValueError:
        return False

def validar_hora(hora_str: str) -> bool:
    """
    Valida formato de hora (HH:MM)
    
    Args:
        hora_str: Hora en formato string
        
    Returns:
        True si es válida, False en caso contrario
    """
    return bool(re.match(r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$', hora_str.strip()))

def es_fecha_futura(fecha_str: str, formato: str = "%d/%m/%Y") -> bool:
    """
    Valida que la fecha sea futura o actual
    
    Args:
        fecha_str: Fecha a validar
        formato: Formato de la fecha
        
    Returns:
        True si es futura o actual, False si es pasada
    """
    try:
        fecha = datetime.strptime(fecha_str.strip(), formato)
        return fecha.date() >= datetime.now().date()
    except ValueError:
        return False

def limpiar_entrada(entrada: str) -> str:
    """
    Limpia y normaliza entrada del usuario
    
    Args:
        entrada: Entrada del usuario
        
    Returns:
        Entrada limpiada
    """
    return entrada.strip()

def obtener_entrada_segura(prompt: str, validador=None) -> str:
    """
    Obtiene entrada del usuario con validación opcional
    
    Args:
        prompt: Mensaje a mostrar
        validador: Función de validación (opcional)
        
    Returns:
        Entrada validada del usuario
    """
    while True:
        entrada = limpiar_entrada(input(prompt))
        
        if not entrada:
            print("⚠️ La entrada no puede estar vacía.")
            continue
        
        if validador and not validador(entrada):
            print("❌ Entrada inválida. Intente de nuevo.")
            continue
        
        return entrada

def formatear_lista(elementos: list, titulo: str = "Registros") -> None:
    """
    Imprime una lista de elementos de forma formateada
    
    Args:
        elementos: Lista de elementos a mostrar
        titulo: Título de la lista
    """
    if not elementos:
        print(f"\n📋 {titulo}: No hay registros disponibles.\n")
        return
    
    print(f"\n📋 {titulo}:")
    print("=" * 80)
    for i, elemento in enumerate(elementos, 1):
        print(f"{i}. {elemento}")
    print("=" * 80 + "\n")

def pausar():
    """Pausa la ejecución hasta que el usuario presione Enter"""
    input("\nPresione Enter para continuar...")
