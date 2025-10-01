# Variables de Entorno Corregidas para Easypanel

## 🔧 Variables Principales (CORREGIDAS)

```bash
# Configuración básica
NODE_ENV=production
PYTHONUNBUFFERED=1

# APIs externas
INDEC_API_URL=https://www.indec.gob.ar/api/v1
CAMARA_CONSTRUCCION_API_URL=https://api.camaraconstruccion.com.ar
PRECIOS_AR_API_URL=https://api.preciosar.com.ar
JWT_SECRET=tu-super-secret-jwt-key-cambiar-en-produccion

# Rate limiting
RATE_LIMIT_WINDOW_MS=900000
RATE_LIMIT_MAX_REQUESTS=100

# Email SMTP (CORREGIDO)
SMTP_SERVER=c1682311.ferozo.com
SMTP_PORT=465
SMTP_USERNAME=marketing@ideasdevops.com
SMTP_PASSWORD=Market1ng2k24@
SMTP_USE_TLS=false
SMTP_USE_SSL=true
CONTACT_EMAIL=marketing@ideasdevops.com

# NocoDB Configuration (CORREGIDO)
NOCODB_URL=https://own-devops-nocodb.2lzju7.easypanel.host
NOCODB_TOKEN=_H3KGTFKGtgMb3pQU5GXR2i17glb1ytl3hxYvVkT
NOCODB_BASE_ID=pjo0a1kfnvm1ai3
NOCODB_TABLE_ID=m6snjo5tgkirewb

# Table IDs (CORREGIDOS)
NOCODB_CONTACTOS_TABLE_ID=m6snjo5tgkirewb
NOCODB_COTIZACIONES_TABLE_ID=m6rk1j231s70p8m
NOCODB_MATERIALES_TABLE_ID=m2p9ng5e1hn53k0
NOCODB_LOGS_TABLE_ID=m1xm2vu3e5bcuiy
```

## 🚨 Cambios Realizados

### 1. **NOCODB_BASE_ID**
- **Antes**: `Cotizador-Solar` (incorrecto)
- **Después**: `pjo0a1kfnvm1ai3` (ID real de la base de datos)

### 2. **NOCODB_TABLE_ID**
- **Antes**: `m6rk1j231s70p8m` (ID de cotizaciones)
- **Después**: `m6snjo5tgkirewb` (ID de contactos)

### 3. **SMTP Configuration**
- **Servidor**: `c1682311.ferozo.com` (corregido)
- **Usuario**: `marketing@ideasdevops.com` (corregido)
- **Contraseña**: `Market1ng2k24@` (corregida)

## 🔍 Endpoints de Prueba Agregados

### Test NocoDB
```
GET /test/nocodb
```
Verifica la conexión con NocoDB y muestra la configuración.

### Test Email
```
GET /test/email
```
Verifica la configuración del servicio de email.

## 📋 Pasos para Corregir

1. **Actualizar variables en Easypanel** con las variables corregidas de arriba
2. **Reiniciar la aplicación** para que tome las nuevas configuraciones
3. **Probar endpoints**:
   - `GET /test/nocodb` - Verificar conexión NocoDB
   - `GET /test/email` - Verificar configuración email
4. **Probar funcionalidad**:
   - Enviar formulario de contacto
   - Generar cotización solar

## 🐛 Problemas Identificados y Solucionados

1. **Base ID incorrecto**: Causaba errores 404 en NocoDB
2. **Table ID incorrecto**: Usaba tabla de cotizaciones para contactos
3. **Configuración SMTP**: Servidor y credenciales incorrectas
4. **Falta de logging**: Agregado logging detallado para debugging
5. **Endpoints de prueba**: Agregados para verificar configuración

## ✅ Verificación

Después de aplicar estos cambios:

1. Ve a `https://tu-dominio.com/test/nocodb`
2. Verifica que la respuesta muestre `"status": "success"`
3. Ve a `https://tu-dominio.com/test/email`
4. Verifica que la configuración SMTP sea correcta
5. Prueba enviar un formulario de contacto
6. Verifica que aparezca en NocoDB
