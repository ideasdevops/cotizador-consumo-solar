// App principal para el Cotizador de Consumo Solar
// Funciones de utilidad y navegación

// Función para scroll suave
function smoothScrollTo(targetId) {
  const target = document.querySelector(targetId);
  if (target) {
    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
}

// Función para actualizar tiempo de última actualización
function updateLastUpdateTime() {
  const lastUpdateElement = document.getElementById('last-update');
  if (lastUpdateElement) {
    const now = new Date();
    lastUpdateElement.textContent = now.toLocaleString('es-AR');
  }
}

// Función para cargar datos guardados
function loadSavedData() {
  try {
    const savedData = localStorage.getItem('solar-calculator-data');
    if (savedData) {
      const data = JSON.parse(savedData);
      
      // Restaurar datos del formulario
      if (data.monthlyConsumption) {
        const consumptionField = document.getElementById('monthlyConsumption');
        if (consumptionField) {
          consumptionField.value = data.monthlyConsumption;
        }
      }
      
      if (data.location) {
        const locationField = document.getElementById('location');
        if (locationField) {
          locationField.value = data.location;
        }
      }
      
      if (data.tariffType) {
        const tariffField = document.getElementById('tariffType');
        if (tariffField) {
          tariffField.value = data.tariffType;
        }
      }
    }
  } catch (error) {
    console.error('Error cargando datos guardados:', error);
  }
}

// Función para guardar datos
function saveData() {
  try {
    const data = {
      monthlyConsumption: document.getElementById('monthlyConsumption')?.value || '',
      location: document.getElementById('location')?.value || '',
      tariffType: document.getElementById('tariffType')?.value || ''
    };
    
    localStorage.setItem('solar-calculator-data', JSON.stringify(data));
  } catch (error) {
    console.error('Error guardando datos:', error);
  }
}

// Función para mostrar notificaciones
function showNotification(message, type = 'info') {
  const notification = document.createElement('div');
  notification.className = `notification notification-${type}`;
  notification.innerHTML = `
    <div class="notification-content">
      <span class="notification-message">${message}</span>
      <button class="notification-close" onclick="this.parentElement.parentElement.remove()">×</button>
    </div>
  `;
  
  document.body.appendChild(notification);
  
  // Auto-remove after 5 seconds
  setTimeout(() => {
    if (notification.parentNode) {
      notification.remove();
    }
  }, 5000);
}

// Función para actualizar precios (placeholder)
function updatePrices() {
  showNotification('Actualizando precios...', 'info');
  // Esta función será manejada por el servicio de precios
}

// Función para scroll a sección
function scrollToSection(sectionId) {
  smoothScrollTo(`#${sectionId}`);
}

// Inicializar la aplicación cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
  console.log('🚀 Inicializando aplicación principal...');
  
  // Configurar scroll suave para navegación
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
        e.preventDefault();
      const targetId = anchor.getAttribute('href');
      smoothScrollTo(targetId);
    });
  });
  
  // Actualizar tiempo de última actualización
  updateLastUpdateTime();
  
  // Cargar datos guardados
  loadSavedData();
  
  // Guardar datos cuando cambien los campos
  const formFields = ['monthlyConsumption', 'location', 'tariffType'];
  formFields.forEach(fieldId => {
    const field = document.getElementById(fieldId);
    if (field) {
      field.addEventListener('change', saveData);
    }
  });
  
  console.log('✅ Aplicación principal inicializada correctamente');
});

// Agregar estilos para notificaciones
const style = document.createElement('style');
style.textContent = `
  .notification {
    position: fixed;
    top: 20px;
    right: 20px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    z-index: 1000;
    max-width: 400px;
    animation: slideInRight 0.3s ease-out;
  }
  
  .notification-info {
    border-left: 4px solid #3b82f6;
  }
  
  .notification-success {
    border-left: 4px solid #10b981;
  }
  
  .notification-error {
    border-left: 4px solid #ef4444;
  }
  
  .notification-content {
    padding: 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  
  .notification-message {
    flex: 1;
    margin-right: 12px;
  }
  
  .notification-close {
    background: none;
    border: none;
    font-size: 18px;
    cursor: pointer;
    color: #6b7280;
    padding: 0;
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .notification-close:hover {
    color: #374151;
  }
  
  @keyframes slideInRight {
    from {
      transform: translateX(100%);
      opacity: 0;
    }
    to {
      transform: translateX(0);
      opacity: 1;
    }
  }
`;
document.head.appendChild(style);