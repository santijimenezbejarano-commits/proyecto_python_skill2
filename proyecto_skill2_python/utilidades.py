
from datetime import datetime
import re


def validar_nombre(nombre: str) -> bool:
    if not nombre:
        return False

    nombre_limpio = nombre.strip()
    if not nombre_limpio:
        return False

    return bool(re.fullmatch(
    r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+(?:[ -][A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+)*",nombre_limpio, )
    )

def validar_documento_inicio(documento: str) -> bool:
    """Valida documentos de 6 a 12 dígitos que no comiencen en cero."""
    if not isinstance(documento, str):
        return False

    return bool(re.fullmatch(r"[1-9]\d{5,11}", documento.strip()))


def validar_si_no(valor: str) -> bool:
    """Valida una respuesta afirmativa o negativa escrita como S o N."""
    if not isinstance(valor, str):
        return False

    return valor.strip().upper() in {"S", "N"}

def validar_si(valor: str) -> bool:
    """Valida una respuesta afirmativa o negativa escrita como S o N."""
    if not isinstance(valor, str):
        return False

    return valor.strip().upper() in {"si"}

def validar_estado(estado: str) -> bool:
    """Valida si un estado es 'activo' o 'inactivo'."""
    if not estado:
        return False

    estado_limpio = estado.strip().lower()
    return estado_limpio in {"activo", "inactivo"}


def esta_activo(estado: str) -> bool:
    """Devuelve True solo si el estado es 'activo'."""
    if not isinstance(estado, str):
        return False

    return estado.strip().lower() == "activo"

def esta_inactivo(estado: str) -> bool:
    """Devuelve True solo si el estado es 'inactivo'."""
    if not isinstance(estado, str):
        return False

    return estado.strip().lower() == "inactivo"

def validar_placa(placa: str, tipo_vehiculo: str = None) -> bool:
    
    placa_limpia = placa.strip().upper()
    if not placa_limpia:
        return False

    tipo = (tipo_vehiculo or "").strip().lower()

    if tipo in {"moto", "motocicleta"}:
        return bool(re.match(r'^[A-Z]{3}\d{2}[A-Z]?$', placa_limpia))

    if tipo in {"automóvil", "carro", "camion", "car"}:
        return bool(re.match(r'^[A-Z]{3}\d{3}$', placa_limpia))

    return bool(re.match(r'^(?:[A-Z]{3}\d{3}|[A-Z]{3}\d{2}[A-Z]?)$', placa_limpia))

def validar_fecha(fecha_str: str, formato: str = "%d/%m/%Y") -> bool:
    
    try:
        datetime.strptime(fecha_str.strip(), formato)
        return True
    except ValueError:
        return False

PATRON_HORA = r"^([0-1]?\d|2[0-3]):[0-5]\d$"

def validar_hora(hora_str: str) -> bool:
    return bool(re.fullmatch(PATRON_HORA, hora_str.strip()))

def es_hora_laboral(hora_str: str) -> bool:
    if not validar_hora(hora_str):
        return False

    hora = datetime.strptime(hora_str.strip(), "%H:%M").time()
    inicio = datetime.strptime("08:00", "%H:%M").time()
    fin = datetime.strptime("17:00", "%H:%M").time()

    return inicio <= hora <= fin

def es_fecha_futura(fecha_str: str, formato: str = "%d/%m/%Y") -> bool:
    
    try:
        fecha = datetime.strptime(fecha_str.strip(), formato)
        return fecha.date() >= datetime.now().date()
    except ValueError:
        return False

def limpiar_entrada(entrada: str) -> str:
    
    return entrada.strip()

def obtener_entrada_segura(prompt: str, validador=None, default: str = None, allow_empty: bool = False, timeout: int = None) -> str:
    
    use_alarm = False
    try:
        import signal
        use_alarm = hasattr(signal, 'alarm') and timeout is not None and timeout > 0
    except Exception:
        signal = None
        use_alarm = False

    while True:
        try:
            if use_alarm:
                # Instala handler temporal que lanza TimeoutError
                def _handler(signum, frame):
                    raise TimeoutError

                old_handler = signal.signal(signal.SIGALRM, _handler)
                signal.alarm(timeout)

            entrada_raw = input(prompt)
            if use_alarm:
                # Desactiva la alarma inmediatamente después de la entrada
                signal.alarm(0)
                signal.signal(signal.SIGALRM, old_handler)

            entrada = limpiar_entrada(entrada_raw)

        except TimeoutError:
            print(f"⚠️ Tiempo de espera ({timeout}s) agotado.")
            if default is not None:
                print(f"Usando valor por defecto: {default}")
                return default
            else:
                # Si no hay default, volver a intentar
                continue
        except Exception as e:
            # En plataformas que no soportan signal.alarm no se interrumpe input; solo informar y continuar
            if timeout is not None and not use_alarm:
                print("⚠️ El parámetro 'timeout' no es compatible con esta plataforma; se ignora.")
            entrada = limpiar_entrada(str(e)) if isinstance(e, str) else ""

        # Si el usuario presionó Enter sin escribir nada
        if entrada == "":
            if default is not None:
                # Devolver el default si está especificado
                return default
            if allow_empty:
                return ""
            print("⚠️ La entrada no puede estar vacía.")
            continue

        # Validación opcional
        if validador and not validador(entrada):
            print("❌ Entrada inválida. Intente de nuevo.")
            continue

        return entrada

def formatear_lista(elementos: list, titulo: str, etiqueta: str = "Registros") -> None:

    if not elementos:
        print(f"\n📋 {titulo}: No hay registros disponibles.\n")
        return

    print(f"\n📋 {titulo}:")
    for i, elemento in enumerate(elementos, 1):
        print(f"{i}. {elemento}")
        
    print("\n")

def pausar():
    """Pausa la ejecución hasta que el usuario presione Enter"""
    input("\nPresione Enter para continuar...")
