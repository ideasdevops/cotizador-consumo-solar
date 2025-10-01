# 🚀 Guía de Despliegue - Cotizador de Consumo Solar

## 📋 Información General

- **Aplicación**: Cotizador de Consumo Solar - Sumpetrol SA
- **Versión**: 1.0.0
- **Sistema de Deploy**: Easypanel
- **Arquitectura**: Frontend + Backend Python + Backend Node.js

## 🏗️ Arquitectura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Frontend    │    │  Backend Python │    │  Backend Node   │
│   (Nginx:80)    │◄──►│   (FastAPI:8000)│    │   (Express:8005)│
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Supervisor    │
                    │   (Processes)   │
                    └─────────────────┘
```

## 🔧 Configuración en Easypanel

### 1. Crear Aplicación

- **Tipo**: SSH Git
- **Repositorio**: `git@github.com:ideasdevops/cotizador-consumo-solar.git`
- **Dockerfile**: `Dockerfile.easypanel-optimized`
- **Puerto**: 80

### 2. Configurar Volúmenes

| Tipo | Nombre | Ruta de Montaje | Descripción |
|------|--------|-----------------|-------------|
| VOLUME | data | /data | Datos persistentes |
| VOLUME | logs | /data/logs | Logs de la aplicación |
| VOLUME | cache | /data/cache | Cache de APIs |
| VOLUME | backups | /data/backups | Backups automáticos |
| VOLUME | temp | /data/temp | Archivos temporales |

### 3. Variables de Entorno

#### Configuración Básica
```bash
APP_NAME=cotizador-solar
APP_VERSION=1.0.0
APP_ENV=production
DEBUG=false
LOG_LEVEL=INFO
```

#### Configuración SMTP
```bash
SMTP_SERVER=c2630942.ferozo.com
SMTP_PORT=465
SMTP_USERNAME=novedades@sumpetrol.com.ar
SMTP_PASSWORD=Novedad3s2k24@@
SMTP_USE_TLS=true
SMTP_USE_SSL=true
CONTACT_EMAIL=marketing@sumpetrol.com.ar
```

#### Configuración NocoDB
```bash
NOCODB_URL=https://bots-nocodb.prskfv.easypanel.host
NOCODB_TOKEN=JvshcwW9JUK_sR4yT7H5r7ygSA2BPFAGNI8nSeWF
NOCODB_BASE_ID=pjo0a1kfnvm1ai3
NOCODB_TABLE_ID=m7i75nx5rkwockg
```

#### Configuración de APIs
```bash
BCRA_API_URL=https://api.estadisticas.bcra.gob.ar/api/Estadistica/GetSeries
INDEC_API_URL=https://www.indec.gob.ar/indec/web/Institucional-Indec-Precios
DOLAR_BLUE_API_URL=https://api-dolar-argentina.herokuapp.com/api/dolares
```

#### Configuración de Servicios
```bash
PYTHON_HOST=0.0.0.0
PYTHON_PORT=8000
PYTHON_WORKERS=2
NODE_HOST=0.0.0.0
NODE_PORT=8005
NGINX_PORT=80
```

#### Configuración de Cache
```bash
CACHE_DURATION_HOURS=12
PRICE_UPDATE_INTERVAL_HOURS=12
EXCHANGE_UPDATE_INTERVAL_HOURS=6
```

## 🌐 Endpoints Disponibles

### Frontend
- **`/`** - Aplicación principal
- **`/health`** - Health check

### API Python (FastAPI)
- **`/api/`** - API principal
- **`/api/cotizar`** - Crear cotización
- **`/api/cotizar/enviar-email`** - Enviar cotización por email
- **`/api/cotizar/descargar-pdf`** - Descargar PDF
- **`/api/contacto/enviar`** - Formulario de contacto
- **`/api/materiales/precios`** - Precios de materiales
- **`/api/argentina/precios`** - Precios desde APIs de Argentina
- **`/api/argentina/tipo-cambio`** - Tipo de cambio actual
- **`/docs`** - Documentación Swagger
- **`/redoc`** - Documentación ReDoc

### API Node.js
- **`/node-api/`** - Servicios adicionales

## 🔍 Monitoreo y Logs

### Logs Disponibles
- **Nginx**: `/data/logs/nginx/`
- **Python**: `/data/logs/python/`
- **Node.js**: `/data/logs/node/`
- **Supervisor**: `/data/logs/supervisor/`

### Health Checks
- **Intervalo**: 30 segundos
- **Timeout**: 10 segundos
- **Retries**: 3
- **Endpoint**: `/health`

## 📊 Características

### ✅ Funcionalidades Implementadas
- [x] Cotización de sistemas solares
- [x] Cálculo de consumo energético
- [x] Integración con APIs de Argentina (INDEC, BCRA)
- [x] Generación de PDFs
- [x] Envío de emails SMTP
- [x] Base de datos NocoDB
- [x] Actualización automática de precios
- [x] Multiplicadores regionales
- [x] Cache inteligente
- [x] Logs centralizados
- [x] Health checks
- [x] Supervisor para gestión de procesos

### 🔄 Servicios Automáticos
- **Actualización de precios**: Cada 12 horas
- **Actualización de tipo de cambio**: Cada 6 horas
- **Backup automático**: Cada 24 horas
- **Health checks**: Cada 30 segundos

## 🛠️ Comandos de Diagnóstico

### Verificar Estado
```bash
# Verificar logs
docker logs <container_id>

