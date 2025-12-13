"""
PRUEBAS UNITARIAS - Ranyave
============================

Tutorial y ejemplos de cómo hacer pruebas unitarias con pytest.

Instalar primero:
    pip install pytest

Ejecutar pruebas:
    pytest test_basics.py -v              # Ver detalles
    pytest test_basics.py -v --tb=short   # Menos detalles
    pytest test_basics.py::TestUsuarios   # Solo una clase
    pytest -k "test_crear"                # Solo tests con "crear"

"""

import pytest
import sqlite3
import os
from pathlib import Path
import sys

# Importar las funciones a probar
sys.path.insert(0, str(Path(__file__).parent))
from sports_local import database


# ============================================================================
# CONFIGURACIÓN - Fixtures (preparar ambiente)
# ============================================================================

@pytest.fixture
def db_test():
    """
    Fixture: Crea una BD de prueba limpia antes de cada test.
    Se ejecuta ANTES del test.
    """
    # Crear BD temporal para pruebas
    test_db = "test_sports.db"
    
    # Monkeypatch: cambiar el nombre de la BD a la temporal
    original_db = database.DB_NAME
    database.DB_NAME = test_db
    
    # Inicializar BD de prueba
    database.init_db()
    
    yield test_db  # Aquí se ejecuta el test
    
    # Cleanup: se ejecuta DESPUÉS del test
    database.DB_NAME = original_db
    if os.path.exists(test_db):
        os.remove(test_db)


# ============================================================================
# CLASE 1: Pruebas de Funciones de Seguridad
# ============================================================================

class TestSeguridad:
    """Pruebas para funciones de cifrado y verificación de contraseñas."""
    
    def test_hash_password_genera_hash(self):
        """
        TEST 1: Verifica que hash_password genera un hash.
        
        Arrange: Preparar datos
        Act: Ejecutar función
        Assert: Verificar resultado
        """
        # Arrange (Preparar)
        password = "MiContraseña123"
        
        # Act (Actuar)
        hashed = database.hash_password(password)
        
        # Assert (Afirmar)
        assert hashed is not None, "El hash no debería ser None"
        assert len(hashed) > 0, "El hash debería tener contenido"
        assert hashed != password, "El hash no debería ser igual a la contraseña"
    
    
    def test_hash_password_hashes_diferentes(self):
        """
        TEST 2: Verifica que el mismo password genera hashes diferentes
        (debido al salt aleatorio).
        """
        password = "password123"
        
        # Act: Hashear dos veces la misma contraseña
        hash1 = database.hash_password(password)
        hash2 = database.hash_password(password)
        
        # Assert: Los hashes deben ser diferentes
        assert hash1 != hash2, "Hashes del mismo password deben ser diferentes"
    
    
    def test_verify_password_correcto(self):
        """
        TEST 3: Verifica que verify_password funciona con contraseña correcta.
        """
        password = "password123"
        
        # Arrange: Crear un hash
        hashed = database.hash_password(password)
        
        # Act: Verificar
        resultado = database.verify_password(password, hashed)
        
        # Assert: Debería ser True
        assert resultado is True, "verify_password debería retornar True"
    
    
    def test_verify_password_incorrecto(self):
        """
        TEST 4: Verifica que verify_password falla con contraseña incorrecta.
        """
        password1 = "password123"
        password2 = "wrongpassword"
        
        # Arrange: Crear un hash con password1
        hashed = database.hash_password(password1)
        
        # Act: Intentar verificar con password2
        resultado = database.verify_password(password2, hashed)
        
        # Assert: Debería ser False
        assert resultado is False, "verify_password debería retornar False"


# ============================================================================
# CLASE 2: Pruebas de Usuarios
# ============================================================================

