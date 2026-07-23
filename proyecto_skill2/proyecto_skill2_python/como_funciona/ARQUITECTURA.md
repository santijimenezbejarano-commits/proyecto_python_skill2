# 🏗️ Arquitectura del Proyecto - Academia DriveSafe

## Visión General

La aplicación **DriveSafe** es un sistema modular basado en POO (Programación Orientada a Objetos) diseñado para gestionar citas de práctica en una academia de conducción.

## 🔄 Flujo de la Aplicación

```
┌─────────────────────────────────────────┐
│      main.py - Punto de Entrada         │
│    (Menú Principal e Interacción)       │
└──────────────┬──────────────────────────┘
               │
       ┌───────┴───────┬────────┬──────────┬──────────┐
       │               │        │          │          │
       v               v        v          v          v
   Clientes      Instructores Vehiculos  Citas    Reportes
   (Opción 1)    (Opción 2)  (Opción 3) (Opción 4)(Opción 5)
       │               │        │          │          │
       └───────┬───────┴────────┴──────────┴──────────┘
               │
       ┌───────v──────────────────────────┐
       │  Utilidades & Validaciones       │
       │  (utilidades.py)                 │
       └───────┬──────────────────────────┘
               │
       ┌───────v──────────────────────────┐
       │  Persistencia (JSON)             │
       │  (persistencia.py)               │
       │  └─> datos/ [JSON files]         │
       └──────────────────────────────────┘
```

## 📦 Módulos Principales

### 1. **main.py** - Punto de Entrada
**Responsabilidad**: Menú interactivo y coordinación

```
┌─────────────────────────────────────────┐
│  Función: main()                        │
│  ├── mostrar_banner()                   │
│  └── menu_principal()                   │
│      ├── menu_clientes()                │
│      ├── menu_instructores()            │
│      ├── menu_vehiculos()               │
│      ├── menu_citas()                   │
│      └── menu_reportes()                │
└─────────────────────────────────────────┘
```

**Exports**: Funciones de menú  
**Dependencias**: clientes, instructores, vehiculos, citas

---

### 2. **clientes.py** - Gestión de Clientes
**Responsabilidad**: CRUD de clientes y menú

```
┌─────────────────────────────────────────┐
│  Clase: Clientes                        │
├─────────────────────────────────────────┤
│  Métodos Estáticos:                     │
│  ├── registrar_cliente()                │
│  ├── obtener_cliente()                  │
│  ├── obtener_cliente_por_documento()    │
│  ├── listar_clientes()                  │
│  ├── actualizar_cliente()               │
│  └── menu_clientes()                    │
├─────────────────────────────────────────┤
│  Constantes:                            │
│  ├── ARCHIVO = "clientes"               │
│  └── TIPOS_VALIDOS = [...]              │
└─────────────────────────────────────────┘
```

**Estructura de Datos**:
```json
{
    "1": {
        "id_cliente": 1,
        "nombre": "Juan Pérez",
        "documento": "1023456789",
        "tipo_vehiculo": "automóvil",
        "estado": "activo"
    }
}
```

**Validaciones**:
- Documento único (6-12 dígitos)
- Nombre no vacío
- Tipo válido (moto, automóvil, ambos)

---

### 3. **instructores.py** - Gestión de Instructores
**Responsabilidad**: CRUD de instructores y menú

```
┌─────────────────────────────────────────┐
│  Clase: Instructores                    │
├─────────────────────────────────────────┤
│  Métodos Estáticos:                     │
│  ├── registrar_instructor()             │
│  ├── obtener_instructor()               │
│  ├── listar_instructores()              │
│  ├── actualizar_instructor()            │
│  └── menu_instructores()                │
├─────────────────────────────────────────┤
│  Constantes:                            │
│  ├── ARCHIVO = "instructores"           │
│  └── ESPECIALIDADES_VALIDAS = [...]     │
└─────────────────────────────────────────┘
```

**Estructura de Datos**:
```json
{
    "1": {
        "id_instructor": 1,
        "nombre": "Carlos López",
        "documento": "987654321",
        "especialidad": "carro",
        "estado": "activo"
    }
}
```

**Validaciones**:
- Documento único (6-12 dígitos)
- Especialidad válida (moto, carro)
- Nombre no vacío

---

### 4. **vehiculos.py** - Gestión de Vehículos
**Responsabilidad**: CRUD de vehículos y control de disponibilidad

```
┌─────────────────────────────────────────┐
│  Clase: Vehiculos                       │
├─────────────────────────────────────────┤
│  Métodos Estáticos:                     │
│  ├── registrar_vehiculo()               │
│  ├── obtener_vehiculo()                 │
│  ├── listar_vehiculos()                 │
│  ├── actualizar_disponibilidad()        │
│  └── menu_vehiculos()                   │
├─────────────────────────────────────────┤
│  Constantes:                            │
│  ├── ARCHIVO = "vehiculos"              │
│  └── TIPOS_VALIDOS = ["moto", ...]      │
└─────────────────────────────────────────┘
```

**Estructura de Datos**:
```json
{
    "1": {
        "id_vehiculo": 1,
        "tipo": "automóvil",
        "placa": "ABC123",
        "modelo": "Toyota Corolla",
        "disponible": true,
        "estado": "activo"
    }
}
```

