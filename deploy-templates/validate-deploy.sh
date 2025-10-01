#!/bin/bash

# ===============================================
# SCRIPT DE VALIDACIÓN PRE-DEPLOY
# ===============================================
# Sistema de Deploy Automático - IdeasDevOps
# Valida la configuración antes del deploy
# ===============================================

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Contadores
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0

# Función para imprimir mensajes
print_message() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
    ((PASSED_CHECKS++))
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
    ((FAILED_CHECKS++))
}

print_check() {
    echo -e "${BLUE}[CHECK]${NC} $1"
    ((TOTAL_CHECKS++))
}

# Función para verificar archivo
check_file() {
    local file="$1"
    local description="$2"
    
    print_check "$description"
    
    if [ -f "$file" ]; then
        print_success "$description - Archivo encontrado"
        return 0
    else
        print_error "$description - Archivo no encontrado: $file"
        return 1
    fi
}

# Función para verificar directorio
check_directory() {
    local dir="$1"
    local description="$2"
    
    print_check "$description"
    
    if [ -d "$dir" ]; then
        print_success "$description - Directorio encontrado"
        return 0
    else
        print_error "$description - Directorio no encontrado: $dir"
        return 1
    fi
}

# Función para verificar contenido de archivo
check_file_content() {
    local file="$1"
    local pattern="$2"
    local description="$3"
    
    print_check "$description"
    
    if [ -f "$file" ] && grep -q "$pattern" "$file"; then
        print_success "$description - Contenido encontrado"
        return 0
    else
        print_error "$description - Contenido no encontrado en $file"
        return 1
    fi
}

# Función para verificar comando
check_command() {
    local cmd="$1"
    local description="$2"
    
    print_check "$description"
    
    if command -v "$cmd" >/dev/null 2>&1; then
        print_success "$description - Comando disponible"
        return 0
    else
        print_error "$description - Comando no encontrado: $cmd"
        return 1
    fi
}

# ===============================================
# INICIO DE VALIDACIONES
# ===============================================

echo "==============================================="
echo "VALIDACIÓN PRE-DEPLOY - IDEASDEVOPS"
echo "==============================================="
echo ""

# ===============================================
# VALIDACIÓN 1: ARCHIVOS REQUERIDOS
# ===============================================
print_message "Validando archivos requeridos..."

check_file "Dockerfile.easypanel-optimized" "Dockerfile optimizado"
check_file "config.json" "Configuración de la aplicación"
check_file "env.example" "Variables de entorno de ejemplo"
check_file ".dockerignore" "Archivo .dockerignore"

# ===============================================
# VALIDACIÓN 2: ESTRUCTURA DE DIRECTORIOS
# ===============================================
print_message "Validando estructura de directorios..."

check_directory "frontend" "Directorio frontend"
check_directory "backend-python" "Directorio backend Python"
check_directory "deploy-templates" "Templates de deploy"

# Verificar si existe backend Node.js (opcional)
if [ -d "backend-node" ]; then
    print_success "Backend Node.js - Directorio encontrado (opcional)"
    ((PASSED_CHECKS++))
else
    print_warning "Backend Node.js - No encontrado (opcional)"
fi

# ===============================================
# VALIDACIÓN 3: CONTENIDO DE ARCHIVOS
# ===============================================
print_message "Validando contenido de archivos..."

check_file_content "Dockerfile.easypanel-optimized" "FROM nginx:alpine" "Dockerfile - Imagen base"
check_file_content "Dockerfile.easypanel-optimized" "EXPOSE 80" "Dockerfile - Puerto expuesto"
check_file_content "Dockerfile.easypanel-optimized" "HEALTHCHECK" "Dockerfile - Healthcheck"

check_file_content "config.json" "app_name" "Config.json - Nombre de aplicación"
check_file_content "config.json" "version" "Config.json - Versión"

# ===============================================
# VALIDACIÓN 4: FRONTEND
# ===============================================
print_message "Validando frontend..."

if [ -f "frontend/index.html" ]; then
    print_success "Frontend - index.html encontrado"
    ((PASSED_CHECKS++))
