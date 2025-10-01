# 🔐 Variables de Entorno - Easypanel

## 📋 Variables Requeridas

### Configuración Básica de la Aplicación
```bash
# Información de la aplicación
APP_NAME=cotizador-solar
APP_VERSION=1.0.0
APP_DESCRIPTION=Cotizador de Consumo Solar - Sumpetrol SA
APP_ENV=production
DEBUG=false
LOG_LEVEL=INFO
```

### Configuración de Servicios
```bash
# Python Backend (FastAPI)
PYTHON_HOST=0.0.0.0
PYTHON_PORT=8000
PYTHON_WORKERS=2
PYTHON_PATH=/app/backend-python

# Node.js Backend (Express)
NODE_HOST=0.0.0.0
NODE_PORT=8005
NODE_ENV=production

# Nginx
NGINX_PORT=80
NGINX_LOG_LEVEL=info
```

### Configuración SMTP - Sumpetrol
```bash
# Servidor SMTP
SMTP_SERVER=c2630942.ferozo.com
SMTP_PORT=465
SMTP_USERNAME=novedades@sumpetrol.com.ar
SMTP_PASSWORD=Novedad3s2k24@@
SMTP_USE_TLS=true
SMTP_USE_SSL=true

# Email de contacto
CONTACT_EMAIL=marketing@sumpetrol.com.ar
```

### Configuración NocoDB
```bash
# Conexión a NocoDB
NOCODB_URL=https://bots-nocodb.prskfv.easypanel.host
NOCODB_TOKEN=JvshcwW9JUK_sR4yT7H5r7ygSA2BPFAGNI8nSeWF
NOCODB_BASE_ID=pjo0a1kfnvm1ai3
NOCODB_TABLE_ID=m7i75nx5rkwockg

# Variables del contenedor NocoDB
NC_DATABASE_URL=postgresql://postgres:password@postgres:5432/nocodb
NC_REDIS_URL=redis://redis:6379
NC_AUTH_JWT_SECRET=your-jwt-secret-here
NC_PUBLIC_URL=https://your-domain.com
```

### Configuración de APIs de Argentina
```bash
# URLs de APIs oficiales
BCRA_API_URL=https://api.estadisticas.bcra.gob.ar/api/Estadistica/GetSeries
INDEC_API_URL=https://www.indec.gob.ar/indec/web/Institucional-Indec-Precios
DOLAR_BLUE_API_URL=https://api-dolar-argentina.herokuapp.com/api/dolares

# Configuración de cache
CACHE_DURATION_HOURS=12
PRICE_UPDATE_INTERVAL_HOURS=12
EXCHANGE_UPDATE_INTERVAL_HOURS=6
```

### Configuración de Volúmenes
```bash
# Directorios de datos
DATA_DIR=/data
LOG_DIR=/data/logs
CACHE_DIR=/data/cache
BACKUP_DIR=/data/backups
TEMP_DIR=/data/temp

# Configuración de logs
NGINX_LOG_LEVEL=info
PYTHON_LOG_LEVEL=info
NODE_LOG_LEVEL=info
```

### Configuración de Seguridad
```bash
# CORS
CORS_ORIGINS=*
CORS_CREDENTIALS=true
CORS_METHODS=GET,POST,PUT,DELETE,OPTIONS
CORS_HEADERS=*

# Rate limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
```

### Configuración de Monitoreo
```bash
# Health checks
HEALTH_CHECK_INTERVAL=30
HEALTH_CHECK_TIMEOUT=10
HEALTH_CHECK_RETRIES=3
HEALTH_CHECK_START_PERIOD=60
```

### Configuración de Backup
```bash
# Backup automático
BACKUP_ENABLED=true
BACKUP_INTERVAL_HOURS=24
BACKUP_RETENTION_DAYS=30
BACKUP_COMPRESSION=true
```

### Configuración de Producción
```bash
# Modo de producción
PROD_MODE=true
PROD_SSL_ENABLED=false
PROD_DOMAIN=your-domain.com
PROD_EMAIL_FROM=noreply@sumpetrol.com.ar
PROD_DEBUG=false
```

### Configuración de Precios Base
```bash
# Precios base en USD
BASE_STEEL_FRAME_PRICE=105.0
BASE_INDUSTRIAL_PRICE=125.0
BASE_CONTAINER_PRICE=80.0
BASE_MATERIALS_PRICE=45.0
BASE_LABOR_PRICE=35.0
BASE_FINISHES_PRICE=25.0
```

