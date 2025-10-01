# 🔧 Configuración para Easypanel - Cotizador de Consumo Solar

## 📋 Información de la Aplicación

- **Nombre**: cotizador-solar
- **Descripción**: Cotizador de Consumo Solar - Sumpetrol SA
- **Versión**: 1.0.0
- **Repositorio**: `git@github.com:ideasdevops/cotizador-consumo-solar.git`
- **Dockerfile**: `Dockerfile.easypanel-optimized`

## 🏗️ Configuración de la Aplicación

### Tipo de Aplicación
- **Tipo**: SSH Git
- **Puerto**: 80
- **Protocolo**: HTTP

### Configuración de Build
- **Dockerfile**: `Dockerfile.easypanel-optimized`
- **Context**: `/`
- **Build Args**: 
  - `APP_NAME=cotizador-solar`
  - `APP_VERSION=1.0.0`
  - `APP_DESCRIPTION=Cotizador de Consumo Solar - Sumpetrol SA`

## 💾 Volúmenes Requeridos

### Volúmenes de Datos
| Nombre | Tipo | Ruta de Montaje | Descripción |
|--------|------|-----------------|-------------|
| `data` | VOLUME | `/data` | Datos persistentes de la aplicación |
| `logs` | VOLUME | `/data/logs` | Logs de todos los servicios |
| `cache` | VOLUME | `/data/cache` | Cache de APIs y precios |
| `backups` | VOLUME | `/data/backups` | Backups automáticos |
| `temp` | VOLUME | `/data/temp` | Archivos temporales |

### Volúmenes de Configuración
| Nombre | Tipo | Ruta de Montaje | Descripción |
|--------|------|-----------------|-------------|
| `nginx-config` | FILE | `/etc/nginx/conf.d/default.conf` | Configuración de nginx |
| `supervisor-config` | FILE | `/etc/supervisor/conf.d/supervisord.conf` | Configuración de supervisor |

## 🔐 Variables de Entorno

### Configuración Básica
```bash
APP_NAME=cotizador-solar
APP_VERSION=1.0.0
APP_DESCRIPTION=Cotizador de Consumo Solar - Sumpetrol SA
APP_ENV=production
DEBUG=false
LOG_LEVEL=INFO
```

### Configuración SMTP
```bash
SMTP_SERVER=c2630942.ferozo.com
SMTP_PORT=465
SMTP_USERNAME=novedades@sumpetrol.com.ar
SMTP_PASSWORD=Novedad3s2k24@@
SMTP_USE_TLS=true
SMTP_USE_SSL=true
CONTACT_EMAIL=marketing@sumpetrol.com.ar
```

### Configuración NocoDB
```bash
NOCODB_URL=https://bots-nocodb.prskfv.easypanel.host
NOCODB_TOKEN=JvshcwW9JUK_sR4yT7H5r7ygSA2BPFAGNI8nSeWF
NOCODB_BASE_ID=pjo0a1kfnvm1ai3
NOCODB_TABLE_ID=m7i75nx5rkwockg
```

### Configuración de APIs de Argentina
```bash
BCRA_API_URL=https://api.estadisticas.bcra.gob.ar/api/Estadistica/GetSeries
INDEC_API_URL=https://www.indec.gob.ar/indec/web/Institucional-Indec-Precios
DOLAR_BLUE_API_URL=https://api-dolar-argentina.herokuapp.com/api/dolares
```

### Configuración de Servicios
```bash
PYTHON_HOST=0.0.0.0
PYTHON_PORT=8000
PYTHON_WORKERS=2
NODE_HOST=0.0.0.0
NODE_PORT=8005
NGINX_PORT=80
```

### Configuración de Cache
```bash
CACHE_DURATION_HOURS=12
PRICE_UPDATE_INTERVAL_HOURS=12
EXCHANGE_UPDATE_INTERVAL_HOURS=6
```

### Configuración de Logs
```bash
LOG_DIR=/data/logs
NGINX_LOG_LEVEL=info
PYTHON_LOG_LEVEL=info
NODE_LOG_LEVEL=info
```

### Configuración de Volúmenes
```bash
DATA_DIR=/data
BACKUP_DIR=/data/backups
CACHE_DIR=/data/cache
TEMP_DIR=/data/temp
```

### Configuración de Seguridad
```bash
CORS_ORIGINS=*
CORS_CREDENTIALS=true
CORS_METHODS=GET,POST,PUT,DELETE,OPTIONS
CORS_HEADERS=*
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
```

### Configuración de Monitoreo
```bash
HEALTH_CHECK_INTERVAL=30
HEALTH_CHECK_TIMEOUT=10
HEALTH_CHECK_RETRIES=3
```

### Configuración de Backup
```bash
BACKUP_ENABLED=true
BACKUP_INTERVAL_HOURS=24
BACKUP_RETENTION_DAYS=30
```

### Configuración de Producción
```bash
PROD_MODE=true
PROD_SSL_ENABLED=false
PROD_DOMAIN=your-domain.com
PROD_EMAIL_FROM=noreply@sumpetrol.com.ar
```

