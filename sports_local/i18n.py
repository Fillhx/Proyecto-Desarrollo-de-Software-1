# -*- coding: utf-8 -*-
"""
Sistema de internacionalización (i18n) para la aplicación Sports Local
Permite cambiar entre inglés y español dinámicamente
"""

import json
import os
from PyQt5.QtCore import QObject, pyqtSignal

class LanguageManager(QObject):
    """Gestor centralizado de idiomas"""
    
    # Señal emitida cuando cambia el idioma
    language_changed = pyqtSignal(str)
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LanguageManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        super().__init__()
        self._initialized = True
        self.current_language = "es"  # Idioma por defecto
        self.translations = self._load_translations()
    
    def _load_translations(self):
        """Carga el archivo de traducciones"""
        translations = {
            "es": {
                # Login
                "login_title": "👤 INICIAR SESIÓN",
                "login_email": "📧 Correo",
                "login_email_placeholder": "ejemplo@correo.com",
                "login_password": "🔒 Contraseña",
                "login_next": "Siguiente ➡️",
                "login_back": "⬅️ Atrás",
                "login_register_text": "¿No tienes cuenta? <a href='#' style='color: white; text-decoration: underline;'><b>Regístrate aquí</b></a>",
                "login_error_empty": "Por favor completa todos los campos",
                "login_error_invalid_email": "Por favor ingresa un email válido",
                "login_error_invalid_credentials": "Email o contraseña incorrectos",
                "error": "Error",
                "warning": "Advertencia",
                "information": "Información",
                
                # Registro
                "register_title": "📝 REGISTRO",
                "register_name": "👤 Nombre",
                "register_name_placeholder": "Tu Nombre Completo",
                "register_email": "📧 Correo",
                "register_email_placeholder": "ejemplo@correo.com",
                "register_phone": "📱 Número de Celular",
                "register_phone_placeholder": "1234567890",
                "register_password": "🔒 Contraseña",
                "register_next": "Siguiente ➡️",
                "register_back": "⬅️ Atrás",
                "register_error_empty": "Por favor completa todos los campos",
                "register_error_invalid_email": "Por favor ingresa un email válido",
                "register_error_invalid_phone": "Por favor ingresa un teléfono válido (10+ dígitos)",
                "register_error_weak_password": "La contraseña debe tener al menos 6 caracteres",
                "register_error_email_exists": "Este email ya está registrado",
                "register_success_admin": "¡Bienvenido {name}!\nTu registro fue completado como administrador. Ahora puedes iniciar sesión.",
                "register_success_user": "¡Bienvenido {name}!\nTu registro fue completado como usuario. Ahora puedes iniciar sesión.",
                "register_error": "Error al registrar usuario",
                
                # Admin Panel
                "admin_title": "🛠️ GESTIÓN DE ADMINISTRADOR",
                "admin_label": "ADMIN",
                "admin_new_stages": "NUEVOS ESCENARIOS 🏟️",
                "admin_stages_info": "INFO ESCENARIOS ℹ️",
                "admin_reservations": "RESERVAS 📅",
                "admin_manage_sports": "GESTIONAR DEPORTES 🏆",
                "admin_manage_events": "GESTIONAR EVENTOS 📅",
                "admin_manage_users": "GESTIONAR USUARIOS 👥",
                "admin_view_history": "VER HISTORIAL 📊",
                "admin_logout": "CERRAR SESIÓN 🚪",
                "admin_back": "⬅️ Volver al inicio",
                "admin_session": "Sesión: {name}",
                
                # User Panel
                "user_title": "🏃 PANEL DE USUARIO",
                "user_label": "USUARIO",
                "user_view_events": "VER EVENTOS 📅",
                "user_view_history": "VER MIS ACTIVIDADES 📊",
                "user_profile": "MI PERFIL 👤",
                "user_logout": "CERRAR SESIÓN 🚪",
                "user_back": "⬅️ Volver al inicio",
                "user_session": "Sesión: {name}",
                "user_reserve": "RESERVAR 📅",
                "user_my_reservations": "MIS RESERVAS 📋",
                "user_history": "HISTORIAL 📜",
                
                # Venue/Sport Stage dialogs
                "venue_title": "🏟️ NUEVO ESCENARIO DEPORTIVO",
                "venue_subtitle": "📝 Complete todos los campos para crear un nuevo escenario deportivo",
                "venue_name": "📋 Nombre del Escenario",
                "venue_name_placeholder": "e.g., Cancha de Fútbol A",
                "venue_type": "⚽ Tipo",
                "venue_location": "📍 Ubicación",
                "venue_location_placeholder": "e.g., Zona B, Edificio 3",
                "venue_capacity": "👥 Capacidad",
                "venue_schedule_date": "📅 Fecha Programada",
                "venue_schedule_time": "🕐 Hora Programada",
                "venue_price": "💵 Precio ($)",
                "venue_save": "Guardar Escenario 💾",
                "venue_cancel": "Cancelar ❌",
                
                # Reservation dialogs (User)
                "reservation_title": "📅 RESERVAR ESCENARIO DEPORTIVO",
                "reservation_subtitle": "Selecciona un escenario disponible de la tabla y haz clic en 'Reservar'",
                "reservation_table_headers": "Nombre|Tipo|Ubicación|Capacidad|Fecha|Hora|Precio",
                "reservation_back": "⬅️ Volver",
                "reservation_reserve_btn": "Reservar ✅",
                "reservation_error_no_venues": "No hay escenarios disponibles",
                "reservation_error_select": "Por favor selecciona un escenario para reservar",
                "reservation_error_invalid_schedule": "Formato de horario inválido",
                "reservation_error_already_reserved": "Este escenario ya está reservado para esta fecha y hora",
                "reservation_payment_error": "El pago no fue procesado",
                "reservation_success": "¡Reserva confirmada!\n\nEscenario: {venue_name}\nFecha: {date}\nHora: {time}\nMonto pagado: ${price}",
                "reservation_success_title": "Éxito",
                
                # My Reservations dialog
                "my_reservations_title": "📋 MIS RESERVAS",
                "my_reservations_table_headers": "Escenario|Fecha|Hora|Estado|Acción",
                "my_reservations_back": "Volver",
                "my_reservations_cancel": "Cancelar",
                "my_reservations_confirm": "¿Estás seguro de que deseas cancelar esta reserva?",
                "my_reservations_confirm_title": "Confirmar",
                "my_reservations_cancelled": "Cancelado",
                
                # Reservation History dialog
                "history_title": "📜 HISTORIAL DE RESERVAS",
                "history_subtitle": "👤 Usuario: {name}",
                "history_table_headers": "Escenario|Fecha|Hora|Estado|Tipo|",
                "history_no_reservations": "No se encontraron reservas",
                "history_back": "⬅️ Volver",
                "history_confirmed": "Confirmado",
                "history_cancelled": "Cancelado",
                
                # Payment dialog
                "payment_title": "💳 PROCESO DE PAGO",
                "payment_amount": "Monto a Pagar:",
                "payment_venue": "Escenario:",
                "payment_card_title": "💳 INFORMACIÓN DE PAGO",
                "payment_card_number": "Número de Tarjeta",
                "payment_card_placeholder": "1234 5678 9012 3456",
                "payment_expiry": "Fecha de Expiración (MM/YY)",
                "payment_expiry_placeholder": "MM/YY",
                "payment_cvv": "CVV",
                "payment_cvv_placeholder": "123",
                "payment_cancel": "Cancelar ❌",
                "payment_confirm": "Procesar Pago ✅",
                "payment_error": "Por favor completa todos los campos de pago",
                
                # Admin Reservations dialog
                "admin_reservations_title": "TODAS LAS RESERVAS",
                "admin_reservations_table": "Usuario|Escenario|Fecha|Hora|Estado|Reservado",
                "admin_reservations_cancel_btn": "Cancelar",
                "admin_reservations_back_btn": "Volver",
                "admin_reservations_confirm": "¿Estás seguro de que deseas cancelar esta reserva?",
                "admin_reservations_confirm_title": "Confirmar",
                
                # Venue Info dialog
                "venue_info_title": "ℹ️ INFORMACIÓN DE ESCENARIOS",
                "venue_info_back": "Volver",
                
                # Venues List dialog
                "venues_list_title": "📋 LISTA DE ESCENARIOS",
                "venues_list_subtitle": "Haga clic en un escenario para editar o eliminar",
                "venues_list_edit_title": "✏️ EDITAR INFO ESCENARIO",
                "venues_list_table": "Id|Nombre|Tipo|Ubicación|Capacidad|Horario|Precio",
                "venues_list_back": "Cancelar ❌",
                "venues_list_save": "Guardar Cambios 💾",
                "venues_list_delete": "Eliminar 🗑️",
                "venues_list_name": "📋 Nombre del Escenario",
                "venues_list_type": "⚽ Tipo",
                "venues_list_location": "📍 Ubicación",
                "venues_list_capacity": "👥 Capacidad",
                "venues_list_date": "📅 Fecha Programada",
                "venues_list_time": "🕐 Hora Programada",
                "venues_list_price": "💵 Precio ($)",
                "venues_list_delete_confirm": "¿Estás seguro de que deseas eliminar este escenario?",
                "venues_list_delete_confirm_title": "Confirmar eliminación",
                "venues_list_delete_success": "Escenario eliminado exitosamente",
                "venues_list_save_success": "Cambios guardados exitosamente",
                
                # Eventos
                "events_title": "EVENTOS",
                "events_add": "Agregar Evento",
                "events_edit": "Editar",
                "events_delete": "Eliminar",
                "events_save": "Guardar",
                "events_cancel": "Cancelar",
                "events_date": "Fecha",
                "events_time": "Hora",
                "events_location": "Ubicación",
                "events_sport": "Deporte",
                "events_capacity": "Capacidad",
                "events_price": "Precio",
                "events_description": "Descripción",
                "events_participants": "Participantes",
                
                # General
                "welcome": "Bienvenido",
                "logout_success": "Has cerrado sesión",
                "cancel": "Cancelar",
                "save": "Guardar",
                "delete": "Eliminar",
                "edit": "Editar",
                "add": "Agregar",
                "search": "Buscar",
                "filter": "Filtrar",
                "english": "English",
                "spanish": "Español",
            },
            "en": {
                # Login
                "login_title": "👤 SIGN IN",
                "login_email": "📧 Email",
                "login_email_placeholder": "example@email.com",
                "login_password": "🔒 Password",
                "login_next": "Next ➡️",
                "login_back": "⬅️ Back",
                "login_register_text": "Don't have an account? <a href='#' style='color: white; text-decoration: underline;'><b>Register here</b></a>",
                "login_error_empty": "Please complete all fields",
                "login_error_invalid_email": "Please enter a valid email",
                "login_error_invalid_credentials": "Email or password incorrect",
                "error": "Error",
                "warning": "Warning",
                "information": "Information",
                
                # Registro
                "register_title": "📝 REGISTRATION",
                "register_name": "👤 Name",
                "register_name_placeholder": "Your Full Name",
                "register_email": "📧 Email",
                "register_email_placeholder": "example@email.com",
                "register_phone": "📱 Cell Phone Number",
                "register_phone_placeholder": "1234567890",
                "register_password": "🔒 Password",
                "register_next": "Next ➡️",
                "register_back": "⬅️ Back",
                "register_error_empty": "Please complete all fields",
                "register_error_invalid_email": "Please enter a valid email",
                "register_error_invalid_phone": "Please enter a valid phone number (10+ digits)",
                "register_error_weak_password": "Password must have at least 6 characters",
                "register_error_email_exists": "This email is already registered",
                "register_success_admin": "Welcome {name}!\nYour registration was completed as administrator. You can now sign in.",
                "register_success_user": "Welcome {name}!\nYour registration was completed as user. You can now sign in.",
                "register_error": "Error registering user",
                
                # Admin Panel
                "admin_title": "🛠️ ADMIN MANAGEMENT",
                "admin_label": "ADMIN",
                "admin_new_stages": "NEW SCENARIOS 🏟️",
                "admin_stages_info": "SCENARIOS INFO ℹ️",
                "admin_reservations": "RESERVATIONS 📅",
                "admin_manage_sports": "MANAGE SPORTS 🏆",
                "admin_manage_events": "MANAGE EVENTS 📅",
                "admin_manage_users": "MANAGE USERS 👥",
                "admin_view_history": "VIEW HISTORY 📊",
                "admin_logout": "SIGN OUT 🚪",
                "admin_back": "⬅️ Back to start",
                "admin_session": "Session: {name}",
                
                # User Panel
                "user_title": "🏃 USER PANEL",
                "user_label": "USER",
                "user_view_events": "VIEW EVENTS 📅",
                "user_view_history": "VIEW MY ACTIVITIES 📊",
                "user_profile": "MY PROFILE 👤",
                "user_logout": "SIGN OUT 🚪",
                "user_back": "⬅️ Back to start",
                "user_session": "Session: {name}",
                "user_reserve": "RESERVE 📅",
                "user_my_reservations": "MY RESERVATIONS 📋",
                "user_history": "HISTORY 📜",
                
                # Venue/Sport Stage dialogs
                "venue_title": "🏟️ NEW SPORT STAGE",
                "venue_subtitle": "📝 Complete all fields to create a new sports venue",
                "venue_name": "📋 Venue Name",
                "venue_name_placeholder": "e.g., Soccer Field A",
                "venue_type": "⚽ Type",
                "venue_location": "📍 Location",
                "venue_location_placeholder": "e.g., Zone B, Building 3",
                "venue_capacity": "👥 Capacity",
                "venue_schedule_date": "📅 Scheduled Date",
                "venue_schedule_time": "🕐 Scheduled Time",
                "venue_price": "💵 Price ($)",
                "venue_save": "Save Venue 💾",
                "venue_cancel": "Cancel ❌",
                
                # Reservation dialogs (User)
                "reservation_title": "📅 RESERVE SPORTS VENUE",
                "reservation_subtitle": "Select an available venue from the table and click 'Reserve'",
                "reservation_table_headers": "Name|Type|Location|Capacity|Date|Time|Price",
                "reservation_back": "⬅️ Back",
                "reservation_reserve_btn": "Reserve ✅",
                "reservation_error_no_venues": "No available venues",
                "reservation_error_select": "Please select a venue to reserve",
                "reservation_error_invalid_schedule": "Invalid schedule format",
                "reservation_error_already_reserved": "This venue is already reserved for this date and time",
                "reservation_payment_error": "Payment was not processed",
                "reservation_success": "Reservation confirmed!\n\nVenue: {venue_name}\nDate: {date}\nTime: {time}\nAmount paid: ${price}",
                "reservation_success_title": "Success",
                
                # My Reservations dialog
                "my_reservations_title": "📋 MY RESERVATIONS",
                "my_reservations_table_headers": "Venue|Date|Time|Status|Action",
                "my_reservations_back": "Back",
                "my_reservations_cancel": "Cancel",
                "my_reservations_confirm": "Are you sure you want to cancel this reservation?",
                "my_reservations_confirm_title": "Confirm",
                "my_reservations_cancelled": "Cancelled",
                
                # Reservation History dialog
                "history_title": "📜 RESERVATION HISTORY",
                "history_subtitle": "👤 User: {name}",
                "history_table_headers": "Venue|Date|Time|Status|Type|",
                "history_no_reservations": "No reservations found",
                "history_back": "⬅️ Back",
                "history_confirmed": "Confirmed",
                "history_cancelled": "Cancelled",
                
                # Payment dialog
                "payment_title": "💳 PAYMENT PROCESS",
                "payment_amount": "Amount to Pay:",
                "payment_venue": "Venue:",
                "payment_card_title": "💳 PAYMENT INFORMATION",
                "payment_card_number": "Card Number",
                "payment_card_placeholder": "1234 5678 9012 3456",
                "payment_expiry": "Expiration Date (MM/YY)",
                "payment_expiry_placeholder": "MM/YY",
                "payment_cvv": "CVV",
                "payment_cvv_placeholder": "123",
                "payment_cancel": "Cancel ❌",
                "payment_confirm": "Process Payment ✅",
                "payment_error": "Please complete all payment fields",
                
                # Admin Reservations dialog
                "admin_reservations_title": "ALL RESERVATIONS",
                "admin_reservations_table": "User|Venue|Date|Time|Status|Reserved",
                "admin_reservations_cancel_btn": "Cancel",
                "admin_reservations_back_btn": "Back",
                "admin_reservations_confirm": "Are you sure you want to cancel this reservation?",
                "admin_reservations_confirm_title": "Confirm",
                
                # Venue Info dialog
                "venue_info_title": "ℹ️ VENUES INFORMATION",
                "venue_info_back": "Back",
                
                # Venues List dialog
                "venues_list_title": "📋 VENUES LIST",
                "venues_list_subtitle": "Click on a venue to edit or delete",
                "venues_list_edit_title": "✏️ EDIT VENUE INFO",
                "venues_list_table": "Id|Name|Type|Location|Capacity|Schedule|Price",
                "venues_list_back": "Cancel ❌",
                "venues_list_save": "Save Changes 💾",
                "venues_list_delete": "Delete 🗑️",
                "venues_list_name": "📋 Venue Name",
                "venues_list_type": "⚽ Type",
                "venues_list_location": "📍 Location",
                "venues_list_capacity": "👥 Capacity",
                "venues_list_date": "📅 Scheduled Date",
                "venues_list_time": "🕐 Scheduled Time",
                "venues_list_price": "💵 Price ($)",
                "venues_list_delete_confirm": "Are you sure you want to delete this venue?",
                "venues_list_delete_confirm_title": "Confirm deletion",
                "venues_list_delete_success": "Venue deleted successfully",
                "venues_list_save_success": "Changes saved successfully",
                
                # Eventos
                "events_title": "EVENTS",
                "events_add": "Add Event",
                "events_edit": "Edit",
                "events_delete": "Delete",
                "events_save": "Save",
                "events_cancel": "Cancel",
                "events_date": "Date",
                "events_time": "Time",
                "events_location": "Location",
                "events_sport": "Sport",
                "events_capacity": "Capacity",
                "events_price": "Price",
                "events_description": "Description",
                "events_participants": "Participants",
                
                # General
                "welcome": "Welcome",
                "logout_success": "You have signed out",
                "cancel": "Cancel",
                "save": "Save",
                "delete": "Delete",
                "edit": "Edit",
                "add": "Add",
                "search": "Search",
                "filter": "Filter",
                "english": "English",
                "spanish": "Español",
            }
        }
        return translations
    
    def get(self, key, **kwargs):
        """
        Obtiene una traducción
        
        Args:
            key: Clave de la traducción
            **kwargs: Parámetros para formato (ej: name="Juan")
        
        Returns:
            Texto traducido o clave si no existe
        """
        text = self.translations.get(self.current_language, {}).get(key, key)
        
        # Formato con kwargs si se proporcionan
        if kwargs:
            try:
                text = text.format(**kwargs)
            except (KeyError, ValueError):
                pass
        
        return text
    
    def set_language(self, language_code):
        """
        Cambia el idioma actual
        
        Args:
            language_code: "es" o "en"
        """
        if language_code in self.translations:
            self.current_language = language_code
            self.language_changed.emit(language_code)
            return True
        return False
    
    def get_current_language(self):
        """Retorna el idioma actual"""
        return self.current_language
    
    def get_available_languages(self):
        """Retorna lista de idiomas disponibles"""
        return list(self.translations.keys())


# Instancia global del gestor de idiomas
_language_manager = None

def get_language_manager():
    """Obtiene la instancia global del gestor de idiomas"""
    global _language_manager
    if _language_manager is None:
        _language_manager = LanguageManager()
    return _language_manager

def tr(key, **kwargs):
    """
    Función de traducción global corta
    
    Uso: tr("login_title") o tr("register_success_admin", name="Juan")
    """
    return get_language_manager().get(key, **kwargs)
