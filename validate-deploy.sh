#!/bin/bash

# ===============================================
# SCRIPT DE VALIDACIÓN DE DEPLOY
# ===============================================
# Cotizador de Consumo Solar - Sumpetrol SA
# ===============================================

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir mensajes
print_status() {
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

# Función para verificar archivos
check_file() {
    if [ -f "$1" ]; then
        print_success "Archivo encontrado: $1"
        return 0
    else
        print_error "Archivo no encontrado: $1"
        return 1
    fi
}

# Función para verificar directorios
check_directory() {
    if [ -d "$1" ]; then
        print_success "Directorio encontrado: $1"
        return 0
    else
        print_error "Directorio no encontrado: $1"
        return 1
    fi
}

# Función para verificar comandos
check_command() {
    if command -v "$1" &> /dev/null; then
        print_success "Comando disponible: $1"
        return 0
    else
        print_error "Comando no disponible: $1"
        return 1
    fi
}

# Función para verificar puertos
check_port() {
    if netstat -tuln | grep -q ":$1 "; then
        print_warning "Puerto $1 está en uso"
        return 1
    else
        print_success "Puerto $1 está disponible"
        return 0
    fi
}

# Función para verificar JSON
check_json() {
    if python3 -m json.tool "$1" > /dev/null 2>&1; then
        print_success "JSON válido: $1"
        return 0
    else
        print_error "JSON inválido: $1"
        return 1
    fi
}

# Función para verificar Python
check_python() {
    if python3 -c "import $1" 2>/dev/null; then
        print_success "Módulo Python disponible: $1"
        return 0
    else
        print_error "Módulo Python no disponible: $1"
        return 1
    fi
}

# Función para verificar Node.js
check_node() {
    if [ -f "$1/package.json" ]; then
        print_success "package.json encontrado: $1"
        return 0
    else
        print_warning "package.json no encontrado: $1"
        return 1
    fi
}

# Función para verificar Docker
check_docker() {
    if docker --version &> /dev/null; then
        print_success "Docker disponible"
        return 0
    else
        print_error "Docker no disponible"
        return 1
    fi
}

# Función para verificar Git
check_git() {
    if git --version &> /dev/null; then
        print_success "Git disponible"
        return 0
    else
        print_error "Git no disponible"
        return 1
    fi
}

# Función para verificar permisos
check_permissions() {
    if [ -r "$1" ] && [ -w "$1" ]; then
        print_success "Permisos correctos: $1"
        return 0
    else
        print_error "Permisos incorrectos: $1"
        return 1
    fi
}

# Función para verificar variables de entorno
check_env_vars() {
    local missing_vars=()
    
    # Variables requeridas
    local required_vars=(
        "APP_NAME"
        "APP_VERSION"
        "SMTP_SERVER"
        "SMTP_USERNAME"
        "SMTP_PASSWORD"
        "NOCODB_URL"
        "NOCODB_TOKEN"
    )
    
    for var in "${required_vars[@]}"; do
        if [ -z "${!var}" ]; then
            missing_vars+=("$var")
        fi
    done
    
    if [ ${#missing_vars[@]} -eq 0 ]; then
        print_success "Todas las variables de entorno requeridas están configuradas"
        return 0
    else
        print_error "Variables de entorno faltantes: ${missing_vars[*]}"
        return 1
    fi
}

# Función para verificar configuración de nginx
check_nginx_config() {
    if nginx -t 2>/dev/null; then
        print_success "Configuración de nginx válida"
        return 0
    else
        print_error "Configuración de nginx inválida"
        return 1
    fi
}

# Función para verificar configuración de supervisor
check_supervisor_config() {
    if [ -f "/etc/supervisor/conf.d/supervisord.conf" ]; then
        print_success "Configuración de supervisor encontrada"
        return 0
    else
        print_error "Configuración de supervisor no encontrada"
        return 1
    fi
}

# Función para verificar dependencias Python
check_python_deps() {
    local deps=(
        "fastapi"
        "uvicorn"
        "pydantic"
        "requests"
        "aiohttp"
        "python-dotenv"
        "apscheduler"
    )
    
    local missing_deps=()
    
    for dep in "${deps[@]}"; do
        if ! check_python "$dep"; then
            missing_deps+=("$dep")
        fi
    done
    
    if [ ${#missing_deps[@]} -eq 0 ]; then
        print_success "Todas las dependencias Python están disponibles"
        return 0
    else
        print_error "Dependencias Python faltantes: ${missing_deps[*]}"
        return 1
    fi
}

# Función para verificar dependencias Node.js
check_node_deps() {
    if [ -f "backend-node/package.json" ]; then
        if [ -d "backend-node/node_modules" ]; then
            print_success "Dependencias Node.js instaladas"
            return 0
        else
            print_warning "Dependencias Node.js no instaladas"
            return 1
        fi
    else
        print_warning "Backend Node.js no configurado"
        return 0
    fi
}

# Función para verificar estructura de directorios
check_directory_structure() {
    local dirs=(
        "backend-python"
        "backend-python/app"
        "frontend"
        "frontend/css"
        "frontend/js"
    )
    
    local missing_dirs=()
    
    for dir in "${dirs[@]}"; do
        if ! check_directory "$dir"; then
            missing_dirs+=("$dir")
        fi
    done
    
    if [ ${#missing_dirs[@]} -eq 0 ]; then
        print_success "Estructura de directorios correcta"
        return 0
    else
        print_error "Directorios faltantes: ${missing_dirs[*]}"
        return 1
    fi
}

# Función para verificar archivos de configuración
check_config_files() {
    local files=(
        "config.json"
        "env.example"
        "Dockerfile.easypanel-optimized"
        ".dockerignore"
        "DEPLOY.md"
    )
    
    local missing_files=()
    
    for file in "${files[@]}"; do
        if ! check_file "$file"; then
            missing_files+=("$file")
        fi
    done
    
    if [ ${#missing_files[@]} -eq 0 ]; then
        print_success "Todos los archivos de configuración están presentes"
        return 0
    else
        print_error "Archivos de configuración faltantes: ${missing_files[*]}"
        return 1
    fi
}

# Función para verificar archivos de aplicación
check_app_files() {
    local files=(
        "backend-python/requirements.txt"
        "backend-python/app/main.py"
        "backend-python/app/config.py"
        "backend-python/app/models.py"
        "frontend/index.html"
    )
    
    local missing_files=()
    
    for file in "${files[@]}"; do
        if ! check_file "$file"; then
            missing_files+=("$file")
        fi
    done
    
    if [ ${#missing_files[@]} -eq 0 ]; then
        print_success "Todos los archivos de aplicación están presentes"
        return 0
    else
        print_error "Archivos de aplicación faltantes: ${missing_files[*]}"
        return 1
    fi
}

# Función para verificar puertos
check_ports() {
    local ports=(80 8000 8005)
    local used_ports=()
    
    for port in "${ports[@]}"; do
        if ! check_port "$port"; then
            used_ports+=("$port")
        fi
    done
    
    if [ ${#used_ports[@]} -eq 0 ]; then
        print_success "Todos los puertos están disponibles"
        return 0
    else
        print_warning "Puertos en uso: ${used_ports[*]}"
        return 1
    fi
}

# Función para verificar Git
check_git_repo() {
    if [ -d ".git" ]; then
        print_success "Repositorio Git configurado"
        return 0
    else
        print_error "Repositorio Git no configurado"
        return 1
    fi
}

# Función para verificar build de Docker
check_docker_build() {
    if check_docker; then
        print_status "Verificando build de Docker..."
        if docker build -f Dockerfile.easypanel-optimized -t cotizador-solar-test . > /dev/null 2>&1; then
            print_success "Build de Docker exitoso"
            return 0
        else
            print_error "Build de Docker falló"
            return 1
        fi
    else
        print_warning "Docker no disponible, saltando verificación de build"
        return 0
    fi
}

# Función para verificar configuración completa
check_complete_config() {
    local errors=0
    
    print_status "Verificando configuración completa..."
    
    # Verificar comandos del sistema
    check_command "python3" || ((errors++))
    check_command "pip3" || ((errors++))
    check_command "curl" || ((errors++))
    check_command "netstat" || ((errors++))
    
    # Verificar estructura de directorios
    check_directory_structure || ((errors++))
    
    # Verificar archivos de configuración
    check_config_files || ((errors++))
    
    # Verificar archivos de aplicación
    check_app_files || ((errors++))
    
    # Verificar JSON
    check_json "config.json" || ((errors++))
    
    # Verificar dependencias Python
    check_python_deps || ((errors++))
    
    # Verificar dependencias Node.js
    check_node_deps || ((errors++))
    
    # Verificar puertos
    check_ports || ((errors++))
    
    # Verificar Git
    check_git_repo || ((errors++))
    
    # Verificar build de Docker
    check_docker_build || ((errors++))
    
    return $errors
}

# Función para mostrar resumen
show_summary() {
    local errors=$1
    
    echo ""
    echo "=========================================="
    echo "RESUMEN DE VALIDACIÓN"
    echo "=========================================="
    
    if [ $errors -eq 0 ]; then
        print_success "✅ Validación exitosa - Listo para deploy"
        echo ""
        echo "Próximos pasos:"
        echo "1. Hacer commit y push de los cambios"
        echo "2. Configurar la aplicación en Easypanel"
        echo "3. Establecer variables de entorno"
        echo "4. Configurar volúmenes"
        echo "5. Ejecutar deploy"
    else
        print_error "❌ Validación falló - $errors errores encontrados"
        echo ""
        echo "Por favor, corrige los errores antes de continuar con el deploy"
    fi
    
    echo ""
    echo "Para más información, consulta DEPLOY.md"
    echo "=========================================="
}

# Función principal
main() {
    echo "🚀 Validando configuración de deploy..."
    echo "=========================================="
    
    # Verificar configuración completa
    check_complete_config
    local errors=$?
    
    # Mostrar resumen
    show_summary $errors
    
    # Salir con código de error si hay problemas
    exit $errors
}

# Ejecutar función principal
main "$@"
