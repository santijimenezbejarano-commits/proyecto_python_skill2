# 📖 Guía de Ejemplo de Uso - Academia DriveSafe

Esta guía muestra un flujo completo de uso de la aplicación con ejemplos prácticos.

## 🎯 Escenario

Imaginemos que es lunes 17 de julio de 2026 y queremos:
1. Registrar un nuevo cliente
2. Registrar instructores
3. Registrar vehículos
4. Programar una cita
5. Registrar asistencia

---

## Paso 1: Registrar Clientes

**Menú Principal → Opción 1 (Gestionar Clientes) → Opción 1 (Registrar)**

```
--- REGISTRAR NUEVO CLIENTE ---
Nombre del cliente: Juan Pérez García
Documento (6-12 dígitos): 1023456789
Tipo de vehículo: automóvil
✅ Cliente 'Juan Pérez García' registrado exitosamente con ID 1.
```

Registrar otro cliente:
```
Nombre del cliente: María López Rodríguez
Documento (6-12 dígitos): 1087654321
Tipo de vehículo: moto
✅ Cliente 'María López Rodríguez' registrado exitosamente con ID 2.
```

---

## Paso 2: Registrar Instructores

**Menú Principal → Opción 2 (Gestionar Instructores) → Opción 1 (Registrar)**

```
--- REGISTRAR NUEVO INSTRUCTOR ---
Nombre del instructor: Carlos Martínez
Documento (6-12 dígitos): 987654321
Especialidades disponibles: moto, carro
Especialidad: carro
✅ Instructor 'Carlos Martínez' registrado exitosamente con ID 1.
```

Registrar otro instructor:
```
Nombre del instructor: Ana Gómez
Documento (6-12 dígitos): 987654322
Especialidad: moto
✅ Instructor 'Ana Gómez' registrado exitosamente con ID 2.
```

---

## Paso 3: Registrar Vehículos

**Menú Principal → Opción 3 (Gestionar Vehículos) → Opción 1 (Registrar)**

```
--- REGISTRAR NUEVO VEHÍCULO ---
Tipos disponibles: moto, automóvil
Tipo de vehículo: automóvil
Placa (formato: ABC123): ABC123
Modelo (opcional): Toyota Corolla 2020
✅ Vehículo 'ABC123' registrado exitosamente con ID 1.
```

Registrar otro vehículo:
```
Tipo de vehículo: moto
Placa (formato: ABC123): XYZ789
Modelo (opcional): Honda CB 500
✅ Vehículo 'XYZ789' registrado exitosamente con ID 2.
```

---

## Paso 4: Programar Cita

**Menú Principal → Opción 4 (Gestionar Citas) → Opción 1 (Programar)**

```
--- PROGRAMAR NUEVA CITA ---
ID del cliente: 1
ID del instructor: 1
ID del vehículo: 1
Fecha (DD/MM/YYYY): 20/07/2026
Hora (HH:MM): 14:30
Duraciones disponibles (minutos): [30, 45, 60, 90, 120]
Duración: 60
Observaciones (opcional): Primera práctica en ciudad
✅ Cita programada exitosamente con ID 1.
```

**Nota**: En este punto:
- La cita se ha creado exitosamente
- El vehículo ABC123 ha sido marcado como "no disponible"
- El cliente, instructor y vehículo deben coincidir en especialidad

---

## Paso 5: Consultar la Cita

**Menú Principal → Opción 4 (Gestionar Citas) → Opción 2 (Consultar)**

```
--- CONSULTAR CITA ---
ID de la cita: 1

✅ Cita encontrada:
   ID: 1
   Cliente: Juan Pérez García
   Instructor: Carlos Martínez
   Vehículo: ABC123
   Fecha: 20/07/2026
   Hora: 14:30
   Duración: 60 minutos
   Estado: programada
   Observaciones: Primera práctica en ciudad
```

---

## Paso 6: Registrar Asistencia

**Menú Principal → Opción 4 (Gestionar Citas) → Opción 4 (Registrar Asistencia)**

Después de que se complete la cita (supongamos que fue exitosa):

```
--- REGISTRAR ASISTENCIA ---
ID de la cita: 1
¿Asistió el cliente?
1. Sí
2. No
Respuesta: 1
Observaciones de la práctica: Práctica exitosa. Cliente mostró buen dominio en giros. Necesita mejorar en estacionamiento.
✅ Asistencia registrada.
```

En este punto:
- La cita pasa a estado "completada"
- El vehículo se libera (marcado como disponible nuevamente)
- Las observaciones se guardan en la cita

---

## Paso 7: Consultar Historial de Cliente

**Menú Principal → Opción 5 (Reportes) → Opción 5 (Historial)**

