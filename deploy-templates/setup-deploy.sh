#!/bin/bash

# ===============================================
# SCRIPT DE CONFIGURACIÓN AUTOMÁTICA PARA EASYPANEL
# ===============================================
# Sistema de Deploy Automático - IdeasDevOps
# Configura automáticamente el deploy para cualquier aplicación
# ===============================================

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir mensajes
print_message() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Función para mostrar ayuda
show_help() {
    echo "==============================================="
    echo "SISTEMA DE DEPLOY AUTOMÁTICO - IDEASDEVOPS"
    echo "==============================================="
    echo ""
    echo "USO:"
    echo "  ./setup-deploy.sh [OPCIONES]"
    echo ""
    echo "OPCIONES:"
    echo "  -n, --name NAME        Nombre de la aplicación"
    echo "  -v, --version VERSION  Versión de la aplicación"
    echo "  -d, --description DESC Descripción de la aplicación"
    echo "  -p, --python REQS      Dependencias Python (separadas por espacios)"
    echo "  -f, --frontend PATH    Ruta del frontend (opcional)"
    echo "  -s, --scripts PATH     Ruta de scripts (opcional)"
    echo "  -c, --config PATH      Ruta de configuración (opcional)"
    echo "  -h, --help             Mostrar esta ayuda"
    echo ""
    echo "EJEMPLO:"
    echo "  ./setup-deploy.sh -n mi-app -v 1.0.0 -p 'requests pandas flask'"
    echo ""
}

# Variables por defecto
APP_NAME=""
APP_VERSION="1.0.0"
APP_DESCRIPTION="Aplicación desarrollada con IdeasDevOps Deploy System"
PYTHON_REQUIREMENTS=""
FRONTEND_PATH=""
SCRIPTS_PATH=""
CONFIG_PATH=""

# Procesar argumentos
while [[ $# -gt 0 ]]; do
    case $1 in
        -n|--name)
            APP_NAME="$2"
            shift 2
            ;;
        -v|--version)
            APP_VERSION="$2"
            shift 2
            ;;
        -d|--description)
            APP_DESCRIPTION="$2"
            shift 2
            ;;
        -p|--python)
            PYTHON_REQUIREMENTS="$2"
            shift 2
            ;;
        -f|--frontend)
            FRONTEND_PATH="$2"
            shift 2
            ;;
        -s|--scripts)
            SCRIPTS_PATH="$2"
            shift 2
            ;;
        -c|--config)
            CONFIG_PATH="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            print_error "Opción desconocida: $1"
            show_help
            exit 1
            ;;
    esac
done

# Validar argumentos requeridos
if [ -z "$APP_NAME" ]; then
    print_error "El nombre de la aplicación es requerido (-n o --name)"
    show_help
    exit 1
fi

print_message "Iniciando configuración de deploy para: $APP_NAME"

# ===============================================
# PASO 1: CREAR ESTRUCTURA DE DIRECTORIOS
# ===============================================
print_message "Creando estructura de directorios..."

# Crear directorios necesarios
mkdir -p frontend scripts config

# Crear archivos básicos si no existen
if [ ! -f "config.json" ]; then
    cat > config.json << EOF
{
    "app_name": "$APP_NAME",
    "version": "$APP_VERSION",
    "description": "$APP_DESCRIPTION",
    "deploy_date": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "environment": "production"
}
EOF
    print_success "Archivo config.json creado"
fi

if [ ! -f "env.example" ]; then
    cat > env.example << EOF
# ===============================================
# CONFIGURACIÓN DE VARIABLES DE ENTORNO
# ===============================================
# Aplicación: $APP_NAME
# Versión: $APP_VERSION
# ===============================================

# Configuración de la aplicación
APP_NAME=$APP_NAME
APP_VERSION=$APP_VERSION
APP_ENV=production

# Configuración de logs
LOG_LEVEL=INFO
LOG_FILE=/data/logs/sistema.log

