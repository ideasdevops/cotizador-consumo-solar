// App principal para el Cotizador de Consumo Solar
class SolarCalculator {
  constructor() {
    this.prices = {
      panelCost: 150000, // Costo por panel en ARS
      inverterCost: 800000, // Costo por kW de inversor
      installationCost: 200000, // Costo de instalación por kWp
      panelPower: 0.5, // Potencia por panel en kWp
      efficiency: 0.85, // Eficiencia del sistema
      sunHours: 5.5, // Horas de sol promedio por día
      tariffRate: {
        residential: 45, // ARS por kWh
        commercial: 38,
        industrial: 32
      }
    };
    
    this.init();
  }

  init() {
    this.setupEventListeners();
    this.updateLastUpdateTime();
    this.loadSavedData();
  }

  setupEventListeners() {
    // Smooth scrolling para navegación
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', (e) => {
        e.preventDefault();
        const target = document.querySelector(anchor.getAttribute('href'));
        if (target) {
          target.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
          });
        }
      });
    });

    // Formulario de contacto
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
      contactForm.addEventListener('submit', (e) => {
        e.preventDefault();
        this.handleContactForm(e);
      });
    }

    // Actualización de precios
    const updateButton = document.querySelector('.btn-ghost');
    if (updateButton) {
      updateButton.addEventListener('click', () => {
        this.updatePrices();
      });
    }
  }

  calculateSolarSystem() {
    const monthlyConsumption = parseFloat(document.getElementById('monthlyConsumption').value);
    const tariffType = document.getElementById('tariffType').value;
    const location = document.getElementById('location').value;

    if (!monthlyConsumption || monthlyConsumption <= 0) {
      this.showError('Por favor ingresa un consumo mensual válido');
      return;
    }

    // Cálculos del sistema solar
    const dailyConsumption = monthlyConsumption / 30;
    const requiredPower = dailyConsumption / (this.prices.sunHours * this.prices.efficiency);
    const panelsCount = Math.ceil(requiredPower / this.prices.panelPower);
    const inverterSize = Math.ceil(requiredPower * 1.2); // 20% de margen
    const systemPower = panelsCount * this.prices.panelPower;

    // Cálculos económicos
    const panelCost = panelsCount * this.prices.panelCost;
    const inverterCost = inverterSize * this.prices.inverterCost;
    const installationCost = systemPower * this.prices.installationCost;
    const totalInvestment = panelCost + inverterCost + installationCost;

    const monthlySavings = monthlyConsumption * this.prices.tariffRate[tariffType];
    const annualSavings = monthlySavings * 12;
    const paybackYears = totalInvestment / annualSavings;

    // Mostrar resultados
    this.displayResults({
      requiredPower: systemPower.toFixed(1),
      panelsCount: panelsCount,
      inverterSize: inverterSize.toFixed(1),
      monthlySavings: this.formatCurrency(monthlySavings),
      investment: this.formatCurrency(totalInvestment),
      payback: paybackYears.toFixed(1)
    });

    // Guardar datos
    this.saveCalculation({
      monthlyConsumption,
      tariffType,
      location,
      results: {
        requiredPower: systemPower,
        panelsCount,
        inverterSize,
        monthlySavings,
        investment: totalInvestment,
        paybackYears
      }
    });
  }

  displayResults(results) {
    const resultsContainer = document.getElementById('results');
    if (!resultsContainer) return;

    // Actualizar valores
    document.getElementById('requiredPower').textContent = results.requiredPower + ' kWp';
    document.getElementById('panelsCount').textContent = results.panelsCount + ' unidades';
    document.getElementById('inverterSize').textContent = results.inverterSize + ' kW';
    document.getElementById('monthlySavings').textContent = results.monthlySavings;
    document.getElementById('investment').textContent = results.investment;
    document.getElementById('payback').textContent = results.payback + ' años';

    // Mostrar resultados con animación
    resultsContainer.style.display = 'block';
    resultsContainer.classList.add('animate-fade-in');

    // Scroll a resultados
    resultsContainer.scrollIntoView({
      behavior: 'smooth',
      block: 'start'
    });
  }

  formatCurrency(amount) {
    return new Intl.NumberFormat('es-AR', {
      style: 'currency',
      currency: 'ARS',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(amount);
  }

  showError(message) {
    // Crear notificación de error
    const notification = document.createElement('div');
    notification.className = 'notification error';
    notification.innerHTML = `
      <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
        <path d="M10 18C14.4183 18 18 14.4183 18 10C18 5.58172 14.4183 2 10 2C5.58172 2 2 5.58172 2 10C2 14.4183 5.58172 18 10 18Z" stroke="currentColor" stroke-width="2"/>
        <path d="M10 6V10M10 14H10.01" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      ${message}
    `;
    
    document.body.appendChild(notification);
    
    // Remover después de 5 segundos
    setTimeout(() => {
      notification.remove();
    }, 5000);
  }

  showSuccess(message) {
    // Crear notificación de éxito
    const notification = document.createElement('div');
    notification.className = 'notification success';
    notification.innerHTML = `
      <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
        <path d="M10 18C14.4183 18 18 14.4183 18 10C18 5.58172 14.4183 2 10 2C5.58172 2 2 5.58172 2 10C2 14.4183 5.58172 18 10 18Z" stroke="currentColor" stroke-width="2"/>
        <path d="M6 10L8.5 12.5L14 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      ${message}
    `;
    
    document.body.appendChild(notification);
    
    // Remover después de 5 segundos
    setTimeout(() => {
      notification.remove();
    }, 5000);
  }

  async handleContactForm(e) {
    const formData = new FormData(e.target);
    const data = {
      name: formData.get('name') || document.getElementById('name').value,
      email: formData.get('email') || document.getElementById('email').value,
      phone: formData.get('phone') || document.getElementById('phone').value,
      message: formData.get('message') || document.getElementById('message').value
    };

    try {
      const response = await fetch('/api/contact', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
      });

      if (response.ok) {
        this.showSuccess('¡Consulta enviada exitosamente! Te contactaremos pronto.');
        e.target.reset();
      } else {
        throw new Error('Error al enviar la consulta');
      }
    } catch (error) {
      this.showError('Error al enviar la consulta. Por favor intenta nuevamente.');
      console.error('Error:', error);
    }
  }

  async updatePrices() {
    try {
      const response = await fetch('/api/update-prices', {
        method: 'POST'
      });

      if (response.ok) {
        this.showSuccess('Precios actualizados exitosamente');
        this.updateLastUpdateTime();
      } else {
        throw new Error('Error al actualizar precios');
      }
    } catch (error) {
      this.showError('Error al actualizar precios. Usando precios en caché.');
      console.error('Error:', error);
    }
  }

  updateLastUpdateTime() {
    const lastUpdateElement = document.getElementById('lastUpdate');
    if (lastUpdateElement) {
      lastUpdateElement.textContent = 'hace un momento';
    }
  }

  saveCalculation(data) {
    try {
      localStorage.setItem('lastSolarCalculation', JSON.stringify(data));
    } catch (error) {
      console.error('Error al guardar cálculo:', error);
    }
  }

  loadSavedData() {
    try {
      const savedData = localStorage.getItem('lastSolarCalculation');
      if (savedData) {
        const data = JSON.parse(savedData);
        document.getElementById('monthlyConsumption').value = data.monthlyConsumption || '';
        document.getElementById('tariffType').value = data.tariffType || 'residential';
        document.getElementById('location').value = data.location || 'buenos-aires';
      }
    } catch (error) {
      console.error('Error al cargar datos guardados:', error);
    }
  }
}

