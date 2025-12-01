import sys
import os
import re
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, 
                             QVBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, 
                             QMessageBox, QStackedWidget, QTableWidget, QTableWidgetItem,
                             QHeaderView, QDialog, QFormLayout, QComboBox, QSpinBox,
                             QDateEdit, QTimeEdit, QDoubleSpinBox)
from PyQt5.QtGui import QFont, QColor, QPixmap, QPainter, QPen
from PyQt5.QtCore import Qt, QDate, QTime
from PIL import Image, ImageDraw
import io
import uuid  # Para generar IDs únicos
import database  # Importar módulo de base de datos

# ============================================================================
# CONFIGURACIÓN: Ruta de la imagen del lado izquierdo
# ============================================================================
IMAGE_PATH = "assets/logo_ranyave.png"  # Cambia esta ruta a tu imagen
# ============================================================================

# Inicializar base de datos
database.init_db()

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

class BasePage(QWidget):
    """Clase base para páginas con fondo decorado"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #1e3a5f;")

    def paintEvent(self, event):
        """Pinta el fondo con líneas decorativas"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Fondo azul
        painter.fillRect(self.rect(), QColor(30, 58, 95))
        
        # Líneas diagonales decorativas
        pen = QPen(QColor(255, 255, 255), 2)
        painter.setPen(pen)
        
        w = self.width()
        h = self.height()
        
        # Líneas estilo "Ranyave" (diagonales desde las esquinas)
        # Esquina superior izquierda
        painter.drawLine(0, 100, 100, 0)
        painter.drawLine(0, 200, 200, 0)
        
        # Esquina inferior derecha
        painter.drawLine(w, h-100, w-100, h)
        painter.drawLine(w, h-200, w-200, h)
        
        # Esquina superior derecha
        painter.drawLine(w, 100, w-100, 0)
        
        # Esquina inferior izquierda
        painter.drawLine(0, h-100, 100, h)

    @staticmethod
    def get_input_style():
        return """
            QLineEdit, QComboBox, QDateEdit, QTimeEdit, QSpinBox {
                background-color: transparent;
                border: 2px solid white;
                border-radius: 0px;
                padding: 8px;
                font-size: 16px;
                color: white;
                font-family: Arial;
            }
            QLineEdit::placeholder {
                color: rgba(255, 255, 255, 180);
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 2px solid white;
                border-top: 2px solid white;
                width: 10px;
                height: 10px;
                margin-right: 10px;
                transform: rotate(45deg);
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
                font-size: 14px;
                font-family: Arial;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """
    
    @staticmethod
    def get_label_style():
        return "color: white; font-size: 18px; font-family: Arial; font-weight: bold;"

class LoginWidget(BasePage):
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
        # left_panel.setStyleSheet("background-color: #1e3a5f;") # Ya no es necesario, BasePage lo maneja
        
        # Panel derecho (formulario)
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_layout.setSpacing(20)
        right_layout.setContentsMargins(80, 60, 80, 60)
        
        # Título
        title = QLabel("LOGIN")
        title_font = QFont("Arial", 36, QFont.Bold)
        title.setFont(title_font)
        title.setStyleSheet("color: white;")
        title.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(title)
        
        right_layout.addSpacing(40)
        
        # Email/Usuario
        email_label = QLabel("Email")
        email_label.setStyleSheet(self.get_label_style())
        right_layout.addWidget(email_label)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("")
        self.email_input.setStyleSheet(self.get_input_style())
        self.email_input.setMinimumHeight(45)
        right_layout.addWidget(self.email_input)
        
        # Contraseña
        password_label = QLabel("Password")
        password_label.setStyleSheet(self.get_label_style())
        right_layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(self.get_input_style())
        self.password_input.setMinimumHeight(45)
        right_layout.addWidget(self.password_input)
        
        right_layout.addSpacing(30)
        
        # Botones
        buttons_layout = QVBoxLayout() # Cambiado a vertical para coincidir más con el estilo general
        buttons_layout.setSpacing(15)
        buttons_layout.setAlignment(Qt.AlignCenter)
        
        next_btn = QPushButton("Next")
        next_btn.setStyleSheet(self.get_button_style())
        next_btn.setMinimumWidth(150)
        next_btn.setMinimumHeight(45)
        next_btn.clicked.connect(self.on_login)
        buttons_layout.addWidget(next_btn)
        
        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(self.get_button_style())
        back_btn.setMinimumWidth(150)
        back_btn.setMinimumHeight(45)
        back_btn.clicked.connect(self.on_back)
        buttons_layout.addWidget(back_btn)
        
        right_layout.addLayout(buttons_layout)
        
        right_layout.addSpacing(20)
        
        # Link a registro
        register_label = QLabel("¿No tienes cuenta? <a href='#' style='color: white; text-decoration: underline;'><b>Regístrate aquí</b></a>")
        register_label.setStyleSheet("color: white; font-size: 12px;")
        register_label.setAlignment(Qt.AlignCenter)
        register_label.linkActivated.connect(self.on_register_link)
        right_layout.addWidget(register_label)
        
        right_layout.addStretch()
        
        right_panel.setLayout(right_layout)
        
        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 1)
        
        self.setLayout(main_layout)

    
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
        user = database.get_user(email)
        if user and user["password"] == password:
            # Login exitoso
            role = user["role"]
            name = user["name"]
            self.parent_window.login_user(name, role)
            return
        
        show_styled_message(self, "Error", "Email o contraseña incorrectos", "warning")
        self.clear_fields()
    
    def on_back(self):
        self.parent_window.show_welcome()
    
    def on_register_link(self):
        self.parent_window.show_register()
    
    def is_valid_email(self, email):
        if email in ["123", "1234"]: return True
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
                font-size: 16px;
                color: white;
                font-family: Arial;
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
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """


class RegisterWidget(BasePage):
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
        # left_panel.setStyleSheet("background-color: #1e3a5f;") # BasePage
        
        # Panel derecho (formulario)
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_layout.setSpacing(15)
        right_layout.setContentsMargins(80, 40, 80, 40)
        
        # Título
        title = QLabel("REGISTER")
        title_font = QFont("Arial", 36, QFont.Bold)
        title.setFont(title_font)
        title.setStyleSheet("color: white;")
        title.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(title)
        
        right_layout.addSpacing(20)
        
        # Nombre
        name_label = QLabel("Name")
        name_label.setStyleSheet(self.get_label_style())
        right_layout.addWidget(name_label)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("")
        self.name_input.setStyleSheet(self.get_input_style())
        self.name_input.setMinimumHeight(40)
        right_layout.addWidget(self.name_input)
        
        # Email
        email_label = QLabel("Email")
        email_label.setStyleSheet(self.get_label_style())
        right_layout.addWidget(email_label)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("")
        self.email_input.setStyleSheet(self.get_input_style())
        self.email_input.setMinimumHeight(40)
        right_layout.addWidget(self.email_input)
        
        # Teléfono
        phone_label = QLabel("Cell Phone Number")
        phone_label.setStyleSheet(self.get_label_style())
        right_layout.addWidget(phone_label)
        
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("")
        self.phone_input.setStyleSheet(self.get_input_style())
        self.phone_input.setMinimumHeight(40)
        right_layout.addWidget(self.phone_input)
        
        # Contraseña
        password_label = QLabel("Password")
        password_label.setStyleSheet(self.get_label_style())
        right_layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(self.get_input_style())
        self.password_input.setMinimumHeight(40)
        right_layout.addWidget(self.password_input)
        
        right_layout.addSpacing(20)
        
        # Botones
        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(15)
        buttons_layout.setAlignment(Qt.AlignCenter)
        
        next_btn = QPushButton("Next")
        next_btn.setStyleSheet(self.get_button_style())
        next_btn.setMinimumWidth(150)
        next_btn.setMinimumHeight(45)
        next_btn.clicked.connect(self.on_register)
        buttons_layout.addWidget(next_btn)
        
        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(self.get_button_style())
        back_btn.setMinimumWidth(150)
        back_btn.setMinimumHeight(45)
        back_btn.clicked.connect(self.on_back)
        buttons_layout.addWidget(back_btn)
        
        right_layout.addLayout(buttons_layout)
        
        right_layout.addStretch()
        
        right_panel.setLayout(right_layout)
        
        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 1)
        
        self.setLayout(main_layout)
    
    def on_register(self):
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
        
        if len(password) < 6 and password != "123":
            show_styled_message(self, "Error", "La contraseña debe tener al menos 6 caracteres", "warning")
            return
        
        if database.get_user(email):
            show_styled_message(self, "Error", "Este email ya está registrado", "warning")
            return
        
        # Registrar usuario
        if database.create_user(email, name, phone, password, "user"):
            show_styled_message(self, "Éxito", f"¡Bienvenido {name}!\nTu registro fue completado. Ahora puedes iniciar sesión.", "information")
            self.clear_fields()
            self.parent_window.show_login()
        else:
            show_styled_message(self, "Error", "Error al registrar usuario", "error")
    
    def on_back(self):
        self.parent_window.show_login()
    
    def is_valid_email(self, email):
        if email in ["123", "1234"]: return True
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
                font-size: 16px;
                color: white;
                font-family: Arial;
            }
            QLineEdit::placeholder {
                color: rgba(255, 255, 255, 150);
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
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """


