import sys
import os
import re
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, 
                             QVBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, 
                             QMessageBox, QStackedWidget, QCalendarWidget, QTimeEdit, QDialog)
from PyQt5.QtGui import QFont, QColor, QPixmap, QPainter, QPen
from PyQt5.QtCore import Qt, QDate, QTime
from PIL import Image, ImageDraw
import io

# ============================================================================
# CONFIGURACIÓN: Ruta de la imagen del lado izquierdo
# ============================================================================
IMAGE_PATH = "assets/logo_ranyave.png"  # Cambia esta ruta a tu imagen
USERS_FILE = "users.json"  # Archivo para guardar usuarios registrados
ADMINS_FILE = "admins.json"  # Archivo para guardar administradores
STAGES_FILE = "stages.json"  # Archivo para guardar etapas deportivas
EVENTS_FILE = "events.json"  # Archivo para guardar eventos
# ============================================================================

def load_users_from_file():
    """Carga usuarios registrados desde archivo JSON"""
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def load_admins_from_file():
    """Carga administradores desde archivo JSON"""
    if os.path.exists(ADMINS_FILE):
        try:
            with open(ADMINS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_users_to_file(users):
    """Guarda usuarios registrados en archivo JSON"""
    try:
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(users, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error guardando usuarios: {e}")

def save_admins_to_file(admins):
    """Guarda administradores en archivo JSON"""
    try:
        with open(ADMINS_FILE, 'w', encoding='utf-8') as f:
            json.dump(admins, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error guardando admins: {e}")

def load_stages_from_file():
    """Carga etapas deportivas desde archivo JSON"""
    if os.path.exists(STAGES_FILE):
        try:
            with open(STAGES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_stages_to_file(stages):
    """Guarda etapas deportivas en archivo JSON"""
    try:
        with open(STAGES_FILE, 'w', encoding='utf-8') as f:
            json.dump(stages, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error guardando etapas: {e}")

def load_events_from_file():
    """Carga eventos desde archivo JSON"""
    if os.path.exists(EVENTS_FILE):
        try:
            with open(EVENTS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_events_to_file(events):
    """Guarda eventos en archivo JSON"""
    try:
        with open(EVENTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(events, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error guardando eventos: {e}")

def create_default_users():
    """Crea usuarios predefinidos si no existen"""
    default_admins = {
        "admin@ranyave.com": {
            "password": "admin123",
            "role": "admin",
            "name": "Administrador"
        }
    }
    
    default_users = {
        "user@example.com": {
            "password": "user123",
            "role": "user",
            "name": "Usuario"
        }
    }
    
    # Crear archivos si no existen
    if not os.path.exists(ADMINS_FILE):
        save_admins_to_file(default_admins)
    
    if not os.path.exists(USERS_FILE):
        save_users_to_file(default_users)

# Cargar usuarios al iniciar
create_default_users()
USERS_DB = load_admins_from_file()
REGISTERED_USERS = load_users_from_file()
STAGES_DB = load_stages_from_file()
EVENTS_DB = load_events_from_file()

def show_styled_message(parent, title, message, message_type="information"):
    """Muestra un mensaje con estilo personalizado (fondo blanco)"""
    msg_box = QMessageBox(parent)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.setStyleSheet("""
        QMessageBox {
            background-color: white;
        }
        QMessageBox QLabel {
            color: black;
            background-color: white;
        }
        QMessageBox QTextEdit {
            color: black;
            background-color: white;
        }
        QMessageBox QPushButton {
            background-color: white;
            border: 1px solid #ccc;
            padding: 5px;
            min-width: 50px;
            color: black;
        }
        QMessageBox QPushButton:hover {
            background-color: #f0f0f0;
        }
    """)
    
    if message_type == "warning":
        msg_box.setIcon(QMessageBox.Warning)
    elif message_type == "information":
        msg_box.setIcon(QMessageBox.Information)
    elif message_type == "error":
        msg_box.setIcon(QMessageBox.Critical)
    
    msg_box.exec_()

class LoginWidget(QWidget):
    """Pantalla de Login"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.init_ui()
    
    def init_ui(self):
        # Layout principal
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Panel izquierdo (imagen)
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_layout.setAlignment(Qt.AlignCenter)
        left_layout.setContentsMargins(40, 40, 40, 40)
        
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignCenter)
        pixmap = self.load_image(IMAGE_PATH)
        if pixmap:
            image_label.setPixmap(pixmap)
        else:
            image_label.setPixmap(self.create_default_logo())
        
        left_layout.addWidget(image_label)
        left_panel.setLayout(left_layout)
        left_panel.setStyleSheet("background-color: #1e3a5f;")
        
        # Panel derecho (formulario)
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_layout.setSpacing(15)
        right_layout.setContentsMargins(60, 60, 60, 60)
        
        # Título
        title = QLabel("LOGIN")
        title_font = QFont("Arial", 28, QFont.Bold)
        title.setFont(title_font)
        title.setStyleSheet("color: white;")
        title.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(title)
        
        right_layout.addSpacing(30)
        
        # Email/Usuario
        email_label = QLabel("Email")
        email_label.setStyleSheet("color: white; font-size: 11px; font-weight: bold;")
        right_layout.addWidget(email_label)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Ingresa tu email")
        self.email_input.setStyleSheet(self.get_input_style())
        self.email_input.setMinimumHeight(40)
        right_layout.addWidget(self.email_input)
        
        # Contraseña
        password_label = QLabel("Password")
        password_label.setStyleSheet("color: white; font-size: 11px; font-weight: bold;")
        right_layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Ingresa tu contraseña")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(self.get_input_style())
        self.password_input.setMinimumHeight(40)
        right_layout.addWidget(self.password_input)
        
        right_layout.addSpacing(20)
        
        # Botones
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        
        next_btn = QPushButton("Next")
        next_btn.setFont(QFont("Arial", 12, QFont.Bold))
        next_btn.setStyleSheet(self.get_button_style())
        next_btn.setMinimumWidth(120)
        next_btn.setMinimumHeight(40)
        next_btn.clicked.connect(self.on_login)
        buttons_layout.addWidget(next_btn)
        
        back_btn = QPushButton("Back")
        back_btn.setFont(QFont("Arial", 12, QFont.Bold))
        back_btn.setStyleSheet(self.get_button_style())
        back_btn.setMinimumWidth(120)
        back_btn.setMinimumHeight(40)
        back_btn.clicked.connect(self.on_back)
        buttons_layout.addWidget(back_btn)
        
        buttons_layout.addStretch()
        right_layout.addLayout(buttons_layout)
        
        right_layout.addSpacing(20)
        
        # Link a registro
        register_label = QLabel("¿No tienes cuenta? <a href='#' style='color: #87CEEB; text-decoration: none;'><b>Regístrate aquí</b></a>")
        register_label.setStyleSheet("color: white; font-size: 11px;")
        register_label.setAlignment(Qt.AlignCenter)
        register_label.linkActivated.connect(self.on_register_link)
        right_layout.addWidget(register_label)
        
        right_layout.addStretch()
        
        right_panel.setLayout(right_layout)
        right_panel.setStyleSheet("background-color: #1e3a5f;")
        
        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 1)
        
        self.setLayout(main_layout)
        self.setStyleSheet("background-color: #1e3a5f;")
    
    def on_login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        
        if not email or not password:
            show_styled_message(self, "Error", "Por favor completa todos los campos", "warning")
            return
        
        # Validar email
        if not self.is_valid_email(email):
            show_styled_message(self, "Error", "Por favor ingresa un email válido", "warning")
            return
        
        # Verificar en BD
        if email in USERS_DB:
            user = USERS_DB[email]
            if user["password"] == password:
                # Login exitoso
                role = user["role"]
                name = user["name"]
                self.parent_window.login_user(name, role)
                return
        
        # Verificar en usuarios registrados
        if email in REGISTERED_USERS:
            user = REGISTERED_USERS[email]
            if user["password"] == password:
                self.parent_window.login_user(user["name"], "user")
                return
        
        show_styled_message(self, "Error", "Email o contraseña incorrectos", "warning")
        self.clear_fields()
    
    def on_back(self):
        self.parent_window.show_welcome()
    
    def on_register_link(self):
        self.parent_window.show_register()
    
    def is_valid_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def clear_fields(self):
        self.email_input.clear()
        self.password_input.clear()
    
    def load_image(self, image_path):
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                return pixmap.scaledToHeight(500, Qt.SmoothTransformation)
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        absolute_path = os.path.join(script_dir, image_path)
        
        if os.path.exists(absolute_path):
            pixmap = QPixmap(absolute_path)
            if not pixmap.isNull():
                return pixmap.scaledToHeight(500, Qt.SmoothTransformation)
        
        return None
    
    def create_default_logo(self):
        size = 350
        img = Image.new('RGBA', (size, size), color=(30, 58, 95, 0))
        draw = ImageDraw.Draw(img)
        
        head_radius = 35
        draw.ellipse([(150-head_radius, 50-head_radius), (150+head_radius, 50+head_radius)], fill='white')
        draw.line([(150, 85), (140, 150)], fill='white', width=8)
        draw.polygon([(140, 95), (90, 70), (110, 110)], fill='white')
        draw.polygon([(160, 95), (210, 70), (190, 110)], fill='white')
        draw.polygon([(140, 150), (120, 250), (135, 250)], fill='white')
        draw.polygon([(140, 150), (170, 240), (185, 240)], fill='white')
        
        data = io.BytesIO()
        img.save(data, format='PNG')
        data.seek(0)
        
        pixmap = QPixmap()
        pixmap.loadFromData(data.getvalue())
        return pixmap.scaledToHeight(500, Qt.SmoothTransformation)
    
    @staticmethod
    def get_input_style():
        return """
            QLineEdit {
                background-color: transparent;
                border: none;
                border-bottom: 2px solid white;
                padding: 8px 5px;
                font-size: 12px;
                color: white;
                font-style: italic;
            }
            QLineEdit::placeholder {
                color: rgba(255, 255, 255, 100);
            }
            QLineEdit:focus {
                outline: none;
                border-bottom: 2px solid #87CEEB;
            }
        """
    
    @staticmethod
    def get_button_style():
        return """
            QPushButton {
                background-color: white;
                color: #1e3a5f;
                border: none;
                border-radius: 20px;
                padding: 10px 20px;
                font-weight: bold;
                cursor: pointer;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """


class RegisterWidget(QWidget):
    """Pantalla de Registro"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.init_ui()
    
    def init_ui(self):
        # Layout principal
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Panel izquierdo (imagen)
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_layout.setAlignment(Qt.AlignCenter)
        left_layout.setContentsMargins(40, 40, 40, 40)
        
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignCenter)
        pixmap = self.load_image(IMAGE_PATH)
        if pixmap:
            image_label.setPixmap(pixmap)
        else:
            image_label.setPixmap(self.create_default_logo())
        
        left_layout.addWidget(image_label)
        left_panel.setLayout(left_layout)
        left_panel.setStyleSheet("background-color: #1e3a5f;")
        
        # Panel derecho (formulario)
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_layout.setSpacing(12)
        right_layout.setContentsMargins(60, 40, 60, 40)
        
        # Título
        title = QLabel("REGISTER")
        title_font = QFont("Arial", 28, QFont.Bold)
        title.setFont(title_font)
        title.setStyleSheet("color: white;")
        title.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(title)
        
        right_layout.addSpacing(20)
        
        # Nombre
        name_label = QLabel("Name")
        name_label.setStyleSheet("color: white; font-size: 11px; font-weight: bold;")
        right_layout.addWidget(name_label)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Name")
        self.name_input.setStyleSheet(self.get_input_style())
        self.name_input.setMinimumHeight(35)
        right_layout.addWidget(self.name_input)
        
        # Email
        email_label = QLabel("Email")
        email_label.setStyleSheet("color: white; font-size: 11px; font-weight: bold;")
        right_layout.addWidget(email_label)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.email_input.setStyleSheet(self.get_input_style())
        self.email_input.setMinimumHeight(35)
        right_layout.addWidget(self.email_input)
        
        # Teléfono
        phone_label = QLabel("Cell Phone Number")
        phone_label.setStyleSheet("color: white; font-size: 11px; font-weight: bold;")
        right_layout.addWidget(phone_label)
        
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Cell Phone Number")
        self.phone_input.setStyleSheet(self.get_input_style())
        self.phone_input.setMinimumHeight(35)
        right_layout.addWidget(self.phone_input)
        
        # Contraseña
        password_label = QLabel("Password")
        password_label.setStyleSheet("color: white; font-size: 11px; font-weight: bold;")
        right_layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(self.get_input_style())
        self.password_input.setMinimumHeight(35)
        right_layout.addWidget(self.password_input)
        
        right_layout.addSpacing(15)
        
        # Botones
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        
        next_btn = QPushButton("Next")
        next_btn.setFont(QFont("Arial", 12, QFont.Bold))
        next_btn.setStyleSheet(self.get_button_style())
        next_btn.setMinimumWidth(120)
        next_btn.setMinimumHeight(40)
        next_btn.clicked.connect(self.on_register)
        buttons_layout.addWidget(next_btn)
        
        back_btn = QPushButton("Back")
        back_btn.setFont(QFont("Arial", 12, QFont.Bold))
        back_btn.setStyleSheet(self.get_button_style())
        back_btn.setMinimumWidth(120)
        back_btn.setMinimumHeight(40)
        back_btn.clicked.connect(self.on_back)
        buttons_layout.addWidget(back_btn)
        
        buttons_layout.addStretch()
        right_layout.addLayout(buttons_layout)
        
        right_layout.addStretch()
        
        right_panel.setLayout(right_layout)
        right_panel.setStyleSheet("background-color: #1e3a5f;")
        
        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 1)
        
        self.setLayout(main_layout)
        self.setStyleSheet("background-color: #1e3a5f;")
    
    def on_register(self):
        global REGISTERED_USERS
        
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        phone = self.phone_input.text().strip()
        password = self.password_input.text().strip()
        
        # Validaciones
        if not all([name, email, phone, password]):
            show_styled_message(self, "Error", "Por favor completa todos los campos", "warning")
            return
        
        if not self.is_valid_email(email):
            show_styled_message(self, "Error", "Por favor ingresa un email válido", "warning")
            return
        
        if not self.is_valid_phone(phone):
            show_styled_message(self, "Error", "Por favor ingresa un teléfono válido (10+ dígitos)", "warning")
            return
        
        if len(password) < 6:
            show_styled_message(self, "Error", "La contraseña debe tener al menos 6 caracteres", "warning")
            return
        
        if email in USERS_DB or email in REGISTERED_USERS:
            show_styled_message(self, "Error", "Este email ya está registrado", "warning")
            return
        
        # Registrar usuario
        REGISTERED_USERS[email] = {
            "name": name,
            "email": email,
            "phone": phone,
            "password": password,
            "role": "user"
        }
        
        # Guardar en archivo
        save_users_to_file(REGISTERED_USERS)
        
        show_styled_message(self, "Éxito", f"¡Bienvenido {name}!\nTu registro fue completado. Ahora puedes iniciar sesión.", "information")
        self.clear_fields()
        self.parent_window.show_login()
    
    def on_back(self):
        self.parent_window.show_login()
    
    def is_valid_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def is_valid_phone(self, phone):
        # Solo números, mínimo 10 dígitos
        digits = ''.join(c for c in phone if c.isdigit())
        return len(digits) >= 10
    
    def clear_fields(self):
        self.name_input.clear()
        self.email_input.clear()
        self.phone_input.clear()
        self.password_input.clear()
    
    def load_image(self, image_path):
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                return pixmap.scaledToHeight(500, Qt.SmoothTransformation)
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        absolute_path = os.path.join(script_dir, image_path)
        
        if os.path.exists(absolute_path):
            pixmap = QPixmap(absolute_path)
            if not pixmap.isNull():
                return pixmap.scaledToHeight(500, Qt.SmoothTransformation)
        
        return None
    
    def create_default_logo(self):
        size = 350
        img = Image.new('RGBA', (size, size), color=(30, 58, 95, 0))
        draw = ImageDraw.Draw(img)
        
        head_radius = 35
        draw.ellipse([(150-head_radius, 50-head_radius), (150+head_radius, 50+head_radius)], fill='white')
        draw.line([(150, 85), (140, 150)], fill='white', width=8)
        draw.polygon([(140, 95), (90, 70), (110, 110)], fill='white')
        draw.polygon([(160, 95), (210, 70), (190, 110)], fill='white')
        draw.polygon([(140, 150), (120, 250), (135, 250)], fill='white')
        draw.polygon([(140, 150), (170, 240), (185, 240)], fill='white')
        
        data = io.BytesIO()
        img.save(data, format='PNG')
        data.seek(0)
        
        pixmap = QPixmap()
        pixmap.loadFromData(data.getvalue())
        return pixmap.scaledToHeight(500, Qt.SmoothTransformation)
    
    @staticmethod
    def get_input_style():
        return """
            QLineEdit {
                background-color: transparent;
                border: 2px solid white;
                border-radius: 2px;
                padding: 8px;
                font-size: 11px;
                color: white;
                font-style: italic;
            }
            QLineEdit::placeholder {
                color: rgba(255, 255, 255, 150);
            }
            QLineEdit:focus {
                outline: none;
                border: 2px solid #87CEEB;
            }
        """
    
    @staticmethod
    def get_button_style():
        return """
            QPushButton {
                background-color: white;
                color: #1e3a5f;
                border: none;
                border-radius: 20px;
                padding: 10px 20px;
                font-weight: bold;
                cursor: pointer;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """


class AdminDashboard(QWidget):
    """Panel de Administrador"""
    def __init__(self, user_name, parent=None):
        super().__init__(parent)
        self.user_name = user_name
        self.parent_window = parent
        self.init_ui()
    
    def paintEvent(self, event):
        """Pinta el fondo con baloncestos decorativos"""
        painter = QPainter(self)
        
        # Fondo azul
        painter.fillRect(self.rect(), QColor(30, 58, 95))
        
        # Líneas diagonales decorativas
        painter.setPen(Qt.white)
        painter.setPen(QPen(QColor(255, 255, 255), 2))
        
        # Líneas diagonales
        painter.drawLine(self.width() - 200, -50, self.width() + 50, 150)
        painter.drawLine(self.width() - 100, -50, self.width() + 150, 250)
        painter.drawLine(-100, self.height() - 200, 200, self.height() + 100)
        painter.drawLine(0, self.height() - 150, 300, self.height() + 100)
    
    def init_ui(self):
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)
        
        # Header con rol
        header_layout = QHBoxLayout()
        header_label = QLabel("ADMIN")
        header_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold;")
        header_layout.addStretch()
        header_layout.addWidget(header_label)
        main_layout.addLayout(header_layout)
        
        # Título
        title = QLabel("MANAGEMENT ADMIN")
        title_font = QFont("Arial", 32, QFont.Bold)
        title.setFont(title_font)
        title.setStyleSheet("color: white;")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        main_layout.addSpacing(40)
        
        # Sección central con botones
        center_layout = QVBoxLayout()
        center_layout.setSpacing(20)
        center_layout.setAlignment(Qt.AlignCenter)
        
        # Botón NEW STAGES
        new_stages_btn = QPushButton("NEW STAGES")
        new_stages_btn.setFont(QFont("Arial", 14, QFont.Bold))
        new_stages_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #1e3a5f;
                border: none;
                border-radius: 6px;
                padding: 15px 50px;
                font-weight: bold;
                min-width: 250px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """)
        new_stages_btn.clicked.connect(self.on_new_stages)
        center_layout.addWidget(new_stages_btn, alignment=Qt.AlignCenter)
        
        # Botón STAGES INFO
        stages_info_btn = QPushButton("STAGES INFO")
        stages_info_btn.setFont(QFont("Arial", 14, QFont.Bold))
        stages_info_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #1e3a5f;
                border: none;
                border-radius: 6px;
                padding: 15px 50px;
                font-weight: bold;
                min-width: 250px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """)
        stages_info_btn.clicked.connect(self.on_stages_info)
        center_layout.addWidget(stages_info_btn, alignment=Qt.AlignCenter)
        
        # Botón EVENTS
        events_btn = QPushButton("EVENTS")
        events_btn.setFont(QFont("Arial", 14, QFont.Bold))
        events_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #1e3a5f;
                border: none;
                border-radius: 6px;
                padding: 15px 50px;
                font-weight: bold;
                min-width: 250px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """)
        events_btn.clicked.connect(self.on_events)
        center_layout.addWidget(events_btn, alignment=Qt.AlignCenter)
        
        # Botón Back to login
        back_btn = QPushButton("Back to login")
        back_btn.setFont(QFont("Arial", 12, QFont.Bold))
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #1e3a5f;
                border: none;
                border-radius: 6px;
                padding: 12px 40px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """)
        back_btn.clicked.connect(self.on_logout)
        center_layout.addWidget(back_btn, alignment=Qt.AlignCenter)
        
        main_layout.addLayout(center_layout)
        
        main_layout.addSpacing(30)
        
        # Información de usuario (opcional)
        user_info = QLabel(f"Sesión de: {self.user_name}")
        user_info.setStyleSheet("color: rgba(255, 255, 255, 150); font-size: 10px;")
        user_info.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(user_info)
        
        main_layout.addStretch()
        
        self.setLayout(main_layout)
        self.setStyleSheet("background-color: #1e3a5f;")
    
    def on_new_stages(self):
        new_sport_stage = NewSportStageWidget(self.parent_window)
        self.parent_window.stacked_widget.addWidget(new_sport_stage)
        self.parent_window.stacked_widget.setCurrentWidget(new_sport_stage)
        self.parent_window.current_admin_dashboard = self
    
    def on_stages_info(self):
        stages_info = StagesInfoWidget(self.parent_window)
        self.parent_window.stacked_widget.addWidget(stages_info)
        self.parent_window.stacked_widget.setCurrentWidget(stages_info)
        self.parent_window.current_admin_dashboard = self
    
    def on_events(self):
        new_events = NewEventsWidget(self.parent_window)
        self.parent_window.stacked_widget.addWidget(new_events)
        self.parent_window.stacked_widget.setCurrentWidget(new_events)
        self.parent_window.current_admin_dashboard = self
    
    def on_logout(self):
        self.parent_window.show_welcome()
    
    def on_logout(self):
        self.parent_window.show_welcome()


class UserDashboard(QWidget):
    """Panel de Usuario Normal"""
    def __init__(self, user_name, parent=None):
        super().__init__(parent)
        self.user_name = user_name
        self.parent_window = parent
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(60, 60, 60, 60)
        layout.setSpacing(20)
        
        # Header con rol
        header_layout = QHBoxLayout()
        header_label = QLabel("USER")
        header_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold;")
        header_layout.addStretch()
        header_layout.addWidget(header_label)
        layout.addLayout(header_layout)
        
        # Título
        title = QLabel("MANAGEMENT USER")
        title_font = QFont("Arial", 32, QFont.Bold)
        title.setFont(title_font)
        title.setStyleSheet("color: white;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        layout.addSpacing(40)
        
        # Sección central con opciones
        center_layout = QVBoxLayout()
        center_layout.setSpacing(20)
        center_layout.setAlignment(Qt.AlignCenter)
        
        # Opciones de usuario
        info = QLabel("Tus opciones disponibles:")
        info.setStyleSheet("color: white; font-size: 14px;")
        center_layout.addWidget(info, alignment=Qt.AlignCenter)
        
        options = [
            "✓ Ver perfil",
            "✓ Editar datos",
            "✓ Ver eventos disponibles",
            "✓ Configuración de cuenta"
        ]
        
        for option in options:
            option_label = QLabel(option)
            option_label.setStyleSheet("color: #87CEEB; font-size: 12px;")
            center_layout.addWidget(option_label, alignment=Qt.AlignCenter)
        
        center_layout.addSpacing(20)
        
        # Botón de logout
        logout_btn = QPushButton("Back to login")
        logout_btn.setFont(QFont("Arial", 12, QFont.Bold))
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #1e3a5f;
                border: none;
                border-radius: 6px;
                padding: 12px 40px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """)
        logout_btn.clicked.connect(self.on_logout)
        center_layout.addWidget(logout_btn, alignment=Qt.AlignCenter)
        
        layout.addLayout(center_layout)
        
        layout.addSpacing(30)
        
        # Información de usuario
        user_info = QLabel(f"Sesión de: {self.user_name}")
        user_info.setStyleSheet("color: rgba(255, 255, 255, 150); font-size: 10px;")
        user_info.setAlignment(Qt.AlignCenter)
        layout.addWidget(user_info)
        
        layout.addStretch()
        
        self.setLayout(layout)
        self.setStyleSheet("background-color: #1e3a5f;")
    
    def on_logout(self):
        self.parent_window.show_welcome()


class NewSportStageWidget(QWidget):
    """Pantalla de Crear Nueva Etapa Deportiva"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.init_ui()
    
    def init_ui(self):
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(60, 40, 60, 40)
        main_layout.setSpacing(20)
        
        # Header con rol
        header_layout = QHBoxLayout()
        header_label = QLabel("ADMIN")
        header_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold;")
        header_layout.addStretch()
        header_layout.addWidget(header_label)
        main_layout.addLayout(header_layout)
        
        # Título
        title = QLabel("NEW SPORT STAGE")
        title_font = QFont("Arial", 28, QFont.Bold)
        title.setFont(title_font)
        title.setStyleSheet("color: white;")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        main_layout.addSpacing(30)
        
        # Formulario con campos
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)
        form_layout.setAlignment(Qt.AlignCenter)
        form_layout.setContentsMargins(100, 0, 100, 0)
        
        # Name
        name_layout = QHBoxLayout()
        name_label = QLabel("Name")
        name_label.setStyleSheet("color: white; font-size: 13px; font-style: italic; min-width: 100px;")
        self.name_input = QLineEdit()
        self.name_input.setStyleSheet(self.get_input_style())
        self.name_input.setMinimumHeight(35)
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        form_layout.addLayout(name_layout)
        
        # Type
        type_layout = QHBoxLayout()
        type_label = QLabel("Type")
        type_label.setStyleSheet("color: white; font-size: 13px; font-style: italic; min-width: 100px;")
        self.type_input = QLineEdit()
        self.type_input.setStyleSheet(self.get_input_style())
        self.type_input.setMinimumHeight(35)
        type_layout.addWidget(type_label)
        type_layout.addWidget(self.type_input)
        form_layout.addLayout(type_layout)
        
        # Location
        location_layout = QHBoxLayout()
        location_label = QLabel("Location")
        location_label.setStyleSheet("color: white; font-size: 13px; font-style: italic; min-width: 100px;")
        self.location_input = QLineEdit()
        self.location_input.setStyleSheet(self.get_input_style())
        self.location_input.setMinimumHeight(35)
        location_layout.addWidget(location_label)
        location_layout.addWidget(self.location_input)
        form_layout.addLayout(location_layout)
        
        # Capacity
        capacity_layout = QHBoxLayout()
        capacity_label = QLabel("Capacity")
        capacity_label.setStyleSheet("color: white; font-size: 13px; font-style: italic; min-width: 100px;")
        self.capacity_input = QLineEdit()
        self.capacity_input.setStyleSheet(self.get_input_style())
        self.capacity_input.setMinimumHeight(35)
        capacity_layout.addWidget(capacity_label)
        capacity_layout.addWidget(self.capacity_input)
        form_layout.addLayout(capacity_layout)
        
        # Schedule
        schedule_layout = QHBoxLayout()
        schedule_label = QLabel("Schedule")
        schedule_label.setStyleSheet("color: white; font-size: 13px; font-style: italic; min-width: 100px;")
        self.schedule_input = QLineEdit()
        self.schedule_input.setPlaceholderText("YYYY-MM-DD HH:MM")
        self.schedule_input.setStyleSheet(self.get_input_style())
        self.schedule_input.setMinimumHeight(35)
        self.schedule_input.setReadOnly(True)
        schedule_layout.addWidget(schedule_label)
        schedule_layout.addWidget(self.schedule_input)
        
        schedule_btn = QPushButton("📅")
        schedule_btn.setFont(QFont("Arial", 14))
        schedule_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #1e3a5f;
                border: none;
                border-radius: 4px;
                padding: 5px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        schedule_btn.setMaximumWidth(50)
        schedule_btn.clicked.connect(self.open_calendar)
        schedule_layout.addWidget(schedule_btn)
        
        form_layout.addLayout(schedule_layout)
        
        main_layout.addLayout(form_layout)
        
        main_layout.addSpacing(30)
        
        # Botones
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)
        buttons_layout.setAlignment(Qt.AlignCenter)
        
        back_btn = QPushButton("Back")
        back_btn.setFont(QFont("Arial", 12, QFont.Bold))
        back_btn.setStyleSheet(self.get_button_style())
        back_btn.setMinimumWidth(120)
        back_btn.setMinimumHeight(40)
        back_btn.clicked.connect(self.on_back)
        buttons_layout.addWidget(back_btn)
        
        save_btn = QPushButton("Save")
        save_btn.setFont(QFont("Arial", 12, QFont.Bold))
        save_btn.setStyleSheet(self.get_button_style())
        save_btn.setMinimumWidth(120)
        save_btn.setMinimumHeight(40)
        save_btn.clicked.connect(self.on_save)
        buttons_layout.addWidget(save_btn)
        
        main_layout.addLayout(buttons_layout)
        
        main_layout.addStretch()
        
        self.setLayout(main_layout)
        self.setStyleSheet("background-color: #1e3a5f;")
    
    def on_save(self):
        name = self.name_input.text().strip()
        type_val = self.type_input.text().strip()
        location = self.location_input.text().strip()
        capacity = self.capacity_input.text().strip()
        schedule = self.schedule_input.text().strip()
        
        if not all([name, type_val, location, capacity, schedule]):
            show_styled_message(self, "Error", "Por favor completa todos los campos", "warning")
            return
        
        try:
            capacity_int = int(capacity)
        except ValueError:
            show_styled_message(self, "Error", "La capacidad debe ser un número", "warning")
            return
        
        # Guardar nueva etapa
        global STAGES_DB
        new_id = str(max([int(k) for k in STAGES_DB.keys()], default=0) + 1)
        
        STAGES_DB[new_id] = {
            'id': new_id,
            'name': name,
            'type': type_val,
            'location': location,
            'capacity': capacity,
            'schedule': schedule,
            'status': 'Active'
        }
        
        # Guardar en archivo
        save_stages_to_file(STAGES_DB)
        
        show_styled_message(self, "Éxito", f"Etapa deportiva '{name}' creada correctamente", "information")
        self.clear_fields()
        self.on_back()
    
    def on_back(self):
        self.parent_window.show_admin_dashboard()
    
    def open_calendar(self):
        """Abre el diálogo de calendario"""
        dialog = DateTimePickerDialog(self, self.schedule_input.text())
        if dialog.exec_() == QDialog.Accepted:
            selected_datetime = dialog.get_selected_datetime()
            if selected_datetime:
                self.schedule_input.setText(selected_datetime)
    
    def clear_fields(self):
        self.name_input.clear()
        self.type_input.clear()
        self.location_input.clear()
        self.capacity_input.clear()
        self.schedule_input.clear()
    
    @staticmethod
    def get_input_style():
        return """
            QLineEdit {
                background-color: transparent;
                border: 2px solid white;
                border-radius: 0px;
                padding: 8px;
                font-size: 12px;
                color: white;
            }
            QLineEdit::placeholder {
                color: rgba(255, 255, 255, 100);
            }
            QLineEdit:focus {
                outline: none;
                border: 2px solid #87CEEB;
            }
        """
    
    @staticmethod
    def get_button_style():
        return """
            QPushButton {
                background-color: white;
                color: #1e3a5f;
                border: none;
                border-radius: 20px;
                padding: 10px 30px;
                font-weight: bold;
                cursor: pointer;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """


class StagesInfoWidget(QWidget):
    """Pantalla de Información de Etapas Deportivas"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.selected_stage_id = None
        self.init_ui()
        self.load_stages()
    
    def init_ui(self):
        # Layout principal
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(30)
        
        # Panel izquierdo - Tabla de etapas
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        header_layout = QHBoxLayout()
        header_label = QLabel("ADMIN")
        header_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold;")
        header_layout.addStretch()
        header_layout.addWidget(header_label)
        left_layout.addLayout(header_layout)
        
        # Título
        title = QLabel("INFO SPORT STAGE")
        title_font = QFont("Arial", 24, QFont.Bold)
        title.setFont(title_font)
        title.setStyleSheet("color: white;")
        title.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(title)
        
        left_layout.addSpacing(20)
        
        # Subtítulo tabla
        info_label = QLabel("INFO STAGES")
        info_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold;")
        left_layout.addWidget(info_label)
        
        # Tabla
        self.table = self.create_table()
        left_layout.addWidget(self.table)
        
        left_panel.setLayout(left_layout)
        
        # Panel derecho - Edición
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_layout.setSpacing(15)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        # Título edición
        edit_title = QLabel("EDIT INFO")
        edit_title_font = QFont("Arial", 14, QFont.Bold)
        edit_title.setFont(edit_title_font)
        edit_title.setStyleSheet("color: white;")
        edit_title.setAlignment(Qt.AlignRight)
        right_layout.addWidget(edit_title)
        
        right_layout.addSpacing(15)
        
        # Formulario de edición
        # Name
        name_label = QLabel("Name")
        name_label.setStyleSheet("color: white; font-size: 12px; font-style: italic;")
        self.edit_name = QLineEdit()
        self.edit_name.setStyleSheet(self.get_input_style())
        self.edit_name.setMinimumHeight(30)
        right_layout.addWidget(name_label)
        right_layout.addWidget(self.edit_name)
        
        # Type
        type_label = QLabel("Type")
        type_label.setStyleSheet("color: white; font-size: 12px; font-style: italic;")
        self.edit_type = QLineEdit()
        self.edit_type.setStyleSheet(self.get_input_style())
        self.edit_type.setMinimumHeight(30)
        right_layout.addWidget(type_label)
        right_layout.addWidget(self.edit_type)
        
        # Location
        location_label = QLabel("Location")
        location_label.setStyleSheet("color: white; font-size: 12px; font-style: italic;")
        self.edit_location = QLineEdit()
        self.edit_location.setStyleSheet(self.get_input_style())
        self.edit_location.setMinimumHeight(30)
        right_layout.addWidget(location_label)
        right_layout.addWidget(self.edit_location)
        
        # Capacity
        capacity_label = QLabel("Capacity")
        capacity_label.setStyleSheet("color: white; font-size: 12px; font-style: italic;")
        self.edit_capacity = QLineEdit()
        self.edit_capacity.setStyleSheet(self.get_input_style())
        self.edit_capacity.setMinimumHeight(30)
        right_layout.addWidget(capacity_label)
        right_layout.addWidget(self.edit_capacity)
        
        # Schedule
        schedule_label = QLabel("Schedule")
        schedule_label.setStyleSheet("color: white; font-size: 12px; font-style: italic;")
        
        schedule_container = QHBoxLayout()
        self.edit_schedule = QLineEdit()
        self.edit_schedule.setStyleSheet(self.get_input_style())
        self.edit_schedule.setMinimumHeight(30)
        self.edit_schedule.setReadOnly(True)
        schedule_container.addWidget(self.edit_schedule)
        
        schedule_btn = QPushButton("📅")
        schedule_btn.setFont(QFont("Arial", 12))
        schedule_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #1e3a5f;
                border: none;
                border-radius: 4px;
                padding: 5px 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        schedule_btn.setMaximumWidth(45)
        schedule_btn.clicked.connect(self.open_calendar)
        schedule_container.addWidget(schedule_btn)
        
        right_layout.addWidget(schedule_label)
        right_layout.addLayout(schedule_container)
        
        right_layout.addSpacing(20)
        
        # Botones
        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(10)
        
        save_btn = QPushButton("Save")
        save_btn.setFont(QFont("Arial", 12, QFont.Bold))
        save_btn.setStyleSheet(self.get_button_style())
        save_btn.setMinimumHeight(35)
        save_btn.clicked.connect(self.on_save)
        buttons_layout.addWidget(save_btn)
        
        back_btn = QPushButton("Back")
        back_btn.setFont(QFont("Arial", 12, QFont.Bold))
        back_btn.setStyleSheet(self.get_button_style())
        back_btn.setMinimumHeight(35)
        back_btn.clicked.connect(self.on_back)
        buttons_layout.addWidget(back_btn)
        
        right_layout.addLayout(buttons_layout)
        right_layout.addStretch()
        
        right_panel.setLayout(right_layout)
        
        # Agregar paneles al layout principal
        main_layout.addWidget(left_panel, 2)
        main_layout.addWidget(right_panel, 1)
        
        self.setLayout(main_layout)
        self.setStyleSheet("background-color: #1e3a5f;")
    
    def create_table(self):
        """Crea la tabla de etapas"""
        table = QFrame()
        table_layout = QVBoxLayout()
        table_layout.setContentsMargins(0, 0, 0, 0)
        table_layout.setSpacing(0)
        
        # Header de la tabla
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid black;
            }
        """)
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(5, 5, 5, 5)
        header_layout.setSpacing(0)
        
        columns = ["Id", "Name", "Type", "Location", "Capacity", "Schedule", "Status"]
        for col in columns:
            label = QLabel(col)
            label.setStyleSheet("color: black; font-weight: bold; font-size: 11px;")
            label.setAlignment(Qt.AlignCenter)
            header_layout.addWidget(label)
        
        header.setLayout(header_layout)
        table_layout.addWidget(header)
        
        # Área para filas (scrollable)
        scroll_area = QFrame()
        scroll_layout = QVBoxLayout()
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(0)
        
        self.rows_container = QWidget()
        self.rows_layout = QVBoxLayout()
        self.rows_layout.setContentsMargins(0, 0, 0, 0)
        self.rows_layout.setSpacing(0)
        
        self.rows_container.setLayout(self.rows_layout)
        
        scroll = QVBoxLayout()
        scroll.addWidget(self.rows_container)
        scroll.addStretch()
        scroll_area.setLayout(scroll)
        
        table_layout.addWidget(scroll_area)
        
        table.setLayout(table_layout)
        return table
    
    def load_stages(self):
        """Carga las etapas de la base de datos"""
        global STAGES_DB
        
        # Limpiar filas anteriores
        while self.rows_layout.count():
            self.rows_layout.takeAt(0).widget().deleteLater()
        
        # Agregar filas
        for stage_id, stage in STAGES_DB.items():
            row = QFrame()
            row.setStyleSheet("""
                QFrame {
                    background-color: white;
                    border-bottom: 1px solid #ddd;
                }
            """)
            row.setCursor(Qt.PointingHandCursor)
            
            row_layout = QHBoxLayout()
            row_layout.setContentsMargins(5, 5, 5, 5)
            row_layout.setSpacing(0)
            
            # Datos de la fila
            data = [
                stage.get('id', ''),
                stage.get('name', ''),
                stage.get('type', ''),
                stage.get('location', ''),
                stage.get('capacity', ''),
                stage.get('schedule', ''),
                stage.get('status', '')
            ]
            
            for value in data:
                label = QLabel(str(value))
                label.setStyleSheet("color: black; font-size: 10px;")
                label.setAlignment(Qt.AlignCenter)
                row_layout.addWidget(label)
            
            row.setLayout(row_layout)
            
            # Conectar click a la selección
            row.mousePressEvent = lambda event, sid=stage_id: self.select_stage(sid)
            
            self.rows_layout.addWidget(row)
    
    def select_stage(self, stage_id):
        """Selecciona una etapa para editar"""
        self.selected_stage_id = stage_id
        stage = STAGES_DB.get(stage_id, {})
        
        self.edit_name.setText(stage.get('name', ''))
        self.edit_type.setText(stage.get('type', ''))
        self.edit_location.setText(stage.get('location', ''))
        self.edit_capacity.setText(stage.get('capacity', ''))
        self.edit_schedule.setText(stage.get('schedule', ''))
    
    def on_save(self):
        """Guarda los cambios en la etapa seleccionada"""
        global STAGES_DB
        
        if not self.selected_stage_id:
            show_styled_message(self, "Error", "Por favor selecciona una etapa", "warning")
            return
        
        name = self.edit_name.text().strip()
        type_val = self.edit_type.text().strip()
        location = self.edit_location.text().strip()
        capacity = self.edit_capacity.text().strip()
        schedule = self.edit_schedule.text().strip()
        
        if not all([name, type_val, location, capacity, schedule]):
            show_styled_message(self, "Error", "Por favor completa todos los campos", "warning")
            return
        
        # Actualizar etapa
        STAGES_DB[self.selected_stage_id].update({
            'name': name,
            'type': type_val,
            'location': location,
            'capacity': capacity,
            'schedule': schedule
        })
        
        # Guardar en archivo
        save_stages_to_file(STAGES_DB)
        
        show_styled_message(self, "Éxito", f"Etapa '{name}' actualizada correctamente", "information")
        self.load_stages()
    
    def on_back(self):
        """Vuelve al dashboard admin"""
        self.parent_window.show_admin_dashboard()
    
    def open_calendar(self):
        """Abre el diálogo de calendario"""
        dialog = DateTimePickerDialog(self, self.edit_schedule.text())
        if dialog.exec_() == QDialog.Accepted:
            selected_datetime = dialog.get_selected_datetime()
            if selected_datetime:
                self.edit_schedule.setText(selected_datetime)
    
    @staticmethod
    def get_input_style():
        return """
            QLineEdit {
                background-color: transparent;
                border: 2px solid white;
                border-radius: 0px;
                padding: 5px;
                font-size: 11px;
                color: white;
            }
            QLineEdit::placeholder {
                color: rgba(255, 255, 255, 100);
            }
            QLineEdit:focus {
                outline: none;
                border: 2px solid #87CEEB;
            }
        """
    
    @staticmethod
    def get_button_style():
        return """
            QPushButton {
                background-color: white;
                color: #1e3a5f;
                border: none;
                border-radius: 15px;
                padding: 8px 20px;
                font-weight: bold;
                cursor: pointer;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """


class DateTimePickerDialog(QDialog):
    """Diálogo para seleccionar fecha y hora"""
    def __init__(self, parent=None, initial_datetime=None):
        super().__init__(parent)
        self.setWindowTitle("Seleccionar Fecha y Hora")
        self.setGeometry(100, 100, 500, 450)
        self.setStyleSheet("background-color: #1e3a5f;")
        self.selected_datetime = None
        self.init_ui(initial_datetime)
    
    def init_ui(self, initial_datetime):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Título
        title = QLabel("Selecciona Fecha y Hora")
        title_font = QFont("Arial", 14, QFont.Bold)
        title.setFont(title_font)
        title.setStyleSheet("color: white;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        layout.addSpacing(10)
        
        # Calendario
        calendar_label = QLabel("Fecha:")
        calendar_label.setStyleSheet("color: white; font-size: 11px; font-weight: bold;")
        layout.addWidget(calendar_label)
        
        self.calendar = QCalendarWidget()
        self.calendar.setStyleSheet("""
            QCalendarWidget {
                background-color: white;
                color: black;
            }
            QCalendarWidget QWidget {
                background-color: white;
                color: black;
            }
            QCalendarWidget QAbstractButton {
                background-color: #87CEEB;
                color: white;
                font-weight: bold;
                border-radius: 3px;
            }
            QCalendarWidget QAbstractButton:hover {
                background-color: #5a9fb5;
            }
        """)
        
        # Si hay fecha inicial, usarla
        if initial_datetime:
            try:
                parts = initial_datetime.split(' ')
                date_parts = parts[0].split('-')
                self.calendar.setSelectedDate(QDate(int(date_parts[0]), int(date_parts[1]), int(date_parts[2])))
            except:
                self.calendar.setSelectedDate(QDate.currentDate())
        else:
            self.calendar.setSelectedDate(QDate.currentDate())
        
        layout.addWidget(self.calendar)
        
        layout.addSpacing(10)
        
        # Hora
        time_label = QLabel("Hora:")
        time_label.setStyleSheet("color: white; font-size: 11px; font-weight: bold;")
        layout.addWidget(time_label)
        
        time_layout = QHBoxLayout()
        time_layout.setSpacing(10)
        
        self.time_edit = QTimeEdit()
        self.time_edit.setStyleSheet("""
            QTimeEdit {
                background-color: white;
                color: black;
                border: 1px solid #ccc;
                padding: 5px;
                border-radius: 3px;
            }
        """)
        
        # Si hay hora inicial, usarla
        if initial_datetime:
            try:
                parts = initial_datetime.split(' ')
                if len(parts) > 1:
                    time_parts = parts[1].split(':')
                    self.time_edit.setTime(QTime(int(time_parts[0]), int(time_parts[1])))
            except:
                self.time_edit.setTime(QTime.currentTime())
        else:
            self.time_edit.setTime(QTime.currentTime())
        
        time_layout.addWidget(QLabel("Hora:"))
        time_layout.addWidget(self.time_edit)
        time_layout.addStretch()
        layout.addLayout(time_layout)
        
        layout.addSpacing(20)
        
        # Botones
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        accept_btn = QPushButton("Aceptar")
        accept_btn.setFont(QFont("Arial", 11, QFont.Bold))
        accept_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #1e3a5f;
                border: none;
                border-radius: 4px;
                padding: 10px 30px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        accept_btn.clicked.connect(self.accept_selection)
        buttons_layout.addStretch()
        buttons_layout.addWidget(accept_btn)
        
        cancel_btn = QPushButton("Cancelar")
        cancel_btn.setFont(QFont("Arial", 11, QFont.Bold))
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #666;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px 30px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #555;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
    
    def accept_selection(self):
        """Acepta la selección y cierra el diálogo"""
        date = self.calendar.selectedDate()
        time = self.time_edit.time()
        self.selected_datetime = date.toString("yyyy-MM-dd") + " " + time.toString("HH:mm")
        self.accept()
    
    def get_selected_datetime(self):
        """Retorna la fecha y hora seleccionada"""
        return self.selected_datetime


class NewEventsWidget(QWidget):
    """Pantalla de Crear Nuevos Eventos"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.init_ui()
    
    def init_ui(self):
        # Layout principal
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(60, 40, 60, 40)
        main_layout.setSpacing(80)
        
        # Panel izquierdo - Formulario
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(20)
        
        # Título
        title = QLabel("NEW EVENTS")
        title_font = QFont("Arial", 24, QFont.Bold)
        title.setFont(title_font)
        title.setStyleSheet("color: white;")
        title.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(title)
        
        left_layout.addSpacing(20)
        
        # Formulario
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)
        
        # Name
        name_label = QLabel("Name")
        name_label.setStyleSheet("color: white; font-size: 13px; font-style: italic;")
        self.name_input = QLineEdit()
        self.name_input.setStyleSheet(self.get_input_style())
        self.name_input.setMinimumHeight(35)
        form_layout.addWidget(name_label)
        form_layout.addWidget(self.name_input)
        
        # Schedule
        schedule_label = QLabel("Schedule")
        schedule_label.setStyleSheet("color: white; font-size: 13px; font-style: italic;")
        
        schedule_container = QHBoxLayout()
        self.schedule_input = QLineEdit()
        self.schedule_input.setPlaceholderText("YYYY-MM-DD HH:MM")
        self.schedule_input.setStyleSheet(self.get_input_style())
        self.schedule_input.setMinimumHeight(35)
        self.schedule_input.setReadOnly(True)
        schedule_container.addWidget(self.schedule_input)
        
        schedule_btn = QPushButton("📅")
        schedule_btn.setFont(QFont("Arial", 14))
        schedule_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #1e3a5f;
                border: none;
                border-radius: 4px;
                padding: 5px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        schedule_btn.setMaximumWidth(50)
        schedule_btn.clicked.connect(self.open_calendar)
        schedule_container.addWidget(schedule_btn)
        
        form_layout.addWidget(schedule_label)
        form_layout.addLayout(schedule_container)
        
        # Location
        location_label = QLabel("Location")
        location_label.setStyleSheet("color: white; font-size: 13px; font-style: italic;")
        self.location_input = QLineEdit()
        self.location_input.setStyleSheet(self.get_input_style())
        self.location_input.setMinimumHeight(35)
        form_layout.addWidget(location_label)
        form_layout.addWidget(self.location_input)
        
        # Capacity
        capacity_label = QLabel("Capacity")
        capacity_label.setStyleSheet("color: white; font-size: 13px; font-style: italic;")
        self.capacity_input = QLineEdit()
        self.capacity_input.setStyleSheet(self.get_input_style())
        self.capacity_input.setMinimumHeight(35)
        form_layout.addWidget(capacity_label)
        form_layout.addWidget(self.capacity_input)
        
        left_layout.addLayout(form_layout)
        left_layout.addSpacing(20)
        
        # Botones
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        
        back_btn = QPushButton("Back")
        back_btn.setFont(QFont("Arial", 12, QFont.Bold))
        back_btn.setStyleSheet(self.get_button_style())
        back_btn.setMinimumWidth(120)
        back_btn.setMinimumHeight(40)
        back_btn.clicked.connect(self.on_back)
        buttons_layout.addWidget(back_btn)
        
        save_btn = QPushButton("Save")
        save_btn.setFont(QFont("Arial", 12, QFont.Bold))
        save_btn.setStyleSheet(self.get_button_style())
        save_btn.setMinimumWidth(120)
        save_btn.setMinimumHeight(40)
        save_btn.clicked.connect(self.on_save)
        buttons_layout.addWidget(save_btn)
        
        left_layout.addLayout(buttons_layout)
        left_layout.addStretch()
        
        left_panel.setLayout(left_layout)
        
        # Panel derecho - Tabla de eventos
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(15)
        
        # Título
        info_title = QLabel("INFO EVENTS")
        info_title_font = QFont("Arial", 14, QFont.Bold)
        info_title.setFont(info_title_font)
        info_title.setStyleSheet("color: white;")
        info_title.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(info_title)
        
        # Tabla
        self.table = self.create_table()
        right_layout.addWidget(self.table)
        
        # Botón Delete
        delete_btn = QPushButton("Delete")
        delete_btn.setFont(QFont("Arial", 11, QFont.Bold))
        delete_btn.setStyleSheet(self.get_button_style())
        delete_btn.setMinimumHeight(35)
        delete_btn.clicked.connect(self.on_delete)
        right_layout.addWidget(delete_btn, alignment=Qt.AlignCenter)
        
        right_layout.addStretch()
        
        right_panel.setLayout(right_layout)
        
        # Agregar paneles
        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 1)
        
        self.setLayout(main_layout)
        self.setStyleSheet("background-color: #1e3a5f;")
        
        # Cargar eventos
        self.load_events()
        self.selected_event_id = None
    
    def create_table(self):
        """Crea la tabla de eventos"""
        table = QFrame()
        table_layout = QVBoxLayout()
        table_layout.setContentsMargins(0, 0, 0, 0)
        table_layout.setSpacing(0)
        
        # Header
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid black;
            }
        """)
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(5, 5, 5, 5)
        header_layout.setSpacing(0)
        
        columns = ["Name", "Schedule", "Location", "Capacity"]
        for col in columns:
            label = QLabel(col)
            label.setStyleSheet("color: black; font-weight: bold; font-size: 11px;")
            label.setAlignment(Qt.AlignCenter)
            header_layout.addWidget(label)
        
        header.setLayout(header_layout)
        table_layout.addWidget(header)
        
        # Filas
        scroll_area = QFrame()
        scroll_layout = QVBoxLayout()
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(0)
        
        self.rows_container = QWidget()
        self.rows_layout = QVBoxLayout()
        self.rows_layout.setContentsMargins(0, 0, 0, 0)
        self.rows_layout.setSpacing(0)
        
        self.rows_container.setLayout(self.rows_layout)
        
        scroll = QVBoxLayout()
        scroll.addWidget(self.rows_container)
        scroll.addStretch()
        scroll_area.setLayout(scroll)
        
        table_layout.addWidget(scroll_area)
        table.setLayout(table_layout)
        return table
    
    def load_events(self):
        """Carga los eventos en la tabla"""
        global EVENTS_DB
        
        # Limpiar filas
        while self.rows_layout.count():
            self.rows_layout.takeAt(0).widget().deleteLater()
        
        # Agregar filas
        for event_id, event in EVENTS_DB.items():
            row = QFrame()
            row.setStyleSheet("""
                QFrame {
                    background-color: white;
                    border-bottom: 1px solid #ddd;
                }
            """)
            row.setCursor(Qt.PointingHandCursor)
            
            row_layout = QHBoxLayout()
            row_layout.setContentsMargins(5, 5, 5, 5)
            row_layout.setSpacing(0)
            
            # Datos
            data = [
                event.get('name', ''),
                event.get('schedule', ''),
                event.get('location', ''),
                event.get('capacity', '')
            ]
            
            for value in data:
                label = QLabel(str(value))
                label.setStyleSheet("color: black; font-size: 10px;")
                label.setAlignment(Qt.AlignCenter)
                row_layout.addWidget(label)
            
            row.setLayout(row_layout)
            row.mousePressEvent = lambda event_obj, eid=event_id: self.select_event(eid)
            
            self.rows_layout.addWidget(row)
    
    def select_event(self, event_id):
        """Selecciona un evento"""
        self.selected_event_id = event_id
    
    def open_calendar(self):
        """Abre el diálogo de calendario"""
        dialog = DateTimePickerDialog(self, self.schedule_input.text())
        if dialog.exec_() == QDialog.Accepted:
            selected_datetime = dialog.get_selected_datetime()
            if selected_datetime:
                self.schedule_input.setText(selected_datetime)
    
    def on_save(self):
        """Guarda el nuevo evento"""
        global EVENTS_DB
        
        name = self.name_input.text().strip()
        schedule = self.schedule_input.text().strip()
        location = self.location_input.text().strip()
        capacity = self.capacity_input.text().strip()
        
        if not all([name, schedule, location, capacity]):
            show_styled_message(self, "Error", "Por favor completa todos los campos", "warning")
            return
        
        try:
            int(capacity)
        except ValueError:
            show_styled_message(self, "Error", "La capacidad debe ser un número", "warning")
            return
        
        # Crear nuevo evento
        new_id = str(max([int(k) for k in EVENTS_DB.keys()], default=0) + 1)
        EVENTS_DB[new_id] = {
            'id': new_id,
            'name': name,
            'schedule': schedule,
            'location': location,
            'capacity': capacity,
            'stage_id': '1'
        }
        
        # Guardar
        save_events_to_file(EVENTS_DB)
        
        show_styled_message(self, "Éxito", f"Evento '{name}' creado correctamente", "information")
        self.clear_fields()
        self.load_events()
    
    def on_delete(self):
        """Elimina el evento seleccionado"""
        global EVENTS_DB
        
        if not self.selected_event_id:
            show_styled_message(self, "Error", "Por favor selecciona un evento para eliminar", "warning")
            return
        
        event_name = EVENTS_DB[self.selected_event_id].get('name', '')
        
        # Diálogo de confirmación
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Confirmar eliminación")
        msg_box.setText(f"¿Estás seguro de que deseas eliminar el evento '{event_name}'?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QMessageBox QLabel {
                color: black;
                background-color: white;
                margin: 0px;
            }
            QMessageBox QAbstractButton {
                background-color: #1e3a5f;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 25px;
                min-width: 70px;
                font-weight: bold;
                margin: 0px 5px;
            }
            QMessageBox QAbstractButton:hover {
                background-color: white;
            }
            QMessageBox QAbstractButton:pressed {
                background-color: white;
            }
        """)
        
        reply = msg_box.exec_()
        
        if reply == QMessageBox.Yes:
            del EVENTS_DB[self.selected_event_id]
            save_events_to_file(EVENTS_DB)
            
            show_styled_message(self, "Éxito", f"Evento '{event_name}' eliminado correctamente", "information")
            self.selected_event_id = None
            self.load_events()
    
    def on_back(self):
        """Vuelve al dashboard"""
        self.parent_window.show_admin_dashboard()
    
    def clear_fields(self):
        """Limpia los campos del formulario"""
        self.name_input.clear()
        self.schedule_input.clear()
        self.location_input.clear()
        self.capacity_input.clear()
    
    @staticmethod
    def get_input_style():
        return """
            QLineEdit {
                background-color: transparent;
                border: 2px solid white;
                border-radius: 0px;
                padding: 8px;
                font-size: 12px;
                color: white;
            }
            QLineEdit::placeholder {
                color: rgba(255, 255, 255, 100);
            }
            QLineEdit:focus {
                outline: none;
                border: 2px solid #87CEEB;
            }
        """
    
    @staticmethod
    def get_button_style():
        return """
            QPushButton {
                background-color: white;
                color: #1e3a5f;
                border: none;
                border-radius: 20px;
                padding: 10px 30px;
                font-weight: bold;
                cursor: pointer;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """


class WelcomeWidget(QWidget):
    """Pantalla de Bienvenida"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(60, 60, 60, 60)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignCenter)
        
        # Título
        title = QLabel("SGED RANYAVE")
        title_font = QFont("Arial", 32, QFont.Bold)
        title.setFont(title_font)
        title.setStyleSheet("color: white;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Subtítulo
        subtitle = QLabel("¡Welcome to Ranyave!")
        subtitle_font = QFont("Arial", 14)
        subtitle.setFont(subtitle_font)
        subtitle.setStyleSheet("color: #87CEEB;")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        layout.addSpacing(40)
        
        # Botones
        login_btn = QPushButton("Iniciar Sesión")
        login_btn.setFont(QFont("Arial", 14, QFont.Bold))
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #1e3a5f;
                border: none;
                border-radius: 4px;
                padding: 15px;
                font-weight: bold;
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        login_btn.clicked.connect(self.parent_window.show_login)
        layout.addWidget(login_btn, alignment=Qt.AlignCenter)
        
        register_btn = QPushButton("Registrarse")
        register_btn.setFont(QFont("Arial", 14, QFont.Bold))
        register_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #1e3a5f;
                border: none;
                border-radius: 4px;
                padding: 15px;
                font-weight: bold;
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: #7dbad1;
            }
        """)
        register_btn.clicked.connect(self.parent_window.show_register)
        layout.addWidget(register_btn, alignment=Qt.AlignCenter)
        
        layout.addStretch()
        
        self.setLayout(layout)
        self.setStyleSheet("background-color: #1e3a5f;")


class MainWindow(QMainWindow):
    """Ventana Principal - Gestor de Pantallas"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SGED RANYAVE")
        self.setGeometry(100, 100, 1200, 700)
        
        # Stack de widgets
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Variable para guardar el dashboard actual
        self.current_admin_dashboard = None
        
        # Crear pantallas
        self.welcome_widget = WelcomeWidget(self)
        self.login_widget = LoginWidget(self)
        self.register_widget = RegisterWidget(self)
        
        self.stacked_widget.addWidget(self.welcome_widget)
        self.stacked_widget.addWidget(self.login_widget)
        self.stacked_widget.addWidget(self.register_widget)
        
        # Mostrar pantalla de bienvenida
        self.show_welcome()
        
        self.setStyleSheet("background-color: #1e3a5f;")
    
    def show_welcome(self):
        self.stacked_widget.setCurrentWidget(self.welcome_widget)
    
    def show_login(self):
        self.login_widget.clear_fields()
        self.stacked_widget.setCurrentWidget(self.login_widget)
    
    def show_register(self):
        self.register_widget.clear_fields()
        self.stacked_widget.setCurrentWidget(self.register_widget)
    
    def show_admin_dashboard(self):
        """Vuelve al dashboard admin actual"""
        if self.current_admin_dashboard:
            self.stacked_widget.setCurrentWidget(self.current_admin_dashboard)
    
    def login_user(self, name, role):
        if role == "admin":
            dashboard = AdminDashboard(name, self)
            self.current_admin_dashboard = dashboard
        else:
            dashboard = UserDashboard(name, self)
        
        self.stacked_widget.addWidget(dashboard)
        self.stacked_widget.setCurrentWidget(dashboard)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

class RanyaveLogin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("SGED RANYAVE")
        self.setGeometry(100, 100, 1200, 700)
        
        # Crear widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal horizontal
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # ===================================================================
        # PANEL IZQUIERDO - IMAGEN CUSTOM
        # ===================================================================
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_layout.setAlignment(Qt.AlignCenter)
        left_layout.setContentsMargins(40, 40, 40, 40)
        
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignCenter)
        
        # Intentar cargar imagen del usuario
        pixmap = self.load_image(IMAGE_PATH)
        if pixmap:
            image_label.setPixmap(pixmap)
            image_label.setScaledContents(False)
        else:
            # Imagen por defecto si no existe la ruta
            pixmap = self.create_default_logo()
            image_label.setPixmap(pixmap)
        
        left_layout.addWidget(image_label)
        left_panel.setLayout(left_layout)
        left_panel.setStyleSheet("background-color: #1e3a5f;")
        
        # ===================================================================
        # PANEL DERECHO - FORMULARIO
        # ===================================================================
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_layout.setSpacing(15)
        right_layout.setContentsMargins(60, 60, 60, 60)
        
        # Título
        title = QLabel("SGED RANYAVE")
        title_font = QFont("Arial", 24, QFont.Bold)
        title.setFont(title_font)
        title.setStyleSheet("color: white;")
        title.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(title)
        
        # Subtítulo
        subtitle = QLabel("¡Welcome to Ranyave!")
        subtitle_font = QFont("Arial", 13)
        subtitle.setFont(subtitle_font)
        subtitle.setStyleSheet("color: white;")
        subtitle.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(subtitle)
        
        # Espacio
        right_layout.addSpacing(20)
        
        # Label Usuario
        user_label = QLabel("Usuario")
        user_label.setStyleSheet("color: white; font-size: 11px; font-weight: bold;")
        right_layout.addWidget(user_label)
        
        # Input Usuario
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Ingresa tu usuario")
        self.username_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: none;
                border-radius: 4px;
                padding: 12px;
                font-size: 11px;
                color: #333;
            }
            QLineEdit:focus {
                outline: none;
                background-color: #f0f0f0;
            }
        """)
        self.username_input.setMinimumHeight(40)
        right_layout.addWidget(self.username_input)
        
        # Label Contraseña
        password_label = QLabel("Contraseña")
        password_label.setStyleSheet("color: white; font-size: 11px; font-weight: bold;")
        right_layout.addWidget(password_label)
        
        # Input Contraseña
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Ingresa tu contraseña")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: none;
                border-radius: 4px;
                padding: 12px;
                font-size: 11px;
                color: #333;
            }
            QLineEdit:focus {
                outline: none;
                background-color: #f0f0f0;
            }
        """)
        self.password_input.setMinimumHeight(40)
        right_layout.addWidget(self.password_input)
        
        # Espacio
        right_layout.addSpacing(15)
        
        # Botones
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        login_btn = QPushButton("Login")
        login_btn.setFont(QFont("Arial", 12, QFont.Bold))
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #1e3a5f;
                border: none;
                border-radius: 4px;
                padding: 12px 40px;
                font-weight: bold;
                cursor: pointer;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """)
        login_btn.clicked.connect(self.on_login)
        buttons_layout.addWidget(login_btn)
        
        register_btn = QPushButton("Register")
        register_btn.setFont(QFont("Arial", 12, QFont.Bold))
        register_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #1e3a5f;
                border: none;
                border-radius: 4px;
                padding: 12px 35px;
                font-weight: bold;
                cursor: pointer;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """)
        register_btn.clicked.connect(self.on_register)
        buttons_layout.addWidget(register_btn)
        
        buttons_layout.addStretch()
        right_layout.addLayout(buttons_layout)
        
        # Agregar stretch al final
        right_layout.addStretch()
        
        right_panel.setLayout(right_layout)
        right_panel.setStyleSheet("background-color: #1e3a5f;")
        
        # Agregar paneles al layout principal
        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 1)
        
        central_widget.setLayout(main_layout)
        
        # Aplicar estilo oscuro
        self.setStyleSheet("background-color: #1e3a5f;")
    
    def load_image(self, image_path):
        """Carga una imagen desde una ruta.
        
        Args:
            image_path (str): Ruta relativa o absoluta de la imagen
            
        Returns:
            QPixmap: Imagen escalada, o None si no existe
        """
        # Intentar cargar desde ruta relativa
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                # Escalar la imagen para que quepa en el panel
                return pixmap.scaledToHeight(500, Qt.SmoothTransformation)
        
        # Intentar cargar desde ruta absoluta relativa al directorio del script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        absolute_path = os.path.join(script_dir, image_path)
        
        if os.path.exists(absolute_path):
            pixmap = QPixmap(absolute_path)
            if not pixmap.isNull():
                return pixmap.scaledToHeight(500, Qt.SmoothTransformation)
        
        print(f"⚠ Imagen no encontrada en: {image_path}")
        print(f"   Rutas buscadas:")
        print(f"   - {image_path}")
        print(f"   - {absolute_path}")
        return None
    
    def create_default_logo(self):
        """Crea un logo por defecto si no se encuentra imagen"""
        size = 350
        img = Image.new('RGBA', (size, size), color=(30, 58, 95, 0))
        draw = ImageDraw.Draw(img)
        
        # Dibujar un logo de corredor estilizado
        head_radius = 35
        draw.ellipse([(150-head_radius, 50-head_radius), (150+head_radius, 50+head_radius)], fill='white')
        draw.line([(150, 85), (140, 150)], fill='white', width=8)
        draw.polygon([(140, 95), (90, 70), (110, 110)], fill='white')
        draw.polygon([(160, 95), (210, 70), (190, 110)], fill='white')
        draw.polygon([(140, 150), (120, 250), (135, 250)], fill='white')
        draw.polygon([(140, 150), (170, 240), (185, 240)], fill='white')
        
        # Convertir a QPixmap
        data = io.BytesIO()
        img.save(data, format='PNG')
        data.seek(0)
        
        pixmap = QPixmap()
        pixmap.loadFromData(data.getvalue())
        return pixmap.scaledToHeight(500, Qt.SmoothTransformation)
    
    def on_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if username and password:
            print(f"✓ Login exitoso: {username}")
            self.clear_fields()
        else:
            print("⚠ Por favor completa todos los campos")
    
    def on_register(self):
        print("→ Ir a pantalla de registro")
    
    def clear_fields(self):
        self.username_input.clear()
        self.password_input.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = RanyaveLogin()
    login_window.show()
    sys.exit(app.exec_())