// Funciones globales para compatibilidad con HTML
function scrollToSection(sectionId) {
  const section = document.getElementById(sectionId);
  if (section) {
    section.scrollIntoView({
      behavior: 'smooth',
      block: 'start'
    });
  }
}

function calculateSolarSystem() {
  if (window.solarCalculator) {
    window.solarCalculator.calculateSolarSystem();
  }
}

function updatePrices() {
  if (window.solarCalculator) {
    window.solarCalculator.updatePrices();
  }
}

// Inicializar la aplicación cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
  window.solarCalculator = new SolarCalculator();
  
  // Agregar estilos para notificaciones
  const style = document.createElement('style');
  style.textContent = `
    .notification {
      position: fixed;
      top: 20px;
      right: 20px;
      padding: 16px 20px;
      border-radius: 8px;
      display: flex;
      align-items: center;
      gap: 12px;
      font-weight: 500;
      z-index: 1000;
      animation: slideIn 0.3s ease-out;
      max-width: 400px;
    }
    
    .notification.success {
      background: #10B981;
      color: white;
    }
    
    .notification.error {
      background: #EF4444;
      color: white;
    }
    
    @keyframes slideIn {
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
});

// Manejar errores globales
window.addEventListener('error', (e) => {
  console.error('Error global:', e.error);
});

// Manejar errores de promesas no capturadas
window.addEventListener('unhandledrejection', (e) => {
  console.error('Promesa rechazada:', e.reason);
});