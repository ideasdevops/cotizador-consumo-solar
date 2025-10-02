"""
Calculadora de sistemas solares - Dimensionamiento y cálculos económicos
"""
import math
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
import logging
from .solar_models import (
    SolarQuoteRequest, SolarSystemDesign, SolarPanel, Inverter, Battery,
    MountingSystem, Cable, ProtectionDevice, InstallationType,
    SolarPanelType, InverterType, BatteryType
)
from .solar_materials_service import SolarMaterialsService

logger = logging.getLogger(__name__)


class SolarCalculator:
    """Calculadora de sistemas solares"""
    
    def __init__(self):
        self.materials_service = SolarMaterialsService()
        
        # Parámetros de cálculo por ubicación
        self.location_params = {
            "buenos-aires": {
                "sun_hours_daily": 5.5,
                "latitude": -34.6037,
                "longitude": -58.3816,
                "temperature_coefficient": -0.35,
                "system_losses": 0.15
            },
            "cordoba": {
                "sun_hours_daily": 6.0,
                "latitude": -31.4201,
                "longitude": -64.1888,
                "temperature_coefficient": -0.35,
                "system_losses": 0.15
            },
            "santa-fe": {
                "sun_hours_daily": 5.8,
                "latitude": -31.6333,
                "longitude": -60.7,
                "temperature_coefficient": -0.35,
                "system_losses": 0.15
            },
            "mendoza": {
                "sun_hours_daily": 6.2,
                "latitude": -32.8908,
                "longitude": -68.8272,
                "temperature_coefficient": -0.35,
                "system_losses": 0.15
            },
            "tucuman": {
                "sun_hours_daily": 5.7,
                "latitude": -26.8083,
                "longitude": -65.2176,
                "temperature_coefficient": -0.35,
                "system_losses": 0.15
            },
            "other": {
                "sun_hours_daily": 5.5,
                "latitude": -34.0,
                "longitude": -58.0,
                "temperature_coefficient": -0.35,
                "system_losses": 0.15
            }
        }
        
        # Tarifas eléctricas por tipo
        self.tariff_rates = {
            "residential": 45.0,  # ARS por kWh
            "commercial": 38.0,
            "industrial": 32.0
        }
    
    def calculate_system_design(self, request: SolarQuoteRequest) -> SolarSystemDesign:
        """Calcular el diseño completo del sistema solar"""
        try:
            logger.info(f"Iniciando cálculo para consumo: {request.monthly_consumption_kwh} kWh/mes")
            
            # 1. Calcular potencia requerida
            required_power = self._calculate_required_power(request)
            
            # 2. Seleccionar componentes
            components = self._select_components(request, required_power)
            
            # 3. Calcular generación energética
            energy_calculation = self._calculate_energy_generation(request, required_power)
            
            # 4. Calcular costos
            cost_calculation = self._calculate_costs(components, request)
            
            # 5. Calcular ROI y payback
            economic_calculation = self._calculate_economics(
                cost_calculation["total_investment"],
                request.monthly_consumption_kwh,
                request.tariff_type
            )
            
            # 6. Crear diseño del sistema
            # Mapear diccionarios a objetos Pydantic
            selected_panels = [self._map_panel_dict(panel) for panel in components["panels"]]
            selected_inverters = [self._map_inverter_dict(inverter) for inverter in components["inverters"]]
            selected_batteries = [self._map_battery_dict(battery) for battery in components.get("batteries", [])]
            selected_mounting = self._map_mounting_dict(components["mounting"])
            selected_cables = [self._map_cable_dict(cable) for cable in components["cables"]]
            selected_protection = [self._map_protection_dict(device) for device in components["protection"]]
            
            design = SolarSystemDesign(
                required_power_kwp=required_power,
                panel_count=components["panel_count"],
                inverter_count=components["inverter_count"],
                battery_count=components.get("battery_count"),
                selected_panels=selected_panels,
                selected_inverters=selected_inverters,
                selected_batteries=selected_batteries,
                selected_mounting=selected_mounting,
                selected_cables=selected_cables,
                selected_protection=selected_protection,
                daily_generation_kwh=energy_calculation["daily_generation"],
                monthly_generation_kwh=energy_calculation["monthly_generation"],
                annual_generation_kwh=energy_calculation["annual_generation"],
                system_efficiency=energy_calculation["system_efficiency"],
                total_investment=cost_calculation["total_investment"],
                monthly_savings=economic_calculation["monthly_savings"],
                annual_savings=economic_calculation["annual_savings"],
                payback_years=economic_calculation["payback_years"],
                roi_percentage=economic_calculation["roi_percentage"],
                panels_cost=cost_calculation["panels_cost"],
                inverters_cost=cost_calculation["inverters_cost"],
                batteries_cost=cost_calculation.get("batteries_cost"),
                mounting_cost=cost_calculation["mounting_cost"],
                cables_cost=cost_calculation["cables_cost"],
                protection_cost=cost_calculation["protection_cost"],
                installation_cost=cost_calculation["installation_cost"],
                permits_cost=cost_calculation["permits_cost"],
                installation_time_days=cost_calculation["installation_time_days"],
                warranty_years=cost_calculation["warranty_years"],
                maintenance_cost_annual=cost_calculation["maintenance_cost_annual"]
            )
            
            logger.info(f"Cálculo completado. Potencia: {required_power} kWp, Inversión: ${cost_calculation['total_investment']:,.0f}")
            return design
            
        except Exception as e:
            logger.error(f"Error en cálculo del sistema: {e}")
            raise
    
    def _calculate_required_power(self, request: SolarQuoteRequest) -> float:
        """Calcular la potencia requerida del sistema"""
        location_params = self.location_params.get(request.location, self.location_params["other"])
        
        # Consumo diario
        daily_consumption = request.monthly_consumption_kwh / 30
        
        # Factor de seguridad (20% adicional)
        safety_factor = 1.2
        
        # Pérdidas del sistema
        system_losses = location_params["system_losses"]
        
        # Horas de sol efectivas
        sun_hours = location_params["sun_hours_daily"]
        
        # Cálculo de potencia requerida
        required_power = (daily_consumption * safety_factor) / (sun_hours * (1 - system_losses))
        
        # Redondear hacia arriba
        return math.ceil(required_power * 10) / 10
    
    def _select_components(self, request: SolarQuoteRequest, required_power: float) -> Dict[str, Any]:
        """Seleccionar componentes del sistema"""
        components = {}
        
        # 1. Seleccionar paneles
        panel_type = request.panel_type_preference or SolarPanelType.MONOCRISTALINO
        panels = self.materials_service.get_panels(panel_type=panel_type)
        
        if not panels:
            # Si no hay paneles del tipo preferido, usar cualquier tipo
            panels = self.materials_service.get_panels()
        
        if not panels:
            raise ValueError("No hay paneles disponibles")
        
        # Seleccionar el panel más eficiente (usar power_watts como criterio)
        selected_panel = max(panels, key=lambda p: p.get("power_watts", 0))
        
        # Calcular cantidad de paneles
        panel_count = math.ceil((required_power * 1000) / selected_panel.get("power_watts", 400))
        components["panels"] = [selected_panel] * panel_count
        components["panel_count"] = panel_count
        
        # 2. Seleccionar inversores
        inverter_type = request.inverter_type_preference or InverterType.STRING
        inverters = self.materials_service.get_inverters(inverter_type=inverter_type)
        
        if not inverters:
            inverters = self.materials_service.get_inverters()
        
        if not inverters:
            raise ValueError("No hay inversores disponibles")
        
        # Seleccionar inversor apropiado (80-120% de la potencia del sistema)
        system_power_kw = (panel_count * selected_panel.get("power_watts", 400)) / 1000
        min_inverter_power = system_power_kw * 0.8
        max_inverter_power = system_power_kw * 1.2
        
        suitable_inverters = [
            inv for inv in inverters 
            if min_inverter_power <= inv.get("power_kw", 0) <= max_inverter_power
        ]
        
        if suitable_inverters:
            selected_inverter = min(suitable_inverters, key=lambda i: i.get("power_kw", 0))
        else:
            # Si no hay inversor en el rango, usar el más cercano
            selected_inverter = min(inverters, key=lambda i: abs(i.get("power_kw", 0) - system_power_kw))
        
        # Calcular cantidad de inversores
        inverter_count = math.ceil(system_power_kw / selected_inverter.get("power_kw", 5.0))
        components["inverters"] = [selected_inverter] * inverter_count
        components["inverter_count"] = inverter_count
        
        # 3. Seleccionar baterías (si se requiere)
        if request.battery_backup:
            battery_type = BatteryType.LITIO
            batteries = self.materials_service.get_batteries(battery_type=battery_type)
            
            if batteries:
                # Calcular capacidad requerida
                autonomy_hours = request.battery_autonomy_hours or 8
                daily_consumption = request.monthly_consumption_kwh / 30
                required_capacity = (daily_consumption * autonomy_hours) / 24
                
                # Seleccionar batería apropiada
                suitable_batteries = [
                    bat for bat in batteries 
                    if bat.get("power_kw", 0) >= required_capacity
                ]
                
                if suitable_batteries:
                    selected_battery = min(suitable_batteries, key=lambda b: b.get("power_kw", 0))
                else:
                    selected_battery = max(batteries, key=lambda b: b.get("power_kw", 0))
                
                battery_count = math.ceil(required_capacity / selected_battery.get("power_kw", 10))
                components["batteries"] = [selected_battery] * battery_count
                components["battery_count"] = battery_count
        
        # 4. Seleccionar sistema de montaje
        mounting_systems = self.materials_service.get_mounting_systems()
        
        if not mounting_systems:
            mounting_systems = self.materials_service.get_mounting_systems()
        
        if mounting_systems:
            components["mounting"] = mounting_systems[0]  # Usar el primero disponible
        else:
            raise ValueError("No hay sistemas de montaje disponibles")
        
        # 5. Seleccionar cables
        # Calcular corriente máxima del sistema (estimación)
        max_current = (panel_count * selected_panel.get("power_watts", 400)) / (inverter_count * 220)  # V estimado
        
        # Seleccionar cable apropiado (con margen de seguridad)
        cables = self.materials_service.get_cables()
        
        if cables:
            selected_cable = cables[0]  # Usar el primer cable disponible
            # Estimar longitud de cables (simplificado)
            cable_length = math.sqrt(request.available_area_m2) * 2  # Estimación
            components["cables"] = [selected_cable]
        else:
            components["cables"] = []
        
        # 6. Seleccionar dispositivos de protección
        protection_devices = self.materials_service.get_protection_devices()
        
        if protection_devices:
            components["protection"] = protection_devices[:2]  # Fusible y disyuntor
        else:
            components["protection"] = []
        
        return components
    
    def _calculate_energy_generation(self, request: SolarQuoteRequest, required_power: float) -> Dict[str, float]:
        """Calcular generación energética del sistema"""
        location_params = self.location_params.get(request.location, self.location_params["other"])
        
        # Horas de sol diarias
        sun_hours = location_params["sun_hours_daily"]
        
        # Eficiencia del sistema (considerando pérdidas)
        system_efficiency = 1 - location_params["system_losses"]
        
        # Generación diaria
        daily_generation = required_power * sun_hours * system_efficiency
        
        # Generación mensual y anual
        monthly_generation = daily_generation * 30
        annual_generation = daily_generation * 365
        
        return {
            "daily_generation": round(daily_generation, 2),
            "monthly_generation": round(monthly_generation, 2),
            "annual_generation": round(annual_generation, 2),
            "system_efficiency": round(system_efficiency * 100, 1)
        }
    
    def _calculate_costs(self, components: Dict[str, Any], request: SolarQuoteRequest) -> Dict[str, float]:
        """Calcular costos del sistema"""
        costs = {}
        
        # Costo de paneles
        panels_cost = sum(panel.get("price_ars", 0) for panel in components["panels"])
        costs["panels_cost"] = panels_cost
        
        # Costo de inversores
        inverters_cost = sum(inverter.get("price_ars", 0) for inverter in components["inverters"])
        costs["inverters_cost"] = inverters_cost
        
        # Costo de baterías (si aplica)
        if "batteries" in components:
            batteries_cost = sum(battery.get("price_ars", 0) for battery in components["batteries"])
            costs["batteries_cost"] = batteries_cost
        else:
            costs["batteries_cost"] = 0
        
        # Costo de montaje
        mounting = components["mounting"]
        system_power_kw = sum(panel.get("power_watts", 0) for panel in components["panels"]) / 1000
        mounting_cost = system_power_kw * mounting.get("price_per_kw", 0)
        costs["mounting_cost"] = mounting_cost
        
        # Costo de cables
        cables_cost = sum(cable.get("price_ars", 0) for cable in components["cables"])
        costs["cables_cost"] = cables_cost
        
        # Costo de protección
        protection_cost = sum(device.get("price_ars", 0) for device in components["protection"])
        costs["protection_cost"] = protection_cost
        
        # Costo de instalación (estimado)
        installation_cost = system_power_kw * 50000  # $50,000 ARS por kW
        costs["installation_cost"] = installation_cost
        
        # Costo de permisos (estimado)
        permits_cost = system_power_kw * 50000  # $50,000 por kW
        costs["permits_cost"] = permits_cost
        
        # Tiempo de instalación (estimado)
        installation_time_days = max(1, int(system_power_kw / 2))  # 2 kW por día
        costs["installation_time_days"] = installation_time_days
        
        # Garantía del sistema (mínima entre componentes)
        warranty_years = min(
            min(panel.get("warranty_years", 25) for panel in components["panels"]),
            min(inverter.get("warranty_years", 10) for inverter in components["inverters"]),
            mounting.get("warranty_years", 10)
        )
        costs["warranty_years"] = warranty_years
        
        # Costo anual de mantenimiento (1% de la inversión)
        total_investment = (
            panels_cost + inverters_cost + costs["batteries_cost"] + 
            mounting_cost + cables_cost + protection_cost + 
            installation_cost + permits_cost
        )
        costs["maintenance_cost_annual"] = total_investment * 0.01
        costs["total_investment"] = total_investment
        
        return costs
    
    def _calculate_economics(self, total_investment: float, monthly_consumption: float, tariff_type: str) -> Dict[str, float]:
        """Calcular indicadores económicos"""
        tariff_rate = self.tariff_rates.get(tariff_type, self.tariff_rates["residential"])
        
        # Ahorro mensual (asumiendo 100% de autoconsumo)
        monthly_savings = monthly_consumption * tariff_rate
        
        # Ahorro anual
        annual_savings = monthly_savings * 12
        
        # Años de retorno de inversión
        payback_years = total_investment / annual_savings
        
        # ROI anual
        roi_percentage = (annual_savings / total_investment) * 100
        
        return {
            "monthly_savings": round(monthly_savings, 2),
            "annual_savings": round(annual_savings, 2),
            "payback_years": round(payback_years, 1),
            "roi_percentage": round(roi_percentage, 1)
        }
    
    def get_location_sun_data(self, location: str) -> Dict[str, Any]:
        """Obtener datos de radiación solar por ubicación"""
        params = self.location_params.get(location, self.location_params["other"])
        
        return {
            "location": location,
            "sun_hours_daily": params["sun_hours_daily"],
            "latitude": params["latitude"],
            "longitude": params["longitude"],
            "temperature_coefficient": params["temperature_coefficient"],
            "system_losses": params["system_losses"],
            "monthly_generation_factor": params["sun_hours_daily"] * 30,
            "annual_generation_factor": params["sun_hours_daily"] * 365
        }
    
    def estimate_system_size(self, monthly_consumption: float, location: str, 
                           installation_type: InstallationType) -> Dict[str, Any]:
        """Estimar tamaño del sistema sin cálculo detallado"""
        location_params = self.location_params.get(location, self.location_params["other"])
        
        # Cálculo simplificado
        daily_consumption = monthly_consumption / 30
        sun_hours = location_params["sun_hours_daily"]
        system_losses = location_params["system_losses"]
        
        # Potencia estimada
        estimated_power = daily_consumption / (sun_hours * (1 - system_losses))
        estimated_power = math.ceil(estimated_power * 10) / 10
        
        # Área estimada (asumiendo paneles de 400W y 2m²)
        estimated_area = estimated_power * 1000 / 400 * 2
        
        # Costo estimado por kW
        cost_per_kw = 800000  # Estimación conservadora
        
        # Calcular ahorros estimados
        monthly_savings = monthly_consumption * 45  # ARS por kWh promedio
        annual_savings = monthly_savings * 12
        payback_years = (estimated_power * cost_per_kw) / annual_savings
        
        return {
            "estimated_power_kwp": estimated_power,
            "estimated_area_m2": round(estimated_area, 1),
            "estimated_cost": round(estimated_power * cost_per_kw, 0),
            "estimated_panels": math.ceil(estimated_power * 1000 / 400),
            "estimated_savings": round(annual_savings, 0),
            "payback_years": round(payback_years, 1),
            "suitable_for_area": estimated_area <= 100,  # Asumiendo área disponible de 100m²
            "monthly_consumption": monthly_consumption,
            "location": location,
            "installation_type": installation_type,
            "daily_generation": round(estimated_power * sun_hours * (1 - system_losses), 1),
            "monthly_generation": round(estimated_power * sun_hours * (1 - system_losses) * 30, 1),
            "yearly_generation": round(estimated_power * sun_hours * (1 - system_losses) * 365, 1)
        }
    
    def _map_panel_dict(self, panel_dict: Dict[str, Any]) -> SolarPanel:
        """Mapear diccionario de panel a objeto SolarPanel"""
        return SolarPanel(
            id=panel_dict.get("id", "panel_default"),
            name=panel_dict.get("model", "Panel Solar"),
            brand=panel_dict.get("brand", "Marca"),
            model=panel_dict.get("model", "Modelo"),
            power_watts=float(panel_dict.get("power_watts", 400)),
            efficiency=float(panel_dict.get("efficiency", 20.0)),
            dimensions={"width": 2000, "height": 1000, "depth": 40},
            weight=float(panel_dict.get("weight", 25.0)),
            temperature_coefficient=float(panel_dict.get("temperature_coefficient", -0.4)),
            max_voltage=float(panel_dict.get("max_voltage", 50.0)),
            max_current=float(panel_dict.get("max_current", 10.0)),
            price_ars=float(panel_dict.get("price_ars", 180000)),
            warranty_years=int(panel_dict.get("warranty_years", 25)),
            type=panel_dict.get("type", "monocristalino")
        )
    
    def _map_inverter_dict(self, inverter_dict: Dict[str, Any]) -> Inverter:
        """Mapear diccionario de inversor a objeto Inverter"""
        return Inverter(
            id=inverter_dict.get("id", "inverter_default"),
            name=inverter_dict.get("model", "Inversor Solar"),
            brand=inverter_dict.get("brand", "Marca"),
            model=inverter_dict.get("model", "Modelo"),
            power_kw=float(inverter_dict.get("power_kw", 5.0)),
            efficiency=float(inverter_dict.get("efficiency", 96.0)),
            input_voltage_range={"min": 90, "max": 500},
            output_voltage=220.0,
            max_input_current=float(inverter_dict.get("max_input_current", 12.0)),
            has_mppt=inverter_dict.get("has_mppt", True),
            has_wifi=inverter_dict.get("has_wifi", True),
            price_ars=float(inverter_dict.get("price_ars", 800000)),
            warranty_years=int(inverter_dict.get("warranty_years", 10)),
            type=inverter_dict.get("type", "string")
        )
    
    def _map_battery_dict(self, battery_dict: Dict[str, Any]) -> Battery:
        """Mapear diccionario de batería a objeto Battery"""
        logger.info(f"🔋 Mapeando batería: {battery_dict.get('id', 'unknown')}")
        logger.info(f"🔋 Datos de batería: {battery_dict}")
        
        # Verificar campos requeridos
        required_fields = ["capacity_ah", "dimensions", "weight"]
        missing_fields = [field for field in required_fields if field not in battery_dict]
        
        if missing_fields:
            logger.warning(f"⚠️ Campos faltantes en batería: {missing_fields}")
            logger.warning(f"⚠️ Usando valores por defecto para: {missing_fields}")
        
        return Battery(
            id=battery_dict.get("id", "battery_default"),
            name=battery_dict.get("model", "Batería Solar"),
            brand=battery_dict.get("brand", "Marca"),
            model=battery_dict.get("model", "Modelo"),
            capacity_ah=float(battery_dict.get("capacity_ah", 200.0)),  # Campo requerido agregado
            voltage=float(battery_dict.get("voltage", 48.0)),
            power_kwh=float(battery_dict.get("power_kw", 10.0)),
            cycles=int(battery_dict.get("cycles", 6000)),
            efficiency=float(battery_dict.get("efficiency", 95.0)),
            dimensions=battery_dict.get("dimensions", {"width": 500, "height": 300, "depth": 200}),  # Campo requerido agregado
            weight=float(battery_dict.get("weight", 50.0)),  # Campo requerido agregado
            price_ars=float(battery_dict.get("price_ars", 3000000)),
            warranty_years=int(battery_dict.get("warranty_years", 10)),
            type=battery_dict.get("type", "litio")
        )
    
    def _map_mounting_dict(self, mounting_dict: Dict[str, Any]) -> MountingSystem:
        """Mapear diccionario de montaje a objeto MountingSystem"""
        return MountingSystem(
            id=mounting_dict.get("id", "mounting_default"),
            name=mounting_dict.get("model", "Sistema de Montaje"),
            brand=mounting_dict.get("brand", "Marca"),
            model=mounting_dict.get("model", "Modelo"),
            type="techo_residencial",
            material=mounting_dict.get("material", "aluminio"),
            max_wind_load=float(mounting_dict.get("max_wind_load", 200.0)),
            max_snow_load=float(mounting_dict.get("max_snow_load", 100.0)),
            price_per_kw=float(mounting_dict.get("price_per_kw", 150000)),
            installation_cost_per_kw=float(mounting_dict.get("installation_cost_per_kw", 50000)),
            warranty_years=int(mounting_dict.get("warranty_years", 10))
        )
    
    def _map_cable_dict(self, cable_dict: Dict[str, Any]) -> Cable:
        """Mapear diccionario de cable a objeto Cable"""
        return Cable(
            id=cable_dict.get("id", "cable_default"),
            name=cable_dict.get("model", "Cable Solar"),
            brand=cable_dict.get("brand", "Marca"),
            model=cable_dict.get("model", "Modelo"),
            type=cable_dict.get("type", "dc"),
            section_mm2=float(cable_dict.get("section_mm2", 4.0)),
            length_meters=float(cable_dict.get("length_meters", 100.0)),
            price_per_meter=float(cable_dict.get("price_per_meter", 250.0)),
            price_ars=float(cable_dict.get("price_ars", 25000))
        )
    
    def _map_protection_dict(self, protection_dict: Dict[str, Any]) -> ProtectionDevice:
        """Mapear diccionario de protección a objeto ProtectionDevice"""
        return ProtectionDevice(
            id=protection_dict.get("id", "protection_default"),
            name=protection_dict.get("model", "Dispositivo de Protección"),
            brand=protection_dict.get("brand", "Marca"),
            model=protection_dict.get("model", "Modelo"),
            type=protection_dict.get("type", "fusible"),
            current_rating=float(protection_dict.get("current_rating", 25.0)),
            voltage_rating=float(protection_dict.get("voltage_rating", 1000.0)),
            price_ars=float(protection_dict.get("price_ars", 45000))
        )