### Configuración de Precios Base
```bash
BASE_STEEL_FRAME_PRICE=105.0
BASE_INDUSTRIAL_PRICE=125.0
BASE_CONTAINER_PRICE=80.0
BASE_MATERIALS_PRICE=45.0
BASE_LABOR_PRICE=35.0
BASE_FINISHES_PRICE=25.0
```

### Multiplicadores Regionales
```bash
REGIONAL_MULTIPLIER_BUENOS_AIRES=1.0
REGIONAL_MULTIPLIER_CORDOBA=0.95
REGIONAL_MULTIPLIER_SANTA_FE=0.92
REGIONAL_MULTIPLIER_MENDOZA=0.88
REGIONAL_MULTIPLIER_TUCUMAN=0.85
REGIONAL_MULTIPLIER_ENTRE_RIOS=0.90
REGIONAL_MULTIPLIER_CHACO=0.83
REGIONAL_MULTIPLIER_CORRIENTES=0.87
REGIONAL_MULTIPLIER_MISIONES=0.89
REGIONAL_MULTIPLIER_FORMOSA=0.82
REGIONAL_MULTIPLIER_CHUBUT=0.93
REGIONAL_MULTIPLIER_RIO_NEGRO=0.91
REGIONAL_MULTIPLIER_NEUQUEN=0.94
REGIONAL_MULTIPLIER_LA_PAMPA=0.86
REGIONAL_MULTIPLIER_SAN_LUIS=0.84
REGIONAL_MULTIPLIER_LA_RIOJA=0.81
REGIONAL_MULTIPLIER_CATAMARCA=0.83
REGIONAL_MULTIPLIER_SANTIAGO=0.80
REGIONAL_MULTIPLIER_SALTA=0.86
REGIONAL_MULTIPLIER_JUJUY=0.85
REGIONAL_MULTIPLIER_SAN_JUAN=0.87
REGIONAL_MULTIPLIER_TIERRA_FUEGO=1.15
```

## 🌐 Configuración de Red

### Puertos Expuestos
- **80**: Nginx (HTTP)
- **8000**: Python Backend (FastAPI)
- **8005**: Node.js Backend (Express)

### Configuración de Proxy
- **Frontend**: `http://localhost/`
- **API Python**: `http://localhost/api/`
- **API Node.js**: `http://localhost/node-api/`
- **Documentación**: `http://localhost/docs`

## 🔍 Health Checks

### Configuración de Health Check
- **Endpoint**: `/health`
- **Intervalo**: 30 segundos
- **Timeout**: 10 segundos
- **Retries**: 3
- **Start Period**: 60 segundos

### Endpoints de Health Check
- **Nginx**: `http://localhost/health`
- **Python**: `http://localhost:8000/health`
- **Node.js**: `http://localhost:8005/health`

## 📊 Monitoreo y Logs

### Logs Disponibles
- **Nginx**: `/data/logs/nginx/`
- **Python**: `/data/logs/python/`
- **Node.js**: `/data/logs/node/`
- **Supervisor**: `/data/logs/supervisor/`

### Métricas Recomendadas
- Disponibilidad del servicio
- Tiempo de respuesta de la API
- Uso de memoria y CPU
- Errores por minuto
- Número de cotizaciones generadas

## 🔒 Seguridad

### Medidas Implementadas
- Validación de entrada en frontend y backend
- Sanitización de datos
- CORS configurado
- Rate limiting en APIs críticas
- Logs de seguridad
- Health checks automáticos

### Recomendaciones
- Mantener dependencias actualizadas
- Monitorear logs de seguridad
- Implementar autenticación si es necesario
- Configurar HTTPS en producción
- Implementar backup automático

## 🚀 Pasos para el Deploy

### 1. Preparación
1. Verificar que el repositorio esté actualizado
2. Ejecutar script de validación: `./validate-deploy.sh`
3. Hacer commit y push de los cambios

### 2. Configuración en Easypanel
1. Crear nueva aplicación
2. Configurar tipo SSH Git
3. Establecer repositorio y Dockerfile
4. Configurar volúmenes
5. Establecer variables de entorno
6. Configurar health checks

### 3. Deploy
1. Ejecutar build de la aplicación
2. Verificar que todos los servicios estén corriendo
3. Probar endpoints principales
4. Verificar logs
5. Configurar monitoreo

### 4. Post-Deploy
1. Verificar funcionalidad completa
2. Probar envío de emails
3. Verificar integración con NocoDB
4. Probar APIs de Argentina
5. Configurar alertas

## 📞 Soporte

### Contacto Técnico
- **Email**: marketing@sumpetrol.com.ar
- **Sitio Web**: https://sumpetrol.com.ar

### Documentación
- **Deploy**: `DEPLOY.md`
- **Técnica**: `DOCUMENTACION_TECNICA.md`
- **Instalación**: `INSTALACION.md`

---

**Configuración optimizada para Easypanel por IdeasDevOps**