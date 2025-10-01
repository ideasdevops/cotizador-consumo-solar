"""
Modelos de datos para el sistema de cotización solar
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class SolarPanelType(str, Enum):
    """Tipos de paneles solares"""
    MONOCRISTALINO = "monocristalino"
    POLICRISTALINO = "policristalino"
    THIN_FILM = "thin_film"
    BIFACIAL = "bifacial"


class InverterType(str, Enum):
    """Tipos de inversores"""
    STRING = "string"
    MICRO = "micro"
    CENTRAL = "central"
    HIBRIDO = "hibrido"


class BatteryType(str, Enum):
    """Tipos de baterías"""
    LITIO = "litio"
    PLOMO_ACIDO = "plomo_acido"
    GEL = "gel"
    AGM = "agm"


class InstallationType(str, Enum):
    """Tipos de instalación"""
    TECHO_RESIDENCIAL = "techo_residencial"
    TECHO_COMERCIAL = "techo_comercial"
    SUELO_RESIDENCIAL = "suelo_residencial"
    SUELO_COMERCIAL = "suelo_comercial"
    CARPORT = "carport"
    FACHADA = "fachada"


class SolarPanel(BaseModel):
    """Modelo de panel solar"""
    id: str
    name: str
    brand: str
    model: str
    type: SolarPanelType
    power_watts: int = Field(..., description="Potencia en watts")
    efficiency: float = Field(..., description="Eficiencia del panel (%)")
    dimensions: Dict[str, float] = Field(..., description="Dimensiones en mm")
    weight: float = Field(..., description="Peso en kg")
    price_ars: float = Field(..., description="Precio en pesos argentinos")
    warranty_years: int = Field(..., description="Garantía en años")
    temperature_coefficient: float = Field(..., description="Coeficiente de temperatura")
    max_voltage: float = Field(..., description="Voltaje máximo")
    max_current: float = Field(..., description="Corriente máxima")
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)


class Inverter(BaseModel):
    """Modelo de inversor"""
    id: str
    name: str
    brand: str
    model: str
    type: InverterType
    power_kw: float = Field(..., description="Potencia en kW")
    efficiency: float = Field(..., description="Eficiencia del inversor (%)")
    input_voltage_range: Dict[str, float] = Field(..., description="Rango de voltaje de entrada")
    output_voltage: float = Field(..., description="Voltaje de salida")
    max_input_current: float = Field(..., description="Corriente máxima de entrada")
    price_ars: float = Field(..., description="Precio en pesos argentinos")
    warranty_years: int = Field(..., description="Garantía en años")
    has_mppt: bool = Field(..., description="Tiene seguimiento MPPT")
    has_wifi: bool = Field(..., description="Tiene conectividad WiFi")
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)


class Battery(BaseModel):
    """Modelo de batería"""
    id: str
    name: str
    brand: str
    model: str
    type: BatteryType
    capacity_ah: float = Field(..., description="Capacidad en Ah")
    voltage: float = Field(..., description="Voltaje nominal")
    power_kwh: float = Field(..., description="Energía en kWh")
    cycles: int = Field(..., description="Ciclos de vida")
    efficiency: float = Field(..., description="Eficiencia de carga/descarga")
    dimensions: Dict[str, float] = Field(..., description="Dimensiones en mm")
    weight: float = Field(..., description="Peso en kg")
    price_ars: float = Field(..., description="Precio en pesos argentinos")
    warranty_years: int = Field(..., description="Garantía en años")
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)


class MountingSystem(BaseModel):
    """Modelo de sistema de montaje"""
    id: str
    name: str
    brand: str
    model: str
    type: InstallationType
    material: str = Field(..., description="Material del sistema")
    max_wind_load: float = Field(..., description="Carga máxima de viento (m/s)")
    max_snow_load: float = Field(..., description="Carga máxima de nieve (kg/m²)")
    price_per_kw: float = Field(..., description="Precio por kW instalado")
    installation_cost_per_kw: float = Field(..., description="Costo de instalación por kW")
    warranty_years: int = Field(..., description="Garantía en años")
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)


class Cable(BaseModel):
    """Modelo de cable solar"""
    id: str
    name: str
    brand: str
    model: str
    section_mm2: float = Field(..., description="Sección en mm²")
    voltage_rating: float = Field(..., description="Tensión nominal")
    current_rating: float = Field(..., description="Corriente nominal")
    length_meters: float = Field(..., description="Longitud en metros")
    price_per_meter: float = Field(..., description="Precio por metro")
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)


class ProtectionDevice(BaseModel):
    """Modelo de dispositivo de protección"""
    id: str
    name: str
    brand: str
    model: str
    type: str = Field(..., description="Tipo de protección (fusible, disyuntor, etc.)")
    current_rating: float = Field(..., description="Corriente nominal")
    voltage_rating: float = Field(..., description="Tensión nominal")
    price_ars: float = Field(..., description="Precio en pesos argentinos")
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)


class SolarQuoteRequest(BaseModel):
    """Solicitud de cotización solar"""
    # Datos del cliente
    client_name: Optional[str] = None
    client_email: Optional[str] = None
    client_phone: Optional[str] = None
    
    # Ubicación
    location: str = Field(..., description="Ubicación del proyecto")
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    
    # Consumo energético
    monthly_consumption_kwh: float = Field(..., description="Consumo mensual en kWh")
    peak_consumption_kw: Optional[float] = Field(None, description="Consumo pico en kW")
    tariff_type: str = Field(..., description="Tipo de tarifa (residencial, comercial, industrial)")
    
    # Dimensiones del área
    available_area_m2: float = Field(..., description="Área disponible en m²")
    roof_type: Optional[str] = Field(None, description="Tipo de techo")
    roof_orientation: Optional[str] = Field(None, description="Orientación del techo")
    roof_tilt: Optional[float] = Field(None, description="Inclinación del techo en grados")
    
    # Preferencias del sistema
    installation_type: InstallationType = Field(..., description="Tipo de instalación")
    panel_type_preference: Optional[SolarPanelType] = None
    inverter_type_preference: Optional[InverterType] = None
    battery_backup: bool = Field(False, description="Requiere respaldo con baterías")
    battery_autonomy_hours: Optional[int] = Field(None, description="Autonomía de baterías en horas")
    
    # Presupuesto
    budget_range: Optional[str] = Field(None, description="Rango de presupuesto")
    financing_required: bool = Field(False, description="Requiere financiamiento")
    
    # Observaciones
    notes: Optional[str] = None


class SolarSystemDesign(BaseModel):
    """Diseño del sistema solar"""
    # Dimensionamiento
    required_power_kwp: float = Field(..., description="Potencia requerida en kWp")
    panel_count: int = Field(..., description="Cantidad de paneles")
    inverter_count: int = Field(..., description="Cantidad de inversores")
    battery_count: Optional[int] = Field(None, description="Cantidad de baterías")
    
    # Componentes seleccionados
    selected_panels: List[SolarPanel] = Field(..., description="Paneles seleccionados")
    selected_inverters: List[Inverter] = Field(..., description="Inversores seleccionados")
    selected_batteries: Optional[List[Battery]] = None
    selected_mounting: MountingSystem = Field(..., description="Sistema de montaje")
    selected_cables: List[Cable] = Field(..., description="Cables necesarios")
    selected_protection: List[ProtectionDevice] = Field(..., description="Dispositivos de protección")
    
    # Cálculos energéticos
    daily_generation_kwh: float = Field(..., description="Generación diaria en kWh")
    monthly_generation_kwh: float = Field(..., description="Generación mensual en kWh")
    annual_generation_kwh: float = Field(..., description="Generación anual en kWh")
    system_efficiency: float = Field(..., description="Eficiencia del sistema")
    
    # Cálculos económicos
    total_investment: float = Field(..., description="Inversión total")
    monthly_savings: float = Field(..., description="Ahorro mensual")
    annual_savings: float = Field(..., description="Ahorro anual")
    payback_years: float = Field(..., description="Años de retorno de inversión")
    roi_percentage: float = Field(..., description="ROI porcentual anual")
    
    # Desglose de costos
    panels_cost: float = Field(..., description="Costo de paneles")
    inverters_cost: float = Field(..., description="Costo de inversores")
    batteries_cost: Optional[float] = Field(None, description="Costo de baterías")
    mounting_cost: float = Field(..., description="Costo de montaje")
    cables_cost: float = Field(..., description="Costo de cables")
    protection_cost: float = Field(..., description="Costo de protección")
    installation_cost: float = Field(..., description="Costo de instalación")
    permits_cost: float = Field(..., description="Costo de permisos")
    
    # Información adicional
    installation_time_days: int = Field(..., description="Tiempo de instalación en días")
    warranty_years: int = Field(..., description="Garantía del sistema en años")
    maintenance_cost_annual: float = Field(..., description="Costo anual de mantenimiento")


class SolarQuoteResponse(BaseModel):
    """Respuesta de cotización solar"""
    quote_id: str = Field(..., description="ID de la cotización")
    request: SolarQuoteRequest = Field(..., description="Solicitud original")
    design: SolarSystemDesign = Field(..., description="Diseño del sistema")
    created_at: datetime = Field(default_factory=datetime.now)
    valid_until: datetime = Field(..., description="Válido hasta")
    status: str = Field("pending", description="Estado de la cotización")


class MaterialPriceUpdate(BaseModel):
    """Actualización de precios de materiales"""
    material_type: str = Field(..., description="Tipo de material")
    material_id: str = Field(..., description="ID del material")
    new_price: float = Field(..., description="Nuevo precio")
    price_source: str = Field(..., description="Fuente del precio")
    updated_at: datetime = Field(default_factory=datetime.now)


class SolarCalculationParams(BaseModel):
    """Parámetros para cálculos solares"""
    location: str = Field(..., description="Ubicación")
    latitude: float = Field(..., description="Latitud")
    longitude: float = Field(..., description="Longitud")
    sun_hours_daily: float = Field(..., description="Horas de sol diarias")
    temperature_coefficient: float = Field(..., description="Coeficiente de temperatura")
    system_losses: float = Field(..., description="Pérdidas del sistema (%)")
    roof_tilt: float = Field(..., description="Inclinación del techo")
    roof_orientation: str = Field(..., description="Orientación del techo")
    shading_factor: float = Field(..., description="Factor de sombreado")
