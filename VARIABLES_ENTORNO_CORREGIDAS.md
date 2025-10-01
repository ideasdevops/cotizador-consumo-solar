# Variables de Entorno Corregidas para Easypanel

## 🔧 Variables NocoDB Correctas

Configura estas variables en Easypanel → Proyecto "sitios" → "cotizador-solar" → Environment Variables:

```bash
# Variables principales de NocoDB (CORRECTAS)
NC_DB_URL=https://own-devops-nocodb.2lzju7.easypanel.host
NC_TOKEN=_H3KGTFKGtgMb3pQU5GXR2i17glb1ytl3hxYvVkT
NC_DB_ID=pjo0a1kfnvm1ai3

# Variables legacy para compatibilidad
NOCODB_URL=https://own-devops-nocodb.2lzju7.easypanel.host
NOCODB_TOKEN=_H3KGTFKGtgMb3pQU5GXR2i17glb1ytl3hxYvVkT
NOCODB_BASE_ID=pjo0a1kfnvm1ai3
NOCODB_TABLE_ID=m6snjo5tgkirewb

# Tablas específicas
NOCODB_CONTACTOS_TABLE_ID=m6snjo5tgkirewb
NOCODB_COTIZACIONES_TABLE_ID=m6rk1j231s70p8m
NOCODB_MATERIALES_TABLE_ID=m2p9ng5e1hn53k0
NOCODB_LOGS_TABLE_ID=m1xm2vu3e5bcuiy
```

## 📧 Variables SMTP (mantener existentes)

```bash
SMTP_SERVER=c2630942.ferozo.com
SMTP_PORT=465
SMTP_USERNAME=novedades@sumpetrol.com.ar
SMTP_PASSWORD=Novedad3s2k24@@
SMTP_USE_TLS=true
SMTP_USE_SSL=true
CONTACT_EMAIL=marketing@sumpetrol.com.ar
```

## 🚀 Pasos para Aplicar

1. **Ve a Easypanel** → Proyecto "sitios" → "cotizador-solar"
2. **Ve a "Environment Variables"**
3. **Actualiza las variables** con los valores de arriba
4. **Haz "Deploy"** para aplicar los cambios

## ✅ Verificación

Después del deploy, verifica que el contenedor esté funcionando:

```bash
# Verificar estado del contenedor
docker ps | grep cotizador-solar

# Verificar logs
docker logs <container_id>
```

## 🔍 Problema Resuelto

- ❌ **Antes:** Variables incorrectas causaban reinicio constante
- ✅ **Ahora:** Variables correctas permiten conexión a NocoDB