# Configuración de base de datos (si aplica)
# DB_HOST=localhost
# DB_PORT=5432
# DB_NAME=$APP_NAME
# DB_USER=user
# DB_PASSWORD=password

# Configuración de API (si aplica)
# API_URL=https://api.example.com
# API_KEY=your-api-key

# Configuración de backup
BACKUP_ENABLED=true
BACKUP_SCHEDULE=0 2 * * *
BACKUP_RETENTION_DAYS=30
EOF
    print_success "Archivo env.example creado"
fi

# ===============================================
# PASO 2: CONFIGURAR DOCKERFILE
# ===============================================
print_message "Configurando Dockerfile..."

# Copiar template y personalizar
cp deploy-templates/Dockerfile.easypanel-template Dockerfile.easypanel-optimized

# Reemplazar variables en el Dockerfile
sed -i "s/ARG APP_NAME=\"mi-aplicacion\"/ARG APP_NAME=\"$APP_NAME\"/g" Dockerfile.easypanel-optimized
sed -i "s/ARG APP_VERSION=\"1.0.0\"/ARG APP_VERSION=\"$APP_VERSION\"/g" Dockerfile.easypanel-optimized
sed -i "s/ARG APP_DESCRIPTION=\"Aplicación desarrollada con IdeasDevOps Deploy System\"/ARG APP_DESCRIPTION=\"$APP_DESCRIPTION\"/g" Dockerfile.easypanel-optimized
sed -i "s/ARG PYTHON_REQUIREMENTS=\"requests python-dotenv pandas openpyxl schedule psutil\"/ARG PYTHON_REQUIREMENTS=\"$PYTHON_REQUIREMENTS\"/g" Dockerfile.easypanel-optimized

print_success "Dockerfile configurado"

