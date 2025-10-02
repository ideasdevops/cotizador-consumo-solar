"""
Servicio de Nocodb para Cotizador Solar
Guarda los datos de los clientes y cotizaciones en la base de datos
"""

import aiohttp
import asyncio
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from .config import settings

logger = logging.getLogger(__name__)

class NocodbService:
    def __init__(self):
        # Usar variables correctas de NocoDB
        self.base_url = getattr(settings, 'NC_DB_URL', settings.NOCODB_URL)
        self.token = getattr(settings, 'NC_TOKEN', settings.NOCODB_TOKEN)
        self.base_id = getattr(settings, 'NC_DB_ID', settings.NOCODB_BASE_ID)
        
        # URLs para diferentes tablas con TABLE_IDs reales
        self.contactos_table_id = getattr(settings, 'NOCODB_CONTACTOS_TABLE_ID', 'm6snjo5tgkirewb')
        self.cotizaciones_table_id = getattr(settings, 'NOCODB_COTIZACIONES_TABLE_ID', 'm6rk1j231s70p8m')
        self.materiales_table_id = getattr(settings, 'NOCODB_MATERIALES_TABLE_ID', 'm2p9ng5e1hn53k0')
        self.logs_table_id = getattr(settings, 'NOCODB_LOGS_TABLE_ID', 'm1xm2vu3e5bcuiy')
        
        # URLs de API v2 (sin base_id para v2)
        self.contactos_url = f"{self.base_url}/api/v2/tables/{self.contactos_table_id}/records"
        self.cotizaciones_url = f"{self.base_url}/api/v2/tables/{self.cotizaciones_table_id}/records"
        self.materiales_url = f"{self.base_url}/api/v2/tables/{self.materiales_table_id}/records"
        self.logs_url = f"{self.base_url}/api/v2/tables/{self.logs_table_id}/records"
        
        self.headers = {
            "xc-token": self.token,
            "Content-Type": "application/json"
        }
        
        logger.info(f"NocoDB Service initialized:")
        logger.info(f"Base URL: {self.base_url}")
        logger.info(f"Contactos URL: {self.contactos_url}")
        logger.info(f"Cotizaciones URL: {self.cotizaciones_url}")
        logger.info(f"Materiales URL: {self.materiales_url}")
        logger.info(f"Logs URL: {self.logs_url}")
    
    async def save_contact_form(self, contact_data: Dict[str, Any]) -> bool:
        """
        Guarda formulario de contacto en NocoDB
        """
        try:
            logger.info(f"🔄 Guardando formulario de contacto: {contact_data.get('nombre', 'Sin nombre')}")
            logger.info(f"🔗 URL de contacto: {self.contactos_url}")
            logger.info(f"🔑 Token: {self.token[:10]}...")
            logger.info(f"📊 Datos recibidos: {contact_data}")
            
            # Preparar datos para NocoDB con columnas correctas
            nocodb_data = {
                "nombre_cliente": contact_data.get("nombre", ""),
                "email_cliente": contact_data.get("email", ""),
                "telefono_cliente": contact_data.get("telefono", ""),
                "mensaje_consulta": contact_data.get("mensaje", ""),
                "fecha_consulta": contact_data.get("fecha", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                "estado_consulta": "Nuevo",
                "origen_consulta": "Web Solar",
                "notas_internas": "",
                "fecha_respuesta": None,
                "usuario_respuesta": None
            }
            
            logger.info(f"📝 Datos preparados para NocoDB: {nocodb_data}")
            logger.info(f"📡 Headers: {self.headers}")
            
            async with aiohttp.ClientSession() as session:
                logger.info(f"🚀 Enviando POST a: {self.contactos_url}")
                async with session.post(
                    self.contactos_url,
                    json=nocodb_data,
                    headers=self.headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    
                    logger.info(f"📡 Respuesta recibida: {response.status}")
                    logger.info(f"📡 Headers de respuesta: {dict(response.headers)}")
                    
                    if response.status == 200:
                        result = await response.json()
                        logger.info(f"✅ Contacto guardado exitosamente: {result}")
                        return True
                    else:
                        error_text = await response.text()
                        logger.error(f"❌ Error guardando contacto: {response.status} - {error_text}")
                        logger.error(f"❌ URL que falló: {self.contactos_url}")
                        logger.error(f"❌ Datos enviados: {nocodb_data}")
                        return False
                        
        except Exception as e:
            logger.error(f"❌ Error guardando contacto: {e}")
            logger.error(f"❌ Tipo de error: {type(e).__name__}")
            import traceback
            logger.error(f"❌ Traceback: {traceback.format_exc()}")
            return False
    
    async def save_solar_quote(self, quote_data: Dict[str, Any]) -> bool:
        """
        Guarda cotización solar en NocoDB
        """
        try:
            logger.info(f"🔄 Guardando cotización solar: {quote_data.get('nombre_cliente', 'Sin nombre')}")
            logger.info(f"🔗 URL de cotizaciones: {self.cotizaciones_url}")
            logger.info(f"🔑 Token: {self.token[:10]}...")
            logger.info(f"📊 Datos recibidos: {quote_data}")
            
            # Preparar datos para NocoDB - Mapeo correcto según los campos enviados
            nocodb_data = {
                "nombre_cliente": quote_data.get("nombre_cliente", ""),
                "email_cliente": quote_data.get("email_cliente", ""),
                "ubicacion_proyecto": quote_data.get("ubicacion_proyecto", ""),
                "consumo_mensual_kwh": quote_data.get("consumo_mensual_kwh", 0),
                "tipo_tarifa": quote_data.get("tipo_tarifa", ""),
                "area_disponible_m2": quote_data.get("area_disponible_m2", 0),
                "tipo_instalacion": quote_data.get("tipo_instalacion", ""),
                "potencia_requerida_kwp": quote_data.get("potencia_requerida_kwp", 0),
                "cantidad_paneles": quote_data.get("cantidad_paneles", 0),
                "generacion_mensual_kwh": quote_data.get("generacion_mensual_kwh", 0),
                "ahorro_mensual_ars": quote_data.get("ahorro_mensual_ars", 0),
                "inversion_total_ars": quote_data.get("inversion_total_ars", 0),
                "roi_anos": quote_data.get("roi_anos", 0),
                "fecha_cotizacion": quote_data.get("fecha_cotizacion", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                "estado_cotizacion": quote_data.get("estado_cotizacion", "generada"),
                "notas_adicionales": quote_data.get("notas_adicionales", "")
            }
            
            logger.info(f"📋 Datos preparados para NocoDB: {nocodb_data}")
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.cotizaciones_url,
                    json=nocodb_data,
                    headers=self.headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        logger.info(f"✅ Cotización guardada exitosamente: {result}")
                        return True
                    else:
                        error_text = await response.text()
                        logger.error(f"❌ Error guardando cotización: {response.status} - {error_text}")
                        return False
                        
        except Exception as e:
            logger.error(f"❌ Error guardando cotización: {e}")
            return False
    
    async def save_material(self, material_data: Dict[str, Any]) -> bool:
        """
        Guarda material solar en NocoDB
        """
        try:
            logger.info(f"🔄 Guardando material: {material_data.get('brand', 'Sin marca')}")
            
            nocodb_data = {
                "tipo_material": material_data.get("type", ""),
                "marca": material_data.get("brand", ""),
                "modelo": material_data.get("model", ""),
                "potencia_watts": material_data.get("power_watts", 0),
                "potencia_kw": material_data.get("power_kw", 0),
                "precio_ars": material_data.get("price_ars", 0),
                "precio_por_kw": material_data.get("price_per_kw", 0),
                "stock_disponible": material_data.get("stock", 0),
                "activo": material_data.get("active", True),
                "especificaciones_tecnicas": material_data.get("specifications", ""),
                "garantia_anos": material_data.get("warranty_years", 0),
                "proveedor": material_data.get("supplier", ""),
                "fecha_actualizacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.materiales_url,
                    json=nocodb_data,
                    headers=self.headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        logger.info(f"✅ Material guardado exitosamente: {result}")
                        return True
                    else:
                        error_text = await response.text()
                        logger.error(f"❌ Error guardando material: {response.status} - {error_text}")
                        return False
                        
        except Exception as e:
            logger.error(f"❌ Error guardando material: {e}")
            return False
    
    async def save_system_log(self, log_data: Dict[str, Any]) -> bool:
        """
        Guarda log del sistema en NocoDB
        """
        try:
            nocodb_data = {
                "tipo_evento": log_data.get("event_type", ""),
                "mensaje": log_data.get("message", ""),
                "nivel_log": log_data.get("level", "INFO"),
                "usuario": log_data.get("user", ""),
                "ip_cliente": log_data.get("ip", ""),
                "fecha_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "datos_adicionales": str(log_data.get("additional_data", {}))
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.logs_url,
                    json=nocodb_data,
                    headers=self.headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    
                    if response.status == 200:
                        logger.info("✅ Log guardado exitosamente")
                        return True
                    else:
                        error_text = await response.text()
                        logger.error(f"❌ Error guardando log: {response.status} - {error_text}")
                        return False
                        
        except Exception as e:
            logger.error(f"❌ Error guardando log: {e}")
            return False
    
    async def get_contacts(self, limit: int = 100) -> Optional[list]:
        """
        Obtiene la lista de contactos desde NocoDB
        """
        try:
            params = {
                "limit": limit,
                "sort": "-fecha_consulta"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.contactos_url,
                    params=params,
                    headers=self.headers
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        return result.get("list", [])
                    else:
                        error_text = await response.text()
                        logger.error(f"Error obteniendo contactos: {response.status} - {error_text}")
                        return None
                        
        except Exception as e:
            logger.error(f"Error obteniendo contactos: {e}")
            return None
    
    async def get_quotes(self, limit: int = 100) -> Optional[list]:
        """
        Obtiene la lista de cotizaciones desde NocoDB
        """
        try:
            params = {
                "limit": limit,
                "sort": "-fecha_creacion"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.cotizaciones_url,
                    params=params,
                    headers=self.headers
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        return result.get("list", [])
                    else:
                        error_text = await response.text()
                        logger.error(f"Error obteniendo cotizaciones: {response.status} - {error_text}")
                        return None
                        
        except Exception as e:
            logger.error(f"Error obteniendo cotizaciones: {e}")
            return None
    
    async def get_materials_from_nocodb(self, limit: int = 1000) -> Optional[List[Dict[str, Any]]]:
        """
        Obtener materiales desde NocoDB
        """
        try:
            logger.info(f"🔄 Obteniendo materiales desde NocoDB (límite: {limit})")
            
            params = {
                "limit": limit,
                "sort": "-fecha_actualizacion"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.materiales_url,
                    params=params,
                    headers=self.headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    
                    logger.info(f"📡 Respuesta recibida de NocoDB (Materiales): {response.status}")
                    
                    if response.status == 200:
                        result = await response.json()
                        materials = result.get("list", [])
                        logger.info(f"✅ Materiales obtenidos exitosamente: {len(materials)} registros")
                        return materials
                    else:
                        error_text = await response.text()
                        logger.error(f"❌ Error obteniendo materiales desde NocoDB: {response.status} - {error_text}")
                        return None
                        
        except aiohttp.ClientError as e:
            logger.error(f"🌐 Error de conexión con NocoDB (Materiales): {e}")
            return None
        except asyncio.TimeoutError:
            logger.error("⏰ Timeout en conexión con NocoDB (Materiales)")
            return None
        except Exception as e:
            logger.error(f"❌ Error inesperado en servicio NocoDB (Materiales): {e}")
            return None
    
    async def update_contact_status(self, contact_id: int, status: str) -> bool:
        """
        Actualiza el estado de un contacto
        """
        try:
            update_data = {"estado_consulta": status}
            
            async with aiohttp.ClientSession() as session:
                async with session.patch(
                    f"{self.contactos_url}/{contact_id}",
                    json=update_data,
                    headers=self.headers
                ) as response:
                    
                    if response.status == 200:
                        logger.info(f"Estado del contacto {contact_id} actualizado a: {status}")
                        return True
                    else:
                        error_text = await response.text()
                        logger.error(f"Error actualizando estado: {response.status} - {error_text}")
                        return False
                        
        except Exception as e:
            logger.error(f"Error actualizando estado del contacto: {e}")
            return False

# Instancia global del servicio de Nocodb
nocodb_service = NocodbService()