class TestUsuarios:
    """Pruebas para operaciones con usuarios."""
    
    def test_crear_usuario(self, db_test):
        """
        TEST 5: Verifica que se puede crear un usuario.
        
        Nota: db_test es una fixture que proporciona una BD limpia.
        """
        # Act: Crear usuario
        exito = database.create_user(
            email='juan@example.com',
            name='Juan Pérez',
            phone='3001234567',
            password='password123',
            role='user'
        )
        
        # Assert
        assert exito is True, "Debería crear usuario exitosamente"
    
    
    def test_crear_usuario_email_duplicado(self, db_test):
        """
        TEST 6: Verifica que no se puede crear usuario con email duplicado.
        """
        # Arrange: Crear primer usuario
        database.create_user(
            email='juan@example.com',
            name='Juan Pérez',
            phone='3001234567',
            password='password123'
        )
        
        # Act: Intentar crear segundo usuario con mismo email
        exito = database.create_user(
            email='juan@example.com',
            name='Juan Otro',
            phone='3009876543',
            password='anotherpass'
        )
        
        # Assert: Debería fallar
        assert exito is False, "No debería permitir email duplicado"
    
    
    def test_obtener_usuario(self, db_test):
        """
        TEST 7: Verifica que se puede obtener un usuario creado.
        """
        # Arrange: Crear usuario
        database.create_user(
            email='maria@example.com',
            name='María García',
            phone='3009876543',
            password='securepass'
        )
        
        # Act: Obtener usuario
        usuario = database.get_user('maria@example.com')
        
        # Assert
        assert usuario is not None, "El usuario debería existir"
        assert usuario['name'] == 'María García', "El nombre debe coincidir"
        assert usuario['email'] == 'maria@example.com', "El email debe coincidir"
        assert usuario['phone'] == '3009876543', "El teléfono debe coincidir"
    
    
    def test_obtener_usuario_inexistente(self, db_test):
        """
        TEST 8: Verifica que get_user retorna None para usuario inexistente.
        """
        # Act
        usuario = database.get_user('noexiste@example.com')
        
        # Assert
        assert usuario is None, "Debería retornar None para usuario inexistente"
    
    
    def test_verificar_credenciales_correctas(self, db_test):
        """
        TEST 9: Simula un login exitoso.
        """
        # Arrange: Crear usuario
        email = 'luis@example.com'
        password = 'password123'
        database.create_user(
            email=email,
            name='Luis López',
            phone='3005555555',
            password=password
        )
        
        # Act: Intentar login
        usuario = database.get_user(email)
        
        # Assert
        assert usuario is not None
        assert database.verify_password(password, usuario['password'])
    
    
    def test_verificar_credenciales_incorrectas(self, db_test):
        """
        TEST 10: Simula un login fallido (contraseña incorrecta).
        """
        # Arrange: Crear usuario
        email = 'luis@example.com'
        database.create_user(
            email=email,
            name='Luis López',
            phone='3005555555',
            password='password123'
        )
        
        # Act: Intentar login con contraseña incorrecta
        usuario = database.get_user(email)
        result = database.verify_password('wrongpassword', usuario['password'])
        
        # Assert
        assert result is False, "Debería fallar con contraseña incorrecta"


# ============================================================================
# CLASE 3: Pruebas de Escenarios
# ============================================================================

class TestEscenarios:
    """Pruebas para operaciones con escenarios deportivos."""
    
    def test_guardar_escenario(self, db_test):
        """
        TEST 11: Verifica que se puede guardar un escenario.
        """
        # Arrange: Preparar datos del escenario
        escenario = {
            'id': 'cancha_001',
            'name': 'Cancha de Tenis 1',
            'type': 'Tenis',
            'capacity': 4,
            'location': 'Centro Deportivo',
            'schedule': '7:00-22:00',
            'price': 50000,
            'status': 'active'
        }
        
        # Act: Guardar escenario
        database.save_venue(escenario)
        
        # Assert: Obtener y verificar
        escenario_guardado = database.get_all_venues()
        assert 'cancha_001' in escenario_guardado
        assert escenario_guardado['cancha_001']['name'] == 'Cancha de Tenis 1'
    
    
    def test_obtener_escenario(self, db_test):
        """
        TEST 12: Verifica que se puede obtener un escenario guardado.
        """
        # Arrange: Guardar escenario
        escenario = {
            'id': 'cancha_002',
            'name': 'Cancha de Fútbol',
            'type': 'Fútbol',
            'capacity': 22,
            'location': 'Centro',
            'schedule': '7:00-22:00',
            'price': 100000,
            'status': 'active'
        }
        database.save_venue(escenario)
        
        # Act: Obtener todos
        escenarios = database.get_all_venues()
        
        # Assert
        assert len(escenarios) > 0, "Debería haber al menos un escenario"
        assert escenarios['cancha_002']['name'] == 'Cancha de Fútbol'
    
    
    def test_eliminar_escenario(self, db_test):
        """
        TEST 13: Verifica que se puede eliminar un escenario.
        """
        # Arrange: Crear escenario
        escenario = {
            'id': 'cancha_003',
            'name': 'Cancha a Eliminar',
            'type': 'Volley',
            'capacity': 12,
            'location': 'Centro',
            'schedule': '7:00-22:00',
            'price': 30000,
            'status': 'active'
        }
        database.save_venue(escenario)
        
        # Act: Eliminar
        database.delete_venue('cancha_003')
        
        # Assert
        escenarios = database.get_all_venues()
        assert 'cancha_003' not in escenarios, "El escenario debería estar eliminado"


