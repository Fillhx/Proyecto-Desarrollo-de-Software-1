from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                             QTableWidget, QTableWidgetItem, QWidget, QMessageBox, QHeaderView)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt
import database


class BaseDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Dialog")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #1e1e1e;")

    @staticmethod
    def get_button_style():
        return """
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 12px 24px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            border-radius: 8px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        QPushButton:pressed {
            background-color: #3d8b40;
        }
        """

    @staticmethod
    def get_input_style():
        return """
        QLineEdit, QTextEdit {
            background-color: white;
            color: black;
            border: 2px solid #4CAF50;
            border-radius: 5px;
            padding: 5px;
            font-size: 14px;
        }
        """

    @staticmethod
    def get_label_style():
        return "color: white; font-size: 14px;"


class ReservationHistoryDialog(BaseDialog):
    """Diálogo para ver el historial completo de reservas del cliente"""
    def __init__(self, user_name, parent=None):
        super().__init__(parent)
        self.user_name = user_name
        self.setWindowTitle("RESERVATION HISTORY")
        self.setMinimumSize(1100, 600)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Título
        title = QLabel("RESERVATION HISTORY")
        title.setFont(QFont("Arial", 22, QFont.Bold))
        title.setStyleSheet("color: white; margin-bottom: 5px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Subtítulo con el nombre del usuario
        subtitle = QLabel(f"User: {self.user_name}")
        subtitle.setFont(QFont("Arial", 11))
        subtitle.setStyleSheet("color: #aaaaaa;")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        # Tabla con historial
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Venue", "Date", "Time", "Status", "Type", ""])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.table.setColumnWidth(5, 0)  # Columna invisible para separación
        
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #f5f5f5;
                color: black;
                gridline-color: #e0e0e0;
                border: 1px solid #cccccc;
                border-radius: 3px;
            }
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #e0e0e0;
            }
            QTableWidget::item:alternate {
                background-color: #ffffff;
            }
            QHeaderView::section {
                background-color: #2c2c2c;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
                border-right: 1px solid #444444;
            }
        """)
        layout.addWidget(self.table)
        
        # Botón para cerrar
        close_btn = QPushButton("Back")
        close_btn.setStyleSheet(self.get_button_style())
        close_btn.setMaximumWidth(150)
        close_btn.clicked.connect(self.accept)
        close_layout = QHBoxLayout()
        close_layout.addStretch()
        close_layout.addWidget(close_btn)
        close_layout.addStretch()
        layout.addLayout(close_layout)
        
        self.load_data()
        self.setLayout(layout)
        
    def load_data(self):
        try:
            reservations = database.get_all_reservations()
            # Filtrar solo las reservas del usuario actual
            user_reservations = {k: v for k, v in reservations.items() 
                               if v.get("user") == self.user_name or v.get("user_email") == self.user_name}
            
            if not user_reservations:
                self.table.setRowCount(1)
                empty_item = QTableWidgetItem("No reservations found")
                empty_item.setForeground(QColor("#999999"))
                self.table.setItem(0, 0, empty_item)
                return
            
            self.table.setRowCount(len(user_reservations))
            
            for i, (rid, res) in enumerate(user_reservations.items()):
                venue_name = res.get("venue_name", "Unknown")
                date = res.get("date", "N/A")
                time = res.get("time", "N/A")
                status = res.get("status", "unknown")
                
                # Determinar el tipo (Confirmed o Cancelled)
                is_cancelled = status == "cancelled"
                status_type = "Cancelled" if is_cancelled else "Confirmed"
                
                # Crear items de la tabla
                venue_item = QTableWidgetItem(venue_name)
                date_item = QTableWidgetItem(date)
                time_item = QTableWidgetItem(time)
                status_item = QTableWidgetItem(status.capitalize())
                type_item = QTableWidgetItem(status_type)
                
                # Aplicar colores según el estado
                if is_cancelled:
                    # Rojo para canceladas
                    for item in [venue_item, date_item, time_item, status_item]:
                        item.setForeground(QColor("#cc6666"))
                    type_item.setForeground(QColor("#ff4444"))
                    font = QFont()
                    font.setBold(True)
                    type_item.setFont(font)
                else:
                    # Verde para confirmadas
                    for item in [venue_item, date_item, time_item, status_item]:
                        item.setForeground(QColor("#333333"))
                    type_item.setForeground(QColor("#4CAF50"))
                    font = QFont()
                    font.setBold(True)
                    type_item.setFont(font)
                
                # Agregar items a la tabla
                self.table.setItem(i, 0, venue_item)
                self.table.setItem(i, 1, date_item)
                self.table.setItem(i, 2, time_item)
                self.table.setItem(i, 3, status_item)
                self.table.setItem(i, 4, type_item)
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error loading history: {str(e)}")

