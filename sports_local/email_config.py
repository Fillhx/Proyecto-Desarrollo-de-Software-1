"""
Configuración para envío de emails
Actualiza estos valores con tus credenciales
"""

# Configuración de SMTP para Gmail
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# IMPORTANTE: Usa una contraseña de aplicación de Google, no tu contraseña normal
# Obtén una en: https://myaccount.google.com/apppasswords
SENDER_EMAIL = "ranyavesports@gmail.com"
SENDER_PASSWORD = "gpetcgusgwwctjoy"

# Asunto y contenido del email
EMAIL_SUBJECT = "¡Bienvenido a Ranyave Sports!"

def get_welcome_email_body(name, email):
    """Genera el cuerpo del email de bienvenida"""
    return f"""
    <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #1e3a5f; color: white; padding: 20px; text-align: center; border-radius: 5px; }}
                .content {{ margin-top: 20px; line-height: 1.6; }}
                .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>¡Bienvenido a Ranyave Sports!</h1>
                </div>
                <div class="content">
                    <p>Hola <strong>{name}</strong>,</p>
                    <p>Tu registro en Ranyave Sports ha sido completado exitosamente.</p>
                    <p><strong>Correo registrado:</strong> {email}</p>
                    <p>Ahora puedes acceder a la plataforma y reservar tus escenarios deportivos favoritos.</p>
                    <p>Si tienes cualquier pregunta, no dudes en contactarnos.</p>
                    <p>¡Que disfrutes tu experiencia con nosotros!</p>
                </div>
                <div class="footer">
                    <p>© 2025 Ranyave Sports. Todos los derechos reservados.</p>
                </div>
            </div>
        </body>
    </html>
    """

def get_reservation_email_body(name, venue_name, date, time, price):
    """Genera el cuerpo del email de confirmación de reserva"""
    return f"""
    <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #1e3a5f; color: white; padding: 20px; text-align: center; border-radius: 5px; }}
                .content {{ margin-top: 20px; line-height: 1.6; }}
                .details {{ background-color: #f5f5f5; padding: 15px; border-left: 4px solid #1e3a5f; margin: 20px 0; }}
                .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>✅ Reserva Confirmada</h1>
                </div>
                <div class="content">
                    <p>Hola <strong>{name}</strong>,</p>
                    <p>Tu reserva en Ranyave Sports ha sido confirmada exitosamente.</p>
                    
                    <div class="details">
                        <h3>Detalles de tu reserva:</h3>
                        <p><strong>Escenario:</strong> {venue_name}</p>
                        <p><strong>Fecha:</strong> {date}</p>
                        <p><strong>Hora:</strong> {time}</p>
                        <p><strong>Precio:</strong> ${price:.2f}</p>
                    </div>
                    
                    <p>Recuerda llegar con 10 minutos de anticipación. ¡Que disfrutes tu experiencia!</p>
                    <p>Para cualquier duda, contacta con nuestro equipo de soporte.</p>
                </div>
                <div class="footer">
                    <p>© 2025 Ranyave Sports. Todos los derechos reservados.</p>
                </div>
            </div>
        </body>
    </html>
    """

def get_cancellation_email_body(name, venue_name, date, time, price):
    """Genera el cuerpo del email de cancelación de reserva"""
    return f"""
    <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #dc3545; color: white; padding: 20px; text-align: center; border-radius: 5px; }}
                .content {{ margin-top: 20px; line-height: 1.6; }}
                .details {{ background-color: #f5f5f5; padding: 15px; border-left: 4px solid #dc3545; margin: 20px 0; }}
                .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>⚠️ Reserva Cancelada</h1>
                </div>
                <div class="content">
                    <p>Hola <strong>{name}</strong>,</p>
                    <p>Tu reserva en Ranyave Sports ha sido cancelada.</p>
                    
                    <div class="details">
                        <h3>Detalles de la cancelación:</h3>
                        <p><strong>Escenario:</strong> {venue_name}</p>
                        <p><strong>Fecha:</strong> {date}</p>
                        <p><strong>Hora:</strong> {time}</p>
                        <p><strong>Reembolso:</strong> ${price:.2f}</p>
                    </div>
                    
                    <p>El monto será reembolsado a tu método de pago en 3-5 días hábiles.</p>
                    <p>Si deseas volver a reservar, estaremos encantados de ayudarte.</p>
                </div>
                <div class="footer">
                    <p>© 2025 Ranyave Sports. Todos los derechos reservados.</p>
                </div>
            </div>
        </body>
    </html>
    """
