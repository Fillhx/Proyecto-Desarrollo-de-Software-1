# Ranyave - Sistema de Reserva de Escenarios Deportivos

## 👥 Integrantes

- **Gustavo Adolfo Restrepo Muñoz** (2380618)
- **Andrés Felipe Castrillón Martínez** (2380664)
- **Javier Andrés Muñoz Tavera** (2380421)

---

## 📋 Descripción General

**Ranyave** es una aplicación de escritorio desarrollada con PyQt5 que permite gestionar la reserva de escenarios deportivos. El sistema proporciona funcionalidades para:

- 🔐 **Autenticación de usuarios** con roles diferenciados (Usuario y Administrador)
- 📅 **Gestión de reservas** de escenarios con fechas y horarios
- 🏟️ **Administración de escenarios** deportivos (crear, editar, eliminar)
- 💾 **Persistencia de datos** mediante SQLite
- 📊 **Historial de reservas** y eventos
- 🌍 **Soporte multiidioma** (i18n)

---

## 🛠️ Requisitos Previos

- **Python 3.8+**
- **pip** (gestor de paquetes de Python)

---

## 📦 Instalación

### 1. Clonar o descargar el proyecto

```bash
cd Proyecto-Desarrollo-de-Software-1
```

### 2. Crear un entorno virtual (recomendado)

```bash
python -m venv venv
```

Activar el entorno virtual:

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 🚀 Ejecución

Desde el directorio del proyecto, ejecuta:

```bash
python sports_local/main.py
```

### Credenciales por defecto:

| Usuario | Contraseña | Rol |
|---------|-----------|-----|
| admin@ranyave.com | admin123 | Administrador |
| user@example.com | user123 | Usuario |
| 123 | 321 | Usuario |

---

## 🧪 Pruebas Unitarias

El proyecto incluye pruebas unitarias automatizadas usando **pytest** para validar el funcionamiento de los módulos críticos.

### Ejecutar todos los tests

```bash
pytest test_basics.py -v
```

### Ejecutar una clase de tests específica

```bash
pytest test_basics.py::TestSeguridad -v
pytest test_basics.py::TestUsuarios -v
pytest test_basics.py::TestEscenarios -v
pytest test_basics.py::TestReservas -v
```

### Ejecutar un test específico

```bash
pytest test_basics.py::TestSeguridad::test_hash_password -v
```

### Resultado esperado

Deberías ver un mensaje como:

```
===== 16 passed in 16.70s =====
```

### Instalación de pytest (si no está instalado)

```bash
pip install pytest
```

### Documentación de pruebas

Para más detalles sobre las pruebas realizadas, consulta [PRUEBA_UNITARIA_RESUMEN.md](PRUEBA_UNITARIA_RESUMEN.md)

---

## 📁 Estructura del Proyecto

```
Proyecto-Desarrollo-de-Software-1/
├── sports_local/
│   ├── main.py                    # Archivo principal de la aplicación
│   ├── database.py                # Operaciones con la BD (SQLite)
│   ├── database_events.py         # Gestión de eventos
│   ├── i18n.py                    # Sistema de idiomas
│   ├── email_config.py            # Configuración de correos
│   ├── events_dialog.py           # Diálogos para eventos
│   ├── history_dialog.py          # Diálogos de historial
│   ├── styles.qss                 # Estilos CSS para la interfaz
│   ├── assets/                    # Imágenes y recursos
│   └── __pycache__/               # Caché de Python
├── docs/
│   ├── INDEX.md                   # Índice central de documentación
│   ├── user/
│   │   └── MANUALES.md            # Manuales de Usuario y Administrador
│   └── technical/
│       └── DOCUMENTACION_TECNICA.md # Documentación técnica completa
├── admins.json                    # Configuración de administradores
├── users.json                     # Base de datos de usuarios (legacy)
├── requirements.txt               # Dependencias del proyecto
└── README.md                      # Este archivo
```

---

## � Documentación

Se ha creado documentación completa para usuarios, administradores y desarrolladores:

### Para Usuarios Finales
- 📖 [Manuales Completos](docs/user/MANUALES.md) - Manual de Usuario + Manual del Administrador

### Para Desarrolladores
- 📖 [Documentación Técnica](docs/technical/DOCUMENTACION_TECNICA.md) - Arquitectura, configuración, estándares y desarrollo

### Índice Central
- 📖 [Índice de Documentación](docs/INDEX.md) - Navegación completa de toda la documentación

---

## �🗄️ Base de Datos

La aplicación utiliza **SQLite** con las siguientes tablas principales:

- **users**: Información de usuarios y credenciales
- **venues**: Escenarios deportivos disponibles
- **reservations**: Reservas realizadas por usuarios
- **events**: Eventos y actividades programadas

---

## 🎯 Características Principales

### Para Usuarios
- Registrarse e iniciar sesión
- Ver escenarios disponibles
- Realizar reservas de escenarios
- Consultar historial de reservas
- Cancelar o modificar reservas

### Para Administradores
- Gestionar escenarios (crear, editar, eliminar)
- Actualizar horarios y precios
- Ver reportes de reservas
- Administrar usuarios

---

## 💡 Notas Importantes

- La base de datos se genera automáticamente al ejecutar la aplicación
- Se utiliza **bcrypt** para el hash seguro de contraseñas
- La interfaz gráfica está construida con **PyQt5**
- El proyecto soporta múltiples idiomas a través del sistema i18n

---

## 📝 Licencia

Este proyecto es desarrollado como parte de un curso de Desarrollo de Software.