else
    print_error "Frontend - index.html no encontrado"
    ((FAILED_CHECKS++))
fi

# ===============================================
# VALIDACIÓN 5: BACKEND PYTHON
# ===============================================
print_message "Validando backend Python..."

check_file "backend-python/app/main.py" "Backend Python - main.py"
check_file "backend-python/requirements.txt" "Backend Python - requirements.txt"

# ===============================================
# VALIDACIÓN 6: BACKEND NODE.JS (OPCIONAL)
# ===============================================
if [ -d "backend-node" ]; then
    print_message "Validando backend Node.js..."
    
    check_file "backend-node/package.json" "Backend Node.js - package.json"
    check_file "backend-node/src/index.ts" "Backend Node.js - index.ts"
fi

# ===============================================
# VALIDACIÓN 7: CONFIGURACIÓN NGINX
# ===============================================
print_message "Validando configuración nginx..."

if [ -f "nginx-simple.conf" ]; then
    print_success "Nginx - Configuración encontrada"
    ((PASSED_CHECKS++))
elif [ -f "nginx.conf" ]; then
    print_success "Nginx - Configuración encontrada (nginx.conf)"
    ((PASSED_CHECKS++))
else
    print_warning "Nginx - No se encontró configuración específica"
fi

# ===============================================
# VALIDACIÓN 8: HERRAMIENTAS DEL SISTEMA
# ===============================================
print_message "Validando herramientas del sistema..."

check_command "docker" "Docker"
check_command "git" "Git"

# ===============================================
# VALIDACIÓN 9: REPOSITORIO GIT
# ===============================================
print_message "Validando repositorio Git..."

if [ -d ".git" ]; then
    print_success "Git - Repositorio inicializado"
    ((PASSED_CHECKS++))
    
    # Verificar si hay cambios sin commit
    if git diff --quiet && git diff --cached --quiet; then
        print_success "Git - No hay cambios pendientes"
        ((PASSED_CHECKS++))
    else
        print_warning "Git - Hay cambios sin commit"
    fi
else
    print_error "Git - Repositorio no inicializado"
    ((FAILED_CHECKS++))
fi

# ===============================================
# VALIDACIÓN 10: BUILD LOCAL (OPCIONAL)
# ===============================================
print_message "Validando build local (opcional)..."

if command -v docker >/dev/null 2>&1; then
    print_check "Docker - Build local"
    
    if docker build -f Dockerfile.easypanel-optimized -t test-build . >/dev/null 2>&1; then
        print_success "Docker - Build local exitoso"
        ((PASSED_CHECKS++))
        
        # Limpiar imagen de prueba
        docker rmi test-build >/dev/null 2>&1 || true
    else
        print_error "Docker - Build local falló"
        ((FAILED_CHECKS++))
    fi
else
    print_warning "Docker - No disponible para build local"
fi

# ===============================================
# RESUMEN DE VALIDACIÓN
# ===============================================
echo ""
echo "==============================================="
echo "RESUMEN DE VALIDACIÓN"
echo "==============================================="
echo "Total de verificaciones: $TOTAL_CHECKS"
echo "Exitosas: $PASSED_CHECKS"
echo "Fallidas: $FAILED_CHECKS"
echo ""

if [ $FAILED_CHECKS -eq 0 ]; then
    print_success "¡Todas las validaciones pasaron exitosamente!"
    echo ""
    echo "✅ La aplicación está lista para deploy"
    echo "✅ Puedes proceder con el deploy en EasyPanel"
    echo ""
    echo "Próximos pasos:"
    echo "  1. Hacer commit y push de los cambios"
    echo "  2. Configurar la aplicación en EasyPanel"
    echo "  3. Ejecutar el deploy"
    exit 0
else
    print_error "Se encontraron $FAILED_CHECKS errores"
    echo ""
    echo "❌ La aplicación NO está lista para deploy"
    echo "❌ Corrige los errores antes de continuar"
    echo ""
    echo "Revisa los errores anteriores y corrige:"
    echo "  - Archivos faltantes"
    echo "  - Configuraciones incorrectas"
    echo "  - Dependencias no instaladas"
    exit 1
fi
