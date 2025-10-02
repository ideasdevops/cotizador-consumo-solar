// Calculadora Solar - Funcionalidad completa
class SolarCalculator {
  constructor() {
    this.apiBaseUrl = '/api/solar';
    this.currentQuote = null;
    this.materials = {
      panels: [],
      inverters: [],
      batteries: [],
      mounting: [],
      cables: [],
      protection: []
    };
    
    this.init();
  }

  async init() {
    console.log('Inicializando calculadora solar...');
    await this.loadMaterials();
    this.setupEventListeners();
    this.setupFormValidation();
    console.log('Calculadora solar inicializada correctamente');
  }

  async loadMaterials() {
    try {
      console.log('Cargando materiales desde:', `${this.apiBaseUrl}/materials`);
      const response = await fetch(`${this.apiBaseUrl}/materials`);
      console.log('Respuesta de materiales:', response.status);
      
      if (response.ok) {
        this.materials = await response.json();
        console.log('Materiales cargados:', this.materials);
        this.populateMaterialSelects();
      } else {
        console.error('Error cargando materiales:', response.statusText);
        // Intentar cargar materiales por defecto
        this.loadDefaultMaterials();
      }
    } catch (error) {
      console.error('Error cargando materiales:', error);
      // Cargar materiales por defecto en caso de error
      this.loadDefaultMaterials();
    }
  }

  loadDefaultMaterials() {
    console.log('Cargando materiales por defecto...');
    this.materials = {
      panels: [
        {
          id: "panel_default",
          brand: "JinkoSolar",
          model: "JKM400M-54HL4-B",
          power_watts: 400,
          price_ars: 180000
        }
      ],
      inverters: [
        {
          id: "inverter_default",
          brand: "SMA",
          model: "STP 5000TL-20",
          power_kw: 5.0,
          price_ars: 800000
        }
      ],
      batteries: [],
      mounting: [
        {
          id: "mounting_default",
          brand: "Schletter",
          model: "FS-R",
          price_per_kw: 150000
        }
      ],
      cables: [],
      protection: []
    };
    this.populateMaterialSelects();
  }

  setupEventListeners() {
    console.log('🔧 Configurando event listeners...');
    
    // Formulario principal
    const solarForm = document.getElementById('solar-form');
    console.log('📋 Formulario solar encontrado:', solarForm);
    if (solarForm) {
      solarForm.addEventListener('submit', (e) => {
        console.log('📝 Formulario enviado, iniciando cálculo completo...');
        e.preventDefault();
        this.calculateSolarSystem();
      });
    } else {
      console.error('❌ No se encontró el formulario solar-form');
    }

    // Botón de estimación rápida
    const estimateBtn = document.getElementById('estimate-btn');
    console.log('⚡ Botón de estimación encontrado:', estimateBtn);
    if (estimateBtn) {
      estimateBtn.addEventListener('click', () => {
        console.log('🚀 Iniciando estimación rápida...');
        this.performQuickEstimate();
      });
    } else {
      console.error('❌ No se encontró el botón estimate-btn');
    }

    // Checkbox de baterías
    const batteryCheckbox = document.getElementById('batteryBackup');
    if (batteryCheckbox) {
      batteryCheckbox.addEventListener('change', () => {
        this.toggleBatteryOptions();
      });
    }

    // Selectores de materiales
    this.setupMaterialSelectors();

    // Validación en tiempo real
    this.setupRealTimeValidation();
  }

  setupFormValidation() {
    const inputs = document.querySelectorAll('#solar-form input, #solar-form select');
    inputs.forEach(input => {
      input.addEventListener('blur', () => {
        this.validateField(input);
      });
    });
  }

  setupRealTimeValidation() {
    const monthlyConsumption = document.getElementById('monthlyConsumption');
    if (monthlyConsumption) {
      monthlyConsumption.addEventListener('input', () => {
        this.updateConsumptionDisplay();
      });
    }
  }

