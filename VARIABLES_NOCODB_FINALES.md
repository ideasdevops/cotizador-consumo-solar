# Variables de Entorno NocoDB - Configuración Final

## 🔧 Variables Principales

```bash
# Configuración básica de NocoDB
NOCODB_URL=https://own-devops-nocodb.2lzju7.easypanel.host
NOCODB_TOKEN=JvshcwW9JUK_sR4yT7H5r7ygSA2BPFAGNI8nSeWF
NOCODB_BASE_ID=pjo0a1kfnvm1ai3
```

## 📋 TABLE_IDs Reales (desde Swagger)

```bash
# Tabla de Contactos
NOCODB_CONTACTOS_TABLE_ID=m6snjo5tgkirewb

# Tabla de Cotizaciones Solares
NOCODB_COTIZACIONES_TABLE_ID=m6rk1j231s70p8m

# Tabla de Materiales Solares
NOCODB_MATERIALES_TABLE_ID=m2p9ng5e1hn53k0

# Tabla de Logs del Sistema
NOCODB_LOGS_TABLE_ID=m1xm2vu3e5bcuiy
```

## 🚀 Configuración Completa para Easypanel

Copia y pega estas variables en la configuración de Easypanel:

```bash
# NocoDB Configuration
NOCODB_URL=https://own-devops-nocodb.2lzju7.easypanel.host
NOCODB_TOKEN=JvshcwW9JUK_sR4yT7H5r7ygSA2BPFAGNI8nSeWF
NOCODB_BASE_ID=pjo0a1kfnvm1ai3

# Table IDs
NOCODB_CONTACTOS_TABLE_ID=m6snjo5tgkirewb
NOCODB_COTIZACIONES_TABLE_ID=m6rk1j231s70p8m
NOCODB_MATERIALES_TABLE_ID=m2p9ng5e1hn53k0
NOCODB_LOGS_TABLE_ID=m1xm2vu3e5bcuiy

# Column Names - Contactos
NOCODB_CONTACTOS_ID_COLUMN=id
NOCODB_CONTACTOS_NOMBRE_COLUMN=nombre_cliente
NOCODB_CONTACTOS_EMAIL_COLUMN=email_cliente
NOCODB_CONTACTOS_TELEFONO_COLUMN=telefono_cliente
NOCODB_CONTACTOS_MENSAJE_COLUMN=mensaje_consulta
NOCODB_CONTACTOS_FECHA_COLUMN=fecha_consulta
NOCODB_CONTACTOS_ESTADO_COLUMN=estado_consulta
NOCODB_CONTACTOS_ORIGEN_COLUMN=origen_consulta
NOCODB_CONTACTOS_NOTAS_COLUMN=notas_internas
NOCODB_CONTACTOS_FECHA_RESPUESTA_COLUMN=fecha_respuesta
NOCODB_CONTACTOS_USUARIO_RESPUESTA_COLUMN=usuario_respuesta

# Column Names - Cotizaciones Solares
NOCODB_COTIZACIONES_ID_COLUMN=id
NOCODB_COTIZACIONES_CLIENTE_ID_COLUMN=cliente_id
NOCODB_COTIZACIONES_NOMBRE_COLUMN=nombre_cliente
NOCODB_COTIZACIONES_EMAIL_COLUMN=email_cliente
NOCODB_COTIZACIONES_UBICACION_COLUMN=ubicacion_proyecto
NOCODB_COTIZACIONES_CONSUMO_COLUMN=consumo_mensual_kwh
NOCODB_COTIZACIONES_TARIFA_COLUMN=tipo_tarifa
NOCODB_COTIZACIONES_AREA_COLUMN=area_disponible_m2
NOCODB_COTIZACIONES_INSTALACION_COLUMN=tipo_instalacion
NOCODB_COTIZACIONES_POTENCIA_COLUMN=potencia_requerida_kwp
NOCODB_COTIZACIONES_PANELES_COLUMN=cantidad_paneles
NOCODB_COTIZACIONES_GENERACION_COLUMN=generacion_mensual_kwh
NOCODB_COTIZACIONES_AHORRO_COLUMN=ahorro_mensual_ars
NOCODB_COTIZACIONES_INVERSION_COLUMN=inversion_total_ars
NOCODB_COTIZACIONES_RETORNO_COLUMN=retorno_inversion_anos
NOCODB_COTIZACIONES_ESTADO_COLUMN=estado_cotizacion
NOCODB_COTIZACIONES_FECHA_CREACION_COLUMN=fecha_creacion
NOCODB_COTIZACIONES_VALIDA_HASTA_COLUMN=valida_hasta
NOCODB_COTIZACIONES_NOTAS_COLUMN=notas_proyecto
NOCODB_COTIZACIONES_PDF_COLUMN=archivo_pdf

# Column Names - Materiales Solares
NOCODB_MATERIALES_ID_COLUMN=id
NOCODB_MATERIALES_TIPO_COLUMN=tipo_material
NOCODB_MATERIALES_MARCA_COLUMN=marca
NOCODB_MATERIALES_MODELO_COLUMN=modelo
NOCODB_MATERIALES_POTENCIA_WATTS_COLUMN=potencia_watts
NOCODB_MATERIALES_POTENCIA_KW_COLUMN=potencia_kw
NOCODB_MATERIALES_PRECIO_ARS_COLUMN=precio_ars
NOCODB_MATERIALES_PRECIO_POR_KW_COLUMN=precio_por_kw
NOCODB_MATERIALES_STOCK_COLUMN=stock_disponible
NOCODB_MATERIALES_ACTIVO_COLUMN=activo
NOCODB_MATERIALES_ESPECIFICACIONES_COLUMN=especificaciones_tecnicas
NOCODB_MATERIALES_GARANTIA_COLUMN=garantia_anos
NOCODB_MATERIALES_PROVEEDOR_COLUMN=proveedor
NOCODB_MATERIALES_FECHA_ACTUALIZACION_COLUMN=fecha_actualizacion

# Column Names - Logs del Sistema
NOCODB_LOGS_ID_COLUMN=id
NOCODB_LOGS_TIPO_EVENTO_COLUMN=tipo_evento
NOCODB_LOGS_MENSAJE_COLUMN=mensaje
NOCODB_LOGS_NIVEL_COLUMN=nivel_log
NOCODB_LOGS_USUARIO_COLUMN=usuario
NOCODB_LOGS_IP_COLUMN=ip_cliente
NOCODB_LOGS_FECHA_COLUMN=fecha_hora
NOCODB_LOGS_DATOS_COLUMN=datos_adicionales
```