# ===============================================
# PASO 3: CONFIGURAR FRONTEND (SI EXISTE)
# ===============================================
if [ -n "$FRONTEND_PATH" ] && [ -d "$FRONTEND_PATH" ]; then
    print_message "Configurando frontend desde: $FRONTEND_PATH"
    cp -r "$FRONTEND_PATH"/* frontend/
    print_success "Frontend configurado"
elif [ -d "frontend" ] && [ "$(ls -A frontend)" ]; then
    print_success "Frontend ya existe"
else
    print_warning "No se encontró frontend, creando página de inicio básica"
    cat > frontend/index.html << EOF
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>$APP_NAME</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #333; text-align: center; }
        .info { background: #e8f4f8; padding: 20px; border-radius: 4px; margin: 20px 0; }
        .status { color: #28a745; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 $APP_NAME</h1>
        <div class="info">
            <p><strong>Versión:</strong> $APP_VERSION</p>
            <p><strong>Estado:</strong> <span class="status">✅ Funcionando</span></p>
            <p><strong>Descripción:</strong> $APP_DESCRIPTION</p>
            <p><strong>Deploy Date:</strong> $(date -u +%Y-%m-%dT%H:%M:%SZ)</p>
        </div>
        <p>Esta aplicación ha sido desplegada exitosamente usando el <strong>Sistema de Deploy Automático de IdeasDevOps</strong>.</p>
    </div>
</body>
</html>
EOF
    print_success "Página de inicio básica creada"
fi

# ===============================================
# PASO 4: CONFIGURAR SCRIPTS (SI EXISTEN)
# ===============================================
if [ -n "$SCRIPTS_PATH" ] && [ -d "$SCRIPTS_PATH" ]; then
    print_message "Configurando scripts desde: $SCRIPTS_PATH"
    cp -r "$SCRIPTS_PATH"/* scripts/
    print_success "Scripts configurados"
elif [ -d "scripts" ] && [ "$(ls -A scripts)" ]; then
    print_success "Scripts ya existen"
else
    print_warning "No se encontraron scripts, creando script básico"
    cat > scripts/healthcheck.sh << 'EOF'
#!/bin/bash
# Script de healthcheck básico
curl -f http://localhost/health || exit 1
EOF
    chmod +x scripts/healthcheck.sh
    print_success "Script de healthcheck básico creado"
fi

# ===============================================
# PASO 5: CREAR .DOCKERIGNORE
# ===============================================
print_message "Creando .dockerignore..."
cat > .dockerignore << EOF
# Archivos de desarrollo
.git
.gitignore
README.md
.env
.env.local
.env.development
.env.test
.env.production

# Directorios de desarrollo
node_modules
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env
venv
.venv
pip-log.txt
pip-delete-this-directory.txt

# Archivos de IDE
.vscode
.idea
*.swp
*.swo
*~

# Archivos de sistema
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Archivos temporales
tmp/
temp/
.tmp/

# Archivos de deploy
deploy-templates/
setup-deploy.sh
EOF
print_success ".dockerignore creado"

# ===============================================
# PASO 6: CREAR README DE DEPLOY
# ===============================================
print_message "Creando documentación de deploy..."
cat > DEPLOY.md << EOF
# 🚀 Deploy de $APP_NAME

## Información de la Aplicación
- **Nombre:** $APP_NAME
- **Versión:** $APP_VERSION
- **Descripción:** $APP_DESCRIPTION
- **Fecha de Deploy:** $(date -u +%Y-%m-%dT%H:%M:%SZ)

## Configuración en EasyPanel

### 1. Crear Nueva Aplicación
1. Ve a EasyPanel
2. Crea una nueva aplicación
3. Selecciona "SSH Git" como método de deploy
4. Configura el repositorio: \`git@github.com:ideasdevops/cotizador-consumo-solar.git\`

### 2. Configurar Dockerfile
- **Dockerfile:** \`Dockerfile.easypanel-optimized\`

### 3. Configurar Volúmenes
Crear los siguientes volúmenes:

| Tipo | Nombre | Ruta de Montaje |
|------|--------|-----------------|
| VOLUME | data | /data |
| VOLUME | logs | /data/logs |
| VOLUME | backup | /data/backups |
| FILE | supervisor-config | /etc/supervisor/conf.d/supervisord.conf |

### 4. Variables de Entorno
Configurar las variables necesarias según \`env.example\`

### 5. Deploy
1. Hacer commit y push de los cambios
2. Ejecutar deploy en EasyPanel
3. Verificar que la aplicación esté funcionando

## Verificación
- **Health Check:** http://tu-dominio/health
- **Aplicación:** http://tu-dominio/

## Logs
Los logs se encuentran en:
- Nginx: /data/logs/nginx/
- Supervisor: /data/logs/supervisor.log
- Aplicación: /data/logs/sistema.log

## Troubleshooting
Si hay problemas:
1. Verificar logs del contenedor
2. Verificar configuración de volúmenes
3. Verificar variables de entorno
4. Verificar conectividad de red

---
*Generado automáticamente por IdeasDevOps Deploy System*
EOF
print_success "Documentación de deploy creada"

# ===============================================
# PASO 7: MOSTRAR RESUMEN
# ===============================================
print_success "¡Configuración completada exitosamente!"
echo ""
echo "==============================================="
echo "RESUMEN DE CONFIGURACIÓN"
echo "==============================================="
echo "Aplicación: $APP_NAME"
echo "Versión: $APP_VERSION"
echo "Descripción: $APP_DESCRIPTION"
echo "Dependencias Python: $PYTHON_REQUIREMENTS"
echo ""
echo "Archivos creados:"
echo "  ✅ Dockerfile.easypanel-optimized"
echo "  ✅ config.json"
echo "  ✅ env.example"
echo "  ✅ .dockerignore"
echo "  ✅ DEPLOY.md"
echo "  ✅ frontend/index.html"
echo "  ✅ scripts/healthcheck.sh"
echo ""
echo "Próximos pasos:"
echo "  1. Revisar y ajustar la configuración según sea necesario"
echo "  2. Hacer commit y push de los cambios"
echo "  3. Configurar la aplicación en EasyPanel"
echo "  4. Ejecutar el deploy"
echo ""
echo "Para más información, consulta DEPLOY.md"
echo "==============================================="
