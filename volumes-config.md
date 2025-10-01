# 💾 Configuración de Volúmenes - Easypanel

## 📋 Volúmenes Requeridos

### Volúmenes de Datos Persistentes

#### 1. Volumen Principal de Datos
- **Nombre**: `cotizador-solar-data`
- **Tipo**: VOLUME
- **Ruta de Montaje**: `/data`
- **Descripción**: Contenedor principal para todos los datos de la aplicación
- **Uso**: Almacena logs, cache, backups y archivos temporales

#### 2. Volumen de Logs
- **Nombre**: `cotizador-solar-logs`
- **Tipo**: VOLUME
- **Ruta de Montaje**: `/data/logs`
- **Descripción**: Logs centralizados de todos los servicios
- **Estructura**:
  ```
  /data/logs/
  ├── nginx/
  │   ├── access.log
  │   └── error.log
  ├── python/
  │   ├── access.log
  │   └── error.log
  ├── node/
  │   ├── access.log
  │   └── error.log
  └── supervisor/
      └── supervisord.log
  ```

#### 3. Volumen de Cache
- **Nombre**: `cotizador-solar-cache`
- **Tipo**: VOLUME
- **Ruta de Montaje**: `/data/cache`
- **Descripción**: Cache de APIs y precios actualizados
- **Estructura**:
  ```
  /data/cache/
  ├── argentina_apis_cache.json
  ├── prices_cache.json
  ├── exchange_cache.json
  └── last_update.txt
  ```

#### 4. Volumen de Backups
- **Nombre**: `cotizador-solar-backups`
- **Tipo**: VOLUME
- **Ruta de Montaje**: `/data/backups`
- **Descripción**: Backups automáticos de la aplicación
- **Estructura**:
  ```
  /data/backups/
  ├── daily/
  ├── weekly/
  ├── monthly/
  └── config/
  ```

#### 5. Volumen de Archivos Temporales
- **Nombre**: `cotizador-solar-temp`
- **Tipo**: VOLUME
- **Ruta de Montaje**: `/data/temp`
- **Descripción**: Archivos temporales y procesamiento
- **Uso**: PDFs temporales, archivos de procesamiento, etc.

### Volúmenes de Configuración

#### 6. Configuración de Nginx
- **Nombre**: `cotizador-solar-nginx-config`
- **Tipo**: FILE
- **Ruta de Montaje**: `/etc/nginx/conf.d/default.conf`
- **Descripción**: Configuración personalizada de nginx
- **Contenido**: Configuración de proxy y rutas

#### 7. Configuración de Supervisor
- **Nombre**: `cotizador-solar-supervisor-config`
- **Tipo**: FILE
- **Ruta de Montaje**: `/etc/supervisor/conf.d/supervisord.conf`
- **Descripción**: Configuración de gestión de procesos
- **Contenido**: Configuración de servicios Python y Node.js

## 🔧 Configuración en Easypanel

### Crear Volúmenes

1. **Ir a la sección de Volúmenes**
2. **Crear cada volumen con la configuración especificada**
3. **Asignar permisos apropiados**

### Configuración de Permisos

```bash
# Permisos para volúmenes de datos
chmod 755 /data
chmod 755 /data/logs
chmod 755 /data/cache
chmod 755 /data/backups
chmod 755 /data/temp

# Propietario
chown -R nginx:nginx /data
```

### Configuración de Montaje

#### Volúmenes de Datos
```yaml
volumes:
  - cotizador-solar-data:/data
  - cotizador-solar-logs:/data/logs
  - cotizador-solar-cache:/data/cache
  - cotizador-solar-backups:/data/backups
  - cotizador-solar-temp:/data/temp
```

#### Volúmenes de Configuración
```yaml
volumes:
  - cotizador-solar-nginx-config:/etc/nginx/conf.d/default.conf
  - cotizador-solar-supervisor-config:/etc/supervisor/conf.d/supervisord.conf
```

## 📊 Monitoreo de Volúmenes

### Métricas Recomendadas
- **Uso de espacio**: Monitorear uso de cada volumen
- **I/O**: Monitorear operaciones de lectura/escritura
- **Disponibilidad**: Verificar que los volúmenes estén montados

### Alertas Recomendadas
- **Espacio disponible < 20%**
- **I/O alto > 1000 ops/seg**
- **Volumen no montado**

