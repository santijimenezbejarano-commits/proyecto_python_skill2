# ❓ Preguntas Frecuentes (FAQ) - Academia DriveSafe

## 🆘 Problemas y Soluciones

### P1: ¿Cómo inicio la aplicación?
**R:** Abra una terminal/consola en la carpeta `proyecto` y ejecute:
```bash
python main.py
```

### P2: ¿Qué versión de Python necesito?
**R:** Python 3.8 o superior. Verifique con:
```bash
python --version
```

### P3: ¿Dónde se guardan los datos?
**R:** En la carpeta `datos/` que se crea automáticamente. Los datos se guardan en archivos JSON:
- `clientes.json`
- `instructores.json`
- `vehiculos.json`
- `citas.json`

### P4: ¿Necesito instalar paquetes adicionales?
**R:** No. La aplicación solo usa librerías estándar de Python (json, os, datetime, re, typing).

### P5: ¿Cómo hago una copia de seguridad?
**R:** Copie la carpeta `datos/` a un lugar seguro:
```bash
# Windows
xcopy datos datos_backup /E

# Linux/Mac
cp -r datos datos_backup
```

---

## 📝 Datos y Validaciones

### P6: ¿Qué formato debe tener el documento?
**R:** 6 a 12 dígitos numéricos. Ej: `1023456789`

### P7: ¿Qué formato debe tener la placa del vehículo?
**R:** Formato colombiano: 3 letras mayúsculas + 3 números. Ej: `ABC123`

### P8: ¿Qué formato debe tener la fecha?
**R:** DD/MM/YYYY. Ej: `20/07/2026`. Debe ser una fecha futura o actual.

### P9: ¿Qué formato debe tener la hora?
**R:** HH:MM en formato 24 horas. Ej: `14:30`

### P10: ¿Cuáles son las duraciones permitidas para una cita?
**R:** 30, 45, 60, 90 o 120 minutos.

### P11: ¿Qué especialidades pueden tener los instructores?
**R:** 
- `moto`: para enseñar conducción de motocicletas
- `carro`: para enseñar conducción de automóviles

### P12: ¿Qué tipos de vehículos puedo registrar?
**R:**
- `moto`: motocicletas
- `automóvil`: vehículos de 4 ruedas

### P13: ¿Qué tipos de vehículo puede practicar un cliente?
**R:** `moto`, `automóvil` o `ambos`

---

## 🚗 Gestión de Citas

### P14: ¿Qué sucede cuando programo una cita?
**R:**
1. Se valida que cliente, instructor y vehículo existan
2. Se valida que el instructor tenga la especialidad correcta
3. Se valida que el vehículo esté disponible
4. Se crea la cita y el vehículo se marca como "no disponible"

### P15: ¿Qué sucede cuando registro asistencia?
**R:**
1. Se registra si asistió o no
2. Se guardan las observaciones
3. El vehículo se libera (se marca como "disponible")
4. El estado de la cita cambia a "completada" o "no_presentado"

### P16: ¿Puedo programar una cita con un vehículo no disponible?
**R:** No, el sistema valida que esté disponible y rechaza la cita si no lo está.

### P17: ¿Puedo programar una cita de un instructor de motos con un vehículo de carro?
**R:** No, el sistema valida que la especialidad del instructor coincida con el tipo de vehículo.

### P18: ¿Puedo programar una cita en una fecha pasada?
**R:** No, el sistema solo permite fechas actuales o futuras.

### P19: ¿Puedo registrar asistencia a una cita ya completada?
**R:** Sí, puede actualizar la información, pero el vehículo solo se libera una vez.

### P20: ¿Cómo consulto el historial de un cliente?
**R:** Menú 4 → Opción 5, o Menú 5 → Opción 5 para ver reportes detallados.

---

## 🆔 IDs y Registros

### P21: ¿Cómo se asignan los IDs?
**R:** Automáticamente de forma incremental (1, 2, 3, ...) al registrar.

### P22: ¿Puedo duplicar documentos?
**R:** No, el sistema valida documentos únicos por cliente e instructor.

### P23: ¿Puedo duplicar placas de vehículos?
**R:** No, el sistema valida placas únicas.

### P24: ¿Qué pasa si ingreso un ID que no existe?
**R:** El sistema mostrará "No encontrado" y no realizará la operación.

### P25: ¿Puedo editar datos después de registrar?
**R:** Actualmente, no. Puede consultar y registrar nuevos, pero no hay opción de edición. Para cambiar datos, puede modificar el archivo JSON directamente.

---

## 📊 Reportes

### P26: ¿Qué reportes están disponibles?
**R:** 
1. Resumen de cliente (datos + historial)
2. Citas próximas (próximos 7 días)
3. Instructores por especialidad
4. Vehículos disponibles
5. Historial detallado de cliente

### P27: ¿Puedo filtrar citas por fecha?
**R:** Sí, Menú 4 → Opción 6

### P28: ¿Puedo filtrar citas por cliente?
**R:** Sí, el Menú 5 → Opción 5 muestra el historial de un cliente específico.