  setupMaterialSelectors() {
    // Selector de tipo de panel
    const panelTypeSelect = document.getElementById('panelType');
    if (panelTypeSelect) {
      panelTypeSelect.addEventListener('change', () => {
        this.filterPanelsByType();
      });
    }

    // Selector de tipo de inversor
    const inverterTypeSelect = document.getElementById('inverterType');
    if (inverterTypeSelect) {
      inverterTypeSelect.addEventListener('change', () => {
        this.filterInvertersByType();
      });
    }
  }

  populateMaterialSelects() {
    this.populatePanelSelect();
    this.populateInverterSelect();
    this.populateBatterySelect();
    this.populateMountingSelect();
  }

  populatePanelSelect() {
    const panelSelect = document.getElementById('panelSelect');
    if (!panelSelect) return;

    panelSelect.innerHTML = '<option value="">Seleccionar panel...</option>';
    
    this.materials.panels.forEach(panel => {
      const option = document.createElement('option');
      option.value = panel.id;
      option.textContent = `${panel.brand} ${panel.model} - ${panel.power_watts}W - $${this.formatCurrency(panel.price_ars)}`;
      panelSelect.appendChild(option);
    });
  }

  populateInverterSelect() {
    const inverterSelect = document.getElementById('inverterSelect');
    if (!inverterSelect) return;

    inverterSelect.innerHTML = '<option value="">Seleccionar inversor...</option>';
    
    this.materials.inverters.forEach(inverter => {
      const option = document.createElement('option');
      option.value = inverter.id;
      option.textContent = `${inverter.brand} ${inverter.model} - ${inverter.power_kw}kW - $${this.formatCurrency(inverter.price_ars)}`;
      inverterSelect.appendChild(option);
    });
  }

  populateBatterySelect() {
    const batterySelect = document.getElementById('batterySelect');
    if (!batterySelect) return;

    batterySelect.innerHTML = '<option value="">Sin baterías</option>';
    
    this.materials.batteries.forEach(battery => {
      const option = document.createElement('option');
      option.value = battery.id;
      option.textContent = `${battery.brand} ${battery.model} - ${battery.power_kwh}kWh - $${this.formatCurrency(battery.price_ars)}`;
      batterySelect.appendChild(option);
    });
  }

  populateMountingSelect() {
    const mountingSelect = document.getElementById('mountingSelect');
    if (!mountingSelect) return;

    mountingSelect.innerHTML = '<option value="">Seleccionar sistema de montaje...</option>';
    
    this.materials.mounting.forEach(mounting => {
      const option = document.createElement('option');
      option.value = mounting.id;
      option.textContent = `${mounting.brand} ${mounting.model} - $${this.formatCurrency(mounting.price_per_kw)}/kW`;
      mountingSelect.appendChild(option);
    });
  }

