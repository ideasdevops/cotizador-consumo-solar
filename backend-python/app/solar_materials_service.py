"""
Servicio para gestión de materiales solares desde NocoDB
"""
import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from enum import Enum

import aiohttp
from app.config import settings

logger = logging.getLogger(__name__)

class SolarMaterialsService:
    """Servicio para gestión de materiales solares desde NocoDB"""
    
    def __init__(self):
        # Usar variables correctas de NocoDB
        self.nocodb_url = getattr(settings, 'NC_DB_URL', settings.NOCODB_URL)
        self.nocodb_token = getattr(settings, 'NC_TOKEN', settings.NOCODB_TOKEN)
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
        """Obtener materiales por defecto como fallback"""
        return {
            "panels": [
                {
                    "id": "panel_default_1",
                    "brand": "JinkoSolar",
                    "model": "JKM400M-54HL4-B",
                    "power_watts": 400,
                    "price_ars": 180000,
                    "active": True,
                    "specifications": "Panel monocristalino de alta eficiencia",
                    "warranty_years": 25,
                    "supplier": "JinkoSolar Argentina",
                    "type": "monocristalino"
                },
                {
                    "id": "panel_default_2",
                    "brand": "Trina Solar",
                    "model": "TSM-400DE14A(II)",
                    "power_watts": 400,
                    "price_ars": 175000,
                    "active": True,
                    "specifications": "Panel monocristalino con tecnología PERC",
                    "warranty_years": 25,
                    "supplier": "Trina Solar Argentina",
                    "type": "monocristalino"
                }
            ],
            "inverters": [
                {
                    "id": "inverter_default_1",
                    "brand": "SMA",
                    "model": "STP 5000TL-20",
                    "power_kw": 5.0,
                    "price_ars": 800000,
                    "active": True,
                    "specifications": "Inversor string de 5kW",
                    "warranty_years": 10,
                    "supplier": "SMA Argentina",
                    "type": "string"
                },
                {
                    "id": "inverter_default_2",
                    "brand": "Fronius",
                    "model": "Primo 5.0-1",
                    "power_kw": 5.0,
                    "price_ars": 750000,
                    "active": True,
                    "specifications": "Inversor string de 5kW con WiFi",
                    "warranty_years": 10,
                    "supplier": "Fronius Argentina",
                    "type": "string"
                }
            ],
            "batteries": [
                {
                    "id": "battery_default_1",
                    "brand": "Tesla",
                    "model": "Powerwall 2",
                    "power_kw": 13.5,
                    "price_ars": 4500000,
                    "active": True,
                    "specifications": "Batería de litio de 13.5kWh",
                    "warranty_years": 10,
                    "supplier": "Tesla Argentina",
                    "type": "litio",
                    # Campos requeridos agregados
                    "capacity_ah": 280.0,
                    "voltage": 48.0,
                    "cycles": 6000,
                    "efficiency": 95.0,
                    "dimensions": {"width": 1150, "height": 755, "depth": 155},
                    "weight": 114.0
                }
            ],
            "mounting": [
                {
                    "id": "mounting_default_1",
                    "brand": "Schletter",
                    "model": "FS-R",
                    "price_per_kw": 150000,
                    "active": True,
                    "specifications": "Sistema de montaje para techo inclinado",
                    "supplier": "Schletter Argentina",
                    "type": "techo"
                }
            ],
            "cables": [],
            "protection": []
        }
    
    def get_materials(self) -> Dict[str, List[Dict]]:
        """Obtener materiales (síncrono para compatibilidad)"""
        return self.materials
    
    async def refresh_materials(self):
        """Actualizar materiales desde NocoDB"""
        try:
            new_materials = await self.load_materials_from_nocodb()
            self.materials = new_materials
            logger.info("Materiales actualizados desde NocoDB")
        except Exception as e:
            logger.error(f"Error actualizando materiales: {e}")
            # Mantener materiales por defecto en caso de error
    
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
                                    "supplier": material.get("proveedor", ""),
                                    "type": "monocristalino"  # Default type
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
                                    "supplier": material.get("proveedor", ""),
                                    "type": "string"  # Default type
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
                                    "supplier": material.get("proveedor", ""),
                                    "type": material.get("type", "litio"),
                                    # Campos requeridos agregados
                                    "capacity_ah": material.get("capacity_ah", 200.0),
                                    "voltage": material.get("voltage", 48.0),
                                    "cycles": material.get("cycles", 6000),
                                    "efficiency": material.get("efficiency", 95.0),
                                    "dimensions": material.get("dimensions", {"width": 500, "height": 300, "depth": 200}),
                                    "weight": material.get("weight", 50.0)
                                })
                            elif material_type == "montaje":
                                organized_materials["mounting"].append({
                                    "id": material.get("id"),
                                    "brand": material.get("marca", ""),
                                    "model": material.get("modelo", ""),
                                    "price_per_kw": material.get("precio_por_kw", 0),
                                    "active": material.get("activo", True),
                                    "specifications": material.get("especificaciones_tecnicas", ""),
                                    "supplier": material.get("proveedor", ""),
                                    "type": "techo"  # Default type
                                })
                            elif material_type == "cable":
                                organized_materials["cables"].append({
                                    "id": material.get("id"),
                                    "brand": material.get("marca", ""),
                                    "model": material.get("modelo", ""),
                                    "price_ars": material.get("precio_ars", 0),
                                    "active": material.get("activo", True),
                                    "specifications": material.get("especificaciones_tecnicas", ""),
                                    "supplier": material.get("proveedor", ""),
                                    "type": "dc"  # Default type
                                })
                            elif material_type == "proteccion":
                                organized_materials["protection"].append({
                                    "id": material.get("id"),
                                    "brand": material.get("marca", ""),
                                    "model": material.get("modelo", ""),
                                    "price_ars": material.get("precio_ars", 0),
                                    "active": material.get("activo", True),
                                    "specifications": material.get("especificaciones_tecnicas", ""),
                                    "supplier": material.get("proveedor", ""),
                                    "type": "sobretencion"  # Default type
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
    
    # Métodos de compatibilidad para el calculador solar
    def get_panels(self, panel_type: Optional[str] = None, 
                   min_power: Optional[int] = None, 
                   max_power: Optional[int] = None) -> List[Dict[str, Any]]:
        """Obtener paneles solares con filtros opcionales"""
        panels = self.materials.get("panels", [])
        panels = [p for p in panels if p.get("active", True)]
        
        if panel_type:
            panels = [p for p in panels if p.get("type", "monocristalino") == panel_type]
        
        if min_power:
            panels = [p for p in panels if p.get("power_watts", 0) >= min_power]
        
        if max_power:
            panels = [p for p in panels if p.get("power_watts", 0) <= max_power]
        
        return sorted(panels, key=lambda x: x.get("power_watts", 0))
    
    def get_inverters(self, inverter_type: Optional[str] = None,
                      min_power: Optional[float] = None,
                      max_power: Optional[float] = None) -> List[Dict[str, Any]]:
        """Obtener inversores con filtros opcionales"""
        inverters = self.materials.get("inverters", [])
        inverters = [i for i in inverters if i.get("active", True)]
        
        if inverter_type:
            inverters = [i for i in inverters if i.get("type", "string") == inverter_type]
        
        if min_power:
            inverters = [i for i in inverters if i.get("power_kw", 0) >= min_power]
        
        if max_power:
            inverters = [i for i in inverters if i.get("power_kw", 0) <= max_power]
        
        return sorted(inverters, key=lambda x: x.get("power_kw", 0))
    
    def get_batteries(self, battery_type: Optional[str] = None,
                      min_capacity: Optional[float] = None,
                      max_capacity: Optional[float] = None) -> List[Dict[str, Any]]:
        """Obtener baterías con filtros opcionales"""
        batteries = self.materials.get("batteries", [])
        batteries = [b for b in batteries if b.get("active", True)]
        
        if battery_type:
            batteries = [b for b in batteries if b.get("type", "litio") == battery_type]
        
        if min_capacity:
            batteries = [b for b in batteries if b.get("power_kw", 0) >= min_capacity]
        
        if max_capacity:
            batteries = [b for b in batteries if b.get("power_kw", 0) <= max_capacity]
        
        return sorted(batteries, key=lambda x: x.get("power_kw", 0))
    
    def get_mounting_systems(self, mounting_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Obtener sistemas de montaje"""
        mounting = self.materials.get("mounting", [])
        mounting = [m for m in mounting if m.get("active", True)]
        
        if mounting_type:
            mounting = [m for m in mounting if m.get("type", "techo") == mounting_type]
        
        return mounting
    
    def get_cables(self, cable_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Obtener cables"""
        cables = self.materials.get("cables", [])
        cables = [c for c in cables if c.get("active", True)]
        
        if cable_type:
            cables = [c for c in cables if c.get("type", "dc") == cable_type]
        
        return cables
    
    def get_protection_devices(self, protection_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Obtener dispositivos de protección"""
        protection = self.materials.get("protection", [])
        protection = [p for p in protection if p.get("active", True)]
        
        if protection_type:
            protection = [p for p in protection if p.get("type", "sobretencion") == protection_type]
        
        return protection
    
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
                "active": len([p for p in protection if p.get("active", True)]),
                "types": list(set(p.get("type", "sobretencion") for p in protection))
            }
        }

# Instancia global del servicio
solar_materials_service = SolarMaterialsService()