# ============================================================================
# CLASE 4: Pruebas de Reservas
# ============================================================================

class TestReservas:
    """Pruebas para operaciones con reservas."""
    
    def test_crear_reserva(self, db_test):
        """
        TEST 14: Verifica que se puede crear una reserva.
        """
        # Arrange
        reserva = {
            'id': 'res_001',
            'user_email': 'juan@example.com',
            'venue_id': 'cancha_001',
            'venue_name': 'Cancha de Tenis',
            'date': '2024-12-25',
            'time': '14:00',
            'status': 'confirmed'
        }
        
        # Act
        database.save_reservation(reserva)
        
        # Assert
        reservas = database.get_all_reservations()
        assert 'res_001' in reservas
        assert reservas['res_001']['venue_name'] == 'Cancha de Tenis'
    
    
    def test_obtener_reserva(self, db_test):
        """
        TEST 15: Verifica que se obtiene reserva correcta.
        """
        # Arrange: Crear reserva
        reserva = {
            'id': 'res_002',
            'user_email': 'maria@example.com',
            'venue_id': 'cancha_001',
            'venue_name': 'Cancha de Tenis',
            'date': '2024-12-26',
            'time': '15:00',
            'status': 'confirmed'
        }
        database.save_reservation(reserva)
        
        # Act: Obtener
        reservas = database.get_all_reservations()
        
        # Assert
        assert reservas['res_002']['date'] == '2024-12-26'
        assert reservas['res_002']['time'] == '15:00'
    
    
    def test_cancelar_reserva(self, db_test):
        """
        TEST 16: Verifica que se puede cambiar estado de reserva.
        """
        # Arrange: Crear reserva
        reserva = {
            'id': 'res_003',
            'user_email': 'luis@example.com',
            'venue_id': 'cancha_001',
            'venue_name': 'Cancha',
            'date': '2024-12-27',
            'time': '16:00',
            'status': 'confirmed'
        }
        database.save_reservation(reserva)
        
        # Act: Actualizar estado
        database.update_reservation_status('res_003', 'cancelled')
        
        # Assert
        reservas = database.get_all_reservations()
        assert reservas['res_003']['status'] == 'cancelled'


# ============================================================================
# EJEMPLO: Cómo NO hacer pruebas
# ============================================================================

# ❌ MAL - Sin estructura
# def test_algo():
#     x = 5
#     y = 10
#     assert x + y == 15

# ✅ BIEN - Con Arrange, Act, Assert
# def test_suma():
#     # Arrange
#     numero1 = 5
#     numero2 = 10
#     
#     # Act
#     resultado = numero1 + numero2
#     
#     # Assert
#     assert resultado == 15

# ============================================================================
# INSTRUCCIONES DE USO
# ============================================================================

"""
PASO A PASO PARA CORRER PRUEBAS:

1. Instalar pytest (si no está instalado):
   pip install pytest

2. Correr TODAS las pruebas:
   pytest test_basics.py -v

3. Correr pruebas de una clase específica:
   pytest test_basics.py::TestSeguridad -v

4. Correr un test específico:
   pytest test_basics.py::TestUsuarios::test_crear_usuario -v

5. Correr solo tests que coincidan con un patrón:
   pytest test_basics.py -k "usuario" -v

6. Ver resumen (sin detalles):
   pytest test_basics.py

7. Parar en el primer error:
   pytest test_basics.py -x

8. Ver output de print() dentro de tests:
   pytest test_basics.py -s

EXPLICACIÓN DE ASSERTS:

assert expresion, "mensaje si falla"

✅ assert True                           # Siempre pasa
❌ assert False                          # Siempre falla
✅ assert 5 == 5, "5 debe igual 5"      # Pasa
❌ assert 5 == 10, "Debería ser 5"      # Falla
✅ assert usuario is not None, "Usuario debe existir"
✅ assert len(lista) > 0, "Lista no vacía"
✅ assert 'email' in usuario, "Debe tener email"
"""
