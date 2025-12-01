import uuid
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QTableWidget, QTableWidgetItem, QFormLayout,
                             QHeaderView, QSpinBox, QDateEdit, QTimeEdit, QMessageBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QDate, QTime
import database

class BaseDialog(QDialog):
    """Clase base para diálogos con estilos personalizados"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #1e3a5f;")
        
    @staticmethod
    def get_button_style():
        return """
            QPushButton {
                background-color: white;
                border: 1px solid #ccc;
                padding: 8px 16px;
                font-weight: bold;
                min-width: 80px;
                border-radius: 3px;
                color: black;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
        """
    
    @staticmethod
    def get_input_style():
        return """
            QLineEdit, QSpinBox, QDateEdit, QTimeEdit {
                background-color: white;
                border: 1px solid #ccc;
                padding: 5px;
                border-radius: 3px;
                color: black;
            }
        """
    
    @staticmethod
    def get_label_style():
        return "color: white; font-size: 14px; font-family: Arial; font-weight: bold;"

class EventsManagerDialog(BaseDialog):
    """Diálogo para gestionar eventos (Crear y Listar)"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("EVENTS MANAGER")
        self.setMinimumSize(1200, 700)
        self.init_ui()
        
    def init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(30)
        
        # ===================================================================
        # LEFT SIDE: NEW EVENTS FORM
        # ===================================================================
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(10, 10, 10, 10)
        
        title_new = QLabel("NEW EVENTS")
        title_new.setFont(QFont("Arial", 20, QFont.Bold))
        title_new.setStyleSheet("color: white;")
        title_new.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(title_new)
        
        left_layout.addSpacing(20)
        
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignLeft)
        
        # Name
        self.name_input = QLineEdit()
        self.name_input.setStyleSheet(self.get_input_style())
        form_layout.addRow(QLabel("Name", styleSheet=self.get_label_style()), self.name_input)
        
        # Schedule - Date and Time widgets
        schedule_label = QLabel("Schedule Date", styleSheet=self.get_label_style())
        self.schedule_date = QDateEdit()
        self.schedule_date.setCalendarPopup(True)
        self.schedule_date.setStyleSheet(self.get_input_style())
        form_layout.addRow(schedule_label, self.schedule_date)
        
        time_label = QLabel("Schedule Time", styleSheet=self.get_label_style())
        self.schedule_time = QTimeEdit()
        self.schedule_time.setStyleSheet(self.get_input_style())
        form_layout.addRow(time_label, self.schedule_time)
        
        # Location
        self.location_input = QLineEdit()
        self.location_input.setStyleSheet(self.get_input_style())
        form_layout.addRow(QLabel("Location", styleSheet=self.get_label_style()), self.location_input)
        
        # Capacity
        self.capacity_input = QSpinBox()
        self.capacity_input.setRange(1, 100000)
        self.capacity_input.setStyleSheet(self.get_input_style())
        form_layout.addRow(QLabel("Capacity", styleSheet=self.get_label_style()), self.capacity_input)
        
        left_layout.addLayout(form_layout)
        
        left_layout.addSpacing(30)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(20)
        btn_layout.setAlignment(Qt.AlignCenter)
        
        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(self.get_button_style())
        back_btn.clicked.connect(self.reject)
        btn_layout.addWidget(back_btn)
        
        save_btn = QPushButton("Save")
        save_btn.setStyleSheet(self.get_button_style())
        save_btn.clicked.connect(self.save_event)
        btn_layout.addWidget(save_btn)
        
        left_layout.addLayout(btn_layout)
        left_layout.addStretch()
        
        layout.addLayout(left_layout, 1)
        
        # ===================================================================
        # RIGHT SIDE: INFO EVENTS TABLE
        # ===================================================================
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(10, 10, 10, 10)
        
        title_info = QLabel("INFO EVENTS")
        title_info.setFont(QFont("Arial", 20, QFont.Bold))
        title_info.setStyleSheet("color: white;")
        title_info.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(title_info)
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Name", "Schedule", "Location", "Capacity"])
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
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        right_layout.addWidget(self.table)
        
        # Delete Button
        delete_btn = QPushButton("Delete")
        delete_btn.setStyleSheet(self.get_button_style())
        delete_btn.clicked.connect(self.delete_event)
        right_layout.addWidget(delete_btn, alignment=Qt.AlignCenter)
        
        layout.addLayout(right_layout, 2)
        
        self.setLayout(layout)
        self.load_events()
        
    def save_event(self):
        name = self.name_input.text().strip()
        location = self.location_input.text().strip()
        capacity = self.capacity_input.value()
        
        # Obtener fecha y hora del calendario y reloj de tiempo
        date_str = self.schedule_date.date().toString("yyyy-MM-dd")
        time_str = self.schedule_time.time().toString("HH:mm")
        schedule = f"{date_str} {time_str}"
        
        if not all([name, location]):
            QMessageBox.warning(self, "Error", "Please fill all fields")
            return
            
        event_id = str(uuid.uuid4())
        event_data = {
            "id": event_id,
            "name": name,
            "schedule": schedule,
            "location": location,
            "capacity": capacity
        }
        
        database.create_event(event_data)
        self.clear_form()
        self.load_events()
        QMessageBox.information(self, "Success", "Event created successfully!")
        
    def load_events(self):
        self.events = database.get_all_events()
        self.table.setRowCount(len(self.events))
        
        for i, (eid, event) in enumerate(self.events.items()):
            self.table.setItem(i, 0, QTableWidgetItem(event["name"]))
            self.table.setItem(i, 1, QTableWidgetItem(event["schedule"]))
            self.table.setItem(i, 2, QTableWidgetItem(event["location"]))
            self.table.setItem(i, 3, QTableWidgetItem(str(event["capacity"])))
            self.table.item(i, 0).setData(Qt.UserRole, eid)
            
    def delete_event(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Please select an event to delete")
            return
            
        event_id = self.table.item(current_row, 0).data(Qt.UserRole)
        
        reply = QMessageBox.question(self, 'Confirm', 
                                   'Are you sure you want to delete this event?',
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            database.delete_event(event_id)
            self.load_events()
            
    def clear_form(self):
        self.name_input.clear()
        self.schedule_date.setDate(QDate.currentDate())
        self.schedule_time.setTime(QTime(12, 0))
        self.location_input.clear()
        self.capacity_input.setValue(1)