### P29: ¿Puedo ver solo vehículos disponibles?
**R:** Sí, Menú 3 → Opción 4

### P30: ¿Puedo ver instructores por especialidad?
**R:** Sí, Menú 2 → Opción 4

---

## 💾 Manejo de Datos

### P31: ¿Qué sucede si elimino la carpeta `datos/`?
**R:** Los archivos se regenerarán vacíos al ejecutar la aplicación. Es como un "reset" del sistema.

### P32: ¿Puedo editar los archivos JSON manualmente?
**R:** Sí, pero debe mantener la estructura correcta para que funcione.

### P33: ¿Qué pasa si hay un error al guardar datos?
**R:** El sistema mostrará un mensaje de error y no completará la operación.

### P34: ¿Se pierden datos si cierro la aplicación sin guardar?
**R:** No, los datos se guardan automáticamente con cada operación.

### P35: ¿Cuánto espacio necesita la aplicación?
**R:** Muy poco. Cada registro ocupa aproximadamente 200-500 bytes en JSON.

---

## ⚡ Rendimiento

### P36: ¿Qué pasa si registro muchas citas?
**R:** La aplicación seguirá funcionando normalmente. Los archivos JSON pueden contener miles de registros.

### P37: ¿Se ralentiza con muchos datos?
**R:** No notablemente. La carga y guardado de JSON es rápido para volúmenes normales de un centro de conducción.

### P38: ¿Hay límite de registros?
**R:** Teóricamente no, pero la práctica es mejor con < 10,000 registros por tipo.

---

## 🔒 Seguridad

### P39: ¿Los datos están encriptados?
**R:** No, los archivos JSON son texto plano. Para producción, considere encriptación.

### P40: ¿Hay contraseñas o autenticación?
**R:** No. La aplicación está diseñada para uso local/confiable. Para uso compartido, considere agregar autenticación.

### P41: ¿Hay auditoría de cambios?
**R:** No. Los datos se sobrescriben sin historial. Para auditoría, exporte los datos regularmente.

---

## 🐛 Errores Comunes

### P42: "❌ Entrada inválida. Intente de nuevo."
**R:** El formato no es correcto. Revise:
- Documentos: 6-12 dígitos
- Placas: ABC123 (3 letras, 3 números)
- Fechas: DD/MM/YYYY
- Horas: HH:MM

### P43: "❌ El documento ya está registrado."
**R:** Ese documento ya existe. Use otro o consulte si es el mismo cliente.

### P44: "❌ El vehículo no está disponible."
**R:** El vehículo está en una cita. Registre asistencia de la cita anterior o use otro vehículo.

### P45: "❌ El instructor está especializado en X, no en Y."
**R:** El tipo de instructor no coincide con el vehículo. Use otro instructor o vehículo.

### P46: "Cliente no encontrado"
**R:** Verifique que el ID del cliente sea correcto.

---

## 📱 Interfaz

### P47: ¿Hay versión web o móvil?
**R:** No, solo versión de consola. Es funcional y eficiente.

### P48: ¿Puedo personalizar el menú?
**R:** Sí, modificando los archivos `.py`. La estructura es clara y modular.

### P49: ¿Puedo agregar más funcionalidades?
**R:** Sí, la arquitectura es extensible. Agregue métodos en las clases.

### P50: ¿Puedo cambiar los colores/emojis de la consola?
**R:** Sí, buscando las líneas con `print()` y modificando los caracteres especiales.

---

## 🌍 Portabilidad

### P51: ¿Funciona en Windows, Linux y Mac?
**R:** Sí, la aplicación es multiplataforma. Solo necesita Python.

### P52: ¿Qué pasa si cambio de computadora?
**R:** Copie la carpeta `proyecto` completa, incluyendo `datos/`.

### P53: ¿Puedo compartir datos entre computadoras?
**R:** Sí, copie la carpeta `datos/` entre máquinas.

---

## 🎓 Aprendizaje

### P54: ¿Puedo usar este código como ejemplo para aprender Python?
**R:** Sí, la estructura es clara, modular y bien comentada. Ideal para aprender.

### P55: ¿Qué conceptos de Python se usan?
**R:** POO, manejo de archivos, validaciones, menús interactivos, manejo de excepciones.

### P56: ¿Dónde está documentado el código?
**R:** Cada módulo tiene docstrings. Vea `README.md` para visión general.

---

## 🆘 Más Ayuda

### P57: ¿Dónde encuentro documentación completa?
**R:** En `README.md`

### P58: ¿Hay ejemplos de uso?
**R:** Sí, en `EJEMPLO_USO.md`

### P59: ¿Hay guía rápida de inicio?
**R:** Sí, en `INICIO_RAPIDO.md`

### P60: ¿Qué hago si tengo más preguntas?
**R:** Revise los archivos de documentación o modifique el código según necesite.

---

**¿No encontró su respuesta?** Revise la documentación en:
- `README.md` - Completa
- `EJEMPLO_USO.md` - Práctico
- `INICIO_RAPIDO.md` - Rápido
- Comentarios en los archivos `.py`

¡**Éxito con DriveSafe!** 🏁
