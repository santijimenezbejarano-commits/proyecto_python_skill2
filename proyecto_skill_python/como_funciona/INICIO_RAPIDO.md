# 🚀 GUÍA RÁPIDA DE INICIO - Academia DriveSafe

## ⚡ Inicio Rápido (2 minutos)

### 1. Verificar Python
```bash
python --version
```
Debe ser Python 3.8 o superior.

### 2. Ejecutar la aplicación
```bash
python main.py
```

### 3. ¡Listo! 
Ya está corriendo la aplicación. Seleccione la opción deseada en el menú.

---

## 📋 Estructura de Carpetas

```
proyecto/
│
├── main.py                    # ▶️ EJECUTE ESTE ARCHIVO
├── clientes.py               # Gestión de clientes
├── instructores.py           # Gestión de instructores
├── vehiculos.py              # Gestión de vehículos
├── citas.py                  # Gestión de citas
├── persistencia.py           # Manejo de archivos
├── utilidades.py             # Funciones auxiliares
│
├── README.md                 # Documentación completa
├── EJEMPLO_USO.md            # Guía con ejemplos
├── INICIO_RAPIDO.md          # Este archivo
│
└── datos/                    # 📁 Se crea automáticamente
    ├── clientes.json         # Datos de clientes
    ├── instructores.json     # Datos de instructores
    ├── vehiculos.json        # Datos de vehículos
    └── citas.json            # Datos de citas
```

---

## 🎮 Opciones del Menú Principal

```
📋 MENÚ PRINCIPAL
═══════════════════════════════════════════════════════════════
1. 👤 Gestionar Clientes
2. 👨‍🏫 Gestionar Instructores
3. 🚗 Gestionar Vehículos
4. 📅 Gestionar Citas
5. 📊 Reportes y Consultas
6. 🚪 Salir
═══════════════════════════════════════════════════════════════
```

---

## 🎯 Flujo Recomendado de Uso

### Primera vez usando la aplicación:

1. **Registrar al menos 1 cliente** (Menú 1 → Opción 1)
   - Nombre: cualquier nombre
   - Documento: 6-12 números
   - Tipo de vehículo: moto, automóvil o ambos

2. **Registrar al menos 1 instructor** (Menú 2 → Opción 1)
   - Nombre: cualquier nombre
   - Documento: 6-12 números
   - Especialidad: moto o carro

3. **Registrar al menos 1 vehículo** (Menú 3 → Opción 1)
   - Tipo: moto o automóvil
   - Placa: formato ABC123
   - Modelo: opcional

4. **Programar una cita** (Menú 4 → Opción 1)
   - ID cliente: el que registró
   - ID instructor: el que registró
   - ID vehículo: el que registró
   - Fecha: futura (DD/MM/YYYY)
   - Hora: formato HH:MM
   - Duración: 30, 45, 60, 90 o 120 minutos

5. **Registrar asistencia** (Menú 4 → Opción 4)
   - ID cita: el que se programó
   - ¿Asistió?: Sí o No
   - Observaciones: opcional

---

## 📝 Datos de Prueba Rápida

Si desea probar rápidamente, use estos datos:

### Cliente
- Nombre: `Juan Pérez`
- Documento: `1023456789`
- Tipo: `automóvil`

### Instructor
- Nombre: `Carlos López`
- Documento: `987654321`
- Especialidad: `carro`

### Vehículo
- Tipo: `automóvil`
- Placa: `ABC123`
- Modelo: `Toyota Corolla`

### Cita
- Cliente ID: `1`
- Instructor ID: `1`
- Vehículo ID: `1`
- Fecha: `20/07/2026`
- Hora: `14:30`
- Duración: `60`

---

## 🔑 Validaciones Importantes

| Campo | Regla | Ejemplo |
|-------|-------|---------|
| Documento | 6-12 dígitos, único | `1023456789` ✅ |
| Placa | ABC123, única | `ABC123` ✅, `abc123` ❌ |
| Fecha | DD/MM/YYYY, futura | `20/07/2026` ✅, `15/07/2026` ❌ |
| Hora | HH:MM (24h) | `14:30` ✅, `1430` ❌ |
| Duración | 30, 45, 60, 90, 120 | `60` ✅, `50` ❌ |

---

## 💾 Copia de Seguridad de Datos

Los datos se guardan automáticamente en `datos/` en formato JSON.

### Hacer backup:
```bash
# Windows
xcopy datos datos_backup /E

# Linux/Mac
cp -r datos datos_backup
```

### Restaurar desde backup:
```bash
# Windows
xcopy datos_backup datos /E

# Linux/Mac
cp -r datos_backup datos
```

---

## 🐛 Solución de Problemas

### Problema: "No such file or directory"
**Solución**: Asegúrese de estar en la carpeta del proyecto:
```bash
cd proyecto
python main.py
```

### Problema: "SyntaxError"
**Solución**: Verifique que tiene Python 3.8+:
```bash
python --version
```

### Problema: "No JSON data files"
**Solución**: Es normal, se crearán al registrar los primeros datos.

### Problema: Error al registrar
**Solución**: Verifique:
- Documento no esté duplicado
- Placa tenga formato correcto (ABC123)
- Valores requeridos no estén vacíos

---

## 📞 Acciones Principales Rápidas

| Acción | Ruta |
|--------|------|
| Registrar cliente | Menú 1 → 1 |
| Registrar instructor | Menú 2 → 1 |
| Registrar vehículo | Menú 3 → 1 |
| Programar cita | Menú 4 → 1 |
| Registrar asistencia | Menú 4 → 4 |
| Ver reportes | Menú 5 → (1-5) |
| Historial cliente | Menú 5 → 5 |
| Citas próximas | Menú 5 → 2 |

---

## 🎓 Flujo de una Cita Típica

```
1. REGISTRAR CLIENTE → ID: 1
2. REGISTRAR INSTRUCTOR → ID: 1  
3. REGISTRAR VEHÍCULO → ID: 1
4. PROGRAMAR CITA → ID: 1 (Vehículo marcado NO disponible)
   └─ Fecha: 20/07/2026 14:30
5. REGISTRAR ASISTENCIA → ID: 1 (Vehículo marcado disponible)
   └─ Estado: completada
```

---

## 📊 Información en Reportes

### Reportes disponibles (Menú 5):
1. **Resumen de cliente**: Datos + historial completo
2. **Citas próximas**: Próximos 7 días
3. **Instructores por especialidad**: Agrupados
4. **Vehículos disponibles**: Solo los disponibles
5. **Historial de cliente**: Estadísticas + historial

---

## ✅ Checklist para Primera Ejecución

- [ ] Python 3.8+ instalado
- [ ] Archivo `main.py` presente
- [ ] En la carpeta `proyecto`
- [ ] Ejecutar: `python main.py`
- [ ] Ver menú principal
- [ ] Registrar 1 cliente
- [ ] Registrar 1 instructor
- [ ] Registrar 1 vehículo
- [ ] Programar 1 cita
- [ ] Registrar asistencia
- [ ] Consultar reportes

---

## 🚀 ¡Ya Está Listo!

La aplicación está completamente funcional. Explore los menús y disfrute del sistema.

**Nota**: Todos los datos se guardan automáticamente en archivos JSON.

---

**¿Preguntas?** Revise `README.md` o `EJEMPLO_USO.md`  
**¿Listo?** Ejecute: `python main.py` 🏁