## 📊 Endpoints de API Disponibles

### Contactos
- **GET** `/api/v2/tables/m6snjo5tgkirewb/records` - Listar contactos
- **POST** `/api/v2/tables/m6snjo5tgkirewb/records` - Crear contacto
- **PATCH** `/api/v2/tables/m6snjo5tgkirewb/records` - Actualizar contacto
- **DELETE** `/api/v2/tables/m6snjo5tgkirewb/records` - Eliminar contacto

### Cotizaciones Solares
- **GET** `/api/v2/tables/m6rk1j231s70p8m/records` - Listar cotizaciones
- **POST** `/api/v2/tables/m6rk1j231s70p8m/records` - Crear cotización
- **PATCH** `/api/v2/tables/m6rk1j231s70p8m/records` - Actualizar cotización
- **DELETE** `/api/v2/tables/m6rk1j231s70p8m/records` - Eliminar cotización

### Materiales Solares
- **GET** `/api/v2/tables/m2p9ng5e1hn53k0/records` - Listar materiales
- **POST** `/api/v2/tables/m2p9ng5e1hn53k0/records` - Crear material
- **PATCH** `/api/v2/tables/m2p9ng5e1hn53k0/records` - Actualizar material
- **DELETE** `/api/v2/tables/m2p9ng5e1hn53k0/records` - Eliminar material

### Logs del Sistema
- **GET** `/api/v2/tables/m1xm2vu3e5bcuiy/records` - Listar logs
- **POST** `/api/v2/tables/m1xm2vu3e5bcuiy/records` - Crear log
- **PATCH** `/api/v2/tables/m1xm2vu3e5bcuiy/records` - Actualizar log
- **DELETE** `/api/v2/tables/m1xm2vu3e5bcuiy/records` - Eliminar log

## ✅ Pasos Finales

1. **Configurar en Easypanel**: Agrega todas las variables de arriba
2. **Reiniciar aplicación**: Para que tome las nuevas configuraciones
3. **Probar funcionalidad**: 
   - Enviar formulario de contacto
   - Generar cotización solar
   - Verificar que los datos aparezcan en NocoDB

## 🔍 Verificación

Para verificar que todo funciona:
1. Ve a `https://own-devops-nocodb.2lzju7.easypanel.host`
2. Revisa las tablas creadas
3. Verifica que los datos se estén guardando correctamente