  async calculateSolarSystem() {
    try {
      this.showLoading(true);
      
      // Primero probar la conexión con la API
      console.log('Probando conexión con la API...');
      const testResponse = await fetch(`${this.apiBaseUrl}/test`);
      if (!testResponse.ok) {
        console.error('API no disponible:', testResponse.status);
        this.showError('El servicio de cálculo no está disponible. Por favor intenta más tarde.');
        this.showLoading(false);
        return;
      }
      
      const formData = this.collectFormData();
      const validation = this.validateFormData(formData);
      
      if (!validation.isValid) {
        this.showError(validation.message);
        this.showLoading(false);
        return;
      }

      console.log('Enviando datos:', formData);

      const response = await fetch(`${this.apiBaseUrl}/quote`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      console.log('Respuesta del servidor:', response.status);

      if (response.ok) {
        const quote = await response.json();
        console.log('Cotización recibida:', quote);
        this.currentQuote = quote;
        this.showDetailedQuoteModal(quote);
        this.showSuccess('Cotización generada exitosamente');
      } else {
        const errorText = await response.text();
        console.error('Error del servidor:', errorText);
        let errorMessage = 'Error generando cotización';
        
        try {
          const errorJson = JSON.parse(errorText);
          errorMessage = errorJson.detail || errorMessage;
        } catch (e) {
          errorMessage = errorText || errorMessage;
        }
        
        this.showError(errorMessage);
      }

    } catch (error) {
      console.error('Error calculando sistema solar:', error);
      this.showError('Error de conexión. Por favor intenta nuevamente.');
    } finally {
      this.showLoading(false);
    }
  }

  async performQuickEstimate() {
    try {
      const monthlyConsumption = parseFloat(document.getElementById('monthlyConsumption').value);
      const location = document.getElementById('location').value;
      const installationType = document.getElementById('installationType').value;

      if (!monthlyConsumption || monthlyConsumption <= 0) {
        this.showError('Por favor ingresa un consumo mensual válido');
        return;
      }

      this.showLoading(true);

      const response = await fetch(`${this.apiBaseUrl}/estimate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          monthly_consumption: monthlyConsumption,
          location: location,
          installation_type: installationType
        })
      });

      if (response.ok) {
        const estimation = await response.json();
        this.showQuickEstimateModal(estimation);
      } else {
        const error = await response.json();
        this.showError(error.detail || 'Error en estimación');
      }

    } catch (error) {
      console.error('Error en estimación rápida:', error);
      this.showError('Error de conexión. Por favor intenta nuevamente.');
    } finally {
      this.showLoading(false);
    }
  }

  collectFormData() {
    return {
      client_name: document.getElementById('clientName')?.value || '',
      client_email: document.getElementById('clientEmail')?.value || '',
      client_phone: document.getElementById('clientPhone')?.value || '',
      location: document.getElementById('location').value,
      monthly_consumption_kwh: parseFloat(document.getElementById('monthlyConsumption').value),
      peak_consumption_kw: parseFloat(document.getElementById('peakConsumption')?.value) || null,
      tariff_type: document.getElementById('tariffType').value,
      available_area_m2: parseFloat(document.getElementById('availableArea').value),
      roof_type: document.getElementById('roofType')?.value || null,
      roof_orientation: document.getElementById('roofOrientation')?.value || null,
      roof_tilt: parseFloat(document.getElementById('roofTilt')?.value) || null,
      installation_type: document.getElementById('installationType').value,
      panel_type_preference: document.getElementById('panelType')?.value || null,
      inverter_type_preference: document.getElementById('inverterType')?.value || null,
      battery_backup: document.getElementById('batteryBackup')?.checked || false,
      battery_autonomy_hours: parseInt(document.getElementById('batteryAutonomy')?.value) || null,
      budget_range: document.getElementById('budgetRange')?.value || null,
      financing_required: document.getElementById('financingRequired')?.checked || false,
      notes: document.getElementById('notes')?.value || ''
    };
  }

  validateFormData(data) {
    if (!data.monthly_consumption_kwh || data.monthly_consumption_kwh <= 0) {
      return { isValid: false, message: 'El consumo mensual debe ser mayor a 0' };
    }

    if (!data.available_area_m2 || data.available_area_m2 <= 0) {
      return { isValid: false, message: 'El área disponible debe ser mayor a 0' };
    }

    if (!data.location) {
      return { isValid: false, message: 'Debe seleccionar una ubicación' };
    }

    if (!data.tariff_type) {
      return { isValid: false, message: 'Debe seleccionar un tipo de tarifa' };
    }

    if (!data.installation_type) {
      return { isValid: false, message: 'Debe seleccionar un tipo de instalación' };
    }

    return { isValid: true };
  }

  validateField(field) {
    const value = field.value.trim();
    const fieldName = field.getAttribute('name') || field.id;

    // Remover clases de error previas
    field.classList.remove('error');

    if (field.hasAttribute('required') && !value) {
      field.classList.add('error');
      return false;
    }

    if (field.type === 'number' && value) {
      const numValue = parseFloat(value);
      if (isNaN(numValue) || numValue <= 0) {
        field.classList.add('error');
        return false;
      }
    }

    if (field.type === 'email' && value) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(value)) {
        field.classList.add('error');
        return false;
      }
    }

    return true;
  }

  displayResults(design) {
    const resultsContainer = document.getElementById('solar-results');
    if (!resultsContainer) return;

    // Actualizar valores principales
    this.updateElement('requiredPower', `${design.required_power_kwp} kWp`);
    this.updateElement('panelsCount', `${design.panel_count} unidades`);
    this.updateElement('inverterCount', `${design.inverter_count} unidades`);
    this.updateElement('systemEfficiency', `${design.system_efficiency}%`);
    
    // Generación energética
    this.updateElement('dailyGeneration', `${design.daily_generation_kwh} kWh`);
    this.updateElement('monthlyGeneration', `${design.monthly_generation_kwh} kWh`);
    this.updateElement('annualGeneration', `${design.annual_generation_kwh} kWh`);
    
    // Costos
    this.updateElement('totalInvestment', this.formatCurrency(design.total_investment));
    this.updateElement('panelsCost', this.formatCurrency(design.panels_cost));
    this.updateElement('invertersCost', this.formatCurrency(design.inverters_cost));
    this.updateElement('mountingCost', this.formatCurrency(design.mounting_cost));
    this.updateElement('installationCost', this.formatCurrency(design.installation_cost));
    
    // Economía
    this.updateElement('monthlySavings', this.formatCurrency(design.monthly_savings));
    this.updateElement('annualSavings', this.formatCurrency(design.annual_savings));
    this.updateElement('paybackYears', `${design.payback_years} años`);
    this.updateElement('roiPercentage', `${design.roi_percentage}%`);

    // Baterías (si aplica)
    if (design.battery_count && design.battery_count > 0) {
      this.updateElement('batteryCount', `${design.battery_count} unidades`);
      this.updateElement('batteriesCost', this.formatCurrency(design.batteries_cost));
      document.getElementById('battery-section').style.display = 'block';
    } else {
      document.getElementById('battery-section').style.display = 'none';
    }

    // Mostrar resultados
    resultsContainer.style.display = 'block';
    resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });

    // Generar gráfico de costos
    this.generateCostChart(design);
  }

  displayQuickEstimate(estimation) {
    const estimateContainer = document.getElementById('quick-estimate');
    if (!estimateContainer) return;

    this.updateElement('estimatedPower', `${estimation.estimated_power_kwp} kWp`);
    this.updateElement('estimatedArea', `${estimation.estimated_area_m2} m²`);
    this.updateElement('estimatedCost', this.formatCurrency(estimation.estimated_cost));
    this.updateElement('estimatedPanels', `${estimation.estimated_panels} unidades`);

    estimateContainer.style.display = 'block';
    estimateContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  updateElement(id, value) {
    const element = document.getElementById(id);
    if (element) {
      element.textContent = value;
    }
  }

  updateConsumptionDisplay() {
    const monthlyConsumption = parseFloat(document.getElementById('monthlyConsumption').value);
    if (monthlyConsumption && monthlyConsumption > 0) {
      const dailyConsumption = monthlyConsumption / 30;
      const annualConsumption = monthlyConsumption * 12;
      
      this.updateElement('dailyConsumption', `${dailyConsumption.toFixed(1)} kWh`);
      this.updateElement('annualConsumption', `${annualConsumption.toFixed(0)} kWh`);
    }
  }

  generateCostChart(design) {
    const chartContainer = document.getElementById('cost-chart');
    if (!chartContainer) return;

    const costData = [
      { label: 'Paneles', value: design.panels_cost, color: '#10B981' },
      { label: 'Inversores', value: design.inverters_cost, color: '#3B82F6' },
      { label: 'Montaje', value: design.mounting_cost, color: '#F59E0B' },
      { label: 'Instalación', value: design.installation_cost, color: '#EF4444' }
    ];

    if (design.batteries_cost && design.batteries_cost > 0) {
      costData.push({ label: 'Baterías', value: design.batteries_cost, color: '#8B5CF6' });
    }

    // Crear gráfico simple con HTML/CSS
    let chartHTML = '<div class="cost-breakdown">';
    costData.forEach(item => {
      const percentage = (item.value / design.total_investment) * 100;
      chartHTML += `
        <div class="cost-item">
          <div class="cost-bar">
            <div class="cost-fill" style="width: ${percentage}%; background-color: ${item.color};"></div>
          </div>
          <div class="cost-label">
            <span class="cost-name">${item.label}</span>
            <span class="cost-value">${this.formatCurrency(item.value)}</span>
            <span class="cost-percentage">${percentage.toFixed(1)}%</span>
          </div>
        </div>
      `;
    });
    chartHTML += '</div>';

    chartContainer.innerHTML = chartHTML;
  }

  filterPanelsByType() {
    const panelType = document.getElementById('panelType').value;
    const panelSelect = document.getElementById('panelSelect');
    
    if (!panelSelect) return;

    panelSelect.innerHTML = '<option value="">Seleccionar panel...</option>';
    
    const filteredPanels = panelType 
      ? this.materials.panels.filter(panel => panel.type === panelType)
      : this.materials.panels;
    
    filteredPanels.forEach(panel => {
      const option = document.createElement('option');
      option.value = panel.id;
      option.textContent = `${panel.brand} ${panel.model} - ${panel.power_watts}W - $${this.formatCurrency(panel.price_ars)}`;
      panelSelect.appendChild(option);
    });
  }

  filterInvertersByType() {
    const inverterType = document.getElementById('inverterType').value;
    const inverterSelect = document.getElementById('inverterSelect');
    
    if (!inverterSelect) return;

    inverterSelect.innerHTML = '<option value="">Seleccionar inversor...</option>';
    
    const filteredInverters = inverterType 
      ? this.materials.inverters.filter(inverter => inverter.type === inverterType)
      : this.materials.inverters;
    
    filteredInverters.forEach(inverter => {
      const option = document.createElement('option');
      option.value = inverter.id;
      option.textContent = `${inverter.brand} ${inverter.model} - ${inverter.power_kw}kW - $${this.formatCurrency(inverter.price_ars)}`;
      inverterSelect.appendChild(option);
    });
  }

  toggleBatteryOptions() {
    const batteryCheckbox = document.getElementById('batteryBackup');
    const batteryOptions = document.getElementById('batteryOptions');
    
    if (batteryCheckbox && batteryOptions) {
      if (batteryCheckbox.checked) {
        batteryOptions.style.display = 'block';
      } else {
        batteryOptions.style.display = 'none';
      }
    }
  }

  formatCurrency(amount) {
    return new Intl.NumberFormat('es-AR', {
      style: 'currency',
      currency: 'ARS',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(amount);
  }

  showLoading(show) {
    const loadingElement = document.getElementById('loading-indicator');
    if (loadingElement) {
      loadingElement.style.display = show ? 'block' : 'none';
    }

    const submitBtn = document.querySelector('#solar-form button[type="submit"]');
    if (submitBtn) {
      submitBtn.disabled = show;
      submitBtn.textContent = show ? 'Calculando...' : 'Calcular Cotización Solar';
    }
  }

  showError(message) {
    this.showNotification(message, 'error');
  }

  showSuccess(message) {
    this.showNotification(message, 'success');
  }

  showNotification(message, type) {
    // Crear notificación
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
      <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
        ${type === 'error' 
          ? '<path d="M10 18C14.4183 18 18 14.4183 18 10C18 5.58172 14.4183 2 10 2C5.58172 2 2 5.58172 2 10C2 14.4183 5.58172 18 10 18Z" stroke="currentColor" stroke-width="2"/><path d="M10 6V10M10 14H10.01" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
          : '<path d="M10 18C14.4183 18 18 14.4183 18 10C18 5.58172 14.4183 2 10 2C5.58172 2 2 5.58172 2 10C2 14.4183 5.58172 18 10 18Z" stroke="currentColor" stroke-width="2"/><path d="M6 10L8.5 12.5L14 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
        }
      </svg>
      ${message}
    `;
    
    document.body.appendChild(notification);
    
    // Remover después de 5 segundos
    setTimeout(() => {
      notification.remove();
    }, 5000);
  }

  // Método para exportar cotización
  exportQuote() {
    if (!this.currentQuote) {
      this.showError('No hay cotización para exportar');
      return;
    }

    const quoteData = {
      quote_id: this.currentQuote.quote_id,
      created_at: this.currentQuote.created_at,
      valid_until: this.currentQuote.valid_until,
      design: this.currentQuote.design,
      request: this.currentQuote.request
    };

    const dataStr = JSON.stringify(quoteData, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    
    const link = document.createElement('a');
    link.href = url;
    link.download = `cotizacion_solar_${this.currentQuote.quote_id}.json`;
    link.click();
    
    URL.revokeObjectURL(url);
  }

  // Métodos para modales
  showQuickEstimateModal(estimation) {
    const modal = document.getElementById('quickEstimateModal');
    const content = document.getElementById('quickEstimateContent');
    
    content.innerHTML = `
      <div class="quick-estimate-summary">
        <div class="estimate-card">
          <h3><i class="fas fa-bolt"></i> Potencia Estimada</h3>
          <div class="value">${estimation.estimated_power_kwp} kWp</div>
          <div class="label">Sistema Solar</div>
        </div>
        <div class="estimate-card">
          <h3><i class="fas fa-solar-panel"></i> Paneles</h3>
          <div class="value">${estimation.estimated_panels}</div>
          <div class="label">Unidades</div>
        </div>
        <div class="estimate-card">
          <h3><i class="fas fa-dollar-sign"></i> Inversión</h3>
          <div class="value">${this.formatCurrency(estimation.estimated_cost)}</div>
          <div class="label">Aproximada</div>
        </div>
        <div class="estimate-card">
          <h3><i class="fas fa-chart-line"></i> Ahorro Anual</h3>
          <div class="value">${this.formatCurrency(estimation.estimated_savings)}</div>
          <div class="label">Estimado</div>
        </div>
      </div>
      <div class="quote-section">
        <h3><i class="fas fa-info-circle"></i> Información de la Estimación</h3>
        <p><strong>Consumo mensual:</strong> ${estimation.monthly_consumption} kWh</p>
        <p><strong>Ubicación:</strong> ${estimation.location}</p>
        <p><strong>Tipo de instalación:</strong> ${estimation.installation_type}</p>
        <p><strong>Fecha de estimación:</strong> ${new Date().toLocaleDateString('es-AR')}</p>
        <p class="text-muted">Esta es una estimación preliminar. Para obtener una cotización precisa, solicita una cotización completa con nuestros expertos.</p>
      </div>
    `;
    
    modal.style.display = 'flex';
    this.currentEstimation = estimation;
  }

  showDetailedQuoteModal(quote) {
    const modal = document.getElementById('detailedQuoteModal');
    const content = document.getElementById('detailedQuoteContent');
    
    const design = quote.design;
    
    content.innerHTML = `
      <div class="detailed-quote-summary">
        <div class="quote-section">
          <h3><i class="fas fa-bolt"></i> Dimensionamiento del Sistema</h3>
          <div class="quote-grid">
            <div class="quote-item">
              <span class="label">Potencia del Sistema:</span>
              <span class="value">${design.required_power_kwp} kWp</span>
            </div>
            <div class="quote-item">
              <span class="label">Cantidad de Paneles:</span>
              <span class="value">${design.panel_count} unidades</span>
            </div>
            <div class="quote-item">
              <span class="label">Cantidad de Inversores:</span>
              <span class="value">${design.inverter_count} unidades</span>
            </div>
            <div class="quote-item">
              <span class="label">Eficiencia del Sistema:</span>
              <span class="value">${design.system_efficiency}%</span>
            </div>
          </div>
        </div>

        <div class="quote-section">
          <h3><i class="fas fa-sun"></i> Generación Energética</h3>
          <div class="quote-grid">
            <div class="quote-item">
              <span class="label">Generación Diaria:</span>
              <span class="value">${design.daily_generation_kwh} kWh</span>
            </div>
            <div class="quote-item">
              <span class="label">Generación Mensual:</span>
              <span class="value">${design.monthly_generation_kwh} kWh</span>
            </div>
            <div class="quote-item">
              <span class="label">Generación Anual:</span>
              <span class="value">${design.annual_generation_kwh} kWh</span>
            </div>
          </div>
        </div>

        <div class="quote-section">
          <h3><i class="fas fa-dollar-sign"></i> Análisis Económico</h3>
          <div class="quote-grid">
            <div class="quote-item">
              <span class="label">Ahorro Mensual:</span>
              <span class="value">${this.formatCurrency(design.monthly_savings)}</span>
            </div>
            <div class="quote-item">
              <span class="label">Ahorro Anual:</span>
              <span class="value">${this.formatCurrency(design.annual_savings)}</span>
            </div>
            <div class="quote-item">
              <span class="label">Retorno de Inversión:</span>
              <span class="value">${design.payback_years} años</span>
            </div>
            <div class="quote-item">
              <span class="label">ROI:</span>
              <span class="value">${design.roi_percentage}%</span>
            </div>
          </div>
        </div>

        <div class="quote-section">
          <h3><i class="fas fa-receipt"></i> Desglose de Costos</h3>
          <div class="quote-grid">
            <div class="quote-item">
              <span class="label">Paneles Solares:</span>
              <span class="value">${this.formatCurrency(design.panels_cost)}</span>
            </div>
            <div class="quote-item">
              <span class="label">Inversores:</span>
              <span class="value">${this.formatCurrency(design.inverters_cost)}</span>
            </div>
            <div class="quote-item">
              <span class="label">Sistema de Montaje:</span>
              <span class="value">${this.formatCurrency(design.mounting_cost)}</span>
            </div>
            <div class="quote-item">
              <span class="label">Instalación:</span>
              <span class="value">${this.formatCurrency(design.installation_cost)}</span>
            </div>
            <div class="quote-item">
              <span class="label">Total de Inversión:</span>
              <span class="value">${this.formatCurrency(design.total_investment)}</span>
            </div>
          </div>
        </div>

        ${design.battery_count > 0 ? `
        <div class="quote-section">
          <h3><i class="fas fa-battery-full"></i> Sistema de Baterías</h3>
          <div class="quote-grid">
            <div class="quote-item">
              <span class="label">Cantidad de Baterías:</span>
              <span class="value">${design.battery_count} unidades</span>
            </div>
            <div class="quote-item">
              <span class="label">Costo de Baterías:</span>
              <span class="value">${this.formatCurrency(design.batteries_cost)}</span>
            </div>
          </div>
        </div>
        ` : ''}

        <div class="quote-section">
          <h3><i class="fas fa-info-circle"></i> Información de la Cotización</h3>
          <p><strong>ID de Cotización:</strong> ${quote.quote_id}</p>
          <p><strong>Fecha de Generación:</strong> ${new Date(quote.created_at).toLocaleDateString('es-AR')}</p>
          <p><strong>Válida hasta:</strong> ${new Date(quote.valid_until).toLocaleDateString('es-AR')}</p>
          <p><strong>Cliente:</strong> ${quote.request.client_name || 'No especificado'}</p>
          <p><strong>Email:</strong> ${quote.request.client_email || 'No especificado'}</p>
          <p class="text-muted">Esta cotización es válida por 30 días y está sujeta a cambios en precios de materiales.</p>
        </div>
      </div>
    `;
    
    modal.style.display = 'flex';
  }
}

// Inicializar calculadora solar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
  window.solarCalculator = new SolarCalculator();
});

// Funciones globales para compatibilidad
function calculateSolarSystem() {
  if (window.solarCalculator) {
    window.solarCalculator.calculateSolarSystem();
  }
}

function performQuickEstimate() {
  if (window.solarCalculator) {
    window.solarCalculator.performQuickEstimate();
  }
}

function exportQuote() {
  if (window.solarCalculator) {
    window.solarCalculator.exportQuote();
  }
}

// Funciones globales para modales
function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.style.display = 'none';
  }
}