### Multiplicadores Regionales
```bash
# Buenos Aires
REGIONAL_MULTIPLIER_BUENOS_AIRES=1.0

# Centro
REGIONAL_MULTIPLIER_CORDOBA=0.95
REGIONAL_MULTIPLIER_SANTA_FE=0.92
REGIONAL_MULTIPLIER_MENDOZA=0.88
REGIONAL_MULTIPLIER_TUCUMAN=0.85
REGIONAL_MULTIPLIER_ENTRE_RIOS=0.90

# Noreste
REGIONAL_MULTIPLIER_CHACO=0.83
REGIONAL_MULTIPLIER_CORRIENTES=0.87
REGIONAL_MULTIPLIER_MISIONES=0.89
REGIONAL_MULTIPLIER_FORMOSA=0.82

# Patagonia
REGIONAL_MULTIPLIER_CHUBUT=0.93
REGIONAL_MULTIPLIER_RIO_NEGRO=0.91
REGIONAL_MULTIPLIER_NEUQUEN=0.94
REGIONAL_MULTIPLIER_LA_PAMPA=0.86
REGIONAL_MULTIPLIER_TIERRA_FUEGO=1.15

# Cuyo
REGIONAL_MULTIPLIER_SAN_LUIS=0.84
REGIONAL_MULTIPLIER_LA_RIOJA=0.81
REGIONAL_MULTIPLIER_CATAMARCA=0.83
REGIONAL_MULTIPLIER_SAN_JUAN=0.87

# Noroeste
REGIONAL_MULTIPLIER_SANTIAGO=0.80
REGIONAL_MULTIPLIER_SALTA=0.86
REGIONAL_MULTIPLIER_JUJUY=0.85
```

## 🔧 Variables Opcionales

### Configuración de Desarrollo
```bash
# Solo para desarrollo local
DEV_MODE=false
DEV_RELOAD=true
DEV_HOST=localhost
DEV_PORT=3000
DEV_DEBUG=true
```

### Configuración de Notificaciones
```bash
# Webhooks para notificaciones
WEBHOOK_URL=
SLACK_WEBHOOK=
DISCORD_WEBHOOK=
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
```

### Configuración de Integración
```bash
# APIs externas
GOOGLE_MAPS_API_KEY=
WEATHER_API_KEY=
SOLAR_API_KEY=
OPENWEATHER_API_KEY=
```

### Configuración de Base de Datos
```bash
# Base de datos local (si se usa)
DATABASE_URL=postgresql://user:password@localhost:5432/cotizador_solar
REDIS_URL=redis://localhost:6379
```

### Configuración de SSL/TLS
```bash
# Certificados SSL
SSL_CERT_PATH=/etc/ssl/certs/cert.pem
SSL_KEY_PATH=/etc/ssl/private/key.pem
SSL_CA_PATH=/etc/ssl/certs/ca.pem
```

### Configuración de Proxy
```bash
# Proxy reverso
PROXY_HOST=localhost
PROXY_PORT=80
PROXY_SSL_ENABLED=false
```

### Configuración de Cache
```bash
# Cache Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_DB=0
```

### Configuración de Logs
```bash
# Logs específicos
LOG_FORMAT=json
LOG_FILE_MAX_SIZE=10MB
LOG_FILE_MAX_FILES=5
LOG_ROTATION=daily
```

### Configuración de Métricas
```bash
# Métricas y monitoreo
METRICS_ENABLED=true
METRICS_PORT=9090
PROMETHEUS_ENABLED=false
GRAFANA_ENABLED=false
```

### Configuración de Alertas
```bash
# Alertas
ALERT_EMAIL=admin@sumpetrol.com.ar
ALERT_SLACK_CHANNEL=#alerts
ALERT_THRESHOLD_ERRORS=10
ALERT_THRESHOLD_RESPONSE_TIME=5000
```

## 📋 Configuración por Categorías

### Variables Críticas (Requeridas)
- `APP_NAME`
- `APP_VERSION`
- `SMTP_SERVER`
- `SMTP_USERNAME`
- `SMTP_PASSWORD`
- `NOCODB_URL`
- `NOCODB_TOKEN`
- `PYTHON_HOST`
- `PYTHON_PORT`
- `NGINX_PORT`

### Variables Importantes (Recomendadas)
- `CONTACT_EMAIL`
- `NOCODB_BASE_ID`
- `NOCODB_TABLE_ID`
- `BCRA_API_URL`
- `INDEC_API_URL`
- `CACHE_DURATION_HOURS`
- `PRICE_UPDATE_INTERVAL_HOURS`
- `LOG_LEVEL`
- `HEALTH_CHECK_INTERVAL`

