import sqlite3
import os

DB_NAME = "sports_local.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

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
        cursor.execute('INSERT INTO users (email, name, phone, password, role) VALUES (?, ?, ?, ?, ?)',
                       ('admin@ranyave.com', 'Administrador', '', 'admin123', 'admin'))
    
    # Create default user if not exists
    cursor.execute('SELECT * FROM users WHERE email = ?', ('user@example.com',))
    if not cursor.fetchone():
        cursor.execute('INSERT INTO users (email, name, phone, password, role) VALUES (?, ?, ?, ?, ?)',
                       ('user@example.com', 'Usuario', '', 'user123', 'user'))

    # Create requested users "123"
    cursor.execute('SELECT * FROM users WHERE email = ?', ('123',))
    if not cursor.fetchone():
        cursor.execute('INSERT INTO users (email, name, phone, password, role) VALUES (?, ?, ?, ?, ?)',
                       ('123', 'Usuario 123', '1234567890', '123', 'user'))
                       
    cursor.execute('SELECT * FROM users WHERE email = ?', ('1234',))
    if not cursor.fetchone():
        cursor.execute('INSERT INTO users (email, name, phone, password, role) VALUES (?, ?, ?, ?, ?)',
                       ('1234', 'Usuario 1234', '1234567890', '123', 'user'))

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
        conn.execute('INSERT INTO users (email, name, phone, password, role) VALUES (?, ?, ?, ?, ?)',
                     (email, name, phone, password, role))
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

# Event Operations
