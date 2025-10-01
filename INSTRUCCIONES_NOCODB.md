# Instrucciones para Configurar NocoDB - Cotizador Solar

## 📋 Archivos CSV Creados

### 1. **contactos.csv**
- **Propósito**: Almacenar formularios de contacto de usuarios
- **Columnas**: nombre_cliente, email_cliente, telefono_cliente, mensaje_consulta, fecha_consulta, estado_consulta, origen_consulta, notas_internas, fecha_respuesta, usuario_respuesta
- **Datos de ejemplo**: Incluye 5 contactos de ejemplo

### 2. **cotizaciones_solares.csv**
- **Propósito**: Almacenar cotizaciones generadas por el sistema
- **Columnas**: nombre_cliente, email_cliente, ubicacion_proyecto, consumo_mensual_kwh, tipo_tarifa, area_disponible_m2, tipo_instalacion, potencia_requerida_kwp, cantidad_paneles, generacion_mensual_kwh, ahorro_mensual_ars, inversion_total_ars, retorno_inversion_anos, estado_cotizacion, fecha_creacion, valida_hasta, notas_proyecto
- **Datos de ejemplo**: Incluye 5 cotizaciones de ejemplo

### 3. **materiales_solares.csv**
- **Propósito**: Catálogo de materiales y precios
- **Columnas**: tipo_material, marca, modelo, potencia_watts, potencia_kw, precio_ars, precio_por_kw, stock_disponible, activo, especificaciones_tecnicas, garantia_anos, proveedor, fecha_actualizacion
- **Datos de ejemplo**: Incluye paneles, inversores, baterías, montajes, cables y protecciones

### 4. **logs_sistema.csv**
- **Propósito**: Logs de la aplicación
- **Columnas**: tipo_evento, mensaje, nivel_log, usuario, ip_cliente, fecha_hora, datos_adicionales
- **Datos de ejemplo**: Incluye diferentes tipos de eventos

## 🚀 Pasos para Configurar en NocoDB

### Paso 1: Importar Archivos CSV
1. Ve a tu instancia de NocoDB
2. Selecciona la base de datos `pjo0a1kfnvm1ai3`
3. Para cada archivo CSV:
   - Haz clic en "Import from CSV"
   - Selecciona el archivo correspondiente
   - NocoDB detectará automáticamente los tipos de datos
   - Confirma la importación

### Paso 2: Obtener TABLE_IDs
Después de importar cada tabla, obtén el TABLE_ID:
1. Ve a cada tabla creada
2. En la URL verás algo como: `/table/[TABLE_ID]`
3. Copia el TABLE_ID

### Paso 3: Actualizar Variables de Entorno
Reemplaza los valores `*_table_id` con los TABLE_ID reales:

```bash
# Ejemplo con TABLE_IDs reales
NOCODB_CONTACTOS_TABLE_ID=m7i75nx5rkwockg  # Ya existe
NOCODB_COTIZACIONES_TABLE_ID=nuevo_table_id_1
NOCODB_MATERIALES_TABLE_ID=nuevo_table_id_2
NOCODB_LOGS_TABLE_ID=nuevo_table_id_3
```

### Paso 4: Configurar en Easypanel
1. Ve a la configuración del proyecto en Easypanel
2. Agrega todas las variables de entorno del archivo `nocodb-env-variables.md`
3. Actualiza los TABLE_IDs con los valores reales
4. Guarda la configuración

### Paso 5: Reiniciar Aplicación
1. Reinicia el contenedor en Easypanel
2. Verifica que la aplicación funcione correctamente
3. Prueba enviando un formulario de contacto

## 🔧 Variables de Entorno Necesarias

### Básicas (ya configuradas)
```bash
NOCODB_URL=https://bots-nocodb.prskfv.easypanel.host
NOCODB_TOKEN=JvshcwW9JUK_sR4yT7H5r7ygSA2BPFAGNI8nSeWF
NOCODB_BASE_ID=pjo0a1kfnvm1ai3
```

### TABLE_IDs (actualizar con valores reales)
```bash
NOCODB_CONTACTOS_TABLE_ID=m7i75nx5rkwockg
NOCODB_COTIZACIONES_TABLE_ID=[ID_REAL_COTIZACIONES]
NOCODB_MATERIALES_TABLE_ID=[ID_REAL_MATERIALES]
NOCODB_LOGS_TABLE_ID=[ID_REAL_LOGS]
```

## ✅ Verificación

Para verificar que todo funciona:
1. Envía un formulario de contacto desde la web
2. Verifica que aparezca en la tabla `contactos` en NocoDB
3. Genera una cotización desde el cotizador
4. Verifica que aparezca en la tabla `cotizaciones_solares` en NocoDB

## 🆘 Solución de Problemas

### Error: "Table not found"
- Verifica que el TABLE_ID sea correcto
- Asegúrate de que la tabla existe en NocoDB

### Error: "Column not found"
- Verifica que los nombres de columnas coincidan exactamente
- Revisa que no haya espacios extra en los nombres

### Error: "Authentication failed"
- Verifica que el token sea correcto
- Asegúrate de que el token tenga permisos de escritura