class AdminDashboard(BasePage):
    """Panel de Administrador"""
    def __init__(self, user_name, parent=None):
        super().__init__(parent)
        self.user_name = user_name
        self.parent_window = parent
        self.init_ui()
    
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
        new_stages_btn.setStyleSheet(self.get_button_style())
        new_stages_btn.setMinimumWidth(250)
        new_stages_btn.clicked.connect(self.on_new_stages)
        center_layout.addWidget(new_stages_btn, alignment=Qt.AlignCenter)
        
        # Botón STAGES INFO
        stages_info_btn = QPushButton("STAGES INFO")
        stages_info_btn.setStyleSheet(self.get_button_style())
        stages_info_btn.setMinimumWidth(250)
        stages_info_btn.clicked.connect(self.on_stages_info)
        center_layout.addWidget(stages_info_btn, alignment=Qt.AlignCenter)
        
        # Botón RESERVATIONS
        reservations_btn = QPushButton("RESERVATIONS")
        reservations_btn.setStyleSheet(self.get_button_style())
        reservations_btn.setMinimumWidth(250)
        reservations_btn.clicked.connect(self.on_reservations)
        center_layout.addWidget(reservations_btn, alignment=Qt.AlignCenter)
        
        # Botón Back to login
        back_btn = QPushButton("Back to login")
        back_btn.setStyleSheet(self.get_button_style())
        back_btn.setMinimumWidth(250)
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

    
    def on_new_stages(self):
        dialog = VenueForm(self)
        if dialog.exec_():
            show_styled_message(self, "Éxito", "Escenario registrado correctamente", "information")
    
    def on_stages_info(self):
        dialog = VenuesListDialog(self)
        dialog.exec_()
    
    def on_reservations(self):
        dialog = AdminReservationsDialog(self)
        dialog.exec_()
    
    def on_logout(self):
        self.parent_window.show_welcome()

class BaseDialog(QDialog):
    """Diálogo base con estilo"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #1e3a5f; color: white;")
    
    def paintEvent(self, event):
        """Pinta el fondo con líneas decorativas"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Fondo azul
        painter.fillRect(self.rect(), QColor(30, 58, 95))
        
        # Líneas diagonales decorativas
        pen = QPen(QColor(255, 255, 255), 2)
        painter.setPen(pen)
        
        w = self.width()
        h = self.height()
        
        # Líneas estilo "Ranyave"
        painter.drawLine(0, 50, 50, 0)
        painter.drawLine(w, h-50, w-50, h)

    @staticmethod
    def get_input_style():
        return """
            QLineEdit, QComboBox, QDateEdit, QTimeEdit, QSpinBox {
                background-color: transparent;
                border: 2px solid white;
                border-radius: 0px;
                padding: 8px;
                font-size: 14px;
                color: white;
                font-family: Arial;
            }
            QLineEdit::placeholder {
                color: rgba(255, 255, 255, 180);
            }
            QComboBox QAbstractItemView {
                background-color: #1e3a5f;
                color: white;
                selection-background-color: #4a90e2;
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
                font-size: 14px;
                font-family: Arial;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """
    
    @staticmethod
    def get_label_style():
        return "color: white; font-size: 14px; font-family: Arial; font-weight: bold;"