```
--- HISTORIAL DETALLADO DE CLIENTE ---
ID del cliente: 1

======================================================================
HISTORIAL DE JUAN PÉREZ GARCÍA
======================================================================

1. [ID: 1] 20/07/2026 14:30 | Cliente: Juan Pérez García | 
   Instructor: Carlos Martínez | Vehículo: ABC123 | 
   Duración: 60min | Estado: completada [✅ Asistió]

======================================================================
RESUMEN:
  - Prácticas completadas: 1
  - No presentado: 0
  - Pendientes: 0
======================================================================
```

---

## Paso 8: Consultar Citas Próximas

**Menú Principal → Opción 5 (Reportes) → Opción 2 (Citas próximas)**

```
--- CITAS PRÓXIMAS (7 DÍAS) ---

======================================================================
Fecha: 21/07/2026 | Hora: 10:00
  Cliente: María López Rodríguez
  Instructor: Ana Gómez
  Vehículo: XYZ789
----------------------------------------------------------------------
Fecha: 22/07/2026 | Hora: 15:30
  Cliente: Pedro García
  Instructor: Carlos Martínez
  Vehículo: ABC123
======================================================================
```

---

## 📋 Listados Disponibles

### Listar Clientes
**Menú → Opción 1 → Opción 3**
```
📋 Clientes Activos:
================================================================================
1. [ID: 1] Juan Pérez García | Doc: 1023456789 | Vehículo: automóvil
2. [ID: 2] María López Rodríguez | Doc: 1087654321 | Vehículo: moto
================================================================================
```

### Listar Instructores
**Menú → Opción 2 → Opción 3**
```
📋 Instructores Activos:
================================================================================
1. [ID: 1] Carlos Martínez | Especialidad: carro
2. [ID: 2] Ana Gómez | Especialidad: moto
================================================================================
```

### Listar Vehículos
**Menú → Opción 3 → Opción 3**
```
📋 Vehículos Activos:
================================================================================
1. [ID: 1] AUTOMÓVIL | Placa: ABC123 | Modelo: Toyota Corolla 2020 | ❌ En uso
2. [ID: 2] MOTO | Placa: XYZ789 | Modelo: Honda CB 500 | ✅ Disponible
================================================================================
```

---

## ⚠️ Casos de Error Comunes

### Error: Documento duplicado
```
Nombre del cliente: otro nombre
Documento: 1023456789  (ya existe)
❌ El documento ya está registrado.
```

### Error: Placa inválida
```
Placa (formato: ABC123): abc123
❌ Entrada inválida. Intente de nuevo.
```

### Error: Instructor no coincide con vehículo
```
ID del cliente: 2
ID del instructor: 1  (especialidad: carro)
ID del vehículo: 2    (tipo: moto)
❌ El instructor está especializado en carro, no en moto.
```

### Error: Vehículo no disponible
```
ID del vehículo: 1
❌ El vehículo no está disponible.
```

### Error: Fecha pasada
```
Fecha (DD/MM/YYYY): 15/07/2026
❌ Entrada inválida. Intente de nuevo.
```

---

## 🎯 Casos de Uso Adicionales

### Caso: Cliente no asistió a la cita

```
--- REGISTRAR ASISTENCIA ---
ID de la cita: 1
¿Asistió el cliente?
1. Sí
2. No
Respuesta: 2
Observaciones de la práctica: Cliente no se presentó a la cita programada.
✅ Asistencia registrada.
```

Estado de la cita cambia a "no_presentado" y el vehículo se libera.

### Caso: Filtrar instructores por especialidad

```
Menú → Opción 2 → Opción 4

--- FILTRAR POR ESPECIALIDAD ---
Especialidades: moto, carro
Especialidad: moto

📋 Instructores de moto:
================================================================================
1. [ID: 2] Ana Gómez | Especialidad: moto
================================================================================
```

---

## 📁 Archivos Generados

Después de los pasos anteriores, se habrán creado automáticamente:

```
datos/
├── clientes.json (2 clientes registrados)
├── instructores.json (2 instructores registrados)
├── vehiculos.json (2 vehículos registrados)
└── citas.json (1 cita programada y completada)
```

Los archivos JSON contienen todos los datos y se actualizan automáticamente con cada operación.

---

## 💡 Consejos de Uso

1. **Siempre registre primero**: Clientes → Instructores → Vehículos → Citas
2. **Verifique disponibilidad**: Antes de programar una cita, consulte vehículos disponibles
3. **Anote IDs**: Mantenga un registro de los IDs para agilizar consultas
4. **Revise reportes regularmente**: Los reportes le darán una visión general del sistema
5. **Cumpla validaciones**: Las validaciones protegen la integridad de los datos

---

**¡Listo! Ya sabe cómo usar DriveSafe. ¡A conducir seguro!** 🏁
