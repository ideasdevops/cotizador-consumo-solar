# Variables de Entorno para NocoDB - Cotizador Solar

## Variables Principales de NocoDB

```bash
# Configuración básica de NocoDB
NOCODB_URL=https://bots-nocodb.prskfv.easypanel.host
NOCODB_TOKEN=JvshcwW9JUK_sR4yT7H5r7ygSA2BPFAGNI8nSeWF
NOCODB_BASE_ID=pjo0a1kfnvm1ai3
```

## Variables de Tablas

```bash
# Tabla de Contactos (ya existe)
NOCODB_CONTACTOS_TABLE_ID=m7i75nx5rkwockg

# Tabla de Cotizaciones Solares (crear nueva)
NOCODB_COTIZACIONES_TABLE_ID=cotizaciones_solares_table_id

# Tabla de Materiales Solares (crear nueva)
NOCODB_MATERIALES_TABLE_ID=materiales_solares_table_id

# Tabla de Logs del Sistema (crear nueva)
NOCODB_LOGS_TABLE_ID=logs_sistema_table_id
```

## Variables de Columnas - Contactos

```bash
# Columnas de la tabla contactos
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
```

## Variables de Columnas - Cotizaciones Solares

```bash
# Columnas de la tabla cotizaciones_solares
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
```

## Variables de Columnas - Materiales Solares

```bash
# Columnas de la tabla materiales_solares
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
```

## Variables de Columnas - Logs del Sistema

```bash
# Columnas de la tabla logs_sistema
NOCODB_LOGS_ID_COLUMN=id
NOCODB_LOGS_TIPO_EVENTO_COLUMN=tipo_evento
NOCODB_LOGS_MENSAJE_COLUMN=mensaje
NOCODB_LOGS_NIVEL_COLUMN=nivel_log
NOCODB_LOGS_USUARIO_COLUMN=usuario
NOCODB_LOGS_IP_COLUMN=ip_cliente
NOCODB_LOGS_FECHA_COLUMN=fecha_hora
NOCODB_LOGS_DATOS_COLUMN=datos_adicionales
```

## Instrucciones de Configuración

1. **Importar el CSV**: Usa el archivo `nocodb-structure.csv` para crear las tablas en NocoDB
2. **Obtener TABLE_IDs**: Después de crear las tablas, obtén los TABLE_ID reales
3. **Actualizar variables**: Reemplaza los valores `*_table_id` con los IDs reales
4. **Configurar en Easypanel**: Agrega todas estas variables en la configuración del proyecto
5. **Reiniciar aplicación**: Reinicia el contenedor para que tome las nuevas variables

## Notas Importantes

- La tabla `contactos` ya existe con TABLE_ID: `m7i75nx5rkwockg`
- Las otras tablas necesitan ser creadas usando el CSV
- Los nombres de columnas deben coincidir exactamente con los del CSV
- Los tipos de datos deben ser los especificados en el CSV
