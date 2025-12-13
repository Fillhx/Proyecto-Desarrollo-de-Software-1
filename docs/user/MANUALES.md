# Manuales de Ranyave

## 📋 Tabla de Contenidos

- [Manual de Usuario](#manual-de-usuario)
- [Manual del Administrador](#manual-del-administrador)

---

# Manual de Usuario

Bienvenido a **Ranyave**, el sistema de reserva de escenarios deportivos. Este manual te guiará paso a paso para usar la aplicación.

## 🔐 Inicio de Sesión

### Paso 1: Abrir la Aplicación

Ejecuta el programa con:
```bash
python sports_local/main.py
```

Verás la pantalla de inicio de sesión.

### Paso 2: Ingresar Credenciales

En la pantalla de login, ingresa:

| Campo | Descripción |
|-------|-------------|
| **Email** | Tu correo electrónico registrado |
| **Contraseña** | Tu contraseña segura |

### Paso 3: Iniciar Sesión

Haz clic en el botón **"Iniciar Sesión"** o presiona `Enter`.

### Crear una Cuenta

Si no tienes cuenta:
1. Haz clic en **"¿No tienes cuenta? Registrate"**
2. Completa los campos:
   - Nombre completo
   - Correo electrónico
   - Teléfono
   - Contraseña (mínimo 8 caracteres)
3. Haz clic en **"Registrarse"**

⚠️ **Nota:** El correo debe ser único. No puedes registrar dos cuentas con el mismo email.

---

## 👤 Panel de Usuario

Después de iniciar sesión, verás el **Panel del Usuario** con las siguientes secciones:

### Barra de Menú
- **Mi Perfil**: Ver información de tu cuenta
- **Escenarios**: Buscar y reservar escenarios
- **Mis Reservas**: Ver tus reservas activas
- **Historial**: Ver reservas pasadas
- **Cerrar Sesión**: Salir de la aplicación

### Vista Principal
Aquí se mostrarán los escenarios disponibles con:
- 📍 Nombre y ubicación
- 🏟️ Tipo de escenario
- 👥 Capacidad
- 💰 Precio por hora
- 📅 Disponibilidad

---

## 📅 Reservar un Escenario

### Paso 1: Seleccionar Escenario

En la sección **"Escenarios"**:
1. Visualiza la lista de escenarios disponibles
2. Lee la descripción de cada uno
3. Haz clic en **"Reservar"** en el escenario que desees

### Paso 2: Seleccionar Fecha y Hora

En el diálogo de reserva:

| Campo | Descripción |
|-------|-------------|
| **Fecha** | Selecciona la fecha (mínimo hoy) |
| **Hora de inicio** | Elige a qué hora deseas usar el escenario |
| **Duración** | Selecciona cuántas horas necesitas |

📌 **Consejo**: Los horarios ocupados se mostrarán en rojo. Solo puedes reservar en horarios verdes.

### Paso 3: Confirmar Reserva

1. Verifica los datos:
   - Escenario
   - Fecha y hora
   - Duración
   - Precio total
2. Haz clic en **"Confirmar Reserva"**

### Paso 4: Confirmación

Se mostrará un mensaje de éxito con:
- ✅ Número de reserva (ID)
- 📅 Fecha y hora
- 💰 Monto a pagar
- 📧 Confirmación por correo

---

## 📜 Ver Historial

### Acceso
Menú → **Historial**

### Información Mostrada

Verás una tabla con tus reservas pasadas:

| Columna | Contenido |
|---------|-----------|
| **ID Reserva** | Identificador único |
| **Escenario** | Nombre del escenario |
| **Fecha** | Fecha de la reserva |
| **Hora** | Hora de inicio |
| **Estado** | Confirmada / Cancelada |
| **Precio** | Monto pagado |

### Filtros
Puedes filtrar por:
- 📅 Rango de fechas
- 🏟️ Escenario específico
- ✅ Estado (confirmada/cancelada)

---

## ✏️ Gestionar Reservas

### Ver Mis Reservas Activas

Menú → **Mis Reservas**

Aquí verás:
- Reservas próximas (no canceladas)
- Información detallada de cada una
- Opciones de acciones

### Modificar una Reserva

1. Selecciona la reserva que deseas cambiar
2. Haz clic en **"Editar"**
3. Cambia:
   - Fecha
   - Hora
   - Duración
4. Haz clic en **"Guardar Cambios"**

⚠️ **Restricciones:**
- No puedes cambiar el escenario (cancela y crea nueva)
- Solo puedes editar si falta 24+ horas
- Debe haber disponibilidad en la nueva fecha/hora

### Cancelar una Reserva

1. Selecciona la reserva
2. Haz clic en **"Cancelar"**
3. Confirma la cancelación
4. Se mostrará el estado de reembolso:
   - Si cancelas 24h+ antes: ✅ **Reembolso 100%**
   - Si cancelas menos de 24h: ⚠️ **Reembolso 50%**

---

## 💳 Métodos de Pago

### Opciones Disponibles

La aplicación soporta:
- 💳 Tarjeta de crédito
- 💳 Tarjeta de débito
- 🏦 Transferencia bancaria
- 📱 Billetera digital

⚠️ **Nota:** Los pagos son procesados de forma segura.

---

## 📞 Contacto y Soporte

### Centro de Ayuda

Si tienes problemas:

1. **Bug o error técnico**
   - Captura pantalla del error
   - Anota la hora exacta
   - Contacta al equipo de soporte

2. **Pregunta sobre reservas**
   - Consulta el historial de transacciones
   - Verifica el email de confirmación

3. **Cambios en política**
   - Consulta la sección "Ayuda" en la app
   - Lee las preguntas frecuentes (FAQ)

### Datos de Contacto

📧 **Email**: soporte@ranyave.com  
📞 **Teléfono**: +57 (1) 2345-6789  
⏰ **Horario**: Lunes a Viernes, 8:00 AM - 6:00 PM

---

## ⚠️ Preguntas Frecuentes (FAQ)

### ¿Cuánto tiempo antes puedo reservar?
Puedes reservar con hasta **30 días de anticipación**.

### ¿Puedo cambiar mi escenario después de reservar?
No directamente. Debes:
1. Cancelar la reserva actual
2. Crear una nueva con el escenario deseado

### ¿Qué pasa si no asisto a mi reserva?
La reserva se marca como **no asistida** y no hay reembolso.

### ¿Cómo recupero mi contraseña?
1. En la pantalla de login, haz clic en **"¿Olvidaste tu contraseña?"**
2. Ingresa tu email
3. Recibirás un enlace de recuperación en tu correo
4. Crea una nueva contraseña

### ¿Es seguro registrar mi tarjeta?
✅ Sí. Usamos encriptación SSL de 256 bits y cumplimos con estándares PCI-DSS.

### ¿Puedo compartir mi cuenta?
❌ No. Cada usuario debe tener su propia cuenta. Las cuentas compartidas pueden ser suspendidas.

---

## 🎓 Tips y Trucos

### Ahorrar Dinero
- 💰 Reserva en horarios no pico (8 AM - 11 AM, 2 PM - 4 PM)
- 📅 Reserva de lunes a jueves (descuentos especiales)
- 🎁 Aprovecha promociones mensuales

### Mejor Experiencia
- 🔔 Activa notificaciones para recordatorios
- 📧 Verifica tu email registrado
- 📱 Descarga la app móvil para mayor comodidad

### Solucionar Problemas
- 🔄 Intenta refrescar la pantalla (F5)
- 🗑️ Borra cache si hay errores visuales
- 🌐 Verifica tu conexión a internet

---

## 🤝 Comunidad y Feedback

Ayúdanos a mejorar:

- 🌟 Califica la app en tu dispositivo
- 💬 Deja comentarios constructivos
- 🐛 Reporta errores que encuentres
- 💡 Sugiere nuevas características

Tu feedback es muy importante para nosotros.

---

**¡Gracias por usar Ranyave! Que disfrutes de tus escenarios deportivos.**

---

# Manual del Administrador

Bienvenido al panel de administración de Ranyave. Este manual te guiará en la gestión de la plataforma.

## 🔐 Acceso al Panel Admin

### Credenciales por Defecto

```
Email: admin@ranyave.com
Contraseña: admin123
```

⚠️ **IMPORTANTE:** Cambia esta contraseña la primera vez que accedas.

### Cambiar Contraseña

1. Inicia sesión con tus credenciales
2. Menú → **Configuración**
3. Haz clic en **"Cambiar Contraseña"**
4. Ingresa:
   - Contraseña actual
   - Nueva contraseña (mínimo 8 caracteres)
   - Confirmar nueva contraseña
5. Haz clic en **"Guardar"**

---

## 📊 Dashboard

Al iniciar sesión como administrador, verás el **Dashboard Principal** con:

### Widgets de Resumen
- 👥 **Total de Usuarios**: Cantidad de usuarios registrados
- 🏟️ **Escenarios Activos**: Cantidad de escenarios disponibles
- 📅 **Reservas Hoy**: Reservas programadas para hoy
- 💰 **Ingresos Mensuales**: Total de dinero recaudado

### Gráficos
- 📈 Tendencia de reservas (últimos 30 días)
- 🥧 Escenarios más reservados
- 📊 Ocupación por hora

### Acciones Rápidas
Botones para:
- ➕ Crear nuevo escenario
- 👥 Agregar usuario
- 📋 Ver todas las reservas
- 🎯 Ir a reportes

---

## 🏟️ Gestión de Escenarios

### Ver Todos los Escenarios

Menú → **Escenarios**

Verás una tabla con:

| Columna | Descripción |
|---------|-------------|
| **ID** | Identificador único |
| **Nombre** | Nombre del escenario |
| **Tipo** | Fútbol, Tenis, Badminton, etc. |
| **Ubicación** | Dirección |
| **Capacidad** | Número de personas |
| **Precio** | Tarifa por hora |
| **Estado** | Activo / Inactivo |
| **Acciones** | Editar / Eliminar |

### Crear Nuevo Escenario

1. Haz clic en **"➕ Nuevo Escenario"**
2. Completa el formulario:

| Campo | Tipo | Requerido | Ejemplo |
|-------|------|-----------|---------|
| **Nombre** | Texto | ✅ | Cancha A Fútbol |
| **Tipo** | Selección | ✅ | Fútbol |
| **Ubicación** | Texto | ✅ | Cra. 5 #12-34 |
| **Capacidad** | Número | ✅ | 20 |
| **Horario** | Texto | ✅ | 6:00 AM - 10:00 PM |
| **Precio/hora** | Decimal | ✅ | 50000 |
| **Estado** | Selección | ✅ | Activo |

3. Haz clic en **"Crear Escenario"**

### Editar Escenario

1. En la tabla, encuentra el escenario
2. Haz clic en **"✏️ Editar"**
3. Modifica los campos necesarios
4. Haz clic en **"Guardar Cambios"**

⚠️ **Nota:** Los cambios se aplican inmediatamente.

### Actualizar Horarios

1. Selecciona el escenario
2. Haz clic en **"📅 Horarios"**
3. Define:
   - Hora de apertura
   - Hora de cierre
   - Días cerrado
   - Franjas no disponibles

4. Haz clic en **"Guardar Horarios"**

### Cambiar Precio

1. En "Editar Escenario"
2. Modifica el campo **"Precio/hora"**
3. Se aplicará a nuevas reservas automáticamente

⚠️ **Nota:** No afecta reservas ya confirmadas.

### Eliminar Escenario

1. Haz clic en **"🗑️ Eliminar"** en la fila
2. Se solicitará confirmación
3. Se mostrarán reservas activas asociadas
4. Puedes elegir:
   - ❌ Cancelar eliminación
   - ⚠️ Eliminar (se cancelan las reservas activas con reembolso)

⚠️ **CUIDADO:** Esta acción es irreversible.

---

## 👥 Gestión de Usuarios

### Ver Todos los Usuarios

Menú → **Usuarios**

Verás tabla con:
- Email
- Nombre
- Teléfono
- Rol
- Fecha de registro
- Estado (Activo/Suspendido)

### Crear Usuario Manualmente

1. Haz clic en **"➕ Nuevo Usuario"**
2. Completa:
   - Email
   - Nombre
   - Teléfono
   - Rol (Usuario / Administrador)
   - Contraseña temporal

3. Haz clic en **"Crear Usuario"**
4. El usuario recibirá email con contraseña temporal

### Editar Usuario

1. Selecciona usuario en la tabla
2. Haz clic en **"✏️ Editar"**
3. Modifica:
   - Nombre
   - Teléfono
   - Rol

4. Haz clic en **"Guardar"**

### Cambiar Rol de Usuario

1. En "Editar Usuario"
2. Selecciona nuevo rol:
   - 👤 **Usuario**: Acceso limitado (reservas)
   - 🔑 **Administrador**: Acceso total

3. Haz clic en **"Guardar"**

### Suspender/Activar Usuario

1. Selecciona usuario
2. Haz clic en **"⛔ Suspender"** o **"✅ Activar"**
3. Se solicitará razón
4. El usuario no podrá acceder

### Resetear Contraseña de Usuario

1. Selecciona usuario
2. Haz clic en **"🔐 Resetear Contraseña"**
3. Se generará contraseña temporal
4. Se enviará por email

---

## 📅 Gestión de Reservas

### Ver Todas las Reservas

Menú → **Reservas**

Tabla con:
- ID de reserva
- Usuario
- Escenario
- Fecha y hora
- Estado
- Precio

### Filtros

Puedes filtrar por:
- 📅 Rango de fechas
- 🏟️ Escenario
- 👤 Usuario
- ✅ Estado (Confirmada/Cancelada/Pendiente)

### Detalles de Reserva

1. Haz clic en una reserva
2. Se mostrarán datos completos:
   - Información del usuario
   - Datos del escenario
   - Fecha, hora y duración
   - Precio y estado de pago
   - Historial de cambios

### Confirmar Reserva Pendiente

1. Selecciona reserva con estado "Pendiente"
2. Haz clic en **"✅ Confirmar"**
3. Se enviará confirmación al usuario

### Modificar Reserva

1. Selecciona reserva
2. Haz clic en **"✏️ Editar"**
3. Puedes cambiar:
   - Fecha y hora
   - Duración

4. Haz clic en **"Guardar"**

### Cancelar Reserva

1. Selecciona reserva
2. Haz clic en **"❌ Cancelar"**
3. Ingresa razón de cancelación
4. Define estado de reembolso:
   - 💰 100% - Cancelación sin cargo
   - 💰 50% - Cancelación con penalidad
   - 💰 0% - Sin reembolso

5. Haz clic en **"Confirmar"**

---

## 📊 Reportes y Estadísticas

### Acceder a Reportes

Menú → **Reportes**

### Tipos de Reportes Disponibles

#### 1. **Reporte de Ocupación**
```
Muestra:
- Ocupación por escenario (últimos 30 días)
- Horarios más y menos concurridos
- Días de mayor reserva
```

#### 2. **Reporte de Ingresos**
```
Muestra:
- Ingresos totales por período
- Ingresos por escenario
- Ingresos por método de pago
- Proyecciones
```

#### 3. **Reporte de Usuarios**
```
Muestra:
- Nuevos usuarios por período
- Usuarios más activos
- Tasa de retención
- Usuarios suspendidos
```

#### 4. **Reporte de Cancelaciones**
```
Muestra:
- Total de cancelaciones
- Razones de cancelación
- Tasa de cancelación por escenario
- Reembolsos procesados
```

### Exportar Reportes

1. Selecciona el reporte
2. Haz clic en **"📥 Descargar"**
3. Elige formato:
   - 📊 Excel (xlsx)
   - 📄 PDF
   - 📋 CSV

4. El archivo se descargará automáticamente

### Gráficos Personalizados

1. En la sección de reportes
2. Haz clic en **"📈 Nuevo Gráfico"**
3. Selecciona:
   - Tipo de datos
   - Rango de fechas
   - Tipo de visualización

4. Haz clic en **"Generar"**

---

## ⚙️ Configuración

### Configuración General

Menú → **Configuración**

#### Información de la Empresa
- Nombre
- Logo
- Email de soporte
- Teléfono
- Dirección

#### Horarios de Operación
- Hora de apertura general
- Hora de cierre general
- Días cerrados

### Configuración de Pagos

1. Haz clic en **"💳 Pagos"**
2. Configura:
   - Métodos aceptados
   - Comisiones
   - Políticas de reembolso

### Configuración de Notificaciones

1. Haz clic en **"🔔 Notificaciones"**
2. Activa/desactiva:
   - Recordatorios por email
   - Alertas de reservas
   - Notificaciones de cancelación
   - Resumen semanal

### Configuración de Idiomas

1. Haz clic en **"🌍 Idiomas"**
2. Selecciona idioma por defecto
3. Activa/desactiva otros idiomas

### Backup de Datos

1. Haz clic en **"💾 Backup"**
2. Opciones:
   - ☁️ **Backup Automático**: Diario/Semanal
   - 📥 **Backup Manual**: Descargar ahora
   - ↩️ **Restaurar**: Desde backup anterior

⚠️ **IMPORTANTE:** Realiza backups regularmente.

---

## 🔍 Monitoreo y Mantenimiento

### Salud del Sistema

Menú → **Sistema**

Verás:
- ✅ Estado de la BD
- ✅ Espacio en disco
- ✅ Última sincronización
- ✅ Logs de errores

### Limpiar Datos Obsoletos

1. Haz clic en **"🧹 Limpiar Datos"**
2. Selecciona:
   - Eliminar logs antiguos (>90 días)
   - Limpiar cache
   - Optimizar BD

3. Haz clic en **"Limpiar"**

### Ver Logs

1. Haz clic en **"📋 Logs"**
2. Filtra por:
   - Tipo (Error/Advertencia/Info)
   - Fecha
   - Usuario

---

## 🆘 Solución de Problemas

### Problema: Usuarios no pueden reservar

**Soluciones:**
1. Verifica que el escenario esté "Activo"
2. Comprueba los horarios
3. Revisa si hay conflictos de reserva
4. Reinicia la aplicación

### Problema: Pagos no procesados

**Soluciones:**
1. Verifica configuración de pagos
2. Comprueba conexión a internet
3. Revisa logs de errores
4. Contacta al proveedor de pagos

### Problema: Base de datos lenta

**Soluciones:**
1. Ejecuta optimización: Sistema → Optimizar
2. Reduce datos históricos innecesarios
3. Aumenta recursos del servidor
4. Contacta a soporte técnico

---

## 📞 Contacto de Soporte Técnico

Para problemas que no puedas resolver:

📧 **Email**: admin-support@ranyave.com  
📞 **Teléfono**: +57 (1) 2345-6789 ext. 100  
⏰ **Horario**: Lunes a Viernes, 9:00 AM - 5:00 PM

---

**¡Gracias por administrar Ranyave! Tu trabajo es esencial para nuestro éxito.**