### Variables Opcionales (Mejoras)
- `GOOGLE_MAPS_API_KEY`
- `WEATHER_API_KEY`
- `WEBHOOK_URL`
- `SLACK_WEBHOOK`
- `METRICS_ENABLED`
- `ALERT_EMAIL`

## 🔒 Seguridad de Variables

### Variables Sensibles
- `SMTP_PASSWORD`
- `NOCODB_TOKEN`
- `NC_AUTH_JWT_SECRET`
- `NC_DATABASE_URL`
- `NC_REDIS_URL`

### Recomendaciones de Seguridad
1. **Nunca** commitear variables sensibles al repositorio
2. Usar variables de entorno en lugar de archivos de configuración
3. Rotar credenciales regularmente
4. Usar secretos de Easypanel para variables sensibles
5. Monitorear acceso a variables sensibles

## 📊 Validación de Variables

### Script de Validación
```bash
#!/bin/bash
# Validar variables de entorno requeridas

required_vars=(
    "APP_NAME"
    "APP_VERSION"
    "SMTP_SERVER"
    "SMTP_USERNAME"
    "SMTP_PASSWORD"
    "NOCODB_URL"
    "NOCODB_TOKEN"
    "PYTHON_HOST"
    "PYTHON_PORT"
    "NGINX_PORT"
)

missing_vars=()

for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        missing_vars+=("$var")
    fi
done

if [ ${#missing_vars[@]} -eq 0 ]; then
    echo "✅ Todas las variables requeridas están configuradas"
    exit 0
else
    echo "❌ Variables faltantes: ${missing_vars[*]}"
    exit 1
fi
```

### Verificación de Tipos
```bash
# Verificar que los puertos sean números
if ! [[ "$PYTHON_PORT" =~ ^[0-9]+$ ]]; then
    echo "❌ PYTHON_PORT debe ser un número"
    exit 1
fi

if ! [[ "$NODE_PORT" =~ ^[0-9]+$ ]]; then
    echo "❌ NODE_PORT debe ser un número"
    exit 1
fi

if ! [[ "$NGINX_PORT" =~ ^[0-9]+$ ]]; then
    echo "❌ NGINX_PORT debe ser un número"
    exit 1
fi
```

## 🚀 Configuración en Easypanel

### Pasos para Configurar Variables
1. **Ir a la sección de Variables de Entorno**
2. **Agregar cada variable con su valor**
3. **Marcar como sensibles las variables que contengan credenciales**
4. **Verificar que todas las variables estén configuradas**
5. **Probar la aplicación**

### Orden de Configuración
1. **Variables básicas** (APP_NAME, APP_VERSION, etc.)
2. **Variables de servicios** (PYTHON_HOST, PYTHON_PORT, etc.)
3. **Variables de SMTP** (SMTP_SERVER, SMTP_USERNAME, etc.)
4. **Variables de NocoDB** (NOCODB_URL, NOCODB_TOKEN, etc.)
5. **Variables de APIs** (BCRA_API_URL, INDEC_API_URL, etc.)
6. **Variables de configuración** (CACHE_DURATION_HOURS, etc.)

### Verificación Post-Configuración
```bash
# Verificar que las variables estén disponibles
echo "APP_NAME: $APP_NAME"
echo "SMTP_SERVER: $SMTP_SERVER"
echo "NOCODB_URL: $NOCODB_URL"
echo "PYTHON_PORT: $PYTHON_PORT"
```

## 📋 Checklist de Variables

### Antes del Deploy
- [ ] Configurar variables básicas
- [ ] Configurar variables de servicios
- [ ] Configurar variables de SMTP
- [ ] Configurar variables de NocoDB
- [ ] Configurar variables de APIs
- [ ] Configurar variables de configuración
- [ ] Verificar variables sensibles
- [ ] Probar configuración

### Después del Deploy
- [ ] Verificar que las variables estén disponibles
- [ ] Probar funcionalidad de SMTP
- [ ] Probar conexión a NocoDB
- [ ] Probar APIs de Argentina
- [ ] Verificar logs
- [ ] Probar health checks

### Monitoreo Continuo
- [ ] Monitorear variables sensibles
- [ ] Verificar rotación de credenciales
- [ ] Monitorear acceso a variables
- [ ] Verificar configuración de seguridad
- [ ] Probar funcionalidad completa

---

**Configuración de variables de entorno optimizada para Easypanel por IdeasDevOps**