function downloadQuickEstimatePDF() {
  if (window.solarCalculator && window.solarCalculator.currentEstimation) {
    // Generar PDF de estimación rápida
    const estimation = window.solarCalculator.currentEstimation;
    const pdfData = {
      type: 'quick_estimate',
      data: estimation,
      generated_at: new Date().toISOString()
    };
    
    const dataStr = JSON.stringify(pdfData, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    
    const link = document.createElement('a');
    link.href = url;
    link.download = `estimacion_rapida_${new Date().toISOString().split('T')[0]}.json`;
    link.click();
    
    URL.revokeObjectURL(url);
    
    window.solarCalculator.showSuccess('Estimación descargada exitosamente');
  }
}

function downloadDetailedQuotePDF() {
  if (window.solarCalculator && window.solarCalculator.currentQuote) {
    // Generar PDF de cotización detallada
    const quote = window.solarCalculator.currentQuote;
    const pdfData = {
      type: 'detailed_quote',
      data: quote,
      generated_at: new Date().toISOString()
    };
    
    const dataStr = JSON.stringify(pdfData, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    
    const link = document.createElement('a');
    link.href = url;
    link.download = `cotizacion_detallada_${quote.quote_id}.json`;
    link.click();
    
    URL.revokeObjectURL(url);
    
    window.solarCalculator.showSuccess('Cotización descargada exitosamente');
  }
}

function requestDetailedQuote() {
  closeModal('quickEstimateModal');
  // Scroll al formulario de cotización completa
  const cotizadorSection = document.getElementById('cotizador');
  if (cotizadorSection) {
    cotizadorSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
}

function requestPersonalizedQuote() {
  closeModal('detailedQuoteModal');
  // Scroll al formulario de contacto
  const contactoSection = document.getElementById('contacto');
  if (contactoSection) {
    contactoSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
}

function submitClientInfo() {
  const form = document.getElementById('clientInfoForm');
  const formData = new FormData(form);
  
  const clientData = {
    name: formData.get('clientName'),
    email: formData.get('clientEmail'),
    phone: formData.get('clientPhone'),
    address: formData.get('clientAddress')
  };
  
  // Validar datos
  if (!clientData.name || !clientData.email) {
    alert('Por favor completa los campos obligatorios (Nombre y Email)');
    return;
  }
  
  // Guardar datos del cliente
  if (window.solarCalculator) {
    window.solarCalculator.clientInfo = clientData;
  }
  
  closeModal('clientInfoModal');
  
  // Continuar con la cotización
  if (window.solarCalculator) {
    window.solarCalculator.calculateSolarSystem();
  }
}

// Cerrar modal al hacer clic fuera del contenido
document.addEventListener('click', (e) => {
  if (e.target.classList.contains('modal')) {
    e.target.style.display = 'none';
  }
});

// Cerrar modal con tecla Escape
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
      if (modal.style.display === 'flex') {
        modal.style.display = 'none';
      }
    });
  }
});