**Validaciones**:
- Placa única en formato ABC123
- Tipo válido (moto, automóvil)
- Control de disponibilidad

---

### 5. **citas.py** - Gestión de Citas
**Responsabilidad**: CRUD de citas, validaciones complejas y menú

```
┌─────────────────────────────────────────┐
│  Clase: Citas                           │
├─────────────────────────────────────────┤
│  Métodos Estáticos:                     │
│  ├── programar_cita()                   │
│  ├── obtener_cita()                     │
│  ├── registrar_asistencia()             │
│  ├── listar_citas()                     │
│  ├── historial_cliente()                │
│  └── menu_citas()                       │
├─────────────────────────────────────────┤
│  Constantes:                            │
│  ├── ARCHIVO = "citas"                  │
│  └── DURACIONES_VALIDAS = [...]         │
└─────────────────────────────────────────┘
```

**Estructura de Datos**:
```json
[
    {
        "id_cita": 1,
        "id_cliente": 1,
        "id_instructor": 1,
        "id_vehiculo": 1,
        "fecha": "20/07/2026",
        "hora": "14:30",
        "duracion": 60,
        "estado": "programada",
        "asistencia": null,
        "observaciones": ""
    }
]
```

**Validaciones**:
- Fecha futura (DD/MM/YYYY)
- Hora válida (HH:MM)
- Duración permitida (30, 45, 60, 90, 120)
- Especialidad instructor = tipo vehículo
- Vehículo disponible
- Cliente, instructor, vehículo existen

---

### 6. **persistencia.py** - Manejo de Datos
**Responsabilidad**: Carga, guardado y gestión de IDs

```
┌─────────────────────────────────────────┐
│  Funciones:                             │
├─────────────────────────────────────────┤
│  ├── inicializar_datos()                │
│  ├── guardar_datos()                    │
│  ├── cargar_datos()                     │
│  └── obtener_proximo_id()               │
└─────────────────────────────────────────┘
```

**Características**:
- Formato JSON
- Carga/guardado automático
- IDs autoincrementales
- Directorio `datos/` automático

**Archivos Generados**:
```
datos/
├── clientes.json
├── instructores.json
├── vehiculos.json
└── citas.json
```

---

### 7. **utilidades.py** - Funciones Auxiliares
**Responsabilidad**: Validaciones y funciones comunes

```
┌──────────────────────────────────────────────┐
│  Validaciones:                               │
├──────────────────────────────────────────────┤
│  ├── validar_documento()                     │
│  ├── validar_placa()                         │
│  ├── validar_fecha()                         │
│  ├── validar_hora()                          │
│  └── es_fecha_futura()                       │
├──────────────────────────────────────────────┤
│  Entrada/Salida:                             │
├──────────────────────────────────────────────┤
│  ├── limpiar_entrada()                       │
│  ├── obtener_entrada_segura()                │
│  ├── formatear_lista()                       │
│  └── pausar()                                │
└──────────────────────────────────────────────┘
```

---

## 🔐 Validaciones del Sistema

```
ANTES DE PROGRAMAR CITA:

Cita
├── ¿Cliente existe? → ❌ Rechazar
├── ¿Instructor existe? → ❌ Rechazar
├── ¿Vehículo existe? → ❌ Rechazar
├── ¿Vehículo disponible? → ❌ Rechazar
├── Especialidad Instructor = Tipo Vehículo? → ❌ Rechazar
├── Fecha futura? → ❌ Rechazar
├── Hora válida? → ❌ Rechazar
├── Duración válida? → ❌ Rechazar
└── ✅ Crear Cita y marcar vehículo NO disponible
```

## 🔄 Ciclo de Vida de una Cita

```
1. PROGRAMADA
   ├── Vehículo: NO disponible
   ├── Asistencia: NULL (pendiente)
   └── Estado: programada

2. ASISTENCIA REGISTRADA
   ├── Vehículo: Disponible
   ├── Asistencia: TRUE/FALSE
   └── Estado: completada / no_presentado
```

## 📊 Flujo de Datos

```
┌──────────────┐
│   Usuario    │
└──────┬───────┘
       │ (entrada)
       v
┌──────────────────┐
│  Menús (.py)     │ Validación inicial
└──────┬───────────┘
       │
       v
┌──────────────────┐
│  Clases (CRUD)   │ Validación de negocio
└──────┬───────────┘
       │
       v
┌──────────────────┐
│  Utilidades      │ Validaciones específicas
└──────┬───────────┘
       │
       v
┌──────────────────┐
│  Persistencia    │ Guardar/Cargar JSON
└──────┬───────────┘
       │
       v
┌──────────────────┐
│  Archivos JSON   │ Almacenamiento
└──────────────────┘
```
Líneas de Código (aprox):
├── main.py:         ~269 líneas
├── clientes.py:     ~221 líneas
├── instructores.py: ~217 líneas
├── vehiculos.py:    ~225 líneas
├── citas.py:        ~280 líneas
├── utilidades.py:   ~129 líneas
├── persistencia.py: ~93 líneas
└── TOTAL:           ~1,434 líneas

Archivos:
├── Código (.py):    7 archivos
└── Datos:           4 directorio (creado dinámicamente)
```