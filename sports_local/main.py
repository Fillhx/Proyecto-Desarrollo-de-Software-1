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
from i18n import get_language_manager, tr  # Importar sistema de idiomas

# ============================================================================
# CONFIGURACIÓN: Ruta de la imagen del lado izquierdo
# ============================================================================
IMAGE_PATH = "assets/logo_ranyave.png"  # Cambia esta ruta a tu imagen
# ============================================================================

# Inicializar base de datos
database.init_db()

def show_styled_message(parent, title, message, message_type="information"):
    """Muestra un mensaje con estilo personalizado y diseño moderno"""
    msg_box = QMessageBox(parent)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.setStyleSheet("""
        QMessageBox {
            background-color: #FFFFFF;
        }
        QMessageBox QLabel {
            color: #1e3a5f;
            background-color: #FFFFFF;
        }
        QMessageBox QTextEdit {
            color: #1e3a5f;
            background-color: #F0F8FF;
        }
        QMessageBox QPushButton {
            background-color: #87CEEB;
            border: none;
            border-radius: 6px;
            padding: 8px 20px;
            color: #FFFFFF;
            font-weight: bold;
            min-width: 80px;
        }
        QMessageBox QPushButton:hover {
            background-color: #4A90E2;
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
        """Pinta el fondo con líneas decorativas y símbolos"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Fondo azul oscuro
        painter.fillRect(self.rect(), QColor(30, 58, 95))
        
        # Líneas diagonales decorativas
        pen = QPen(QColor(255, 255, 255, 50), 2)  # Transparencia añadida
        painter.setPen(pen)
        
        w = self.width()
        h = self.height()
        
        # Líneas estilo "Ranyave" (diagonales desde las esquinas)
        # Esquina superior izquierda
        painter.drawLine(0, 100, 100, 0)
        painter.drawLine(0, 200, 200, 0)
        painter.drawLine(0, 300, 300, 0)
        
        # Esquina inferior derecha
        painter.drawLine(w, h-100, w-100, h)
        painter.drawLine(w, h-200, w-200, h)
        painter.drawLine(w, h-300, w-300, h)
        
        # Esquina superior derecha
        painter.drawLine(w, 100, w-100, 0)
        painter.drawLine(w, 200, w-200, 0)
        
        # Esquina inferior izquierda
        painter.drawLine(0, h-100, 100, h)
        painter.drawLine(0, h-200, 200, h)

        # Círculos decorativos sutiles
        painter.setBrush(QColor(255, 255, 255, 10))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(w - 150, -50, 200, 200)
        painter.drawEllipse(-50, h - 150, 200, 200)

    @staticmethod
    def get_input_style():
        return """
            QLineEdit, QComboBox, QDateEdit, QTimeEdit, QSpinBox, QDoubleSpinBox {
                background-color: #FFFFFF;
                border: 2px solid #87CEEB;
                border-radius: 8px;
                padding: 10px 12px;
                font-size: 14px;
                color: #1e3a5f;
                font-family: 'Segoe UI', Arial;
                font-weight: 500;
            }
            QLineEdit:focus, QComboBox:focus, QDateEdit:focus, QTimeEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {
                border: 3px solid #4A90E2;
                background-color: #F0F8FF;
                color: #1e3a5f;
            }
            QLineEdit::placeholder {
                color: #ADD8E6;
            }
            QComboBox::drop-down {
                border: none;
                background: transparent;
            }
            QComboBox::down-arrow {
                image: none;
                width: 8px;
                height: 8px;
                margin-right: 8px;
            }
            QComboBox QAbstractItemView {
                background-color: #FFFFFF;
                color: #1e3a5f;
                selection-background-color: #B3E5FC;
                border: 1px solid #87CEEB;
            }
        """
    
    @staticmethod
    def get_button_style():
        return """
            QPushButton {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #87CEEB, stop:1 #4A90E2);
                color: #FFFFFF;
                border: none;
                border-radius: 8px;
                padding: 12px 28px;
                font-weight: bold;
                font-size: 14px;
                font-family: 'Segoe UI', Arial;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #4A90E2, stop:1 #2E5C8A);
                padding: 12px 28px;
            }
            QPushButton:pressed {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2E5C8A, stop:1 #1a3a5f);
            }
        """
    
    @staticmethod
    def get_label_style():
        return """
            color: #FFFFFF;
            font-size: 14px;
            font-family: 'Segoe UI', Arial;
            font-weight: 600;
        """

class LoginWidget(BasePage):
    """Pantalla de Login"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.init_ui()
        
        # Conectar a cambios de idioma
        get_language_manager().language_changed.connect(self.update_ui)
    
    @staticmethod
    def get_input_style():
        return BasePage.get_input_style()
    
    @staticmethod
    def get_button_style():
        return """
            QPushButton {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #5FA3D0, stop:1 #3D7BAC);
                color: #FFFFFF;
                border: none;
                border-radius: 8px;
                padding: 12px 28px;
                font-weight: bold;
                font-size: 14px;
                font-family: 'Segoe UI', Arial;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #3D7BAC, stop:1 #2E5C8A);
            }
            QPushButton:pressed {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2E5C8A, stop:1 #1a3a5f);
            }
        """
    
    @staticmethod
    def get_label_style():
        return BasePage.get_label_style()
    
    def init_ui(self):
        # Layout principal
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Panel izquierdo (imagen)
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_layout.setAlignment(Qt.AlignCenter)
        left_layout.setContentsMargins(16, 16, 16, 16)
        
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignCenter)
        pixmap = self.load_image(IMAGE_PATH)
        if pixmap:
            image_label.setPixmap(pixmap)
        else:
            image_label.setPixmap(self.create_default_logo())
        
        left_layout.addWidget(image_label)
        left_panel.setLayout(left_layout)
        
        # Panel derecho (formulario)
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_layout.setSpacing(10)
        right_layout.setContentsMargins(30, 20, 30, 20)
        
        # Título
        self.title = QLabel(tr("login_title"))
        title_font = QFont("Segoe UI", 20, QFont.Bold)
        self.title.setFont(title_font)
        self.title.setStyleSheet("color: white;")
        self.title.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(self.title)
        
        right_layout.addSpacing(10)
        
        # Email/Usuario
        self.email_label = QLabel(tr("login_email"))
        self.email_label.setStyleSheet(self.get_label_style())
        right_layout.addWidget(self.email_label)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText(tr("login_email_placeholder"))
        self.email_input.setStyleSheet(self.get_input_style())
        self.email_input.setMinimumHeight(34)
        right_layout.addWidget(self.email_input)
        
        # Contraseña
        self.password_label = QLabel(tr("login_password"))
        self.password_label.setStyleSheet(self.get_label_style())
        right_layout.addWidget(self.password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(self.get_input_style())
        self.password_input.setMinimumHeight(34)
        right_layout.addWidget(self.password_input)
        
        right_layout.addSpacing(8)
        
        # Botones
        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(8)
        buttons_layout.setAlignment(Qt.AlignCenter)
        
        self.next_btn = QPushButton(tr("login_next"))
        self.next_btn.setStyleSheet(self.get_button_style())
        self.next_btn.setMinimumWidth(120)
        self.next_btn.setMinimumHeight(34)
        self.next_btn.clicked.connect(self.on_login)
        buttons_layout.addWidget(self.next_btn)
        
        self.back_btn = QPushButton(tr("login_back"))
        self.back_btn.setStyleSheet(self.get_button_style())
        self.back_btn.setMinimumWidth(120)
        self.back_btn.setMinimumHeight(34)
        self.back_btn.clicked.connect(self.on_back)
        buttons_layout.addWidget(self.back_btn)
        
        right_layout.addLayout(buttons_layout)
        
        right_layout.addSpacing(8)
        
        # Link a registro
        self.register_label = QLabel(tr("login_register_text"))
        self.register_label.setStyleSheet("color: white; font-size: 11px;")
        self.register_label.setAlignment(Qt.AlignCenter)
        self.register_label.linkActivated.connect(self.on_register_link)
        right_layout.addWidget(self.register_label)
        
        right_layout.addStretch()
        
        right_panel.setLayout(right_layout)
        
        main_layout.addWidget(left_panel, 0)
        main_layout.addWidget(right_panel, 1)
        
        self.setLayout(main_layout)

    def update_ui(self):
        """Actualiza los textos cuando cambia el idioma"""
        self.title.setText(tr("login_title"))
        self.email_label.setText(tr("login_email"))
        self.email_input.setPlaceholderText(tr("login_email_placeholder"))
        self.password_label.setText(tr("login_password"))
        self.next_btn.setText(tr("login_next"))
        self.back_btn.setText(tr("login_back"))
        self.register_label.setText(tr("login_register_text"))
    
    def on_login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        
        if not email or not password:
            show_styled_message(self, tr("error"), tr("login_error_empty"), "warning")
            return
        
        # Validar email
        if not self.is_valid_email(email):
            show_styled_message(self, tr("error"), tr("login_error_invalid_email"), "warning")
            return
        
        # Verificar en BD
        user = database.get_user(email)
        if user and database.verify_password(password, user["password"]):
            # Login exitoso
            role = user["role"]
            name = user["name"]
            self.parent_window.login_user(email, role)  # Pasar email en lugar de name
            return
        
        show_styled_message(self, tr("error"), tr("login_error_invalid_credentials"), "warning")
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
                return pixmap.scaledToHeight(260, Qt.SmoothTransformation)
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        absolute_path = os.path.join(script_dir, image_path)
        
        if os.path.exists(absolute_path):
            pixmap = QPixmap(absolute_path)
            if not pixmap.isNull():
                return pixmap.scaledToHeight(260, Qt.SmoothTransformation)
        
        return None
    
    def create_default_logo(self):
        size = 260
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
        return pixmap.scaledToHeight(260, Qt.SmoothTransformation)
    
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
        
        # Conectar a cambios de idioma
        get_language_manager().language_changed.connect(self.update_ui)
    
    @staticmethod
    def get_input_style():
        return BasePage.get_input_style()
    
    @staticmethod
    def get_button_style():
        return """
            QPushButton {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #6DADE2, stop:1 #3498DB);
                color: #FFFFFF;
                border: none;
                border-radius: 8px;
                padding: 12px 28px;
                font-weight: bold;
                font-size: 14px;
                font-family: 'Segoe UI', Arial;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #3498DB, stop:1 #2E86C1);
            }
            QPushButton:pressed {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2E86C1, stop:1 #1a3a5f);
            }
        """
    
    def init_ui(self):
        # Layout principal
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Panel izquierdo (imagen)
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_layout.setAlignment(Qt.AlignCenter)
        left_layout.setContentsMargins(16, 16, 16, 16)
        
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignCenter)
        pixmap = self.load_image(IMAGE_PATH)
        if pixmap:
            image_label.setPixmap(pixmap)
        else:
            image_label.setPixmap(self.create_default_logo())
        
        left_layout.addWidget(image_label)
        left_panel.setLayout(left_layout)
        
        # Panel derecho (formulario)
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_layout.setSpacing(8)
        right_layout.setContentsMargins(30, 20, 30, 20)
        
        # Título
        self.title = QLabel(tr("register_title"))
        title_font = QFont("Segoe UI", 20, QFont.Bold)
        self.title.setFont(title_font)
        self.title.setStyleSheet("color: white;")
        self.title.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(self.title)
        
        right_layout.addSpacing(8)
        
        # Nombre
        self.name_label = QLabel(tr("register_name"))
        self.name_label.setStyleSheet(self.get_label_style())
        right_layout.addWidget(self.name_label)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText(tr("register_name_placeholder"))
        self.name_input.setStyleSheet(self.get_input_style())
        self.name_input.setMinimumHeight(30)
        right_layout.addWidget(self.name_input)
        
        # Email
        self.email_label = QLabel(tr("register_email"))
        self.email_label.setStyleSheet(self.get_label_style())
        right_layout.addWidget(self.email_label)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText(tr("register_email_placeholder"))
        self.email_input.setStyleSheet(self.get_input_style())
        self.email_input.setMinimumHeight(30)
        right_layout.addWidget(self.email_input)
        
        # Teléfono
        self.phone_label = QLabel(tr("register_phone"))
        self.phone_label.setStyleSheet(self.get_label_style())
        right_layout.addWidget(self.phone_label)
        
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText(tr("register_phone_placeholder"))
        self.phone_input.setStyleSheet(self.get_input_style())
        self.phone_input.setMinimumHeight(30)
        right_layout.addWidget(self.phone_input)
        
        # Contraseña
        self.password_label = QLabel(tr("register_password"))
        self.password_label.setStyleSheet(self.get_label_style())
        right_layout.addWidget(self.password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(self.get_input_style())
        self.password_input.setMinimumHeight(30)
        right_layout.addWidget(self.password_input)
        
        right_layout.addSpacing(8)
        
        # Botones
        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(8)
        buttons_layout.setAlignment(Qt.AlignCenter)
        
        self.next_btn = QPushButton(tr("register_next"))
        self.next_btn.setStyleSheet(self.get_button_style())
        self.next_btn.setMinimumWidth(120)
        self.next_btn.setMinimumHeight(34)
        self.next_btn.clicked.connect(self.on_register)
        buttons_layout.addWidget(self.next_btn)
        
        self.back_btn = QPushButton(tr("register_back"))
        self.back_btn.setStyleSheet(self.get_button_style())
        self.back_btn.setMinimumWidth(120)
        self.back_btn.setMinimumHeight(34)
        self.back_btn.clicked.connect(self.on_back)
        buttons_layout.addWidget(self.back_btn)
        
        right_layout.addLayout(buttons_layout)
        
        right_layout.addStretch()
        
        right_panel.setLayout(right_layout)
        
        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 1)
        
        self.setLayout(main_layout)
    
    def update_ui(self):
        """Actualiza los textos cuando cambia el idioma"""
        self.title.setText(tr("register_title"))
        self.name_label.setText(tr("register_name"))
        self.name_input.setPlaceholderText(tr("register_name_placeholder"))
        self.email_label.setText(tr("register_email"))
        self.email_input.setPlaceholderText(tr("register_email_placeholder"))
        self.phone_label.setText(tr("register_phone"))
        self.phone_input.setPlaceholderText(tr("register_phone_placeholder"))
        self.password_label.setText(tr("register_password"))
        self.next_btn.setText(tr("register_next"))
        self.back_btn.setText(tr("register_back"))
    
    def on_register(self):
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        phone = self.phone_input.text().strip()
        password = self.password_input.text().strip()
        
        # Validaciones
        if not all([name, email, phone, password]):
            show_styled_message(self, tr("error"), tr("register_error_empty"), "warning")
            return
        
        if len(name) < 3:
            show_styled_message(self, tr("error"), "El nombre debe tener al menos 3 caracteres", "warning")
            return
        
        if not self.is_valid_email(email):
            show_styled_message(self, tr("error"), tr("register_error_invalid_email"), "warning")
            return
        
        if not self.is_valid_phone(phone):
            show_styled_message(self, tr("error"), tr("register_error_invalid_phone"), "warning")
            return
        
        if len(password) < 6 and password != "123":
            show_styled_message(self, tr("error"), tr("register_error_weak_password"), "warning")
            return
        
        if database.get_user(email):
            show_styled_message(self, tr("error"), tr("register_error_email_exists"), "warning")
            return
        
        # Detectar si el email es de dominio ranyave.com
        is_admin = email.endswith("@ranyave.com")
        role = "admin" if is_admin else "user"
        
        # Registrar usuario
        if database.create_user(email, name, phone, password, role):
            # Enviar email de bienvenida
            email_sent = database.send_welcome_email(email, name)
            
            if is_admin:
                msg = tr("register_success_admin", name=name)
            else:
                msg = tr("register_success_user", name=name)
            
            # Agregar nota si el email fue enviado
            if email_sent:
                msg += "\n\n✅ Se ha enviado un email de bienvenida a " + email
            
            show_styled_message(self, tr("information"), msg, "information")
            self.clear_fields()
            self.parent_window.show_login()
        else:
            show_styled_message(self, tr("error"), tr("register_error"), "error")
    
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
        
        # Conectar a cambios de idioma
        get_language_manager().language_changed.connect(self.update_ui)
        
        self.init_ui()
    
    def init_ui(self):
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)
        
        # Header con rol
        header_layout = QHBoxLayout()
        self.header_label = QLabel(tr("admin_label"))
        self.header_label.setStyleSheet("color: rgba(255,255,255,180); font-size: 11px; font-weight: bold;")
        header_layout.addStretch()
        header_layout.addWidget(self.header_label)
        main_layout.addLayout(header_layout)

        # Título
        self.title = QLabel(tr("admin_title"))
        title_font = QFont("Segoe UI", 20, QFont.Bold)
        self.title.setFont(title_font)
        self.title.setStyleSheet("color: white;")
        self.title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.title)

        main_layout.addSpacing(12)
        
        # Sección central con botones
        center_layout = QVBoxLayout()
        center_layout.setSpacing(12)
        center_layout.setAlignment(Qt.AlignCenter)
        
        # Botón NEW STAGES
        self.new_stages_btn = QPushButton(tr("admin_new_stages"))
        self.new_stages_btn.setStyleSheet(self.get_button_style())
        self.new_stages_btn.setMinimumWidth(160)
        self.new_stages_btn.clicked.connect(self.on_new_stages)
        center_layout.addWidget(self.new_stages_btn, alignment=Qt.AlignCenter)
        
        # Botón STAGES INFO
        self.stages_info_btn = QPushButton(tr("admin_stages_info"))
        self.stages_info_btn.setStyleSheet(self.get_button_style())
        self.stages_info_btn.setMinimumWidth(160)
        self.stages_info_btn.clicked.connect(self.on_stages_info)
        center_layout.addWidget(self.stages_info_btn, alignment=Qt.AlignCenter)
        
        # Botón RESERVATIONS
        self.reservations_btn = QPushButton(tr("admin_reservations"))
        self.reservations_btn.setStyleSheet(self.get_button_style())
        self.reservations_btn.setMinimumWidth(160)
        self.reservations_btn.clicked.connect(self.on_reservations)
        center_layout.addWidget(self.reservations_btn, alignment=Qt.AlignCenter)
        
        # Botón Back to login
        self.back_btn = QPushButton(tr("admin_back"))
        self.back_btn.setStyleSheet(self.get_button_style())
        self.back_btn.setMinimumWidth(160)
        self.back_btn.clicked.connect(self.on_logout)
        center_layout.addWidget(self.back_btn, alignment=Qt.AlignCenter)
        
        main_layout.addLayout(center_layout)
        
        main_layout.addSpacing(12)

        # Información de usuario (compacta)
        self.user_info = QLabel(tr("admin_session", name=self.user_name))
        self.user_info.setStyleSheet("color: rgba(255, 255, 255, 150); font-size: 11px;")
        self.user_info.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.user_info)

        main_layout.addStretch()
        
        self.setLayout(main_layout)
    
    def update_ui(self):
        """Actualiza los textos cuando cambia el idioma"""
        self.header_label.setText(tr("admin_label"))
        self.title.setText(tr("admin_title"))
        self.new_stages_btn.setText(tr("admin_new_stages"))
        self.stages_info_btn.setText(tr("admin_stages_info"))
        self.reservations_btn.setText(tr("admin_reservations"))
        self.back_btn.setText(tr("admin_back"))
        self.user_info.setText(tr("admin_session", name=self.user_name))

    
    def on_new_stages(self):
        dialog = VenueForm(self)
        dialog.exec_()
    
    def on_stages_info(self):
        dialog = VenuesListDialog(self)
        dialog.exec_()
    
    def on_reservations(self):
        dialog = AdminReservationsDialog(self)
        dialog.exec_()
    
    def on_logout(self):
        self.parent_window.show_welcome()
    
    @staticmethod
    def get_button_style():
        return """
            QPushButton {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #7FB3D5, stop:1 #5B9FC6);
                color: #FFFFFF;
                border: none;
                border-radius: 8px;
                padding: 14px 32px;
                font-weight: bold;
                font-size: 14px;
                font-family: 'Segoe UI', Arial;
                min-width: 160px;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #5B9FC6, stop:1 #4A90E2);
            }
            QPushButton:pressed {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #4A90E2, stop:1 #2E5C8A);
            }
        """

class BaseDialog(QDialog):
    """Diálogo base con estilo"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #1e3a5f; color: white;")
    
    def paintEvent(self, event):
        """Pinta el fondo con líneas decorativas y símbolos"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Fondo azul
        painter.fillRect(self.rect(), QColor(30, 58, 95))
        
        # Líneas diagonales decorativas
        pen = QPen(QColor(255, 255, 255, 50), 2)
        painter.setPen(pen)
        
        w = self.width()
        h = self.height()
        
        # Líneas estilo "Ranyave"
        painter.drawLine(0, 50, 50, 0)
        painter.drawLine(w, h-50, w-50, h)
        
        # Círculos decorativos sutiles
        painter.setBrush(QColor(255, 255, 255, 10))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(w - 100, -30, 150, 150)
        painter.drawEllipse(-30, h - 100, 150, 150)

    @staticmethod
    def get_input_style():
        return BasePage.get_input_style()
    
    @staticmethod
    def get_button_style():
        return """
            QPushButton {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #87CEEB, stop:1 #4A90E2);
                color: #FFFFFF;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #4A90E2, stop:1 #2E5C8A);
            }
            QPushButton:pressed {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2E5C8A, stop:1 #1a3a5f);
            }
        """
    
    @staticmethod
    def get_label_style():
        return BasePage.get_label_style()

class VenueForm(BaseDialog):
    def get_label_style():
        return "color: white; font-size: 14px; font-family: Arial; font-weight: bold;"

class VenueForm(BaseDialog):
    """Formulario para crear/editar escenarios"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr("venue_title"))
        self.setMinimumWidth(600)
        self.setMinimumHeight(700)
        
        # Conectar a cambios de idioma
        get_language_manager().language_changed.connect(self.update_ui)
        
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 14, 20, 14)
        layout.setSpacing(12)
        
        # Title
        self.title = QLabel(tr("venue_title"))
        self.title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        self.title.setStyleSheet("color: white;")
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)
        
        # Subtitle
        self.subtitle = QLabel(tr("venue_subtitle"))
        self.subtitle.setStyleSheet("color: rgba(255, 255, 255, 200); font-size: 11px;")
        self.subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.subtitle)
        
        layout.addSpacing(8)
        
        # Separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("color: rgba(255, 255, 255, 100);")
        layout.addWidget(separator)
        
        layout.addSpacing(15)
        
        # Form with improved styling
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        form_layout.setLabelAlignment(Qt.AlignLeft)
        form_layout.setHorizontalSpacing(12)
        
        # Name
        self.name_label = QLabel(tr("venue_name"))
        self.name_label.setStyleSheet("color: white; font-size: 14px; font-family: Arial; font-weight: bold;")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText(tr("venue_name_placeholder"))
        self.name_input.setStyleSheet(self.get_input_style())
        self.name_input.setMinimumHeight(30)
        form_layout.addRow(self.name_label, self.name_input)
        
        # Type
        self.type_label = QLabel(tr("venue_type"))
        self.type_label.setStyleSheet("color: white; font-size: 14px; font-family: Arial; font-weight: bold;")
        self.type_input = QComboBox()
        self.type_input.addItems(["Fútbol", "Baloncesto", "Tenis", "Voleibol", "Natación", "Otro"])
        self.type_input.setStyleSheet(self.get_input_style())
        self.type_input.setMinimumHeight(30)
        form_layout.addRow(self.type_label, self.type_input)
        
        # Location
        self.loc_label = QLabel(tr("venue_location"))
        self.loc_label.setStyleSheet("color: white; font-size: 14px; font-family: Arial; font-weight: bold;")
        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText(tr("venue_location_placeholder"))
        self.location_input.setStyleSheet(self.get_input_style())
        self.location_input.setMinimumHeight(30)
        form_layout.addRow(self.loc_label, self.location_input)
        
        # Capacity
        self.cap_label = QLabel(tr("venue_capacity"))
        self.cap_label.setStyleSheet("color: white; font-size: 14px; font-family: Arial; font-weight: bold;")
        self.capacity_input = QSpinBox()
        self.capacity_input.setRange(1, 100000)
        self.capacity_input.setValue(50)
        self.capacity_input.setStyleSheet(self.get_input_style())
        self.capacity_input.setMinimumHeight(30)
        form_layout.addRow(self.cap_label, self.capacity_input)
        
        # Schedule - Date
        self.sch_label = QLabel(tr("venue_schedule_date"))
        self.sch_label.setStyleSheet("color: white; font-size: 14px; font-family: Arial; font-weight: bold;")
        self.schedule_date = QDateEdit()
        self.schedule_date.setCalendarPopup(True)
        self.schedule_date.setDate(QDate.currentDate())
        self.schedule_date.setStyleSheet(self.get_input_style())
        self.schedule_date.setMinimumHeight(30)
        form_layout.addRow(self.sch_label, self.schedule_date)
        
        # Schedule - Time
        self.time_label = QLabel(tr("venue_schedule_time"))
        self.time_label.setStyleSheet("color: white; font-size: 14px; font-family: Arial; font-weight: bold;")
        self.schedule_time = QTimeEdit()
        self.schedule_time.setTime(QTime(12, 0))
        self.schedule_time.setStyleSheet(self.get_input_style())
        self.schedule_time.setMinimumHeight(30)
        form_layout.addRow(self.time_label, self.schedule_time)
        
        # Price
        self.price_label = QLabel(tr("venue_price"))
        self.price_label.setStyleSheet("color: white; font-size: 14px; font-family: Arial; font-weight: bold;")
        self.price_input = QDoubleSpinBox()
        self.price_input.setRange(0.0, 100000.0)
        self.price_input.setDecimals(2)
        self.price_input.setSingleStep(10.0)
        self.price_input.setValue(50.0)
        self.price_input.setStyleSheet(self.get_input_style())
        self.price_input.setMinimumHeight(30)
        form_layout.addRow(self.price_label, self.price_input)
        
        layout.addLayout(form_layout)
        
        layout.addSpacing(12)
        
        # Separator line
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.HLine)
        separator2.setFrameShadow(QFrame.Sunken)
        separator2.setStyleSheet("color: rgba(255, 255, 255, 100);")
        layout.addWidget(separator2)
        
        layout.addSpacing(8)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)
        btn_layout.setAlignment(Qt.AlignCenter)
        
        self.back_btn = QPushButton(tr("venue_cancel"))
        self.back_btn.setStyleSheet(self.get_button_style())
        self.back_btn.setMinimumWidth(120)
        self.back_btn.setMinimumHeight(34)
        self.back_btn.setFont(QFont("Arial", 12, QFont.Bold))
        self.back_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.back_btn)
        
        self.save_btn = QPushButton(tr("venue_save"))
        self.save_btn.setStyleSheet("""
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
        self.save_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.save_btn.clicked.connect(self.save_venue)
        btn_layout.addWidget(self.save_btn)
        
        layout.addLayout(btn_layout)
        
        layout.addStretch()
        
        self.setLayout(layout)
    
    def update_ui(self):
        """Actualiza los textos cuando cambia el idioma"""
        self.setWindowTitle(tr("venue_title"))
        self.title.setText(tr("venue_title"))
        self.subtitle.setText(tr("venue_subtitle"))
        self.name_label.setText(tr("venue_name"))
        self.name_input.setPlaceholderText(tr("venue_name_placeholder"))
        self.type_label.setText(tr("venue_type"))
        self.loc_label.setText(tr("venue_location"))
        self.location_input.setPlaceholderText(tr("venue_location_placeholder"))
        self.cap_label.setText(tr("venue_capacity"))
        self.sch_label.setText(tr("venue_schedule_date"))
        self.time_label.setText(tr("venue_schedule_time"))
        self.price_label.setText(tr("venue_price"))
        self.back_btn.setText(tr("venue_cancel"))
        self.save_btn.setText(tr("venue_save"))
        
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
            show_styled_message(self, tr("error"), "Por favor completa todos los campos", "warning")
            return
        
        if capacity <= 0:
            show_styled_message(self, tr("error"), "La capacidad debe ser mayor a 0", "warning")
            return
        
        if price < 0:
            show_styled_message(self, tr("error"), "El precio no puede ser negativo", "warning")
            return
        
        # Validar fecha y hora no en el pasado
        from datetime import datetime
        selected_date = self.schedule_date.date()
        selected_time = self.schedule_time.time()
        current_date = QDate.currentDate()
        current_time = QTime.currentTime()
        
        if selected_date < current_date:
            show_styled_message(self, tr("error"), "La fecha no puede estar en el pasado", "warning")
            return
        
        if selected_date == current_date and selected_time <= current_time:
            show_styled_message(self, tr("error"), "La hora debe ser posterior a la hora actual", "warning")
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
            show_styled_message(self, tr("error"), tr("venue_error_save", error=str(e)), "error")

class VenuesListDialog(BaseDialog):
    """Diálogo para ver lista de escenarios"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr("admin_stages_info"))
        self.setMinimumSize(1400, 700)
        
        # Conectar a cambios de idioma
        get_language_manager().language_changed.connect(self.update_ui)
        
        self.init_ui()
        
    def init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(12)
        
        # Left side: Table
        left_layout = QVBoxLayout()
        left_layout.setSpacing(15)
        
        self.title = QLabel(tr("venues_list_title"))
        self.title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.title.setStyleSheet("color: white;")
        self.title.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(self.title)
        
        # Subtitle
        self.subtitle = QLabel(tr("venues_list_subtitle"))
        self.subtitle.setStyleSheet("color: rgba(255, 255, 255, 200); font-size: 10px;")
        self.subtitle.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(self.subtitle)
        
        # Separator
        separator1 = QFrame()
        separator1.setFrameShape(QFrame.HLine)
        separator1.setFrameShadow(QFrame.Sunken)
        separator1.setStyleSheet("color: rgba(255, 255, 255, 100);")
        left_layout.addWidget(separator1)
        
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.update_table_headers()
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
        
        # Configurar altura de filas (compacta)
        try:
            self.table.verticalHeader().setDefaultSectionSize(28)
        except Exception:
            pass
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
        right_layout.setContentsMargins(12, 12, 12, 12)
        right_layout.setSpacing(10)
        
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
        form_frame_layout.setContentsMargins(12, 12, 12, 12)
        form_frame_layout.setSpacing(10)
        
        self.edit_title = QLabel(tr("venues_list_edit_title"))
        self.edit_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.edit_title.setStyleSheet("color: white;")
        self.edit_title.setAlignment(Qt.AlignCenter)
        form_frame_layout.addWidget(self.edit_title)
        
        # Separator
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.HLine)
        separator2.setFrameShadow(QFrame.Sunken)
        separator2.setStyleSheet("color: rgba(255, 255, 255, 100);")
        form_frame_layout.addWidget(separator2)
        
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        form_layout.setHorizontalSpacing(12)
        
        # Name
        self.name_label = QLabel(tr("venues_list_name"))
        self.name_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold;")
        self.edit_name = QLineEdit()
        self.edit_name.setStyleSheet(self.get_input_style())
        self.edit_name.setMinimumHeight(28)
        form_layout.addRow(self.name_label, self.edit_name)
        
        # Type
        self.type_label = QLabel(tr("venues_list_type"))
        self.type_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold;")
        self.edit_type = QLineEdit()
        self.edit_type.setStyleSheet(self.get_input_style())
        self.edit_type.setMinimumHeight(28)
        form_layout.addRow(self.type_label, self.edit_type)
        
        # Location
        self.location_label = QLabel(tr("venues_list_location"))
        self.location_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold;")
        self.edit_location = QLineEdit()
        self.edit_location.setStyleSheet(self.get_input_style())
        self.edit_location.setMinimumHeight(28)
        form_layout.addRow(self.location_label, self.edit_location)
        
        # Capacity
        self.capacity_label = QLabel(tr("venues_list_capacity"))
        self.capacity_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold;")
        self.edit_capacity = QLineEdit()
        self.edit_capacity.setStyleSheet(self.get_input_style())
        self.edit_capacity.setMinimumHeight(28)
        form_layout.addRow(self.capacity_label, self.edit_capacity)
        
        # Schedule Date
        self.date_label = QLabel(tr("venues_list_date"))
        self.date_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold;")
        self.edit_schedule_date = QDateEdit()
        self.edit_schedule_date.setCalendarPopup(True)
        self.edit_schedule_date.setStyleSheet(self.get_input_style())
        self.edit_schedule_date.setMinimumHeight(28)
        form_layout.addRow(self.date_label, self.edit_schedule_date)
        
        # Schedule Time
        self.time_label = QLabel(tr("venues_list_time"))
        self.time_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold;")
        self.edit_schedule_time = QTimeEdit()
        self.edit_schedule_time.setStyleSheet(self.get_input_style())
        self.edit_schedule_time.setMinimumHeight(28)
        form_layout.addRow(self.time_label, self.edit_schedule_time)
        
        # Price
        self.price_label = QLabel(tr("venues_list_price"))
        self.price_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold;")
        self.edit_price = QDoubleSpinBox()
        self.edit_price.setRange(0.0, 100000.0)
        self.edit_price.setDecimals(2)
        self.edit_price.setSingleStep(10.0)
        self.edit_price.setStyleSheet(self.get_input_style())
        self.edit_price.setMinimumHeight(28)
        form_layout.addRow(self.price_label, self.edit_price)
        
        right_layout.addLayout(form_layout)
        
        right_layout.addSpacing(20)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        btn_layout.setAlignment(Qt.AlignCenter)
        
        self.back_btn = QPushButton(tr("venues_list_back"))
        self.back_btn.setStyleSheet(self.get_button_style())
        self.back_btn.setMinimumWidth(110)
        self.back_btn.setMinimumHeight(32)
        self.back_btn.clicked.connect(self.accept)
        btn_layout.addWidget(self.back_btn)
        
        self.save_btn = QPushButton(tr("venues_list_save"))
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                border: 1px solid #45a049;
                padding: 6px 12px;
                font-weight: bold;
                min-width: 110px;
                min-height: 32px;
                border-radius: 4px;
                color: white;
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.save_btn.clicked.connect(self.save_changes)
        btn_layout.addWidget(self.save_btn)
        
        self.delete_btn = QPushButton(tr("venues_list_delete"))
        self.delete_btn.setStyleSheet("""
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
        self.delete_btn.clicked.connect(self.delete_venue)
        btn_layout.addWidget(self.delete_btn)
        
        right_layout.addLayout(btn_layout)
        
        right_layout.addStretch()
        
        layout.addLayout(right_layout, 1)
        
        self.load_data()
        self.setLayout(layout)
        
        self.current_venue_id = None
    
    def update_table_headers(self):
        """Actualiza los encabezados de la tabla con el idioma actual"""
        headers = tr("venues_list_table").split("|")
        self.table.setHorizontalHeaderLabels(headers)
    
    def update_ui(self):
        """Actualiza los textos cuando cambia el idioma"""
        self.setWindowTitle(tr("admin_stages_info"))
        self.title.setText(tr("venues_list_title"))
        self.subtitle.setText(tr("venues_list_subtitle"))
        self.update_table_headers()
        self.edit_title.setText(tr("venues_list_edit_title"))
        self.name_label.setText(tr("venues_list_name"))
        self.type_label.setText(tr("venues_list_type"))
        self.location_label.setText(tr("venues_list_location"))
        self.capacity_label.setText(tr("venues_list_capacity"))
        self.date_label.setText(tr("venues_list_date"))
        self.time_label.setText(tr("venues_list_time"))
        self.price_label.setText(tr("venues_list_price"))
        self.back_btn.setText(tr("venues_list_back"))
        self.save_btn.setText(tr("venues_list_save"))
        self.delete_btn.setText(tr("venues_list_delete"))
        
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
            show_styled_message(self, tr("information"), tr("venues_list_save_success"), "information")
        except Exception as e:
            show_styled_message(self, tr("error"), f"Error guardando cambios: {str(e)}", "warning")
            print(f"Error details: {e}")
            import traceback
            traceback.print_exc()
    
    def delete_venue(self):
        if not self.current_venue_id:
            show_styled_message(self, tr("warning"), "Por favor selecciona un escenario para eliminar", "warning")
            return
        
        venue_name = self.venues[self.current_venue_id]["name"]
        
        # Confirmar eliminación
        reply = QMessageBox.question(
            self, 
            tr("venues_list_delete_confirm_title"), 
            tr("venues_list_delete_confirm"),
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                database.delete_venue(self.current_venue_id)
                self.load_data()
                show_styled_message(self, tr("information"), tr("venues_list_delete_success"), "information")
                self.current_venue_id = None
                # Limpiar los campos del formulario
                self.edit_name.clear()
                self.edit_type.clear()
                self.edit_location.clear()
                self.edit_capacity.clear()
                self.edit_price.setValue(0.0)
            except Exception as e:
                show_styled_message(self, tr("error"), f"Error eliminando escenario: {str(e)}", "warning")
                print(f"Error details: {e}")
                import traceback
                traceback.print_exc()


class UserDashboard(BasePage):
    """Panel de Usuario Normal"""
    def __init__(self, user_name, parent=None):
        super().__init__(parent)
        self.user_name = user_name
        self.parent_window = parent
        
        # Conectar a cambios de idioma
        get_language_manager().language_changed.connect(self.update_ui)
        
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        
        # Header con rol
        header_layout = QHBoxLayout()
        self.header_label = QLabel(tr("user_label"))
        self.header_label.setStyleSheet("color: rgba(255,255,255,180); font-size: 11px; font-weight: bold;")
        header_layout.addStretch()
        header_layout.addWidget(self.header_label)
        layout.addLayout(header_layout)

        # Título
        self.title = QLabel(tr("user_title"))
        title_font = QFont("Segoe UI", 20, QFont.Bold)
        self.title.setFont(title_font)
        self.title.setStyleSheet("color: white;")
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)

        layout.addSpacing(12)
        
        # Sección central con botones (Primera fila)
        center_layout = QHBoxLayout()
        center_layout.setSpacing(16)
        center_layout.setAlignment(Qt.AlignCenter)
        
        # Botón RESERVE
        self.reserve_btn = QPushButton(tr("user_reserve"))
        self.reserve_btn.setStyleSheet(self.get_button_style())
        self.reserve_btn.setMinimumWidth(140)
        self.reserve_btn.clicked.connect(self.on_reserve)
        center_layout.addWidget(self.reserve_btn)
        
        # Botón RESERVATIONS
        self.reservations_btn = QPushButton(tr("user_my_reservations"))
        self.reservations_btn.setStyleSheet(self.get_button_style())
        self.reservations_btn.setMinimumWidth(140)
        self.reservations_btn.clicked.connect(self.on_my_reservations)
        center_layout.addWidget(self.reservations_btn)
        
        layout.addLayout(center_layout)
        
        # Segunda fila con botón de historial
        history_layout = QHBoxLayout()
        history_layout.setSpacing(16)
        history_layout.setAlignment(Qt.AlignCenter)
        
        self.history_btn = QPushButton(tr("user_history"))
        self.history_btn.setStyleSheet(self.get_button_style())
        self.history_btn.setMinimumWidth(140)
        self.history_btn.clicked.connect(self.on_history)
        history_layout.addWidget(self.history_btn)
        
        layout.addLayout(history_layout)
        
        layout.addSpacing(12)

        # Botón Back to login (compacto)
        bottom_layout = QHBoxLayout()
        bottom_layout.setAlignment(Qt.AlignCenter)
        self.logout_btn = QPushButton(tr("user_back"))
        self.logout_btn.setStyleSheet(self.get_button_style())
        self.logout_btn.setMinimumWidth(140)
        self.logout_btn.setMaximumHeight(34)
        self.logout_btn.clicked.connect(self.on_logout)
        bottom_layout.addWidget(self.logout_btn)
        layout.addLayout(bottom_layout)
        layout.addStretch()
        
        self.setLayout(layout)

    def update_ui(self):
        """Actualiza los textos cuando cambia el idioma"""
        self.header_label.setText(tr("user_label"))
        self.title.setText(tr("user_title"))
        self.reserve_btn.setText(tr("user_reserve"))
        self.reservations_btn.setText(tr("user_my_reservations"))
        self.history_btn.setText(tr("user_history"))
        self.logout_btn.setText(tr("user_back"))

    
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
    
    @staticmethod
    def get_button_style():
        return """
            QPushButton {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #B2EBF2, stop:1 #80DEEA);
                color: #00838F;
                border: none;
                border-radius: 8px;
                padding: 14px 32px;
                font-weight: bold;
                font-size: 14px;
                font-family: 'Segoe UI', Arial;
                min-width: 140px;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #80DEEA, stop:1 #4DD0E1);
            }
            QPushButton:pressed {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #4DD0E1, stop:1 #26C6DA);
            }
        """

class ReservationDialog(BaseDialog):
    """Diálogo para crear reservas con tabla de escenarios disponibles"""
    def __init__(self, user_name, parent=None):
        super().__init__(parent)
        self.user_name = user_name
        self.setWindowTitle(tr("user_reserve"))
        self.setMinimumSize(1000, 600)
        
        # Conectar a cambios de idioma
        get_language_manager().language_changed.connect(self.update_ui)
        
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        self.title = QLabel(tr("reservation_title"))
        self.title.setFont(QFont("Arial", 24, QFont.Bold))
        self.title.setStyleSheet("color: white;")
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)
        
        layout.addSpacing(20)
        
        # Subtítulo informativo
        self.subtitle = QLabel(tr("reservation_subtitle"))
        self.subtitle.setStyleSheet("color: rgba(255, 255, 255, 200); font-size: 12px;")
        self.subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.subtitle)
        
        layout.addSpacing(10)
        
        # Tabla de escenarios disponibles
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.update_table_headers()
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
        
        self.back_btn = QPushButton(tr("reservation_back"))
        self.back_btn.setStyleSheet(self.get_button_style())
        self.back_btn.setMinimumWidth(150)
        self.back_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.back_btn)
        
        self.reserve_btn = QPushButton(tr("reservation_reserve_btn"))
        self.reserve_btn.setStyleSheet(self.get_button_style())
        self.reserve_btn.setMinimumWidth(150)
        self.reserve_btn.clicked.connect(self.make_reservation)
        btn_layout.addWidget(self.reserve_btn)
        
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
        
        # Cargar los escenarios disponibles en la tabla
        self.load_available_venues()
    
    def update_table_headers(self):
        """Actualiza los encabezados de la tabla con el idioma actual"""
        headers = tr("reservation_table_headers").split("|")
        self.table.setHorizontalHeaderLabels(headers)
    
    def update_ui(self):
        """Actualiza los textos cuando cambia el idioma"""
        self.setWindowTitle(tr("user_reserve"))
        self.title.setText(tr("reservation_title"))
        self.subtitle.setText(tr("reservation_subtitle"))
        self.update_table_headers()
        self.back_btn.setText(tr("reservation_back"))
        self.reserve_btn.setText(tr("reservation_reserve_btn"))
    
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
            no_venues_item = QTableWidgetItem(tr("reservation_error_no_venues"))
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
            show_styled_message(self, tr("error"), tr("reservation_error_select"), "warning")
            return
        
        venue_id = self.venues_list[current_row]
        venue = database.get_all_venues()[venue_id]
        
        # Extraer fecha y hora del schedule
        schedule = venue.get("schedule", "")
        if not schedule or " " not in schedule:
            show_styled_message(self, tr("error"), tr("reservation_error_invalid_schedule"), "warning")
            return
        
        date_str, time_str = schedule.split(" ", 1)
        
        # Validar que la fecha y hora no estén en el pasado
        try:
            from datetime import datetime, date as date_class, time as time_class
            schedule_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            schedule_time = datetime.strptime(time_str, "%H:%M").time()
            today = date_class.today()
            current_time = datetime.now().time()
            
            if schedule_date < today:
                show_styled_message(self, tr("error"), "No se puede reservar un escenario con fecha en el pasado", "warning")
                return
            
            if schedule_date == today and schedule_time <= current_time:
                show_styled_message(self, tr("error"), "No se puede reservar un escenario con hora en el pasado", "warning")
                return
        except:
            pass
        
        # Verificar disponibilidad
        reservations = database.get_all_reservations()
        for r in reservations.values():
            if r["venue_id"] == venue_id and r["date"] == date_str and r["time"] == time_str and r["status"] == "confirmed":
                show_styled_message(self, tr("error"), tr("reservation_error_already_reserved"), "warning")
                return
        
        # Procesar pago antes de confirmar la reserva
        venue_name = venue.get("name", "")
        price = float(venue.get("price", 0.0))
        
        payment_dialog = PaymentDialog(price, venue_name, self)
        if payment_dialog.exec_() != QDialog.Accepted:
            # El usuario canceló el pago
            return
        
        if not payment_dialog.payment_successful:
            show_styled_message(self, tr("error"), tr("reservation_payment_error"), "warning")
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
        
        # Enviar email de confirmación de reserva
        # Obtener nombre del usuario desde la BD
        try:
            user = database.get_user(self.user_name)
            if user:
                user_name = user.get("name", "Usuario")
                user_email = self.user_name
                print(f"DEBUG: Enviando email a {user_email} con nombre {user_name}")
                database.send_reservation_email(user_email, user_name, venue_name, date_str, time_str, price)
            else:
                print(f"DEBUG: Usuario no encontrado en BD: {self.user_name}")
        except Exception as e:
            print(f"ERROR: {e}")
        
        show_styled_message(
            self,
            tr("reservation_success_title"),
            tr("reservation_success", venue_name=venue_name, date=date_str, time=time_str, price=f"{price:.2f}") + "\n\n✅ Se ha enviado un email de confirmación",
            "information"
        )
        self.accept()


class PaymentDialog(BaseDialog):
    """Diálogo para procesar pagos de prueba"""
    def __init__(self, amount, venue_name, parent=None):
        super().__init__(parent)
        self.amount = amount
        self.venue_name = venue_name
        self.payment_successful = False
        self.setWindowTitle("PAGO")
        self.setMinimumWidth(500)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("💳 PROCESO DE PAGO")
        title.setFont(QFont("Arial", 22, QFont.Bold))
        title.setStyleSheet("color: white;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        layout.addSpacing(20)
        
        # Amount info
        amount_frame = QVBoxLayout()
        amount_frame.setSpacing(10)
        
        venue_label = QLabel(f"Escenario: {self.venue_name}")
        venue_label.setStyleSheet("color: white; font-size: 14px;")
        amount_frame.addWidget(venue_label)
        
        price_label = QLabel(f"Monto a pagar: ${self.amount:.2f}")
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
        card_label = QLabel("💳 Número de Tarjeta")
        card_label.setStyleSheet(self.get_label_style())
        self.card_input = QLineEdit()
        self.card_input.setPlaceholderText("1234 5678 9012 3456")
        self.card_input.setStyleSheet(self.get_input_style())
        form_layout.addRow(card_label, self.card_input)
        
        # Cardholder Name
        name_label = QLabel("👤 Nombre del Titular")
        name_label.setStyleSheet(self.get_label_style())
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("John Doe")
        self.name_input.setStyleSheet(self.get_input_style())
        form_layout.addRow(name_label, self.name_input)
        
        # Expiry Date
        expiry_label = QLabel("📅 Fecha de Expiración (MM/AA)")
        expiry_label.setStyleSheet(self.get_label_style())
        self.expiry_input = QLineEdit()
        self.expiry_input.setPlaceholderText("12/25")
        self.expiry_input.setStyleSheet(self.get_input_style())
        form_layout.addRow(expiry_label, self.expiry_input)
        
        # CVV
        cvv_label = QLabel("🔒 CVV")
        cvv_label.setStyleSheet(self.get_label_style())
        self.cvv_input = QLineEdit()
        self.cvv_input.setPlaceholderText("123")
        self.cvv_input.setMaxLength(3)
        self.cvv_input.setStyleSheet(self.get_input_style())
        form_layout.addRow(cvv_label, self.cvv_input)
        
        layout.addLayout(form_layout)
        
        layout.addSpacing(20)
        
        # Info label
        info_label = QLabel("⚠ Este es un formulario de pago de prueba. Usa cualquier número para probar.")
        info_label.setStyleSheet("color: #ffaa00; font-size: 11px; font-style: italic;")
        info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(info_label)
        
        layout.addSpacing(20)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(20)
        btn_layout.setAlignment(Qt.AlignCenter)
        
        cancel_btn = QPushButton("Cancelar ❌")
        cancel_btn.setStyleSheet(self.get_button_style())
        cancel_btn.setMinimumWidth(150)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        pay_btn = QPushButton("Pagar Ahora 💳")
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
            QMessageBox.warning(self, "Error", "Por favor ingresa un número de tarjeta válido")
            return
        
        if not name:
            show_styled_message(self, tr("error"), tr("payment_error_name"), "warning")
            return
        
        if not expiry or "/" not in expiry:
            show_styled_message(self, tr("error"), tr("payment_error_expiry"), "warning")
            return
        
        if not cvv or len(cvv) != 3 or not cvv.isdigit():
            show_styled_message(self, tr("error"), tr("payment_error_cvv"), "warning")
            return
        
        # Simular procesamiento del pago
        show_styled_message(self, tr("success"), tr("payment_success_message", amount=f"{self.amount:.2f}"), "information")
        self.payment_successful = True
        self.accept()


class MyReservationsDialog(BaseDialog):
    """Diálogo para ver mis reservas"""
    def __init__(self, user_name, parent=None):
        super().__init__(parent)
        self.user_name = user_name
        self.setWindowTitle(tr("user_my_reservations"))
        self.setMinimumSize(800, 500)
        
        # Conectar a cambios de idioma
        get_language_manager().language_changed.connect(self.update_ui)
        
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        self.title = QLabel(tr("my_reservations_title"))
        self.title.setFont(QFont("Arial", 20, QFont.Bold))
        self.title.setStyleSheet("color: white;")
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.update_table_headers()
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
        
        self.close_btn = QPushButton(tr("my_reservations_back"))
        self.close_btn.setStyleSheet(self.get_button_style())
        self.close_btn.clicked.connect(self.accept)
        layout.addWidget(self.close_btn, alignment=Qt.AlignCenter)
        
        self.load_data()
        self.setLayout(layout)
    
    def update_table_headers(self):
        """Actualiza los encabezados de la tabla con el idioma actual"""
        headers = tr("my_reservations_table_headers").split("|")
        self.table.setHorizontalHeaderLabels(headers)
    
    def update_ui(self):
        """Actualiza los textos cuando cambia el idioma"""
        self.setWindowTitle(tr("user_my_reservations"))
        self.title.setText(tr("my_reservations_title"))
        self.update_table_headers()
        self.close_btn.setText(tr("my_reservations_back"))
        self.load_data()
        
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
                status_label = QLabel(tr("my_reservations_cancelled"))
                status_label.setAlignment(Qt.AlignCenter)
                status_label.setStyleSheet("color: gray; font-weight: bold;")
                self.table.setCellWidget(i, 4, status_label)
            else:
                cancel_btn = QPushButton(tr("my_reservations_cancel"))
                cancel_btn.setStyleSheet("background-color: #ff4444; color: white; border-radius: 5px; padding: 5px;")
                cancel_btn.clicked.connect(lambda checked, r=rid: self.cancel_reservation(r))
                self.table.setCellWidget(i, 4, cancel_btn)
            
    def cancel_reservation(self, res_id):
        reply = QMessageBox.question(self, tr("my_reservations_confirm_title"), 
                                   tr("my_reservations_confirm"),
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # Obtener datos de la reserva antes de cancelar
            try:
                reservations = database.get_all_reservations()
                reservation = reservations.get(res_id, {})
                
                # Enviar email de cancelación
                if reservation:
                    user_email = reservation.get("user_email", self.user_name)
                    venue_name = reservation.get("venue_name", "Escenario")
                    date = reservation.get("date", "")
                    time = reservation.get("time", "")
                    
                    # Obtener el nombre del usuario y el precio del venue
                    user = database.get_user(user_email)
                    user_name = user.get("name", "Usuario") if user else "Usuario"
                    
                    venue_id = reservation.get("venue_id", "")
                    venues = database.get_all_venues()
                    price = 0.0
                    if venue_id in venues:
                        price = float(venues[venue_id].get("price", 0.0))
                    
                    print(f"DEBUG: Cancelación - Enviando email a {user_email}")
                    database.send_cancellation_email(user_email, user_name, venue_name, date, time, price)
                else:
                    print(f"DEBUG: Reserva no encontrada: {res_id}")
            except Exception as e:
                print(f"ERROR en cancelación: {e}")
            
            database.update_reservation_status(res_id, 'cancelled')
            self.load_data()


class AdminReservationsDialog(BaseDialog):
    """Diálogo para que el admin vea todas las reservas y su estado"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr("admin_reservations"))
        self.setMinimumSize(1000, 600)
        
        # Conectar a cambios de idioma
        get_language_manager().language_changed.connect(self.update_ui)
        
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        self.title = QLabel(tr("admin_reservations_title"))
        self.title.setFont(QFont("Arial", 20, QFont.Bold))
        self.title.setStyleSheet("color: white;")
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)
        
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.update_table_headers()
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
        
        self.cancel_btn = QPushButton(tr("admin_reservations_cancel_btn"))
        self.cancel_btn.setStyleSheet(self.get_button_style())
        self.cancel_btn.clicked.connect(self.cancel_reservation)
        btn_layout.addWidget(self.cancel_btn)
        
        self.refresh_btn = QPushButton("Actualizar")
        self.refresh_btn.setStyleSheet(self.get_button_style())
        self.refresh_btn.clicked.connect(self.load_data)
        btn_layout.addWidget(self.refresh_btn)
        
        self.close_btn = QPushButton(tr("admin_reservations_back_btn"))
        self.close_btn.setStyleSheet(self.get_button_style())
        self.close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(self.close_btn)
        
        layout.addLayout(btn_layout)
        
        self.load_data()
        self.setLayout(layout)
    
    def update_table_headers(self):
        """Actualiza los encabezados de la tabla con el idioma actual"""
        headers = tr("admin_reservations_table").split("|")
        self.table.setHorizontalHeaderLabels(headers)
    
    def update_ui(self):
        """Actualiza los textos cuando cambia el idioma"""
        self.setWindowTitle(tr("admin_reservations"))
        self.title.setText(tr("admin_reservations_title"))
        self.update_table_headers()
        self.cancel_btn.setText(tr("admin_reservations_cancel_btn"))
        self.close_btn.setText(tr("admin_reservations_back_btn"))
        self.load_data()
        
    def load_data(self):
        reservations = database.get_all_reservations()
        venues = database.get_all_venues()
        
        self.table.setRowCount(len(reservations))
        
        for i, (rid, res) in enumerate(reservations.items()):
            user = res.get("user", res.get("user_email", "Unknown"))
            venue_name = res.get("venue_name", "Unknown")
            
            # Verificar si el escenario fue reservado (si hay una reservación con status 'confirmed')
            is_reserved = res.get("status", "") == "confirmed"
            reserved_text = "Sí" if is_reserved else "No"
            
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
            QMessageBox.warning(self, "Advertencia", "Por favor selecciona una reserva para cancelar")
            return
        
        res_id = self.table.item(current_row, 0).data(Qt.UserRole)
        
        reply = QMessageBox.question(self, 'Confirmar', 
                                   '¿Estás seguro de que deseas cancelar esta reserva?',
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # Obtener datos de la reserva antes de cancelar
            try:
                reservations = database.get_all_reservations()
                reservation = reservations.get(res_id, {})
                
                # Enviar email de cancelación
                if reservation:
                    user_email = reservation.get("user_email", "")
                    venue_name = reservation.get("venue_name", "Escenario")
                    date = reservation.get("date", "")
                    time = reservation.get("time", "")
                    
                    # Obtener el nombre del usuario y el precio
                    user = database.get_user(user_email)
                    user_name = user.get("name", "Usuario") if user else "Usuario"
                    
                    venue_id = reservation.get("venue_id", "")
                    venues = database.get_all_venues()
                    price = 0.0
                    if venue_id in venues:
                        price = float(venues[venue_id].get("price", 0.0))
                    
                    print(f"DEBUG: Admin cancelación - Enviando email a {user_email}")
                    database.send_cancellation_email(user_email, user_name, venue_name, date, time, price)
                else:
                    print(f"DEBUG: Reserva no encontrada por admin: {res_id}")
            except Exception as e:
                print(f"ERROR en cancelación admin: {e}")
            
            database.update_reservation_status(res_id, 'cancelled')
            self.load_data()

class WelcomeWidget(BasePage):
    """Pantalla de Bienvenida"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.init_ui()
        
        # Conectar a cambios de idioma
        get_language_manager().language_changed.connect(self.update_ui)
    
    @staticmethod
    def get_button_style():
        return """
            QPushButton {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #52B3D9, stop:1 #2980B9);
                color: #FFFFFF;
                border: none;
                border-radius: 10px;
                padding: 15px 40px;
                font-weight: bold;
                font-size: 15px;
                font-family: 'Segoe UI', Arial;
                min-width: 200px;
                min-height: 50px;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2980B9, stop:1 #1a5a7f);
            }
            QPushButton:pressed {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #1a5a7f, stop:1 #0d3a52);
            }
        """
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(60, 60, 60, 60)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignCenter)
        
        # Título
        self.title = QLabel("SGED RANYAVE")
        title_font = QFont("Arial", 36, QFont.Bold)
        self.title.setFont(title_font)
        self.title.setStyleSheet("color: white;")
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)
        
        # Subtítulo
        self.subtitle = QLabel("¡Bienvenido a Ranyave!")
        subtitle_font = QFont("Arial", 16)
        self.subtitle.setFont(subtitle_font)
        self.subtitle.setStyleSheet("color: white;")
        self.subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.subtitle)
        
        layout.addSpacing(40)
        
        # Botones
        self.login_btn = QPushButton("Iniciar Sesión")
        self.login_btn.setStyleSheet(self.get_button_style())
        self.login_btn.setMinimumWidth(250)
        self.login_btn.clicked.connect(self.parent_window.show_login)
        layout.addWidget(self.login_btn, alignment=Qt.AlignCenter)
        
        self.register_btn = QPushButton("Registrarse")
        self.register_btn.setStyleSheet(self.get_button_style())
        self.register_btn.setMinimumWidth(250)
        self.register_btn.clicked.connect(self.parent_window.show_register)
        layout.addWidget(self.register_btn, alignment=Qt.AlignCenter)
        
        layout.addStretch()
        
        self.setLayout(layout)
    
    def update_ui(self):
        """Actualiza los textos cuando cambia el idioma"""
        if get_language_manager().get_current_language() == "es":
            self.subtitle.setText("¡Bienvenido a Ranyave!")
            self.login_btn.setText("Iniciar Sesión")
            self.register_btn.setText("Registrarse")
        else:
            self.subtitle.setText("Welcome to Ranyave!")
            self.login_btn.setText("Sign In")
            self.register_btn.setText("Register")



class MainWindow(QMainWindow):
    """Ventana Principal - Gestor de Pantallas"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SGED RANYAVE")
        self.setGeometry(100, 100, 1200, 700)
        
        # Obtener gestor de idiomas
        self.language_manager = get_language_manager()
        self.language_manager.language_changed.connect(self.on_language_changed)
        
        # Stack de widgets
        self.stacked_widget = QStackedWidget()
        
        # Crear widget central con layout para botón de idioma
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Barra superior con botón de idioma
        top_bar = QWidget()
        top_bar.setStyleSheet("background-color: #1a2a4a; border-bottom: 1px solid #4a7ba7;")
        top_bar_layout = QHBoxLayout()
        top_bar_layout.setContentsMargins(10, 8, 10, 8)
        top_bar_layout.setSpacing(10)
        
        # Título de la aplicación
        app_title = QLabel("SGED RANYAVE")
        app_title.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")
        top_bar_layout.addWidget(app_title)
        
        top_bar_layout.addStretch()
        
        # Botón para cambiar idioma
        lang_label = QLabel("🌐 " + tr("spanish"))
        lang_label.setStyleSheet("color: white; font-size: 11px;")
        top_bar_layout.addWidget(lang_label)
        
        lang_combo = QComboBox()
        lang_combo.addItems([tr("spanish"), tr("english")])
        lang_combo.setCurrentIndex(0)  # Español por defecto
        lang_combo.setStyleSheet("""
            QComboBox {
                background-color: #1e3a5f;
                color: white;
                border: 1px solid white;
                border-radius: 3px;
                padding: 4px;
                font-size: 11px;
            }
            QComboBox QAbstractItemView {
                background-color: #1e3a5f;
                color: white;
                selection-background-color: #4a90e2;
            }
        """)
        lang_combo.currentIndexChanged.connect(self.on_language_combo_changed)
        top_bar_layout.addWidget(lang_combo)
        self.lang_combo = lang_combo
        self.lang_label = lang_label
        
        top_bar.setLayout(top_bar_layout)
        main_layout.addWidget(top_bar)
        
        # Stack principal
        main_layout.addWidget(self.stacked_widget, 1)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
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
    
    def on_language_combo_changed(self, index):
        """Cambia el idioma cuando se selecciona en el combobox"""
        if index == 0:  # Español
            self.language_manager.set_language("es")
        else:  # Inglés
            self.language_manager.set_language("en")
    
    def on_language_changed(self, language_code):
        """Se ejecuta cuando cambia el idioma"""
        # Actualizar label
        if language_code == "es":
            self.lang_label.setText("🌐 " + tr("spanish"))
            self.lang_combo.blockSignals(True)
            self.lang_combo.setCurrentIndex(0)
            self.lang_combo.blockSignals(False)
        else:
            self.lang_label.setText("🌐 " + tr("english"))
            self.lang_combo.blockSignals(True)
            self.lang_combo.setCurrentIndex(1)
            self.lang_combo.blockSignals(False)
        
        # Actualizar todas las pantallas visibles
        self.update_all_widgets()
    
    def update_all_widgets(self):
        """Actualiza todos los widgets con el nuevo idioma"""
        self.welcome_widget.update_ui()
        self.login_widget.update_ui()
        self.register_widget.update_ui()
    
    def show_welcome(self):
        self.stacked_widget.setCurrentWidget(self.welcome_widget)
    
    def show_login(self):
        self.login_widget.clear_fields()
        self.login_widget.update_ui()
        self.stacked_widget.setCurrentWidget(self.login_widget)
    
    def show_register(self):
        self.register_widget.clear_fields()
        self.register_widget.update_ui()
        self.stacked_widget.setCurrentWidget(self.register_widget)
    
    def login_user(self, email, role):
        if role == "admin":
            dashboard = AdminDashboard(email, self)
        else:
            dashboard = UserDashboard(email, self)
        
        self.stacked_widget.addWidget(dashboard)
        self.stacked_widget.setCurrentWidget(dashboard)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Cargar estilo global QSS para una apariencia compacta y profesional
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        qss_path = os.path.join(script_dir, "styles.qss")
        if os.path.exists(qss_path):
            with open(qss_path, 'r', encoding='utf-8') as f:
                app.setStyleSheet(f.read())
    except Exception:
        pass
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
