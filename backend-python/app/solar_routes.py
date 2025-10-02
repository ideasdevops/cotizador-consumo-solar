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
from .nocodb_service import nocodb_service

logger = logging.getLogger(__name__)

# Router para las rutas solares
router = APIRouter(prefix="/api/solar", tags=["solar"])

@router.get("/health")
async def health_check():
    """Endpoint de salud para verificar conectividad"""
    return {
        "status": "ok",
        "message": "Solar API is running",
        "timestamp": datetime.now().isoformat()
    }

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
        logger.info(f"🔍 Iniciando estimación rápida:")
        logger.info(f"   📊 Consumo mensual: {monthly_consumption} kWh")
        logger.info(f"   📍 Ubicación: {location}")
        logger.info(f"   🏠 Tipo de instalación: {installation_type}")
        
        if monthly_consumption <= 0:
            raise HTTPException(status_code=400, detail="El consumo mensual debe ser mayor a 0")
        
        estimation = solar_calculator.estimate_system_size(
            monthly_consumption=monthly_consumption,
            location=location,
            installation_type=installation_type
        )
        
        logger.info(f"✅ Estimación completada: {estimation}")
        return estimation
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error estimando sistema: {e}")
        logger.error(f"❌ Tipo de error: {type(e).__name__}")
        import traceback
        logger.error(f"❌ Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.post("/quote", response_model=SolarQuoteResponse)
async def create_solar_quote(
    request: SolarQuoteRequest,
    background_tasks: BackgroundTasks
) -> SolarQuoteResponse:
    """Crear cotización solar completa"""
    try:
        logger.info(f"Iniciando cotización para: {request.client_name or 'Cliente anónimo'}")
        logger.info(f"Datos recibidos: consumo={request.monthly_consumption_kwh}, área={request.available_area_m2}, ubicación={request.location}")
        
        # Validar datos de entrada
        if request.monthly_consumption_kwh <= 0:
            logger.error("Consumo mensual inválido")
            raise HTTPException(status_code=400, detail="El consumo mensual debe ser mayor a 0")
        
        if request.available_area_m2 <= 0:
            logger.error("Área disponible inválida")
            raise HTTPException(status_code=400, detail="El área disponible debe ser mayor a 0")
        
        if not request.location:
            logger.error("Ubicación no especificada")
            raise HTTPException(status_code=400, detail="Debe especificar una ubicación")
        
        if not request.tariff_type:
            logger.error("Tipo de tarifa no especificado")
            raise HTTPException(status_code=400, detail="Debe especificar un tipo de tarifa")
        
        if not request.installation_type:
            logger.error("Tipo de instalación no especificado")
            raise HTTPException(status_code=400, detail="Debe especificar un tipo de instalación")
        
        # Generar ID único para la cotización
        quote_id = str(uuid.uuid4())
        logger.info(f"ID de cotización generado: {quote_id}")
        
        # Calcular diseño del sistema
        logger.info("Iniciando cálculo del sistema...")
        design = solar_calculator.calculate_system_design(request)
        logger.info(f"Cálculo completado. Potencia: {design.required_power_kwp} kWp")
        
        # Crear respuesta de cotización
        quote_response = SolarQuoteResponse(
            quote_id=quote_id,
            request=request,
            design=design,
            valid_until=datetime.now() + timedelta(days=30)  # Válida por 30 días
        )
        
        # Guardar cotización
        quotes_storage[quote_id] = quote_response
        
        # Guardar en NocoDB (en background)
        background_tasks.add_task(save_quote_to_nocodb, quote_response)
        
        # Enviar email de confirmación (en background)
        if request.client_email:
            background_tasks.add_task(send_quote_email, quote_response)
        
        logger.info(f"Cotización creada exitosamente: {quote_id}")
        return quote_response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creando cotización: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


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

@router.get("/test")
async def test_solar_calculator() -> Dict[str, Any]:
    """Endpoint de prueba para el calculador solar"""
    try:
        # Crear una solicitud de prueba
        test_request = SolarQuoteRequest(
            client_name="Test Cliente",
            client_email="test@example.com",
            location="buenos-aires",
            monthly_consumption_kwh=300,
            tariff_type="residential",
            available_area_m2=50,
            installation_type=InstallationType.TECHO_RESIDENCIAL
        )
        
        # Calcular sistema
        design = solar_calculator.calculate_system_design(test_request)
        
        return {
            "status": "success",
            "test_data": {
                "required_power_kwp": design.required_power_kwp,
                "panel_count": design.panel_count,
                "total_investment": design.total_investment,
                "monthly_savings": design.monthly_savings,
                "payback_years": design.payback_years
            },
            "message": "Calculador solar funcionando correctamente"
        }
        
    except Exception as e:
        logger.error(f"Error en test del calculador: {e}", exc_info=True)
        return {
            "status": "error",
            "error": str(e),
            "message": "Error en el calculador solar"
        }

@router.post("/materials/sync")
async def sync_materials_from_external_source():
    """Sincronizar materiales desde fuente externa y guardar en NocoDB"""
    try:
        logger.info("Iniciando sincronización de materiales desde fuente externa...")
        
        # Obtener materiales desde fuente externa (simulada)
        external_materials = await get_external_solar_materials()
        
        # Guardar cada material en NocoDB
        saved_count = 0
        for material in external_materials:
            try:
                success = await nocodb_service.save_material(material)
                if success:
                    saved_count += 1
                    logger.info(f"Material guardado: {material.get('marca', '')} {material.get('modelo', '')}")
                else:
                    logger.error(f"Error guardando material: {material.get('marca', '')} {material.get('modelo', '')}")
            except Exception as e:
                logger.error(f"Error procesando material: {e}")
        
        return {
            "status": "success",
            "message": f"Sincronización completada: {saved_count}/{len(external_materials)} materiales guardados",
            "total_materials": len(external_materials),
            "saved_materials": saved_count
        }
        
    except Exception as e:
        logger.error(f"Error en sincronización de materiales: {e}", exc_info=True)
        return {
            "status": "error",
            "error": str(e),
            "message": "Error en sincronización de materiales"
        }

@router.get("/materials/from-nocodb")
async def get_materials_from_nocodb():
    """Obtener materiales desde NocoDB para el frontend"""
    try:
        logger.info("Obteniendo materiales desde NocoDB...")
        
        # Obtener materiales desde NocoDB
        materials_data = await nocodb_service.get_materials_from_nocodb()
        
        if materials_data:
            # Organizar materiales por tipo para el frontend
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
            
            logger.info(f"Materiales organizados: {len(materials_data)} registros")
            return organized_materials
            
        else:
            logger.warning("No se encontraron materiales en NocoDB")
            return {
                "panels": [],
                "inverters": [],
                "batteries": [],
                "mounting": [],
                "cables": [],
                "protection": []
            }
            
    except Exception as e:
        logger.error(f"Error obteniendo materiales desde NocoDB: {e}", exc_info=True)
        return {
            "status": "error",
            "error": str(e),
            "message": "Error obteniendo materiales desde NocoDB"
        }


async def get_external_solar_materials() -> List[Dict[str, Any]]:
    """Obtener materiales solares desde fuente externa (simulada)"""
    # En producción, aquí harías una llamada a una API externa
    # Por ahora, simulamos con datos de ejemplo
    return [
        # Paneles solares
        {
            "tipo_material": "panel",
            "marca": "JinkoSolar",
            "modelo": "JKM400M-54HL4-B",
            "potencia_watts": 400,
            "potencia_kw": 0.4,
            "precio_ars": 180000,
            "precio_por_kw": 450000,
            "stock_disponible": 50,
            "activo": True,
            "especificaciones_tecnicas": "Panel monocristalino de alta eficiencia",
            "garantia_anos": 25,
            "proveedor": "JinkoSolar Argentina",
            "fecha_actualizacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            "tipo_material": "panel",
            "marca": "Trina Solar",
            "modelo": "TSM-400DE14A(II)",
            "potencia_watts": 400,
            "potencia_kw": 0.4,
            "precio_ars": 175000,
            "precio_por_kw": 437500,
            "stock_disponible": 45,
            "activo": True,
            "especificaciones_tecnicas": "Panel monocristalino con tecnología PERC",
            "garantia_anos": 25,
            "proveedor": "Trina Solar Argentina",
            "fecha_actualizacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            "tipo_material": "panel",
            "marca": "LG Solar",
            "modelo": "LG400N2W-A5",
            "potencia_watts": 400,
            "potencia_kw": 0.4,
            "precio_ars": 195000,
            "precio_por_kw": 487500,
            "stock_disponible": 30,
            "activo": True,
            "especificaciones_tecnicas": "Panel monocristalino con tecnología NeON",
            "garantia_anos": 25,
            "proveedor": "LG Electronics",
            "fecha_actualizacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        # Inversores
        {
            "tipo_material": "inversor",
            "marca": "SMA",
            "modelo": "STP 5000TL-20",
            "potencia_watts": 5000,
            "potencia_kw": 5.0,
            "precio_ars": 800000,
            "precio_por_kw": 160000,
            "stock_disponible": 25,
            "activo": True,
            "especificaciones_tecnicas": "Inversor string de 5kW",
            "garantia_anos": 10,
            "proveedor": "SMA Argentina",
            "fecha_actualizacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            "tipo_material": "inversor",
            "marca": "Fronius",
            "modelo": "Primo 5.0-1",
            "potencia_watts": 5000,
            "potencia_kw": 5.0,
            "precio_ars": 750000,
            "precio_por_kw": 150000,
            "stock_disponible": 30,
            "activo": True,
            "especificaciones_tecnicas": "Inversor string de 5kW con WiFi",
            "garantia_anos": 10,
            "proveedor": "Fronius Argentina",
            "fecha_actualizacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            "tipo_material": "inversor",
            "marca": "Huawei",
            "modelo": "SUN2000-5KTL-L1",
            "potencia_watts": 5000,
            "potencia_kw": 5.0,
            "precio_ars": 700000,
            "precio_por_kw": 140000,
            "stock_disponible": 35,
            "activo": True,
            "especificaciones_tecnicas": "Inversor string de 5kW inteligente",
            "garantia_anos": 10,
            "proveedor": "Huawei Argentina",
            "fecha_actualizacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        # Baterías
        {
            "tipo_material": "bateria",
            "marca": "Tesla",
            "modelo": "Powerwall 2",
            "potencia_watts": 13500,
            "potencia_kw": 13.5,
            "precio_ars": 4500000,
            "precio_por_kw": 333333,
            "stock_disponible": 15,
            "activo": True,
            "especificaciones_tecnicas": "Batería de litio de 13.5kWh",
            "garantia_anos": 10,
            "proveedor": "Tesla Argentina",
            "fecha_actualizacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            "tipo_material": "bateria",
            "marca": "LG Chem",
            "modelo": "RESU10H",
            "potencia_watts": 9600,
            "potencia_kw": 9.6,
            "precio_ars": 3200000,
            "precio_por_kw": 333333,
            "stock_disponible": 20,
            "activo": True,
            "especificaciones_tecnicas": "Batería de litio de 9.6kWh",
            "garantia_anos": 10,
            "proveedor": "LG Chem Argentina",
            "fecha_actualizacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        # Sistemas de montaje
        {
            "tipo_material": "montaje",
            "marca": "Schletter",
            "modelo": "FS-R",
            "potencia_watts": 0,
            "potencia_kw": 0,
            "precio_ars": 0,
            "precio_por_kw": 150000,
            "stock_disponible": 100,
            "activo": True,
            "especificaciones_tecnicas": "Sistema de montaje para techo inclinado",
            "garantia_anos": 20,
            "proveedor": "Schletter Argentina",
            "fecha_actualizacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            "tipo_material": "montaje",
            "marca": "K2 Systems",
            "modelo": "K2 Solar Mount",
            "potencia_watts": 0,
            "potencia_kw": 0,
            "precio_ars": 0,
            "precio_por_kw": 140000,
            "stock_disponible": 80,
            "activo": True,
            "especificaciones_tecnicas": "Sistema de montaje universal",
            "garantia_anos": 20,
            "proveedor": "K2 Systems Argentina",
            "fecha_actualizacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        # Cables
        {
            "tipo_material": "cable",
            "marca": "Helukabel",
            "modelo": "Solar Cable 4mm2",
            "potencia_watts": 0,
            "potencia_kw": 0,
            "precio_ars": 25000,
            "precio_por_kw": 0,
            "stock_disponible": 500,
            "activo": True,
            "especificaciones_tecnicas": "Cable solar 4mm2 DC",
            "garantia_anos": 10,
            "proveedor": "Helukabel Argentina",
            "fecha_actualizacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        # Protecciones
        {
            "tipo_material": "proteccion",
            "marca": "ABB",
            "modelo": "OVR 1P 25A",
            "potencia_watts": 0,
            "potencia_kw": 0,
            "precio_ars": 45000,
            "precio_por_kw": 0,
            "stock_disponible": 200,
            "activo": True,
            "especificaciones_tecnicas": "Protector contra sobretensiones",
            "garantia_anos": 5,
            "proveedor": "ABB Argentina",
            "fecha_actualizacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    ]

async def save_quote_to_nocodb(quote: SolarQuoteResponse):
    """Guardar cotización en NocoDB (función de background)"""
    try:
        logger.info(f"Guardando cotización {quote.quote_id} en NocoDB...")
        
        # Preparar datos para NocoDB
        quote_data = {
            "id_cotizacion": quote.quote_id,
            "id_cliente": quote.request.client_email or "anonimo",
            "nombre_cliente": quote.request.client_name or "Cliente Anónimo",
            "email_cliente": quote.request.client_email or "",
            "ubicacion_proyecto": quote.request.location,
            "consumo_mensual_kwh": quote.request.monthly_consumption_kwh,
            "tipo_tarifa": quote.request.tariff_type,
            "area_disponible_m2": quote.request.available_area_m2,
            "tipo_instalacion": quote.request.installation_type,
            "potencia_requerida_kwp": quote.design.required_power_kwp,
            "cantidad_paneles": quote.design.panel_count,
            "generacion_mensual_kwh": quote.design.monthly_generation_kwh,
            "ahorro_mensual_ars": quote.design.monthly_savings,
            "inversion_total_ars": quote.design.total_investment,
            "roi_anos": quote.design.payback_years,
            "fecha_cotizacion": quote.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "estado_cotizacion": "generada",
            "notas_adicionales": f"Tipo de batería: {quote.request.battery_type or 'No especificado'}"
        }
        
        # Guardar en NocoDB
        success = await nocodb_service.save_solar_quote(quote_data)
        
        if success:
            logger.info(f"Cotización {quote.quote_id} guardada exitosamente en NocoDB")
        else:
            logger.error(f"Error guardando cotización {quote.quote_id} en NocoDB")
        
    except Exception as e:
        logger.error(f"Error guardando cotización en NocoDB: {e}")

async def send_quote_email(quote: SolarQuoteResponse):
    """Enviar email con la cotización (función de background)"""
    try:
        logger.info(f"Enviando email de cotización {quote.quote_id} a {quote.request.client_email}")
        
        # Importar el servicio de email mejorado
        from .email_service_improved import improved_email_service
        
        # Enviar email al cliente
        success = improved_email_service.send_solar_quote_email(
            to_email=quote.request.client_email,
            customer_name=quote.request.client_name,
            quote_data=quote.dict()
        )
        
        if success:
            logger.info(f"Email de cotización enviado exitosamente a {quote.request.client_email}")
        else:
            logger.error(f"Error enviando email de cotización a {quote.request.client_email}")
        
        # Enviar notificación interna a marketing
        notification_success = improved_email_service.send_quote_notification_email(quote.dict())
        
        if notification_success:
            logger.info("Notificación interna enviada a marketing@sumpetrol.com.ar")
        else:
            logger.error("Error enviando notificación interna")
        
    except Exception as e:
        logger.error(f"Error enviando email de cotización: {e}")


# Rutas de compatibilidad con el frontend existente
@router.get("/materials")
async def get_materials():
    """Obtener lista de materiales solares desde NocoDB"""
    try:
        logger.info("🔍 Obteniendo materiales desde NocoDB...")
        logger.info(f"📡 URL de NocoDB: {nocodb_service.materiales_url}")
        logger.info(f"🔑 Token configurado: {'Sí' if nocodb_service.nocodb_token else 'No'}")
        
        # Obtener materiales desde NocoDB
        materials_data = await nocodb_service.get_materials_from_nocodb()
        logger.info(f"📦 Materiales obtenidos: {len(materials_data) if materials_data else 0} registros")
        
        if materials_data:
            # Organizar materiales por tipo para el frontend
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
            
            logger.info(f"Materiales organizados: {len(materials_data)} registros")
            return organized_materials
            
        else:
            logger.warning("No se encontraron materiales en NocoDB, usando materiales por defecto")
            # Fallback a materiales por defecto
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
            
    except Exception as e:
        logger.error(f"Error obteniendo materiales: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error obteniendo materiales: {str(e)}")


@router.post("/calculate")
async def calculate_solar_system(request: SolarQuoteRequest) -> SolarSystemDesign:
    """Calcular sistema solar (endpoint de compatibilidad)"""
    try:
        design = solar_calculator.calculate_system_design(request)
        return design
    except Exception as e:
        logger.error(f"Error calculando sistema solar: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")
