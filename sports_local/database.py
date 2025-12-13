import sqlite3
import os
import bcrypt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

DB_NAME = "sports_local.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    """Genera un hash seguro de la contraseña usando bcrypt"""
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password, hashed_password):
    """Verifica que una contraseña coincida con su hash"""
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    except:
        return False

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            phone TEXT,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    
    # Create Venues table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS venues (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            capacity INTEGER,
            location TEXT NOT NULL,
            schedule TEXT,
            price REAL DEFAULT 0.0,
            status TEXT DEFAULT 'active'
        )
    ''')
    
    # Verificar si la columna price existe, si no, agregarla
    try:
        cursor.execute('ALTER TABLE venues ADD COLUMN price REAL DEFAULT 0.0')
        conn.commit()
    except sqlite3.OperationalError:
        # La columna ya existe, no hay problema
        pass
    
    # Create Reservations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reservations (
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
    ''')

    # Create Events table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            schedule TEXT NOT NULL,
            location TEXT NOT NULL,
            capacity INTEGER NOT NULL
        )
    ''')
    
    # Create default admin if not exists
    cursor.execute('SELECT * FROM users WHERE email = ?', ('admin@ranyave.com',))
    if not cursor.fetchone():
        admin_password = hash_password('admin123')
        cursor.execute('INSERT INTO users (email, name, phone, password, role) VALUES (?, ?, ?, ?, ?)',
                       ('admin@ranyave.com', 'Administrador', '', admin_password, 'admin'))
    
    # Create default user if not exists
    cursor.execute('SELECT * FROM users WHERE email = ?', ('user@example.com',))
    if not cursor.fetchone():
        user_password = hash_password('user123')
        cursor.execute('INSERT INTO users (email, name, phone, password, role) VALUES (?, ?, ?, ?, ?)',
                       ('user@example.com', 'Usuario', '', user_password, 'user'))

    # Create requested users "123"
    cursor.execute('SELECT * FROM users WHERE email = ?', ('123',))
    if not cursor.fetchone():
        user_pass_123 = hash_password('321')
        cursor.execute('INSERT INTO users (email, name, phone, password, role) VALUES (?, ?, ?, ?, ?)',
                       ('123', 'Usuario 123', '1234567890', user_pass_123, 'user'))
                       
    cursor.execute('SELECT * FROM users WHERE email = ?', ('1234',))
    if not cursor.fetchone():
        user_pass_1234 = hash_password('123')
        cursor.execute('INSERT INTO users (email, name, phone, password, role) VALUES (?, ?, ?, ?, ?)',
                       ('1234', 'Usuario 1234', '1234567890', user_pass_1234, 'user'))

    # Create Gustavo user if not exists
    cursor.execute('SELECT * FROM users WHERE email = ?', ('gustavorestrepo54321@gmail.com',))
    if not cursor.fetchone():
        gustavo_pass = hash_password('gustabayern7')
        cursor.execute('INSERT INTO users (email, name, phone, password, role) VALUES (?, ?, ?, ?, ?)',
                       ('gustavorestrepo54321@gmail.com', 'gustavo', '3112887019', gustavo_pass, 'user'))

    conn.commit()
    conn.close()

# User Operations
def get_user(email):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    conn.close()
    if user:
        return dict(user)
    return None

def create_user(email, name, phone, password, role='user'):
    conn = get_db_connection()
    try:
        # Hashear la contraseña antes de guardar
        hashed_password = hash_password(password)
        conn.execute('INSERT INTO users (email, name, phone, password, role) VALUES (?, ?, ?, ?, ?)',
                     (email, name, phone, hashed_password, role))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# Venue Operations
def get_all_venues():
    conn = get_db_connection()
    venues = conn.execute('SELECT * FROM venues').fetchall()
    conn.close()
    # Convert to dictionary format expected by the app {id: {data}}
    result = {}
    for v in venues:
        v_dict = dict(v)
        # Asegurar que price existe y es un float
        if 'price' not in v_dict:
            v_dict['price'] = 0.0
        else:
            try:
                v_dict['price'] = float(v_dict['price'])
            except (ValueError, TypeError):
                v_dict['price'] = 0.0
        result[v_dict['id']] = v_dict
    return result

def save_venue(venue_data):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if exists to update or insert
    cursor.execute('SELECT id FROM venues WHERE id = ?', (venue_data['id'],))
    exists = cursor.fetchone()
    
    if exists:
        cursor.execute('''
            UPDATE venues SET name=?, type=?, capacity=?, location=?, schedule=?, price=?, status=?
            WHERE id=?
        ''', (venue_data['name'], venue_data['type'], venue_data['capacity'], 
              venue_data['location'], venue_data.get('schedule', ''), venue_data.get('price', 0.0), venue_data['status'], venue_data['id']))
    else:
        cursor.execute('''
            INSERT INTO venues (id, name, type, capacity, location, schedule, price, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (venue_data['id'], venue_data['name'], venue_data['type'], venue_data['capacity'], 
              venue_data['location'], venue_data.get('schedule', ''), venue_data.get('price', 0.0), venue_data['status']))
    
    conn.commit()
    conn.close()

def delete_venue(venue_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM venues WHERE id = ?', (venue_id,))
    conn.commit()
    conn.close()

# Reservation Operations
def get_all_reservations():
    conn = get_db_connection()
    reservations = conn.execute('SELECT * FROM reservations').fetchall()
    conn.close()
    # Convert to dictionary format expected by the app {id: {data}}
    result = {}
    for r in reservations:
        r_dict = dict(r)
        r_dict['user'] = r_dict['user_email'] # Mapping back for compatibility
        result[r_dict['id']] = r_dict
    return result

def save_reservation(res_data):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if exists
    cursor.execute('SELECT id FROM reservations WHERE id = ?', (res_data['id'],))
    exists = cursor.fetchone()
    
    user_val = res_data.get('user') or res_data.get('user_email')

    if exists:
        cursor.execute('''
            UPDATE reservations SET user_email=?, venue_id=?, venue_name=?, date=?, time=?, status=?
            WHERE id=?
        ''', (user_val, res_data['venue_id'], res_data['venue_name'], 
              res_data['date'], res_data['time'], res_data['status'], res_data['id']))
    else:
        cursor.execute('''
            INSERT INTO reservations (id, user_email, venue_id, venue_name, date, time, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (res_data['id'], user_val, res_data['venue_id'], res_data['venue_name'], 
              res_data['date'], res_data['time'], res_data['status']))
    
    conn.commit()
    conn.close()

def delete_reservation(res_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM reservations WHERE id = ?', (res_id,))
    conn.commit()
    conn.close()

def update_reservation_status(res_id, status):
    conn = get_db_connection()
    conn.execute('UPDATE reservations SET status = ? WHERE id = ?', (status, res_id))
    conn.commit()
    conn.close()

def send_welcome_email(user_email, user_name):
    """Envía un email de bienvenida al usuario registrado"""
    try:
        from email_config import SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD, EMAIL_SUBJECT, get_welcome_email_body
        
        # Validar que las credenciales estén configuradas
        if SENDER_EMAIL == "tu_correo@gmail.com" or SENDER_PASSWORD == "tu_contraseña_aplicacion":
            print("⚠️  Advertencia: Las credenciales de email no están configuradas en email_config.py")
            return False
        
        # Crear mensaje
        message = MIMEMultipart("alternative")
        message["Subject"] = EMAIL_SUBJECT
        message["From"] = SENDER_EMAIL
        message["To"] = user_email
        
        # Obtener contenido HTML del email
        html_body = get_welcome_email_body(user_name, user_email)
        part = MIMEText(html_body, "html")
        message.attach(part)
        
        # Enviar email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Iniciar encriptación TLS
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, user_email, message.as_string())
        
        print(f"✅ Email de bienvenida enviado a {user_email}")
        return True
        
    except ImportError:
        print("⚠️  Error: No se encontró el archivo email_config.py")
        return False
    except smtplib.SMTPAuthenticationError:
        print("❌ Error: Credenciales de email inválidas")
        return False
    except smtplib.SMTPException as e:
        print(f"❌ Error SMTP: {e}")
        return False
    except Exception as e:
        print(f"❌ Error al enviar email: {e}")
        return False

def send_reservation_email(user_email, user_name, venue_name, date, time, price):
    """Envía un email de confirmación de reserva"""
    try:
        from email_config import SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD, get_reservation_email_body
        
        if SENDER_EMAIL == "tu_correo@gmail.com" or SENDER_PASSWORD == "tu_contraseña_aplicacion":
            print("⚠️  Advertencia: Las credenciales de email no están configuradas")
            return False
        
        message = MIMEMultipart("alternative")
        message["Subject"] = "✅ Reserva Confirmada - Ranyave Sports"
        message["From"] = SENDER_EMAIL
        message["To"] = user_email
        
        html_body = get_reservation_email_body(user_name, venue_name, date, time, price)
        part = MIMEText(html_body, "html")
        message.attach(part)
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, user_email, message.as_string())
        
        print(f"✅ Email de reserva confirmada enviado a {user_email}")
        return True
        
    except Exception as e:
        print(f"❌ Error al enviar email de reserva: {e}")
        return False

def send_cancellation_email(user_email, user_name, venue_name, date, time, price):
    """Envía un email de cancelación de reserva"""
    try:
        from email_config import SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD, get_cancellation_email_body
        
        if SENDER_EMAIL == "tu_correo@gmail.com" or SENDER_PASSWORD == "tu_contraseña_aplicacion":
            print("⚠️  Advertencia: Las credenciales de email no están configuradas")
            return False
        
        message = MIMEMultipart("alternative")
        message["Subject"] = "⚠️ Reserva Cancelada - Ranyave Sports"
        message["From"] = SENDER_EMAIL
        message["To"] = user_email
        
        html_body = get_cancellation_email_body(user_name, venue_name, date, time, price)
        part = MIMEText(html_body, "html")
        message.attach(part)
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, user_email, message.as_string())
        
        print(f"✅ Email de cancelación enviado a {user_email}")
        return True
        
    except Exception as e:
        print(f"❌ Error al enviar email de cancelación: {e}")
        return False


# Event Operations
