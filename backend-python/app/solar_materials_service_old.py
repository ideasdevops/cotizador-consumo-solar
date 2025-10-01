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
    
    async def refresh_materials(self):
        """Actualizar materiales desde NocoDB"""
        try:
            new_materials = await self.load_materials_from_nocodb()
            self.materials = new_materials
            logger.info("Materiales actualizados desde NocoDB")
        except Exception as e:
            logger.error(f"Error actualizando materiales: {e}")
            # Mantener materiales por defecto en caso de error
    
    def ensure_data_directory(self):
        """Asegurar que existe el directorio de datos"""
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Crear archivos de datos si no existen
        if not os.path.exists(f"{self.data_dir}/panels.json"):
            self.initialize_default_materials()
    
    def initialize_default_materials(self):
        """Inicializar materiales por defecto"""
        logger.info("Inicializando materiales solares por defecto...")
        
        # Paneles solares por defecto
        default_panels = [
            {
                "id": "panel_mono_400w",
                "name": "Panel Solar Monocristalino 400W",
                "brand": "JinkoSolar",
                "model": "JKM400M-54HL4-B",
                "type": "monocristalino",
                "power_watts": 400,
                "efficiency": 20.78,
                "dimensions": {"width": 2094, "height": 1038, "thickness": 35},
                "weight": 22.5,
                "price_ars": 180000,
                "warranty_years": 25,
                "temperature_coefficient": -0.35,
                "max_voltage": 37.8,
                "max_current": 10.59
            },
            {
                "id": "panel_mono_450w",
                "name": "Panel Solar Monocristalino 450W",
                "brand": "Trina Solar",
                "model": "TSM-450DE09H(II)",
                "type": "monocristalino",
                "power_watts": 450,
                "efficiency": 21.1,
                "dimensions": {"width": 2108, "height": 1048, "thickness": 35},
                "weight": 24.5,
                "price_ars": 200000,
                "warranty_years": 25,
                "temperature_coefficient": -0.34,
                "max_voltage": 40.9,
                "max_current": 11.0
            },
            {
                "id": "panel_poly_350w",
                "name": "Panel Solar Policristalino 350W",
                "brand": "Canadian Solar",
                "model": "CS3K-350MS",
                "type": "policristalino",
                "power_watts": 350,
                "efficiency": 17.8,
                "dimensions": {"width": 1956, "height": 992, "thickness": 40},
                "weight": 20.5,
                "price_ars": 150000,
                "warranty_years": 25,
                "temperature_coefficient": -0.41,
                "max_voltage": 37.4,
                "max_current": 9.36
            }
        ]
        
        # Inversores por defecto
        default_inverters = [
            {
                "id": "inverter_string_5kw",
                "name": "Inversor String 5kW",
                "brand": "SMA",
                "model": "STP 5000TL-20",
                "type": "string",
                "power_kw": 5.0,
                "efficiency": 97.5,
                "input_voltage_range": {"min": 125, "max": 1000},
                "output_voltage": 230,
                "max_input_current": 11.0,
                "price_ars": 800000,
                "warranty_years": 10,
                "has_mppt": True,
                "has_wifi": True
            },
            {
                "id": "inverter_string_10kw",
                "name": "Inversor String 10kW",
                "brand": "Fronius",
                "model": "Primo 10.0-1",
                "type": "string",
                "power_kw": 10.0,
                "efficiency": 98.0,
                "input_voltage_range": {"min": 125, "max": 1000},
                "output_voltage": 230,
                "max_input_current": 22.0,
                "price_ars": 1500000,
                "warranty_years": 10,
                "has_mppt": True,
                "has_wifi": True
            },
            {
                "id": "inverter_micro_1kw",
                "name": "Microinversor 1kW",
                "brand": "Enphase",
                "model": "IQ7+",
                "type": "micro",
                "power_kw": 1.0,
                "efficiency": 97.5,
                "input_voltage_range": {"min": 16, "max": 48},
                "output_voltage": 240,
                "max_input_current": 1.0,
                "price_ars": 180000,
                "warranty_years": 25,
                "has_mppt": True,
                "has_wifi": True
            }
        ]
        
        # Baterías por defecto
        default_batteries = [
            {
                "id": "battery_lithium_5kwh",
                "name": "Batería Litio 5kWh",
                "brand": "Tesla",
                "model": "Powerwall 2",
                "type": "litio",
                "capacity_ah": 208,
                "voltage": 24,
                "power_kwh": 5.0,
                "cycles": 6000,
                "efficiency": 90,
                "dimensions": {"width": 755, "height": 1475, "thickness": 190},
                "weight": 114,
                "price_ars": 2500000,
                "warranty_years": 10
            },
            {
                "id": "battery_lithium_10kwh",
                "name": "Batería Litio 10kWh",
                "brand": "LG Chem",
                "model": "RESU10H",
                "type": "litio",
                "capacity_ah": 400,
                "voltage": 24,
                "power_kwh": 10.0,
                "cycles": 6000,
                "efficiency": 95,
                "dimensions": {"width": 600, "height": 1200, "thickness": 300},
                "weight": 95,
                "price_ars": 4500000,
                "warranty_years": 10
            }
        ]
        
        # Sistemas de montaje por defecto
        default_mounting = [
            {
                "id": "mounting_roof_residential",
                "name": "Sistema Montaje Techo Residencial",
                "brand": "Schletter",
                "model": "FS-R",
                "type": "techo_residencial",
                "material": "Aluminio anodizado",
                "max_wind_load": 60,
                "max_snow_load": 150,
                "price_per_kw": 150000,
                "installation_cost_per_kw": 200000,
                "warranty_years": 20
            },
            {
                "id": "mounting_ground_residential",
                "name": "Sistema Montaje Suelo Residencial",
                "brand": "Schletter",
                "model": "FS-G",
                "type": "suelo_residencial",
                "material": "Acero galvanizado",
                "max_wind_load": 50,
                "max_snow_load": 100,
                "price_per_kw": 200000,
                "installation_cost_per_kw": 250000,
                "warranty_years": 20
            }
        ]
        
        # Cables por defecto
        default_cables = [
            {
                "id": "cable_solar_4mm",
                "name": "Cable Solar 4mm²",
                "brand": "Nexans",
                "model": "SolarFlex",
                "section_mm2": 4.0,
                "voltage_rating": 1000,
                "current_rating": 25,
                "length_meters": 100,
                "price_per_meter": 2500
            },
            {
                "id": "cable_solar_6mm",
                "name": "Cable Solar 6mm²",
                "brand": "Nexans",
                "model": "SolarFlex",
                "section_mm2": 6.0,
                "voltage_rating": 1000,
                "current_rating": 35,
                "length_meters": 100,
                "price_per_meter": 3500
            }
        ]
        
        # Dispositivos de protección por defecto
        default_protection = [
            {
                "id": "disyuntor_32a",
                "name": "Disyuntor 32A",
                "brand": "Schneider",
                "model": "iID 32A",
                "type": "disyuntor",
                "current_rating": 32,
                "voltage_rating": 230,
                "price_ars": 25000
            },
            {
                "id": "fusible_20a",
                "name": "Fusible 20A",
                "brand": "ABB",
                "model": "FUS20A",
                "type": "fusible",
                "current_rating": 20,
                "voltage_rating": 1000,
                "price_ars": 15000
            }
        ]
        
        # Guardar datos por defecto
        self.save_materials("panels", default_panels)
        self.save_materials("inverters", default_inverters)
        self.save_materials("batteries", default_batteries)
        self.save_materials("mounting", default_mounting)
        self.save_materials("cables", default_cables)
        self.save_materials("protection", default_protection)
        
        logger.info("Materiales solares inicializados correctamente")
    
    def load_materials(self):
        """Cargar materiales desde archivos JSON"""
        self.panels = self.load_material_type("panels", SolarPanel)
        self.inverters = self.load_material_type("inverters", Inverter)
        self.batteries = self.load_material_type("batteries", Battery)
        self.mounting_systems = self.load_material_type("mounting", MountingSystem)
        self.cables = self.load_material_type("cables", Cable)
        self.protection_devices = self.load_material_type("protection", ProtectionDevice)
    
    def load_material_type(self, material_type: str, model_class):
        """Cargar un tipo específico de material"""
        file_path = f"{self.data_dir}/{material_type}.json"
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return [model_class(**item) for item in data]
            return []
        except Exception as e:
            logger.error(f"Error cargando {material_type}: {e}")
            return []
    
    def save_materials(self, material_type: str, materials: List[Dict]):
        """Guardar materiales en archivo JSON"""
        file_path = f"{self.data_dir}/{material_type}.json"
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(materials, f, indent=2, ensure_ascii=False, default=str)
        except Exception as e:
            logger.error(f"Error guardando {material_type}: {e}")
    
    def get_panels(self, panel_type: Optional[SolarPanelType] = None, 
                   min_power: Optional[int] = None, 
                   max_power: Optional[int] = None) -> List[SolarPanel]:
        """Obtener paneles solares con filtros opcionales"""
        panels = [p for p in self.panels if p.is_active]
        
        if panel_type:
            panels = [p for p in panels if p.type == panel_type]
        
        if min_power:
            panels = [p for p in panels if p.power_watts >= min_power]
        
        if max_power:
            panels = [p for p in panels if p.power_watts <= max_power]
        
        return sorted(panels, key=lambda x: x.power_watts)
    
    def get_inverters(self, inverter_type: Optional[InverterType] = None,
                      min_power: Optional[float] = None,
                      max_power: Optional[float] = None) -> List[Inverter]:
        """Obtener inversores con filtros opcionales"""
        inverters = [i for i in self.inverters if i.is_active]
        
        if inverter_type:
            inverters = [i for i in inverters if i.type == inverter_type]
        
        if min_power:
            inverters = [i for i in inverters if i.power_kw >= min_power]
        
        if max_power:
            inverters = [i for i in inverters if i.power_kw <= max_power]
        
        return sorted(inverters, key=lambda x: x.power_kw)
    
    def get_batteries(self, battery_type: Optional[BatteryType] = None,
                      min_capacity: Optional[float] = None,
                      max_capacity: Optional[float] = None) -> List[Battery]:
        """Obtener baterías con filtros opcionales"""
        batteries = [b for b in self.batteries if b.is_active]
        
        if battery_type:
            batteries = [b for b in batteries if b.type == battery_type]
        
        if min_capacity:
            batteries = [b for b in batteries if b.power_kwh >= min_capacity]
        
        if max_capacity:
            batteries = [b for b in batteries if b.power_kwh <= max_capacity]
        
        return sorted(batteries, key=lambda x: x.power_kwh)
    
    def get_mounting_systems(self, installation_type: Optional[InstallationType] = None) -> List[MountingSystem]:
        """Obtener sistemas de montaje con filtros opcionales"""
        mounting = [m for m in self.mounting_systems if m.is_active]
        
        if installation_type:
            mounting = [m for m in mounting if m.type == installation_type]
        
        return mounting
    
    def get_cables(self, min_section: Optional[float] = None,
                   max_section: Optional[float] = None) -> List[Cable]:
        """Obtener cables con filtros opcionales"""
        cables = [c for c in self.cables if c.is_active]
        
        if min_section:
            cables = [c for c in cables if c.section_mm2 >= min_section]
        
        if max_section:
            cables = [c for c in cables if c.section_mm2 <= max_section]
        
        return sorted(cables, key=lambda x: x.section_mm2)
    
    def get_protection_devices(self, device_type: Optional[str] = None,
                               min_current: Optional[float] = None,
                               max_current: Optional[float] = None) -> List[ProtectionDevice]:
        """Obtener dispositivos de protección con filtros opcionales"""
        devices = [d for d in self.protection_devices if d.is_active]
        
        if device_type:
            devices = [d for d in devices if d.type == device_type]
        
        if min_current:
            devices = [d for d in devices if d.current_rating >= min_current]
        
        if max_current:
            devices = [d for d in devices if d.current_rating <= max_current]
        
        return sorted(devices, key=lambda x: x.current_rating)
    
    def update_material_price(self, material_type: str, material_id: str, new_price: float, price_source: str):
        """Actualizar precio de un material"""
        try:
            materials_map = {
                "panels": self.panels,
                "inverters": self.inverters,
                "batteries": self.batteries,
                "mounting": self.mounting_systems,
                "cables": self.cables,
                "protection": self.protection_devices
            }
            
            if material_type not in materials_map:
                raise ValueError(f"Tipo de material no válido: {material_type}")
            
            materials = materials_map[material_type]
            material = next((m for m in materials if m.id == material_id), None)
            
            if not material:
                raise ValueError(f"Material no encontrado: {material_id}")
            
            # Actualizar precio
            if material_type == "panels":
                material.price_ars = new_price
            elif material_type == "inverters":
                material.price_ars = new_price
            elif material_type == "batteries":
                material.price_ars = new_price
            elif material_type == "mounting":
                material.price_per_kw = new_price
            elif material_type == "cables":
                material.price_per_meter = new_price
            elif material_type == "protection":
                material.price_ars = new_price
            
            # Guardar cambios
            materials_data = [m.dict() for m in materials]
            self.save_materials(material_type, materials_data)
            
            logger.info(f"Precio actualizado para {material_type}:{material_id} = ${new_price}")
            return True
            
        except Exception as e:
            logger.error(f"Error actualizando precio: {e}")
            return False
    
    def get_material_by_id(self, material_type: str, material_id: str):
        """Obtener un material específico por ID"""
        materials_map = {
            "panels": self.panels,
            "inverters": self.inverters,
            "batteries": self.batteries,
            "mounting": self.mounting_systems,
            "cables": self.cables,
            "protection": self.protection_devices
        }
        
        if material_type not in materials_map:
            return None
        
        materials = materials_map[material_type]
        return next((m for m in materials if m.id == material_id), None)
    
    def get_materials_summary(self) -> Dict[str, Any]:
        """Obtener resumen de todos los materiales"""
        return {
            "panels": {
                "total": len(self.panels),
                "active": len([p for p in self.panels if p.is_active]),
                "types": list(set(p.type.value for p in self.panels)),
                "power_range": {
                    "min": min(p.power_watts for p in self.panels) if self.panels else 0,
                    "max": max(p.power_watts for p in self.panels) if self.panels else 0
                }
            },
            "inverters": {
                "total": len(self.inverters),
                "active": len([i for i in self.inverters if i.is_active]),
                "types": list(set(i.type.value for i in self.inverters)),
                "power_range": {
                    "min": min(i.power_kw for i in self.inverters) if self.inverters else 0,
                    "max": max(i.power_kw for i in self.inverters) if self.inverters else 0
                }
            },
            "batteries": {
                "total": len(self.batteries),
                "active": len([b for b in self.batteries if b.is_active]),
                "types": list(set(b.type.value for b in self.batteries)),
                "capacity_range": {
                    "min": min(b.power_kwh for b in self.batteries) if self.batteries else 0,
                    "max": max(b.power_kwh for b in self.batteries) if self.batteries else 0
                }
            },
            "mounting_systems": {
                "total": len(self.mounting_systems),
                "active": len([m for m in self.mounting_systems if m.is_active]),
                "types": list(set(m.type.value for m in self.mounting_systems))
            },
            "cables": {
                "total": len(self.cables),
                "active": len([c for c in self.cables if c.is_active]),
                "section_range": {
                    "min": min(c.section_mm2 for c in self.cables) if self.cables else 0,
                    "max": max(c.section_mm2 for c in self.cables) if self.cables else 0
                }
            },
            "protection_devices": {
                "total": len(self.protection_devices),
                "active": len([d for d in self.protection_devices if d.is_active]),
                "types": list(set(d.type for d in self.protection_devices))
            }
        }
