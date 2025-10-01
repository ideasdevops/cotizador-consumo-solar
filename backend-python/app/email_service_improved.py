"""
Servicio de Email Mejorado para Cotizador Solar
Usa Nodemailer con templates HTML profesionales
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Optional, Dict, Any
import logging
import json
from datetime import datetime
from .config import settings

logger = logging.getLogger(__name__)

class ImprovedEmailService:
    def __init__(self):
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.username = settings.SMTP_USERNAME
        self.password = settings.SMTP_PASSWORD
        self.use_tls = settings.SMTP_USE_TLS
        self.use_ssl = settings.SMTP_USE_SSL
        self.contact_email = settings.CONTACT_EMAIL
        
    def send_solar_quote_email(self, 
                              to_email: str, 
                              customer_name: str, 
                              quote_data: Dict[str, Any],
                              pdf_path: Optional[str] = None) -> bool:
        """
        Envía email con cotización solar al cliente
        """
        try:
            # Crear mensaje
            msg = MIMEMultipart()
            msg['From'] = f"Sumpetrol Solar <{self.username}>"
            msg['To'] = to_email
            msg['Subject'] = f"🌞 Cotización Solar Personalizada - {customer_name}"
            
            # Cuerpo del email
            body = self._create_solar_quote_email_body(customer_name, quote_data)
            msg.attach(MIMEText(body, 'html', 'utf-8'))
            
            # Adjuntar PDF si existe
            if pdf_path:
                self._attach_pdf(msg, pdf_path)
            
            # Enviar email
            return self._send_email(msg)
            
        except Exception as e:
            logger.error(f"Error enviando email de cotización solar: {e}")
            return False
    
    def send_contact_form_email(self, 
                               name: str, 
                               email: str, 
                               phone: str, 
                               message: str) -> bool:
        """
        Envía email de formulario de contacto
        """
        try:
            # Email al cliente
            client_msg = MIMEMultipart()
            client_msg['From'] = f"Sumpetrol Solar <{self.username}>"
            client_msg['To'] = email
            client_msg['Subject'] = "✅ Consulta recibida - Sumpetrol Solar"
            
            client_body = self._create_contact_confirmation_body(name)
            client_msg.attach(MIMEText(client_body, 'html', 'utf-8'))
            
            # Email interno
            internal_msg = MIMEMultipart()
            internal_msg['From'] = self.username
            internal_msg['To'] = self.contact_email
            internal_msg['Subject'] = f"🔔 Nueva consulta solar - {name}"
            
            internal_body = self._create_contact_internal_body(name, email, phone, message)
            internal_msg.attach(MIMEText(internal_body, 'html', 'utf-8'))
            
            # Enviar ambos emails
            client_sent = self._send_email(client_msg)
            internal_sent = self._send_email(internal_msg)
            
            return client_sent and internal_sent
            
        except Exception as e:
            logger.error(f"Error enviando email de contacto: {e}")
            return False
    
    def send_quote_notification_email(self, quote_data: Dict[str, Any]) -> bool:
        """
        Envía notificación interna de nueva cotización
        """
        try:
            msg = MIMEMultipart()
            msg['From'] = self.username
            msg['To'] = self.contact_email
            msg['Subject'] = f"📊 Nueva cotización solar - {quote_data.get('client_name', 'Cliente')}"
            
            body = self._create_quote_notification_body(quote_data)
            msg.attach(MIMEText(body, 'html', 'utf-8'))
            
            return self._send_email(msg)
            
        except Exception as e:
            logger.error(f"Error enviando notificación de cotización: {e}")
            return False
    
    def _create_solar_quote_email_body(self, customer_name: str, quote_data: Dict[str, Any]) -> str:
        """Crear cuerpo del email de cotización solar"""
        design = quote_data.get('design', {})
        
        return f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Cotización Solar - Sumpetrol</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #f97316, #ea580c); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: white; padding: 30px; border: 1px solid #e5e7eb; }}
                .footer {{ background: #1f2937; color: white; padding: 20px; text-align: center; border-radius: 0 0 10px 10px; }}
                .quote-summary {{ background: #f9fafb; padding: 20px; border-radius: 8px; margin: 20px 0; }}
                .quote-item {{ display: flex; justify-content: space-between; margin: 10px 0; padding: 10px; background: white; border-radius: 5px; }}
                .quote-label {{ font-weight: 600; color: #374151; }}
                .quote-value {{ color: #1f2937; font-weight: 700; }}
                .cta-button {{ background: #f97316; color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; display: inline-block; margin: 20px 0; }}
                .contact-info {{ background: #e5f3ff; padding: 15px; border-radius: 8px; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🌞 Cotización Solar Personalizada</h1>
                    <p>Estimado/a {customer_name}</p>
                </div>
                
                <div class="content">
                    <p>Gracias por confiar en Sumpetrol para tu proyecto de energía solar. Hemos preparado una cotización personalizada basada en tus necesidades específicas.</p>
                    
                    <div class="quote-summary">
                        <h3>📊 Resumen de tu Sistema Solar</h3>
                        <div class="quote-item">
                            <span class="quote-label">Potencia del Sistema:</span>
                            <span class="quote-value">{design.get('required_power_kwp', 'N/A')} kWp</span>
                        </div>
                        <div class="quote-item">
                            <span class="quote-label">Cantidad de Paneles:</span>
                            <span class="quote-value">{design.get('panel_count', 'N/A')} unidades</span>
                        </div>
                        <div class="quote-item">
                            <span class="quote-label">Generación Mensual:</span>
                            <span class="quote-value">{design.get('monthly_generation_kwh', 'N/A')} kWh</span>
                        </div>
                        <div class="quote-item">
                            <span class="quote-label">Ahorro Mensual:</span>
                            <span class="quote-value">${design.get('monthly_savings', 'N/A'):,.0f}</span>
                        </div>
                        <div class="quote-item">
                            <span class="quote-label">Inversión Total:</span>
                            <span class="quote-value">${design.get('total_investment', 'N/A'):,.0f}</span>
                        </div>
                        <div class="quote-item">
                            <span class="quote-label">Retorno de Inversión:</span>
                            <span class="quote-value">{design.get('payback_years', 'N/A')} años</span>
                        </div>
                    </div>
                    
                    <p>Esta cotización es válida por 30 días y incluye:</p>
                    <ul>
                        <li>✅ Paneles solares de alta eficiencia</li>
                        <li>✅ Inversores de última generación</li>
                        <li>✅ Sistema de montaje profesional</li>
                        <li>✅ Instalación completa</li>
                        <li>✅ Garantía extendida</li>
                        <li>✅ Monitoreo del sistema</li>
                    </ul>
                    
                    <div class="contact-info">
                        <h4>📞 ¿Tienes preguntas?</h4>
                        <p>Nuestro equipo de expertos está listo para ayudarte:</p>
                        <p><strong>Teléfono:</strong> +54 9 261 7110120</p>
                        <p><strong>Email:</strong> ventas@sumpetrol.com.ar</p>
                        <p><strong>Asistente 24/7:</strong> Disponible en nuestro sitio web</p>
                    </div>
                    
                    <div style="text-align: center;">
                        <a href="https://sumpetrol.com.ar" class="cta-button">Ver más información</a>
                    </div>
                </div>
                
                <div class="footer">
                    <p><strong>Sumpetrol Argentina</strong></p>
                    <p>Acceso Sur - Lateral Este 4585, Luján de Cuyo, Mendoza</p>
                    <p>Vicente Lazaretti 903 - Cipolletti, Río Negro</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _create_contact_confirmation_body(self, name: str) -> str:
        """Crear cuerpo del email de confirmación de contacto"""
        return f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Consulta Recibida - Sumpetrol</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #f97316, #ea580c); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: white; padding: 30px; border: 1px solid #e5e7eb; }}
                .footer {{ background: #1f2937; color: white; padding: 20px; text-align: center; border-radius: 0 0 10px 10px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>✅ Consulta Recibida</h1>
                    <p>Estimado/a {name}</p>
                </div>
                
                <div class="content">
                    <p>Hemos recibido tu consulta sobre energía solar y nuestro equipo de expertos se pondrá en contacto contigo en las próximas 24 horas.</p>
                    
                    <p>Mientras tanto, puedes:</p>
                    <ul>
                        <li>🌞 Usar nuestra calculadora solar online</li>
                        <li>📚 Revisar nuestros tipos de sistemas</li>
                        <li>💬 Chatear con nuestro asistente 24/7</li>
                    </ul>
                    
                    <p><strong>Gracias por elegir Sumpetrol para tu proyecto de energía solar.</strong></p>
                </div>
                
                <div class="footer">
                    <p><strong>Sumpetrol Argentina</strong></p>
                    <p>+54 9 261 7110120 | ventas@sumpetrol.com.ar</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _create_contact_internal_body(self, name: str, email: str, phone: str, message: str) -> str:
        """Crear cuerpo del email interno de contacto"""
        return f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Nueva Consulta Solar</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #1f2937; color: white; padding: 20px; text-align: center; }}
                .content {{ background: white; padding: 20px; border: 1px solid #e5e7eb; }}
                .info-item {{ margin: 15px 0; padding: 10px; background: #f9fafb; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔔 Nueva Consulta Solar</h1>
                    <p>{datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
                </div>
                
                <div class="content">
                    <div class="info-item">
                        <strong>Nombre:</strong> {name}
                    </div>
                    <div class="info-item">
                        <strong>Email:</strong> {email}
                    </div>
                    <div class="info-item">
                        <strong>Teléfono:</strong> {phone or 'No proporcionado'}
                    </div>
                    <div class="info-item">
                        <strong>Mensaje:</strong><br>
                        {message}
                    </div>
                    
                    <p><strong>Acción requerida:</strong> Contactar al cliente en las próximas 24 horas.</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _create_quote_notification_body(self, quote_data: Dict[str, Any]) -> str:
        """Crear cuerpo del email de notificación de cotización"""
        return f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Nueva Cotización Solar</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #1f2937; color: white; padding: 20px; text-align: center; }}
                .content {{ background: white; padding: 20px; border: 1px solid #e5e7eb; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📊 Nueva Cotización Solar Generada</h1>
                    <p>{datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
                </div>
                
                <div class="content">
                    <p><strong>Cliente:</strong> {quote_data.get('client_name', 'N/A')}</p>
                    <p><strong>Email:</strong> {quote_data.get('client_email', 'N/A')}</p>
                    <p><strong>Teléfono:</strong> {quote_data.get('client_phone', 'N/A')}</p>
                    <p><strong>Ubicación:</strong> {quote_data.get('location', 'N/A')}</p>
                    <p><strong>Consumo Mensual:</strong> {quote_data.get('monthly_consumption_kwh', 'N/A')} kWh</p>
                    <p><strong>Inversión Estimada:</strong> ${quote_data.get('design', {}).get('total_investment', 'N/A'):,.0f}</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _attach_pdf(self, msg: MIMEMultipart, pdf_path: str):
        """Adjuntar archivo PDF al email"""
        try:
            with open(pdf_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {pdf_path.split("/")[-1]}'
            )
            msg.attach(part)
        except Exception as e:
            logger.error(f"Error adjuntando PDF: {e}")
    
    def _send_email(self, msg: MIMEMultipart) -> bool:
        """Enviar email usando SMTP"""
        try:
            if self.use_ssl:
                server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
            else:
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                if self.use_tls:
                    server.starttls()
            
            server.login(self.username, self.password)
            text = msg.as_string()
            server.sendmail(self.username, msg['To'], text)
            server.quit()
            
            logger.info(f"Email enviado exitosamente a {msg['To']}")
            return True
            
        except Exception as e:
            logger.error(f"Error enviando email: {e}")
            return False

# Instancia global del servicio mejorado
improved_email_service = ImprovedEmailService()
