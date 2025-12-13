# Documentación Técnica - Ranyave

## 📑 Tabla de Contenidos

1. [Arquitectura del Sistema](#arquitectura-del-sistema)
2. [Estructura de Módulos](#estructura-de-módulos)
3. [Esquema de Base de Datos](#esquema-de-base-de-datos)
4. [Seguridad](#seguridad)
5. [Configuración del Entorno de Desarrollo](#configuración-del-entorno-de-desarrollo)
6. [Estándares de Código](#estándares-de-código)
7. [Testing](#testing)
8. [Workflow de Git](#workflow-de-git)
9. [Deployment](#deployment)
10. [Debugging](#debugging)

---

## 📐 Arquitectura del Sistema

Ranyave utiliza una arquitectura de **3 capas**:

```
┌─────────────────────────────────────┐
│      Capa de Presentación (UI)      │
│  PyQt5 - Interfaz Gráfica           │
└────────────┬────────────────────────┘
             │
┌────────────▼────────────────────────┐
│     Capa de Lógica de Negocio       │
│  main.py, dialog*.py, i18n.py       │
└────────────┬────────────────────────┘
             │
┌────────────▼────────────────────────┐
│      Capa de Persistencia           │
│  SQLite - database.py               │
└─────────────────────────────────────┘
```

---

## 🏗️ Estructura de Módulos

### **main.py** (Principal)
- Inicialización de la aplicación
- Gestión de ventanas principales
- Control de flujo de pantallas
- Autenticación y sesiones

**Clases principales:**
- `BasePage`: Clase base para todas las páginas
- `LoginPage`: Pantalla de inicio de sesión
- `AdminDashboard`: Panel de administrador
- `UserDashboard`: Panel de usuario

---

### **database.py** (Base de Datos)
Maneja todas las operaciones CRUD con SQLite.

**Funciones principales:**
```python
# Usuarios
get_user(email)
create_user(email, name, phone, password, role)
verify_password(password, hashed_password)

# Venues (Escenarios)
get_all_venues()
create_venue(venue_data)
update_venue(venue_id, venue_data)
delete_venue(venue_id)

# Reservas
get_all_reservations()
create_reservation(reservation_data)
update_reservation_status(reservation_id, status)
cancel_reservation(reservation_id)

# Eventos
get_all_events()
create_event(event_data)
delete_event(event_id)
```

---

### **database_events.py** (Gestión de Eventos)
Funciones especializadas para operaciones con eventos.

---

### **i18n.py** (Internacionalización)
Sistema de idiomas multilingües.

```python
get_language_manager()  # Obtiene el gestor de idiomas
tr(key)                 # Traduce una clave
```

---

### **email_config.py** (Correos)
Configuración para envío de correos (notificaciones).

---

### **events_dialog.py** (Diálogos de Eventos)
Ventanas emergentes para crear/editar eventos.

---

### **history_dialog.py** (Diálogos de Historial)
Ventanas para ver historial de reservas y eventos.

---

## 🗄️ Esquema de Base de Datos

### Tabla: **users**
```sql
CREATE TABLE users (
    email TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT,
    password TEXT NOT NULL,
    role TEXT NOT NULL
)
```

### Tabla: **venues**
```sql
CREATE TABLE venues (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    capacity INTEGER,
    location TEXT NOT NULL,
    schedule TEXT,
    price REAL DEFAULT 0.0,
    status TEXT DEFAULT 'active'
)
```

### Tabla: **reservations**
```sql
CREATE TABLE reservations (
    id TEXT PRIMARY KEY,
    user_email TEXT NOT NULL,
    venue_id TEXT NOT NULL,
    venue_name TEXT,
    date TEXT NOT NULL,
    time TEXT NOT NULL,
    status TEXT DEFAULT 'confirmed',
    FOREIGN KEY (user_email) REFERENCES users (email),
    FOREIGN KEY (venue_id) REFERENCES venues (id)
)
```

### Tabla: **events**
```sql
CREATE TABLE events (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    schedule TEXT NOT NULL,
    location TEXT NOT NULL,
    capacity INTEGER NOT NULL
)
```

---

## 🔐 Seguridad

### Hashing de Contraseñas
Se utiliza **bcrypt** con 12 rondas para proteger contraseñas:

```python
from bcrypt import gensalt, hashpw

salt = gensalt(rounds=12)
hashed = hashpw(password.encode('utf-8'), salt).decode('utf-8')
```

### Validación de Entrada
- Validación de formatos de email
- Verificación de fortaleza de contraseña
- Sanitización de datos de entrada

---

## 🎨 Interfaz Gráfica

### Framework
- **PyQt5**: Framework de interfaz gráfica multiplataforma

### Temas y Estilos
- Estilos definidos en `styles.qss`
- Paleta de colores principal: Azul oscuro (#1e3a5f)
- Soporte para temas personalizados

### Flujo de Navegación
```
Login → Selección de Rol → Dashboard (Admin/Usuario) → Operaciones
```

---

## 🔄 Flujos Principales

### Autenticación
1. Usuario ingresa email y contraseña
2. Sistema verifica credenciales en BD
3. Se determina el rol (admin/user)
4. Se redirige al dashboard correspondiente

### Crear Reserva
1. Usuario selecciona escenario
2. Elige fecha y hora disponible
3. Confirma la reserva
4. Sistema genera ID único (UUID)
5. Se guarda en BD con estado "confirmed"

### Gestionar Escenarios (Admin)
1. Admin accede a sección de escenarios
2. Puede crear, editar o eliminar
3. Los cambios se reflejan inmediatamente en BD
4. Los usuarios ven los cambios actualizados

---

## 📦 Dependencias Principales

```
PyQt5==5.15.7           # Interfaz gráfica
Pillow==9.5.0          # Procesamiento de imágenes
bcrypt==4.0.1          # Hashing de contraseñas
```

Ver `requirements.txt` para la lista completa.

---

## 🔧 Configuración del Entorno de Desarrollo

### Requisitos
- Python 3.8+
- Git
- IDE recomendado: VS Code, PyCharm o similares

### Instalación Inicial

```bash
# 1. Clonar repositorio
git clone <repo-url>
cd Proyecto-Desarrollo-de-Software-1

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno
# Windows
.\venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Ejecutar la aplicación
python sports_local/main.py
```

---

## 📋 Estándares de Código

### Nombrado de Variables
- **snake_case** para variables y funciones: `user_email`, `create_venue()`
- **PascalCase** para clases: `LoginPage`, `AdminDashboard`
- **UPPER_CASE** para constantes: `DB_NAME`, `IMAGE_PATH`

### Docstrings
Usar docstrings para todas las funciones:

```python
def create_venue(venue_data):
    """
    Crea un nuevo escenario en la base de datos.
    
    Args:
        venue_data (dict): Diccionario con datos del escenario
                          {name, type, location, capacity, schedule, price}
    
    Returns:
        bool: True si se creó exitosamente, False en caso contrario
    """
    pass
```

### Comentarios
- Comentarios en español
- Explicar el "por qué", no el "qué"
- Máximo 80 caracteres por línea

```python
# ❌ Malo
result = x + y  # Suma x y y

# ✅ Bueno
# Calcular el total incluyendo impuestos (15%)
result = x + y * 0.15
```

---

## 🏗️ Estructura de Clases en PyQt5

### Plantilla Base
```python
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QFont

class MyPage(QWidget):
    """Descripción de la página"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz de usuario"""
        layout = QVBoxLayout()
        
        # Crear componentes
        label = QLabel("Mi Página")
        label.setFont(QFont("Arial", 14, QFont.Bold))
        
        # Agregar a layout
        layout.addWidget(label)
        self.setLayout(layout)
    
    def on_button_clicked(self):
        """Maneja el click del botón"""
        pass
```

---

## 🗄️ Operaciones de Base de Datos

### Patrón para Nuevas Operaciones

```python
def mi_operacion(param1, param2):
    """Descripción breve de la operación"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM tabla WHERE columna = ?
        ''', (param1,))
        result = cursor.fetchall()
        return result
    except sqlite3.Error as e:
        print(f"Error BD: {e}")
        return None
    finally:
        conn.close()
```

### Mejores Prácticas
- ✅ Siempre cerrar la conexión en el bloque `finally`
- ✅ Usar parámetros vinculados (`?`) para prevenir SQL injection
- ✅ Manejar excepciones adecuadamente
- ✅ Validar entrada antes de ejecutar query

---

## 🧪 Testing

### Crear Tests
```bash
# Crear carpeta para tests
mkdir tests

# Crear archivo de test
touch tests/test_database.py
```

### Ejemplo de Test
```python
import unittest
from sports_local import database

class TestDatabase(unittest.TestCase):
    def setUp(self):
        """Se ejecuta antes de cada test"""
        self.test_email = "test@example.com"
    
    def test_create_user(self):
        """Verifica que se pueda crear un usuario"""
        result = database.create_user(
            self.test_email, "Test User", "123456", "pass123", "user"
        )
        self.assertTrue(result)
    
    def test_get_user(self):
        """Verifica que se pueda obtener un usuario"""
        user = database.get_user(self.test_email)
        self.assertIsNotNone(user)

if __name__ == '__main__':
    unittest.main()
```

Ejecutar tests:
```bash
python -m unittest discover tests/
```

---

## 🔄 Workflow de Git

### Crear una Nueva Característica
```bash
# 1. Actualizar rama principal
git checkout main
git pull origin main

# 2. Crear rama de feature
git checkout -b feature/nombre-feature

# 3. Hacer cambios y commits
git add .
git commit -m "feat: agregar nueva funcionalidad"

# 4. Push a repositorio remoto
git push origin feature/nombre-feature

# 5. Crear Pull Request
```

### Convención de Commits
```
feat:    Nueva característica
fix:     Corrección de bug
docs:    Cambios en documentación
style:   Cambios de formato
refactor: Refactorización de código
test:    Agregar o actualizar tests
```

Ejemplos:
```
git commit -m "feat: agregar validación de email"
git commit -m "fix: corregir error en cálculo de precio"
git commit -m "docs: actualizar guía de instalación"
```

---

## 📦 Agregar Nuevas Dependencias

```bash
# Instalar paquete
pip install nombre-paquete

# Actualizar requirements.txt
pip freeze > requirements.txt

# Commitar cambios
git add requirements.txt
git commit -m "feat: agregar nueva dependencia"
```

---

## 🚀 Deployment

### Generar Ejecutable (pyinstaller)
```bash
pip install pyinstaller
pyinstaller --onefile sports_local/main.py
```

El ejecutable se generará en la carpeta `dist/`.

---

## 🐛 Debugging

### Usar el Debugger de PyQt5
```python
# En el código
import pdb; pdb.set_trace()  # Pausa la ejecución aquí
```

Comandos útiles:
- `n` - siguiente línea
- `c` - continuar ejecución
- `p variable` - imprimir variable
- `q` - salir del debugger

### Logs
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("Mensaje de debug")
logger.info("Mensaje informativo")
logger.warning("Advertencia")
logger.error("Error")
```

### Base de Datos
SQLite guarda los datos en `sports_local.db` en el directorio raíz.

Para inspeccionar:
```bash
sqlite3 sports_local.db
sqlite> .tables
sqlite> SELECT * FROM users;
```

---

## 📚 Recursos Útiles

- [PyQt5 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt5/)
- [Python sqlite3](https://docs.python.org/3/library/sqlite3.html)
- [bcrypt](https://github.com/pyca/bcrypt)
- [Git Workflow](https://git-scm.com/book/en/v2)

---

## ✅ Checklist antes de hacer Commit

- [ ] Código sigue estándares de nombrado
- [ ] Funciones tienen docstrings
- [ ] Sin errores de sintaxis
- [ ] Tests pasan correctamente
- [ ] Base de datos está actualizada
- [ ] Documentación está actualizada
- [ ] Sin código comentado innecesario

---

## 📝 Notas para Desarrolladores

- Todos los IDs se generan con UUID
- Las fechas se almacenan en formato ISO (YYYY-MM-DD)
- Las horas se almacenan en formato 24h (HH:MM)
- El rol de usuario puede ser: "admin" o "user"
- Los estados de reserva pueden ser: "confirmed", "cancelled", "pending"
