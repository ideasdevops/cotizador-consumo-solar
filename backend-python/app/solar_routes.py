"""
Rutas de la API para el sistema de cotización solar
"""
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import logging
import uuid

from .solar_models import (
    SolarQuoteRequest, SolarQuoteResponse, SolarSystemDesign,
    SolarPanel, Inverter, Battery, MountingSystem, Cable, ProtectionDevice,
    SolarPanelType, InverterType, BatteryType, InstallationType,
    MaterialPriceUpdate
)
from .solar_calculator import SolarCalculator
from .solar_materials_service import SolarMaterialsService

logger = logging.getLogger(__name__)

# Router para las rutas solares
router = APIRouter(prefix="/api/solar", tags=["solar"])

# Instancias de servicios
materials_service = SolarMaterialsService()
solar_calculator = SolarCalculator()

# Almacenamiento temporal de cotizaciones (en producción usar base de datos)
quotes_storage: Dict[str, SolarQuoteResponse] = {}


@router.get("/materials/panels")
async def get_solar_panels(
    panel_type: Optional[SolarPanelType] = None,
    min_power: Optional[int] = None,
    max_power: Optional[int] = None
) -> List[SolarPanel]:
    """Obtener paneles solares con filtros opcionales"""
    try:
        panels = materials_service.get_panels(
            panel_type=panel_type,
            min_power=min_power,
            max_power=max_power
        )
        return panels
    except Exception as e:
        logger.error(f"Error obteniendo paneles: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/materials/inverters")
async def get_inverters(
    inverter_type: Optional[InverterType] = None,
    min_power: Optional[float] = None,
    max_power: Optional[float] = None
) -> List[Inverter]:
    """Obtener inversores con filtros opcionales"""
    try:
        inverters = materials_service.get_inverters(
            inverter_type=inverter_type,
            min_power=min_power,
            max_power=max_power
        )
        return inverters
    except Exception as e:
        logger.error(f"Error obteniendo inversores: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/materials/batteries")
async def get_batteries(
    battery_type: Optional[BatteryType] = None,
    min_capacity: Optional[float] = None,
    max_capacity: Optional[float] = None
) -> List[Battery]:
    """Obtener baterías con filtros opcionales"""
    try:
        batteries = materials_service.get_batteries(
            battery_type=battery_type,
            min_capacity=min_capacity,
            max_capacity=max_capacity
        )
        return batteries
    except Exception as e:
        logger.error(f"Error obteniendo baterías: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/materials/mounting")
async def get_mounting_systems(
    installation_type: Optional[InstallationType] = None
) -> List[MountingSystem]:
    """Obtener sistemas de montaje"""
    try:
        mounting = materials_service.get_mounting_systems(installation_type=installation_type)
        return mounting
    except Exception as e:
        logger.error(f"Error obteniendo sistemas de montaje: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/materials/cables")
async def get_cables(
    min_section: Optional[float] = None,
    max_section: Optional[float] = None
) -> List[Cable]:
    """Obtener cables con filtros opcionales"""
    try:
        cables = materials_service.get_cables(
            min_section=min_section,
            max_section=max_section
        )
        return cables
    except Exception as e:
        logger.error(f"Error obteniendo cables: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/materials/protection")
async def get_protection_devices(
    device_type: Optional[str] = None,
    min_current: Optional[float] = None,
    max_current: Optional[float] = None
) -> List[ProtectionDevice]:
    """Obtener dispositivos de protección"""
    try:
        devices = materials_service.get_protection_devices(
            device_type=device_type,
            min_current=min_current,
            max_current=max_current
        )
        return devices
    except Exception as e:
        logger.error(f"Error obteniendo dispositivos de protección: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/materials/summary")
