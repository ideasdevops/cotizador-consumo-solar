"""
Servicio de materiales solares - Gestión de componentes y precios desde NocoDB
"""
import json
import os
import aiohttp
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import logging
from .solar_models import (
    SolarPanel, Inverter, Battery, MountingSystem, Cable, ProtectionDevice,
    SolarPanelType, InverterType, BatteryType, InstallationType
)
from .config import settings

logger = logging.getLogger(__name__)


class SolarMaterialsService:
    """Servicio para gestión de materiales solares desde NocoDB"""
    
    def __init__(self):
        self.nocodb_url = settings.NOCODB_URL
        self.nocodb_token = settings.NOCODB_TOKEN
        self.materiales_table_id = getattr(settings, 'NOCODB_MATERIALES_TABLE_ID', 'm2p9ng5e1hn53k0')
        self.materials_url = f"{self.nocodb_url}/api/v2/tables/{self.materiales_table_id}/records"
        
        self.headers = {
            "xc-token": self.nocodb_token,
            "Content-Type": "application/json"
        }
        
        # Cache de materiales
        self.materials_cache = {}
        self.cache_expiry = None
        self.cache_duration = timedelta(hours=1)
        
        # Inicializar materiales por defecto
        self.materials = self.get_default_materials()
    
    def get_default_materials(self) -> Dict[str, List[Dict]]:
        """Obtener materiales por defecto en caso de error"""
        logger.info("Usando materiales por defecto...")
        return {
            "panels": [
                {
                    "id": "panel_default",
                    "brand": "JinkoSolar",
                    "model": "JKM400M-54HL4-B",
                    "power_watts": 400,
                    "price_ars": 180000,
                    "active": True,
                    "specifications": "Panel monocristalino de alta eficiencia",
                    "warranty_years": 25,
                    "supplier": "JinkoSolar Argentina"
                }
            ],
            "inverters": [
                {
                    "id": "inverter_default",
                    "brand": "SMA",
                    "model": "STP 5000TL-20",
                    "power_kw": 5.0,
                    "price_ars": 800000,
                    "active": True,
                    "specifications": "Inversor string de 5kW",
                    "warranty_years": 10,
                    "supplier": "SMA Argentina"
                }
            ],
            "batteries": [],
            "mounting": [
                {
                    "id": "mounting_default",
                    "brand": "Schletter",
                    "model": "FS-R",
                    "price_per_kw": 150000,
                    "active": True,
                    "specifications": "Sistema de montaje para techo inclinado",
                    "supplier": "Schletter Argentina"
                }
            ],
            "cables": [],
            "protection": []
        }
    
    def get_materials(self) -> Dict[str, List[Dict]]:
        """Obtener materiales (síncrono para compatibilidad)"""
        return self.materials
    
    def get_materials_summary(self) -> Dict[str, Any]:
        """Obtener resumen de todos los materiales"""
        panels = self.materials.get("panels", [])
        inverters = self.materials.get("inverters", [])
        batteries = self.materials.get("batteries", [])
        mounting = self.materials.get("mounting", [])
        cables = self.materials.get("cables", [])
        protection = self.materials.get("protection", [])
        
        return {
            "panels": {
                "total": len(panels),
                "active": len([p for p in panels if p.get("active", True)]),
                "types": list(set(p.get("type", "monocristalino") for p in panels)),
                "power_range": {
                    "min": min(p.get("power_watts", 0) for p in panels) if panels else 0,
                    "max": max(p.get("power_watts", 0) for p in panels) if panels else 0
                }
            },
            "inverters": {
                "total": len(inverters),
                "active": len([i for i in inverters if i.get("active", True)]),
                "types": list(set(i.get("type", "string") for i in inverters)),
                "power_range": {
                    "min": min(i.get("power_kw", 0) for i in inverters) if inverters else 0,
                    "max": max(i.get("power_kw", 0) for i in inverters) if inverters else 0
                }
            },
            "batteries": {
                "total": len(batteries),
                "active": len([b for b in batteries if b.get("active", True)]),
                "types": list(set(b.get("type", "litio") for b in batteries)),
                "capacity_range": {
                    "min": min(b.get("power_kw", 0) for b in batteries) if batteries else 0,
                    "max": max(b.get("power_kw", 0) for b in batteries) if batteries else 0
                }
            },
            "mounting_systems": {
                "total": len(mounting),
                "active": len([m for m in mounting if m.get("active", True)]),
                "types": list(set(m.get("type", "techo") for m in mounting))
            },
            "cables": {
                "total": len(cables),
                "active": len([c for c in cables if c.get("active", True)]),
                "section_range": {
                    "min": min(c.get("section_mm2", 0) for c in cables) if cables else 0,
                    "max": max(c.get("section_mm2", 0) for c in cables) if cables else 0
                }
            },
            "protection_devices": {
                "total": len(protection),
                "active": len([p for p in protection if p.get("active", True)])
            }
        }
    
    async def load_materials_from_nocodb(self) -> Dict[str, List[Dict]]:
        """Cargar materiales desde NocoDB"""
        try:
            logger.info("Cargando materiales desde NocoDB...")
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.materials_url,
                    headers=self.headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        materials_data = result.get("list", [])
                        
                        # Organizar materiales por tipo
                        organized_materials = {
                            "panels": [],
                            "inverters": [],
                            "batteries": [],
                            "mounting": [],
                            "cables": [],
                            "protection": []
                        }
                        
                        for material in materials_data:
                            material_type = material.get("tipo_material", "").lower()
                            
                            if material_type == "panel":
                                organized_materials["panels"].append({
                                    "id": material.get("id"),
                                    "brand": material.get("marca", ""),
                                    "model": material.get("modelo", ""),
                                    "power_watts": material.get("potencia_watts", 0),
                                    "price_ars": material.get("precio_ars", 0),
                                    "active": material.get("activo", True),
                                    "specifications": material.get("especificaciones_tecnicas", ""),
                                    "warranty_years": material.get("garantia_anos", 0),
                                    "supplier": material.get("proveedor", "")
                                })
                            elif material_type == "inversor":
                                organized_materials["inverters"].append({
                                    "id": material.get("id"),
                                    "brand": material.get("marca", ""),
                                    "model": material.get("modelo", ""),
                                    "power_kw": material.get("potencia_kw", 0),
                                    "price_ars": material.get("precio_ars", 0),
                                    "active": material.get("activo", True),
                                    "specifications": material.get("especificaciones_tecnicas", ""),
                                    "warranty_years": material.get("garantia_anos", 0),
                                    "supplier": material.get("proveedor", "")
                                })
                            elif material_type == "bateria":
                                organized_materials["batteries"].append({
                                    "id": material.get("id"),
                                    "brand": material.get("marca", ""),
                                    "model": material.get("modelo", ""),
                                    "power_kw": material.get("potencia_kw", 0),
                                    "price_ars": material.get("precio_ars", 0),
                                    "active": material.get("activo", True),
                                    "specifications": material.get("especificaciones_tecnicas", ""),
                                    "warranty_years": material.get("garantia_anos", 0),
                                    "supplier": material.get("proveedor", "")
                                })
                            elif material_type == "montaje":
                                organized_materials["mounting"].append({
                                    "id": material.get("id"),
                                    "brand": material.get("marca", ""),
                                    "model": material.get("modelo", ""),
                                    "price_per_kw": material.get("precio_por_kw", 0),
                                    "active": material.get("activo", True),
                                    "specifications": material.get("especificaciones_tecnicas", ""),
                                    "supplier": material.get("proveedor", "")
                                })
                            elif material_type == "cable":
                                organized_materials["cables"].append({
                                    "id": material.get("id"),
                                    "brand": material.get("marca", ""),
                                    "model": material.get("modelo", ""),
                                    "price_ars": material.get("precio_ars", 0),
                                    "active": material.get("activo", True),
                                    "specifications": material.get("especificaciones_tecnicas", ""),
                                    "supplier": material.get("proveedor", "")
                                })
                            elif material_type == "proteccion":
                                organized_materials["protection"].append({
                                    "id": material.get("id"),
                                    "brand": material.get("marca", ""),
                                    "model": material.get("modelo", ""),
                                    "price_ars": material.get("precio_ars", 0),
                                    "active": material.get("activo", True),
                                    "specifications": material.get("especificaciones_tecnicas", ""),
                                    "supplier": material.get("proveedor", "")
                                })
                        
                        logger.info(f"Materiales cargados desde NocoDB: {len(materials_data)} registros")
                        return organized_materials
                        
                    else:
                        error_text = await response.text()
                        logger.error(f"Error cargando materiales desde NocoDB: {response.status} - {error_text}")
                        return self.get_default_materials()
                        
        except Exception as e:
            logger.error(f"Error cargando materiales desde NocoDB: {e}")
            return self.get_default_materials()
    
    async def refresh_materials(self):
        """Actualizar materiales desde NocoDB"""
        try:
            new_materials = await self.load_materials_from_nocodb()
            self.materials = new_materials
            logger.info("Materiales actualizados desde NocoDB")
        except Exception as e:
            logger.error(f"Error actualizando materiales: {e}")
            # Mantener materiales por defecto en caso de error

# Instancia global del servicio
materials_service = SolarMaterialsService()