## 🔒 Seguridad de Volúmenes

### Medidas de Seguridad
- **Permisos restrictivos**: Solo lectura/escritura necesaria
- **Backup automático**: Respaldos regulares
- **Encriptación**: Para datos sensibles
- **Acceso controlado**: Solo servicios necesarios

### Configuración de Backup
```bash
# Backup diario
0 2 * * * tar -czf /data/backups/daily/backup-$(date +%Y%m%d).tar.gz /data

# Backup semanal
0 3 * * 0 tar -czf /data/backups/weekly/backup-$(date +%Y%m%d).tar.gz /data

# Backup mensual
0 4 1 * * tar -czf /data/backups/monthly/backup-$(date +%Y%m%d).tar.gz /data
```

## 🚀 Configuración de Deploy

### Script de Inicialización
```bash
#!/bin/bash
# Inicializar volúmenes en el primer deploy

# Crear directorios necesarios
mkdir -p /data/logs/nginx
mkdir -p /data/logs/python
mkdir -p /data/logs/node
mkdir -p /data/logs/supervisor
mkdir -p /data/cache
mkdir -p /data/backups/daily
mkdir -p /data/backups/weekly
mkdir -p /data/backups/monthly
mkdir -p /data/temp

# Configurar permisos
chown -R nginx:nginx /data
chmod -R 755 /data

# Crear archivos de configuración inicial
touch /data/cache/last_update.txt
echo "{}" > /data/cache/argentina_apis_cache.json
echo "{}" > /data/cache/prices_cache.json
echo "{}" > /data/cache/exchange_cache.json
```

### Variables de Entorno Relacionadas
```bash
# Configuración de volúmenes
DATA_DIR=/data
LOG_DIR=/data/logs
CACHE_DIR=/data/cache
BACKUP_DIR=/data/backups
TEMP_DIR=/data/temp

# Configuración de logs
NGINX_LOG_LEVEL=info
PYTHON_LOG_LEVEL=info
NODE_LOG_LEVEL=info

# Configuración de cache
CACHE_DURATION_HOURS=12
PRICE_UPDATE_INTERVAL_HOURS=12
EXCHANGE_UPDATE_INTERVAL_HOURS=6

# Configuración de backup
BACKUP_ENABLED=true
BACKUP_INTERVAL_HOURS=24
BACKUP_RETENTION_DAYS=30
```

## 📋 Checklist de Configuración

### Antes del Deploy
- [ ] Crear todos los volúmenes en Easypanel
- [ ] Configurar permisos apropiados
- [ ] Verificar montaje de volúmenes
- [ ] Configurar variables de entorno
- [ ] Probar acceso a volúmenes

### Después del Deploy
- [ ] Verificar que los volúmenes estén montados
- [ ] Verificar permisos de escritura
- [ ] Probar creación de logs
- [ ] Probar cache de APIs
- [ ] Verificar backup automático

### Monitoreo Continuo
- [ ] Monitorear uso de espacio
- [ ] Verificar logs de errores
- [ ] Probar funcionalidad de backup
- [ ] Verificar performance de I/O
- [ ] Monitorear disponibilidad

## 🔧 Troubleshooting

### Problemas Comunes

#### 1. Volumen no Montado
```bash
# Verificar montaje
docker exec <container_id> df -h
docker exec <container_id> mount | grep /data
```

#### 2. Permisos Incorrectos
```bash
# Verificar permisos
docker exec <container_id> ls -la /data
docker exec <container_id> touch /data/test.txt
```

#### 3. Espacio Insuficiente
```bash
# Verificar espacio
docker exec <container_id> df -h /data
docker exec <container_id> du -sh /data/*
```

#### 4. I/O Alto
```bash
# Verificar I/O
docker exec <container_id> iostat -x 1
docker exec <container_id> iotop
```

### Comandos de Recuperación
```bash
# Reiniciar servicios
docker exec <container_id> supervisorctl restart all

# Limpiar cache
docker exec <container_id> rm -rf /data/cache/*

# Limpiar logs antiguos
docker exec <container_id> find /data/logs -name "*.log" -mtime +7 -delete

# Limpiar archivos temporales
docker exec <container_id> rm -rf /data/temp/*
```

---

**Configuración de volúmenes optimizada para Easypanel por IdeasDevOps**