async def get_materials_summary() -> Dict[str, Any]:
    """Obtener resumen de todos los materiales disponibles"""
    try:
        summary = materials_service.get_materials_summary()
        return summary
    except Exception as e:
        logger.error(f"Error obteniendo resumen de materiales: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.post("/materials/update-price")
async def update_material_price(price_update: MaterialPriceUpdate) -> Dict[str, Any]:
    """Actualizar precio de un material"""
    try:
        success = materials_service.update_material_price(
            material_type=price_update.material_type,
            material_id=price_update.material_id,
            new_price=price_update.new_price,
            price_source=price_update.price_source
        )
        
        if success:
            return {
                "success": True,
                "message": "Precio actualizado correctamente",
                "material_type": price_update.material_type,
                "material_id": price_update.material_id,
                "new_price": price_update.new_price,
                "updated_at": price_update.updated_at
            }
        else:
            raise HTTPException(status_code=400, detail="Error actualizando precio")
            
    except Exception as e:
        logger.error(f"Error actualizando precio: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/locations/{location}/sun-data")
async def get_location_sun_data(location: str) -> Dict[str, Any]:
    """Obtener datos de radiación solar por ubicación"""
    try:
        sun_data = solar_calculator.get_location_sun_data(location)
        return sun_data
    except Exception as e:
        logger.error(f"Error obteniendo datos solares para {location}: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.post("/estimate")
async def estimate_system_size(
    monthly_consumption: float,
    location: str,
    installation_type: InstallationType
) -> Dict[str, Any]:
    """Estimar tamaño del sistema solar"""
    try:
        if monthly_consumption <= 0:
            raise HTTPException(status_code=400, detail="El consumo mensual debe ser mayor a 0")
        
        estimation = solar_calculator.estimate_system_size(
            monthly_consumption=monthly_consumption,
            location=location,
            installation_type=installation_type
        )
        
        return estimation
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error estimando sistema: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.post("/quote", response_model=SolarQuoteResponse)
async def create_solar_quote(
    request: SolarQuoteRequest,
    background_tasks: BackgroundTasks
) -> SolarQuoteResponse:
    """Crear cotización solar completa"""
    try:
        # Validar datos de entrada
        if request.monthly_consumption_kwh <= 0:
            raise HTTPException(status_code=400, detail="El consumo mensual debe ser mayor a 0")
        
        if request.available_area_m2 <= 0:
            raise HTTPException(status_code=400, detail="El área disponible debe ser mayor a 0")
        
        # Generar ID único para la cotización
        quote_id = str(uuid.uuid4())
        
        # Calcular diseño del sistema
        design = solar_calculator.calculate_system_design(request)
        
        # Crear respuesta de cotización
        quote_response = SolarQuoteResponse(
            quote_id=quote_id,
            request=request,
            design=design,
            valid_until=datetime.now() + timedelta(days=30)  # Válida por 30 días
        )
        
        # Guardar cotización
        quotes_storage[quote_id] = quote_response
        
        # Enviar email de confirmación (en background)
        if request.client_email:
            background_tasks.add_task(send_quote_email, quote_response)
        
        logger.info(f"Cotización creada: {quote_id}")
        return quote_response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creando cotización: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/quote/{quote_id}", response_model=SolarQuoteResponse)
async def get_solar_quote(quote_id: str) -> SolarQuoteResponse:
    """Obtener cotización por ID"""
    try:
        if quote_id not in quotes_storage:
            raise HTTPException(status_code=404, detail="Cotización no encontrada")
        
        quote = quotes_storage[quote_id]
        
        # Verificar si la cotización sigue siendo válida
        if quote.valid_until < datetime.now():
            raise HTTPException(status_code=410, detail="Cotización expirada")
        
        return quote
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error obteniendo cotización {quote_id}: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/quotes")
async def list_solar_quotes(
    limit: int = 10,
    offset: int = 0
) -> Dict[str, Any]:
    """Listar cotizaciones (para administración)"""
    try:
        quotes_list = list(quotes_storage.values())
        
        # Ordenar por fecha de creación (más recientes primero)
        quotes_list.sort(key=lambda x: x.created_at, reverse=True)
        
        # Paginación
        total = len(quotes_list)
        quotes_page = quotes_list[offset:offset + limit]
        
        return {
            "quotes": quotes_page,
            "total": total,
            "limit": limit,
            "offset": offset,
            "has_more": offset + limit < total
        }
        
    except Exception as e:
        logger.error(f"Error listando cotizaciones: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.delete("/quote/{quote_id}")
async def delete_solar_quote(quote_id: str) -> Dict[str, Any]:
    """Eliminar cotización"""
    try:
        if quote_id not in quotes_storage:
            raise HTTPException(status_code=404, detail="Cotización no encontrada")
        
        del quotes_storage[quote_id]
        
        return {
            "success": True,
            "message": "Cotización eliminada correctamente",
            "quote_id": quote_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error eliminando cotización {quote_id}: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/health")
async def solar_health_check() -> Dict[str, Any]:
    """Health check del sistema solar"""
    try:
        # Verificar servicios
        materials_summary = materials_service.get_materials_summary()
        
        # Contar materiales activos
        active_materials = sum(
            summary["active"] for summary in materials_summary.values()
        )
        
        return {
            "status": "healthy",
            "timestamp": datetime.now(),
            "active_materials": active_materials,
            "quotes_count": len(quotes_storage),
            "services": {
                "materials_service": "ok",
                "solar_calculator": "ok"
            }
        }
        
    except Exception as e:
        logger.error(f"Error en health check: {e}")
        return {
            "status": "unhealthy",
            "timestamp": datetime.now(),
            "error": str(e)
        }


async def send_quote_email(quote: SolarQuoteResponse):
    """Enviar email con la cotización (función de background)"""
    try:
        # Aquí implementarías el envío de email
        # Por ahora solo log
        logger.info(f"Enviando email de cotización {quote.quote_id} a {quote.request.client_email}")
        
        # TODO: Implementar envío real de email
        # email_service.send_quote_email(quote)
        
    except Exception as e:
        logger.error(f"Error enviando email de cotización: {e}")


# Rutas de compatibilidad con el frontend existente
@router.get("/materials")
async def get_all_materials() -> Dict[str, Any]:
    """Obtener todos los materiales (endpoint de compatibilidad)"""
    try:
        return {
            "panels": materials_service.get_panels(),
            "inverters": materials_service.get_inverters(),
            "batteries": materials_service.get_batteries(),
            "mounting": materials_service.get_mounting_systems(),
            "cables": materials_service.get_cables(),
            "protection": materials_service.get_protection_devices()
        }
    except Exception as e:
        logger.error(f"Error obteniendo todos los materiales: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.post("/calculate")
async def calculate_solar_system(request: SolarQuoteRequest) -> SolarSystemDesign:
    """Calcular sistema solar (endpoint de compatibilidad)"""
    try:
        design = solar_calculator.calculate_system_design(request)
        return design
    except Exception as e:
        logger.error(f"Error calculando sistema solar: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")