# Verificar health check
curl http://localhost/health

# Verificar API Python
curl http://localhost:8000/health

# Verificar API Node.js
curl http://localhost:8005/health
```

### Verificar Servicios
```bash
# Verificar supervisor
docker exec <container_id> supervisorctl status

# Verificar nginx
docker exec <container_id> nginx -t

# Verificar procesos
docker exec <container_id> ps aux
```

## 🔧 Troubleshooting

### Problemas Comunes

#### 1. Contenedor no Inicia
- Verificar volúmenes en Easypanel
- Verificar variables de entorno
- Revisar logs del contenedor

#### 2. API no Responde
- Verificar que Python backend esté corriendo
- Verificar configuración de nginx
- Revisar logs de Python

#### 3. Emails no se Envían
- Verificar configuración SMTP
- Verificar credenciales
- Revisar logs de email

#### 4. NocoDB no Conecta
- Verificar URL y token
- Verificar conectividad de red
- Revisar logs de NocoDB

### Comandos de Recuperación

```bash
# Reiniciar servicios
docker exec <container_id> supervisorctl restart all

# Reiniciar nginx
docker exec <container_id> supervisorctl restart nginx

# Reiniciar Python backend
docker exec <container_id> supervisorctl restart python-backend

# Reiniciar Node.js backend
docker exec <container_id> supervisorctl restart node-backend
```

## 📈 Métricas y Monitoreo

### Métricas Clave
- Número de cotizaciones generadas
- Tiempo de respuesta de la API
- Uso de memoria y CPU
- Errores por minuto
- Disponibilidad del servicio

### Alertas Recomendadas
- Disponibilidad < 99%
- Tiempo de respuesta > 5 segundos
- Errores > 10 por minuto
- Uso de memoria > 80%
- Uso de CPU > 80%

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

## 📞 Soporte

### Contacto Técnico
- **Email**: marketing@sumpetrol.com.ar
- **Sitio Web**: https://sumpetrol.com.ar

### Reportar Issues
1. Verificar que el issue no esté ya reportado
2. Usar el template de issue
3. Incluir pasos para reproducir
4. Adjuntar logs y screenshots si es necesario

## 📄 Licencia

Este proyecto es propiedad de **Sumpetrol SA** y está destinado para uso interno y comercial de la empresa.

---

**Desarrollado con ❤️ para Sumpetrol SA**

*Sistema de deploy optimizado por IdeasDevOps*