class VenueForm(BaseDialog):
    """Formulario para crear/editar escenarios"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("NEW SPORT STAGE")
        self.setMinimumWidth(600)
        self.setMinimumHeight(700)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 40, 50, 40)
        layout.setSpacing(25)
        
        # Title
        title = QLabel("NEW SPORT STAGE")
        title.setFont(QFont("Arial", 28, QFont.Bold))
        title.setStyleSheet("color: white;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Complete all fields to create a new sport stage")
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 200); font-size: 12px;")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        layout.addSpacing(15)
        
        # Separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("color: rgba(255, 255, 255, 100);")
        layout.addWidget(separator)
        
        layout.addSpacing(15)
        
        # Form with improved styling
        form_layout = QFormLayout()
        form_layout.setSpacing(18)
        form_layout.setLabelAlignment(Qt.AlignLeft)
        form_layout.setHorizontalSpacing(25)
        
        # Name
        name_label = QLabel("📋 Venue Name")
        name_label.setStyleSheet("color: white; font-size: 14px; font-family: Arial; font-weight: bold;")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g., Football Field A")
        self.name_input.setStyleSheet(self.get_input_style())
        self.name_input.setMinimumHeight(40)
        form_layout.addRow(name_label, self.name_input)
        
        # Type
        type_label = QLabel("⚽ Type")
        type_label.setStyleSheet("color: white; font-size: 14px; font-family: Arial; font-weight: bold;")
        self.type_input = QComboBox()
        self.type_input.addItems(["Fútbol", "Baloncesto", "Tenis", "Voleibol", "Natación", "Otro"])
        self.type_input.setStyleSheet(self.get_input_style())
        self.type_input.setMinimumHeight(40)
        form_layout.addRow(type_label, self.type_input)
        
        # Location
        loc_label = QLabel("📍 Location")
        loc_label.setStyleSheet("color: white; font-size: 14px; font-family: Arial; font-weight: bold;")
        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText("e.g., Zone B, Building 3")
        self.location_input.setStyleSheet(self.get_input_style())
        self.location_input.setMinimumHeight(40)
        form_layout.addRow(loc_label, self.location_input)
        
        # Capacity
        cap_label = QLabel("👥 Capacity")
        cap_label.setStyleSheet("color: white; font-size: 14px; font-family: Arial; font-weight: bold;")
        self.capacity_input = QSpinBox()
        self.capacity_input.setRange(1, 100000)
        self.capacity_input.setValue(50)
        self.capacity_input.setStyleSheet(self.get_input_style())
        self.capacity_input.setMinimumHeight(40)
        form_layout.addRow(cap_label, self.capacity_input)
        
        # Schedule - Date
        sch_label = QLabel("📅 Schedule Date")
        sch_label.setStyleSheet("color: white; font-size: 14px; font-family: Arial; font-weight: bold;")
        self.schedule_date = QDateEdit()
        self.schedule_date.setCalendarPopup(True)
        self.schedule_date.setDate(QDate.currentDate())
        self.schedule_date.setStyleSheet(self.get_input_style())
        self.schedule_date.setMinimumHeight(40)
        form_layout.addRow(sch_label, self.schedule_date)
        
        # Schedule - Time
        time_label = QLabel("🕐 Schedule Time")
        time_label.setStyleSheet("color: white; font-size: 14px; font-family: Arial; font-weight: bold;")
        self.schedule_time = QTimeEdit()
        self.schedule_time.setTime(QTime(12, 0))
        self.schedule_time.setStyleSheet(self.get_input_style())
        self.schedule_time.setMinimumHeight(40)
        form_layout.addRow(time_label, self.schedule_time)
        
        # Price
        price_label = QLabel("💵 Price ($)")
        price_label.setStyleSheet("color: white; font-size: 14px; font-family: Arial; font-weight: bold;")
        self.price_input = QDoubleSpinBox()
        self.price_input.setRange(0.0, 100000.0)
        self.price_input.setDecimals(2)
        self.price_input.setSingleStep(10.0)
        self.price_input.setValue(50.0)
        self.price_input.setStyleSheet(self.get_input_style())
        self.price_input.setMinimumHeight(40)
        form_layout.addRow(price_label, self.price_input)
        
        layout.addLayout(form_layout)
        
        layout.addSpacing(25)
        
        # Separator line
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.HLine)
        separator2.setFrameShadow(QFrame.Sunken)
        separator2.setStyleSheet("color: rgba(255, 255, 255, 100);")
        layout.addWidget(separator2)
        
        layout.addSpacing(15)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(20)
        btn_layout.setAlignment(Qt.AlignCenter)
        
        back_btn = QPushButton("Cancel")
        back_btn.setStyleSheet(self.get_button_style())
        back_btn.setMinimumWidth(150)
        back_btn.setMinimumHeight(45)
        back_btn.setFont(QFont("Arial", 12, QFont.Bold))
        back_btn.clicked.connect(self.reject)
        btn_layout.addWidget(back_btn)
        
        save_btn = QPushButton("Save Stage")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                border: 1px solid #45a049;
                padding: 10px 20px;
                font-weight: bold;
                min-width: 150px;
                min-height: 45px;
                border-radius: 5px;
                color: white;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        save_btn.setFont(QFont("Arial", 12, QFont.Bold))
        save_btn.clicked.connect(self.save_venue)
        btn_layout.addWidget(save_btn)
        
        layout.addLayout(btn_layout)
        
        layout.addStretch()
        
        self.setLayout(layout)
        
    def save_venue(self):
        name = self.name_input.text().strip()
        venue_type = self.type_input.currentText()
        capacity = self.capacity_input.value()
        location = self.location_input.text().strip()
        price = float(self.price_input.value())
        
        # Obtener fecha y hora del calendario y reloj de tiempo
        date_str = self.schedule_date.date().toString("yyyy-MM-dd")
        time_str = self.schedule_time.time().toString("HH:mm")
        schedule = f"{date_str} {time_str}"
        
        if not name or not location:
            QMessageBox.warning(self, "Error", "Por favor completa todos los campos")
            return
            
        venue_id = str(uuid.uuid4())
        venue_data = {
            "id": venue_id,
            "name": name,
            "type": venue_type,
            "capacity": capacity,
            "location": location,
            "schedule": schedule,
            "price": price,
            "status": "active"
        }
        
        try:
            database.save_venue(venue_data)
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error saving venue: {str(e)}")
            print(f"Error details: {e}")
            import traceback
            traceback.print_exc()

class VenuesListDialog(BaseDialog):
    """Diálogo para ver lista de escenarios"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("INFO SPORT STAGE")
        self.setMinimumSize(1400, 700)
        self.init_ui()
        
    def init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(25)
        
        # Left side: Table
        left_layout = QVBoxLayout()
        left_layout.setSpacing(15)
        
        title = QLabel("📋 ALL SPORT STAGES")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setStyleSheet("color: white;")
        title.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Click on a stage to edit or delete")
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 200); font-size: 11px;")
        subtitle.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(subtitle)
        
        # Separator
        separator1 = QFrame()
        separator1.setFrameShape(QFrame.HLine)
        separator1.setFrameShadow(QFrame.Sunken)
        separator1.setStyleSheet("color: rgba(255, 255, 255, 100);")
        left_layout.addWidget(separator1)
        
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["Id", "Name", "Type", "Location", "Capacity", "Schedule", "Price"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Mejorar el styling de la tabla
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #f5f5f5;
                color: #333;
                gridline-color: #ddd;
                border: 1px solid #ccc;
                border-radius: 4px;
                selection-background-color: #4a90e2;
            }
            QTableWidget::item {
                padding: 8px;
                border: none;
            }
            QTableWidget::item:selected {
                background-color: #4a90e2;
                color: white;
                font-weight: bold;
            }
            QHeaderView::section {
                background-color: #2c3e50;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
                font-size: 12px;
                text-align: center;
            }
            QHeaderView::section:hover {
                background-color: #34495e;
            }
        """)
        
        # Configurar altura de filas
        self.table.verticalHeader().setDefaultSectionSize(45)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        
        # Ocultar números de fila
        self.table.verticalHeader().setVisible(False)
        
        self.table.itemClicked.connect(self.on_table_click)
        left_layout.addWidget(self.table)
        
        layout.addLayout(left_layout, 1)
        
        # Right side: Edit Form
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(25, 25, 25, 25)
        right_layout.setSpacing(15)
        
        # Frame para el formulario
        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
            }
        """)
        form_frame_layout = QVBoxLayout()
        form_frame_layout.setContentsMargins(20, 20, 20, 20)
        form_frame_layout.setSpacing(15)
        
        edit_title = QLabel("✏️ EDIT STAGE INFO")
        edit_title.setFont(QFont("Arial", 20, QFont.Bold))
        edit_title.setStyleSheet("color: white;")
        edit_title.setAlignment(Qt.AlignCenter)
        form_frame_layout.addWidget(edit_title)
        
        # Separator
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.HLine)
        separator2.setFrameShadow(QFrame.Sunken)
        separator2.setStyleSheet("color: rgba(255, 255, 255, 100);")
        form_frame_layout.addWidget(separator2)
        
        form_layout = QFormLayout()
        form_layout.setSpacing(16)
        form_layout.setHorizontalSpacing(15)
        
        # Name
        self.edit_name = QLineEdit()
        self.edit_name.setStyleSheet(self.get_input_style())
        self.edit_name.setMinimumHeight(35)
        name_label = QLabel("📋 Venue Name")
        name_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold;")
        form_layout.addRow(name_label, self.edit_name)
        
        # Type
        self.edit_type = QLineEdit()
        self.edit_type.setStyleSheet(self.get_input_style())
        self.edit_type.setMinimumHeight(35)
        type_label = QLabel("⚽ Type")
        type_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold;")
        form_layout.addRow(type_label, self.edit_type)
        
        # Location
        self.edit_location = QLineEdit()
        self.edit_location.setStyleSheet(self.get_input_style())
        self.edit_location.setMinimumHeight(35)
        location_label = QLabel("📍 Location")
        location_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold;")
        form_layout.addRow(location_label, self.edit_location)
        
        # Capacity
        self.edit_capacity = QLineEdit()
        self.edit_capacity.setStyleSheet(self.get_input_style())
        self.edit_capacity.setMinimumHeight(35)
        capacity_label = QLabel("👥 Capacity")
        capacity_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold;")
        form_layout.addRow(capacity_label, self.edit_capacity)
        
        # Schedule Date
        self.edit_schedule_date = QDateEdit()
        self.edit_schedule_date.setCalendarPopup(True)
        self.edit_schedule_date.setStyleSheet(self.get_input_style())
        self.edit_schedule_date.setMinimumHeight(35)
        date_label = QLabel("📅 Schedule Date")
        date_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold;")
        form_layout.addRow(date_label, self.edit_schedule_date)
        
        # Schedule Time
        self.edit_schedule_time = QTimeEdit()
        self.edit_schedule_time.setStyleSheet(self.get_input_style())
        self.edit_schedule_time.setMinimumHeight(35)
        time_label = QLabel("🕐 Schedule Time")
        time_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold;")
        form_layout.addRow(time_label, self.edit_schedule_time)
        
        # Price
        self.edit_price = QDoubleSpinBox()
        self.edit_price.setRange(0.0, 100000.0)
        self.edit_price.setDecimals(2)
        self.edit_price.setSingleStep(10.0)
        self.edit_price.setStyleSheet(self.get_input_style())
        self.edit_price.setMinimumHeight(35)
        price_label = QLabel("💵 Price ($)")
        price_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold;")
        form_layout.addRow(price_label, self.edit_price)
        
        right_layout.addLayout(form_layout)
        
        right_layout.addSpacing(20)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)
        btn_layout.setAlignment(Qt.AlignCenter)
        
        back_btn = QPushButton("Cancel")
        back_btn.setStyleSheet(self.get_button_style())
        back_btn.setMinimumWidth(120)
        back_btn.setMinimumHeight(40)
        back_btn.clicked.connect(self.accept)
        btn_layout.addWidget(back_btn)
        
        save_btn = QPushButton("Save Changes")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                border: 1px solid #45a049;
                padding: 8px 16px;
                font-weight: bold;
                min-width: 120px;
                min-height: 40px;
                border-radius: 4px;
                color: white;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        save_btn.clicked.connect(self.save_changes)
        btn_layout.addWidget(save_btn)
        
        delete_btn = QPushButton("Delete")
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                border: 1px solid #d32f2f;
                padding: 8px 16px;
                font-weight: bold;
                min-width: 120px;
                min-height: 40px;
                border-radius: 4px;
                color: white;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        delete_btn.clicked.connect(self.delete_venue)
        btn_layout.addWidget(delete_btn)
        
        right_layout.addLayout(btn_layout)
        
        right_layout.addStretch()
        
        layout.addLayout(right_layout, 1)
        
        self.load_data()
        self.setLayout(layout)
        
        self.current_venue_id = None
        
    def load_data(self):
        self.venues = database.get_all_venues()
        self.table.setRowCount(len(self.venues))
        
        for i, (venue_id, venue) in enumerate(self.venues.items()):
            self.table.setItem(i, 0, QTableWidgetItem(venue.get("id", "")[:8])) # Short ID
            self.table.setItem(i, 1, QTableWidgetItem(venue["name"]))
            self.table.setItem(i, 2, QTableWidgetItem(venue["type"]))
            self.table.setItem(i, 3, QTableWidgetItem(venue["location"]))
            self.table.setItem(i, 4, QTableWidgetItem(str(venue["capacity"])))
            self.table.setItem(i, 5, QTableWidgetItem(venue.get("schedule", "")))
            
            # Price
            price = float(venue.get("price", 0.0))
            self.table.setItem(i, 6, QTableWidgetItem(f"${price:.2f}"))
            
            # Store full ID in first item data
            self.table.item(i, 0).setData(Qt.UserRole, venue_id)
            
    def on_table_click(self, item):
        row = item.row()
        venue_id = self.table.item(row, 0).data(Qt.UserRole)
        self.current_venue_id = venue_id
        venue = self.venues[venue_id]
        
        self.edit_name.setText(venue["name"])
        self.edit_type.setText(venue["type"])
        self.edit_location.setText(venue["location"])
        self.edit_capacity.setText(str(venue["capacity"]))
        
        try:
            price_value = float(venue.get("price", 0.0))
        except (ValueError, TypeError):
            price_value = 0.0
        self.edit_price.setValue(price_value)
        
        # Parsear la fecha y hora desde el formato guardado
        schedule = venue.get("schedule", "")
        if schedule:
            try:
                parts = schedule.split(" ")
                if len(parts) >= 2:
                    date_part = parts[0]  # YYYY-MM-DD
                    time_part = parts[1]  # HH:mm
                    self.edit_schedule_date.setDate(QDate.fromString(date_part, "yyyy-MM-dd"))
                    self.edit_schedule_time.setTime(QTime.fromString(time_part, "HH:mm"))
                else:
                    self.edit_schedule_date.setDate(QDate.currentDate())
                    self.edit_schedule_time.setTime(QTime(12, 0))
            except:
                self.edit_schedule_date.setDate(QDate.currentDate())
                self.edit_schedule_time.setTime(QTime(12, 0))
        else:
            self.edit_schedule_date.setDate(QDate.currentDate())
            self.edit_schedule_time.setTime(QTime(12, 0))
        
    def save_changes(self):
        if not self.current_venue_id:
            return
            
        # Obtener fecha y hora del calendario y reloj de tiempo
        date_str = self.edit_schedule_date.date().toString("yyyy-MM-dd")
        time_str = self.edit_schedule_time.time().toString("HH:mm")
        schedule = f"{date_str} {time_str}"
        
        self.venues[self.current_venue_id]["name"] = self.edit_name.text()
        self.venues[self.current_venue_id]["type"] = self.edit_type.text()
        self.venues[self.current_venue_id]["location"] = self.edit_location.text()
        self.venues[self.current_venue_id]["price"] = float(self.edit_price.value())
        try:
            self.venues[self.current_venue_id]["capacity"] = int(self.edit_capacity.text())
        except:
            pass
        self.venues[self.current_venue_id]["schedule"] = schedule
        
        try:
            database.save_venue(self.venues[self.current_venue_id])
            self.load_data()
            QMessageBox.information(self, "Success", "Changes saved!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error saving changes: {str(e)}")
            print(f"Error details: {e}")
            import traceback
            traceback.print_exc()
    
    def delete_venue(self):
        if not self.current_venue_id:
            QMessageBox.warning(self, "Warning", "Please select a venue to delete")
            return
        
        venue_name = self.venues[self.current_venue_id]["name"]
        
        # Confirmar eliminación
        reply = QMessageBox.question(
            self, 
            'Confirm Deletion', 
            f'Are you sure you want to delete "{venue_name}"?\n\nThis action cannot be undone.',
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                database.delete_venue(self.current_venue_id)
                self.load_data()
                QMessageBox.information(self, "Success", f"Venue '{venue_name}' has been deleted!")
                self.current_venue_id = None
                # Limpiar los campos del formulario
                self.edit_name.clear()
                self.edit_type.clear()
                self.edit_location.clear()
                self.edit_capacity.clear()
                self.edit_price.setValue(0.0)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error deleting venue: {str(e)}")
                print(f"Error details: {e}")
                import traceback
                traceback.print_exc()


class UserDashboard(BasePage):
    """Panel de Usuario Normal"""
    def __init__(self, user_name, parent=None):
        super().__init__(parent)
        self.user_name = user_name
        self.parent_window = parent
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
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
        
        # Sección central con botones (Primera fila)
        center_layout = QHBoxLayout()
        center_layout.setSpacing(40)
        center_layout.setAlignment(Qt.AlignCenter)
        
        # Botón RESERVE
        reserve_btn = QPushButton("RESERVE")
        reserve_btn.setStyleSheet(self.get_button_style())
        reserve_btn.setMinimumWidth(200)
        reserve_btn.clicked.connect(self.on_reserve)
        center_layout.addWidget(reserve_btn)
        
        # Botón RESERVATIONS
        reservations_btn = QPushButton("RESERVATIONS")
        reservations_btn.setStyleSheet(self.get_button_style())
        reservations_btn.setMinimumWidth(200)
        reservations_btn.clicked.connect(self.on_my_reservations)
        center_layout.addWidget(reservations_btn)
        
        layout.addLayout(center_layout)
        
        # Segunda fila con botón de historial
        history_layout = QHBoxLayout()
        history_layout.setSpacing(40)
        history_layout.setAlignment(Qt.AlignCenter)
        
        history_btn = QPushButton("HISTORY")
        history_btn.setStyleSheet(self.get_button_style())
        history_btn.setMinimumWidth(200)
        history_btn.clicked.connect(self.on_history)
        history_layout.addWidget(history_btn)
        
        layout.addLayout(history_layout)
        
        layout.addSpacing(40)
        
        # Botón Back to login (centrado abajo)
        bottom_layout = QVBoxLayout()
        bottom_layout.setAlignment(Qt.AlignCenter)
        
        logout_btn = QPushButton("Back to login")
        logout_btn.setStyleSheet(self.get_button_style())
        logout_btn.setMinimumWidth(200)
        logout_btn.clicked.connect(self.on_logout)
        bottom_layout.addWidget(logout_btn)
        
        layout.addLayout(bottom_layout)
        
        layout.addStretch()
        
        self.setLayout(layout)

    
    def on_reserve(self):
        dialog = ReservationDialog(self.user_name, self)
        dialog.exec_()
    
    def on_my_reservations(self):
        dialog = MyReservationsDialog(self.user_name, self)
        dialog.exec_()
    
    def on_history(self):
        from history_dialog import ReservationHistoryDialog
        dialog = ReservationHistoryDialog(self.user_name, self)
        dialog.exec_()
    
    def on_profile(self):
        show_styled_message(self, "Perfil", f"Usuario: {self.user_name}\nRol: Usuario", "information")
    
    def on_logout(self):
        self.parent_window.show_welcome()

class ReservationDialog(BaseDialog):
    """Diálogo para crear reservas con tabla de escenarios disponibles"""
    def __init__(self, user_name, parent=None):
        super().__init__(parent)
        self.user_name = user_name
        self.setWindowTitle("RESERVE")
        self.setMinimumSize(1000, 600)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        title = QLabel("RESERVE A SPORT STAGE")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setStyleSheet("color: white;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        layout.addSpacing(20)
        
        # Subtítulo informativo
        subtitle = QLabel("Select an available stage from the table below and click 'Reserve'")
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 200); font-size: 12px;")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        layout.addSpacing(10)
        
        # Tabla de escenarios disponibles
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["Name", "Type", "Location", "Capacity", "Date", "Time", "Price"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                color: black;
                gridline-color: #ccc;
                selection-background-color: #4a90e2;
            }
            QHeaderView::section {
                background-color: white;
                color: black;
                font-weight: bold;
                border: 1px solid #ccc;
            }
        """)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        layout.addWidget(self.table)
        
        layout.addSpacing(10)
        
        # Botones
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(20)
        btn_layout.setAlignment(Qt.AlignCenter)
        
        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(self.get_button_style())
        back_btn.setMinimumWidth(150)
        back_btn.clicked.connect(self.reject)
        btn_layout.addWidget(back_btn)
        
        reserve_btn = QPushButton("Reserve")
        reserve_btn.setStyleSheet(self.get_button_style())
        reserve_btn.setMinimumWidth(150)
        reserve_btn.clicked.connect(self.make_reservation)
        btn_layout.addWidget(reserve_btn)
        
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
        
        # Cargar los escenarios disponibles en la tabla
        self.load_available_venues()
        
    def load_available_venues(self):
        """Carga los escenarios activos y no reservados en la tabla"""
        venues = database.get_all_venues()
        reservations = database.get_all_reservations()
        
        # Crear un conjunto de (venue_id, date, time) que ya están reservados
        reserved_slots = set()
        for res in reservations.values():
            if res.get("status") == "confirmed":
                reserved_slots.add((res.get("venue_id"), res.get("date"), res.get("time")))
        
        # Filtrar escenarios activos que no estén reservados
        available_venues = {}
        for vid, vdata in venues.items():
            if vdata.get('status') == 'active':
                schedule = vdata.get('schedule', '')
                if schedule:
                    parts = schedule.split(" ")
                    date_str = parts[0] if len(parts) > 0 else ""
                    time_str = parts[1] if len(parts) > 1 else ""
                    
                    # Solo incluir si no está reservado
                    if (vid, date_str, time_str) not in reserved_slots:
                        available_venues[vid] = vdata
        
        self.table.setRowCount(len(available_venues))
        self.venues_list = []  # Para guardar el ID asociado a cada fila
        
        if not available_venues:
            self.table.setRowCount(1)
            no_venues_item = QTableWidgetItem("No available stages")
            no_venues_item.setForeground(QColor(200, 0, 0))
            self.table.setItem(0, 0, no_venues_item)
            return
        
        row = 0
        for venue_id, venue in available_venues.items():
            self.venues_list.append(venue_id)
            
            # Name
            name_item = QTableWidgetItem(venue.get("name", ""))
            name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 0, name_item)
            
            # Type
            type_item = QTableWidgetItem(venue.get("type", ""))
            type_item.setFlags(type_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 1, type_item)
            
            # Location
            location_item = QTableWidgetItem(venue.get("location", ""))
            location_item.setFlags(location_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 2, location_item)
            
            # Capacity
            capacity_item = QTableWidgetItem(str(venue.get("capacity", "")))
            capacity_item.setFlags(capacity_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 3, capacity_item)
            
            # Date and Time from schedule
            schedule = venue.get("schedule", "")
            if schedule:
                parts = schedule.split(" ")
                date_str = parts[0] if len(parts) > 0 else ""
                time_str = parts[1] if len(parts) > 1 else ""
            else:
                date_str = ""
                time_str = ""
            
            date_item = QTableWidgetItem(date_str)
            date_item.setFlags(date_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 4, date_item)
            
            time_item = QTableWidgetItem(time_str)
            time_item.setFlags(time_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 5, time_item)
            
            # Price
            price = float(venue.get("price", 0.0))
            price_item = QTableWidgetItem(f"${price:.2f}")
            price_item.setFlags(price_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 6, price_item)
            
            row += 1
        
    def make_reservation(self):
        current_row = self.table.currentRow()
        
        if current_row < 0 or current_row >= len(self.venues_list):
            QMessageBox.warning(self, "Error", "Please select a stage to reserve")
            return
        
        venue_id = self.venues_list[current_row]
        venue = database.get_all_venues()[venue_id]
        
        # Extraer fecha y hora del schedule
        schedule = venue.get("schedule", "")
        if not schedule or " " not in schedule:
            QMessageBox.warning(self, "Error", "Invalid schedule format")
            return
        
        date_str, time_str = schedule.split(" ", 1)
        
        # Verificar disponibilidad
        reservations = database.get_all_reservations()
        for r in reservations.values():
            if r["venue_id"] == venue_id and r["date"] == date_str and r["time"] == time_str and r["status"] == "confirmed":
                QMessageBox.warning(self, "Error", "This stage is already reserved for this date and time")
                return
        
        # Procesar pago antes de confirmar la reserva
        venue_name = venue.get("name", "")
        price = float(venue.get("price", 0.0))
        
        payment_dialog = PaymentDialog(price, venue_name, self)
        if payment_dialog.exec_() != QDialog.Accepted:
            # El usuario canceló el pago
            return
        
        if not payment_dialog.payment_successful:
            QMessageBox.warning(self, "Error", "Payment was not processed")
            return
        
        # Crear reserva después de pago exitoso
        res_id = str(uuid.uuid4())
        res_data = {
            "id": res_id,
            "user_email": self.user_name,
            "venue_id": venue_id,
            "venue_name": venue_name,
            "date": date_str,
            "time": time_str,
            "status": "confirmed"
        }
        
        database.save_reservation(res_data)
        QMessageBox.information(self, "Success", f"Reservation confirmed!\n\nStage: {venue_name}\nDate: {date_str}\nTime: {time_str}\nAmount paid: ${price:.2f}")
        self.accept()


class PaymentDialog(BaseDialog):
    """Diálogo para procesar pagos de prueba"""
    def __init__(self, amount, venue_name, parent=None):
        super().__init__(parent)
        self.amount = amount
        self.venue_name = venue_name
        self.payment_successful = False
        self.setWindowTitle("PAYMENT")
        self.setMinimumWidth(500)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("PAYMENT PROCESS")
        title.setFont(QFont("Arial", 22, QFont.Bold))
        title.setStyleSheet("color: white;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        layout.addSpacing(20)
        
        # Amount info
        amount_frame = QVBoxLayout()
        amount_frame.setSpacing(10)
        
        venue_label = QLabel(f"Venue: {self.venue_name}")
        venue_label.setStyleSheet("color: white; font-size: 14px;")
        amount_frame.addWidget(venue_label)
        
        price_label = QLabel(f"Amount to pay: ${self.amount:.2f}")
        price_label.setStyleSheet("color: #4a90e2; font-size: 18px; font-weight: bold;")
        price_label.setAlignment(Qt.AlignCenter)
        amount_frame.addWidget(price_label)
        
        layout.addLayout(amount_frame)
        layout.addSpacing(20)
        
        # Form
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignLeft)
        
        # Card Number
        card_label = QLabel("Card Number")
        card_label.setStyleSheet(self.get_label_style())
        self.card_input = QLineEdit()
        self.card_input.setPlaceholderText("1234 5678 9012 3456")
        self.card_input.setStyleSheet(self.get_input_style())
        form_layout.addRow(card_label, self.card_input)
        
        # Cardholder Name
        name_label = QLabel("Cardholder Name")
        name_label.setStyleSheet(self.get_label_style())
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("John Doe")
        self.name_input.setStyleSheet(self.get_input_style())
        form_layout.addRow(name_label, self.name_input)
        
        # Expiry Date
        expiry_label = QLabel("Expiry Date (MM/YY)")
        expiry_label.setStyleSheet(self.get_label_style())
        self.expiry_input = QLineEdit()
        self.expiry_input.setPlaceholderText("12/25")
        self.expiry_input.setStyleSheet(self.get_input_style())
        form_layout.addRow(expiry_label, self.expiry_input)
        
        # CVV
        cvv_label = QLabel("CVV")
        cvv_label.setStyleSheet(self.get_label_style())
        self.cvv_input = QLineEdit()
        self.cvv_input.setPlaceholderText("123")
        self.cvv_input.setMaxLength(3)
        self.cvv_input.setStyleSheet(self.get_input_style())
        form_layout.addRow(cvv_label, self.cvv_input)
        
        layout.addLayout(form_layout)
        
        layout.addSpacing(20)
        
        # Info label
        info_label = QLabel("⚠ This is a test payment form. Use any numbers for testing.")
        info_label.setStyleSheet("color: #ffaa00; font-size: 11px; font-style: italic;")
        info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(info_label)
        
        layout.addSpacing(20)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(20)
        btn_layout.setAlignment(Qt.AlignCenter)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet(self.get_button_style())
        cancel_btn.setMinimumWidth(150)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        pay_btn = QPushButton("Pay Now")
        pay_btn.setStyleSheet(self.get_button_style())
        pay_btn.setMinimumWidth(150)
        pay_btn.clicked.connect(self.process_payment)
        btn_layout.addWidget(pay_btn)
        
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
        
    def process_payment(self):
        """Procesa el pago (solo validación básica)"""
        card = self.card_input.text().strip()
        name = self.name_input.text().strip()
        expiry = self.expiry_input.text().strip()
        cvv = self.cvv_input.text().strip()
        
        # Validaciones básicas
        if not card or len(card) < 13:
            QMessageBox.warning(self, "Error", "Please enter a valid card number")
            return
        
        if not name:
            QMessageBox.warning(self, "Error", "Please enter the cardholder name")
            return
        
        if not expiry or "/" not in expiry:
            QMessageBox.warning(self, "Error", "Please enter expiry date (MM/YY)")
            return
        
        if not cvv or len(cvv) != 3 or not cvv.isdigit():
            QMessageBox.warning(self, "Error", "Please enter a valid CVV (3 digits)")
            return
        
        # Simular procesamiento del pago
        QMessageBox.information(self, "Success", f"Payment of ${self.amount:.2f} processed successfully!\n\nThank you for your purchase.")
        self.payment_successful = True
        self.accept()


class MyReservationsDialog(BaseDialog):
    """Diálogo para ver mis reservas"""
    def __init__(self, user_name, parent=None):
        super().__init__(parent)
        self.user_name = user_name
        self.setWindowTitle("RESERVATIONS")
        self.setMinimumSize(800, 500)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        title = QLabel("MY RESERVATIONS")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setStyleSheet("color: white;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Venue", "Date", "Time", "Status", "Action"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                color: black;
                gridline-color: #ccc;
            }
            QHeaderView::section {
                background-color: white;
                color: black;
                font-weight: bold;
                border: 1px solid #ccc;
            }
        """)
        layout.addWidget(self.table)
        
        close_btn = QPushButton("Back")
        close_btn.setStyleSheet(self.get_button_style())
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn, alignment=Qt.AlignCenter)
        
        self.load_data()
        self.setLayout(layout)
        
    def load_data(self):
        reservations = database.get_all_reservations()
        user_reservations = {k: v for k, v in reservations.items() if v.get("user") == self.user_name or v.get("user_email") == self.user_name}
        
        self.table.setRowCount(len(user_reservations))
        
        for i, (rid, res) in enumerate(user_reservations.items()):
            self.table.setItem(i, 0, QTableWidgetItem(res["venue_name"]))
            self.table.setItem(i, 1, QTableWidgetItem(res["date"]))
            self.table.setItem(i, 2, QTableWidgetItem(res["time"]))
            self.table.setItem(i, 3, QTableWidgetItem(res["status"]))
            
            if res["status"] == "cancelled":
                status_label = QLabel("Cancelled")
                status_label.setAlignment(Qt.AlignCenter)
                status_label.setStyleSheet("color: gray; font-weight: bold;")
                self.table.setCellWidget(i, 4, status_label)
            else:
                cancel_btn = QPushButton("Cancel")
                cancel_btn.setStyleSheet("background-color: #ff4444; color: white; border-radius: 5px; padding: 5px;")
                cancel_btn.clicked.connect(lambda checked, r=rid: self.cancel_reservation(r))
                self.table.setCellWidget(i, 4, cancel_btn)
            
    def cancel_reservation(self, res_id):
        reply = QMessageBox.question(self, 'Confirm', 
                                   'Are you sure you want to cancel this reservation?',
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            database.update_reservation_status(res_id, 'cancelled')
            self.load_data()

class AdminReservationsDialog(BaseDialog):
    """Diálogo para que el admin vea todas las reservas y su estado"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("ADMIN RESERVATIONS")
        self.setMinimumSize(1000, 600)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        title = QLabel("ALL RESERVATIONS")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setStyleSheet("color: white;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["User", "Venue", "Date", "Time", "Status", "Reserved"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                color: black;
                gridline-color: #ccc;
            }
            QHeaderView::section {
                background-color: white;
                color: black;
                font-weight: bold;
                border: 1px solid #ccc;
            }
        """)
        layout.addWidget(self.table)
        
        # Botones
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(20)
        btn_layout.setAlignment(Qt.AlignCenter)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet(self.get_button_style())
        cancel_btn.clicked.connect(self.cancel_reservation)
        btn_layout.addWidget(cancel_btn)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setStyleSheet(self.get_button_style())
        refresh_btn.clicked.connect(self.load_data)
        btn_layout.addWidget(refresh_btn)
        
        close_btn = QPushButton("Back")
        close_btn.setStyleSheet(self.get_button_style())
        close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(close_btn)
        
        layout.addLayout(btn_layout)
        
        self.load_data()
        self.setLayout(layout)
        
    def load_data(self):
        reservations = database.get_all_reservations()
        venues = database.get_all_venues()
        
        self.table.setRowCount(len(reservations))
        
        for i, (rid, res) in enumerate(reservations.items()):
            user = res.get("user", res.get("user_email", "Unknown"))
            venue_name = res.get("venue_name", "Unknown")
            
            # Verificar si el escenario fue reservado (si hay una reservación con status 'confirmed')
            is_reserved = res.get("status", "") == "confirmed"
            reserved_text = "Yes" if is_reserved else "No"
            
            self.table.setItem(i, 0, QTableWidgetItem(user))
            self.table.setItem(i, 1, QTableWidgetItem(venue_name))
            self.table.setItem(i, 2, QTableWidgetItem(res.get("date", "")))
            self.table.setItem(i, 3, QTableWidgetItem(res.get("time", "")))
            self.table.setItem(i, 4, QTableWidgetItem(res.get("status", "")))
            self.table.setItem(i, 5, QTableWidgetItem(reserved_text))
            
            # Guardar el ID de la reserva
            self.table.item(i, 0).setData(Qt.UserRole, rid)
    
    def cancel_reservation(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a reservation to cancel")
            return
        
        res_id = self.table.item(current_row, 0).data(Qt.UserRole)
        
        reply = QMessageBox.question(self, 'Confirm', 
                                   'Are you sure you want to cancel this reservation?',
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            database.update_reservation_status(res_id, 'cancelled')
            self.load_data()

class WelcomeWidget(BasePage):
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
        title_font = QFont("Arial", 36, QFont.Bold)
        title.setFont(title_font)
        title.setStyleSheet("color: white;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Subtítulo
        subtitle = QLabel("¡Welcome to Ranyave!")
        subtitle_font = QFont("Arial", 16)
        subtitle.setFont(subtitle_font)
        subtitle.setStyleSheet("color: white;")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        layout.addSpacing(40)
        
        # Botones
        login_btn = QPushButton("Iniciar Sesión")
        login_btn.setStyleSheet(self.get_button_style())
        login_btn.setMinimumWidth(250)
        login_btn.clicked.connect(self.parent_window.show_login)
        layout.addWidget(login_btn, alignment=Qt.AlignCenter)
        
        register_btn = QPushButton("Registrarse")
        register_btn.setStyleSheet(self.get_button_style())
        register_btn.setMinimumWidth(250)
        register_btn.clicked.connect(self.parent_window.show_register)
        layout.addWidget(register_btn, alignment=Qt.AlignCenter)
        
        layout.addStretch()
        
        self.setLayout(layout)



class MainWindow(QMainWindow):
    """Ventana Principal - Gestor de Pantallas"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SGED RANYAVE")
        self.setGeometry(100, 100, 1200, 700)
        
        # Stack de widgets
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
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
    
    def login_user(self, name, role):
        if role == "admin":
            dashboard = AdminDashboard(name, self)
        else:
            dashboard = UserDashboard(name, self)
        
        self.stacked_widget.addWidget(dashboard)
        self.stacked_widget.setCurrentWidget(dashboard)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
