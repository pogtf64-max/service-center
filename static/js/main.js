// Main JavaScript for Service Center

document.addEventListener('DOMContentLoaded', function() {
    console.log('Main.js loaded, initializing...');
    
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Add loading states to buttons (except registration and login forms)
    const submitButtons = document.querySelectorAll('button[type="submit"]');
    console.log('Found submit buttons:', submitButtons.length);
    
    submitButtons.forEach(function(button) {
        // Skip loading state for registration, login, and service selection forms
        if (button.closest('#registerForm') || 
            button.closest('form[action*="register"]') ||
            button.closest('form[action*="login"]') ||
            button.closest('form[action*="join"]') ||
            button.closest('form[action*="select"]') ||
            button.closest('form[action*="services/add"]')) {
            console.log('Skipping loading state for form:', button.closest('form'));
            return;
        }
        
        button.addEventListener('click', function(e) {
            console.log('Button clicked:', this);
            console.log('Form action:', this.form.action);
            console.log('Form method:', this.form.method);
            
            if (this.form.checkValidity()) {
                console.log('Form is valid, adding loading state');
                this.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span> Загрузка...';
                // НЕ блокируем кнопку, чтобы форма могла отправиться
                // this.disabled = true;
                
                // Add form submit listener to track submission
                this.form.addEventListener('submit', function(e) {
                    console.log('Form submitting...');
                });
                
                // Allow form to submit naturally
                return true;
            } else {
                console.log('Form is not valid');
            }
        });
    });

    // Table search functionality
    if (document.getElementById('clientsTable')) {
        initTableSearch('clientsTable');
    }

    // Автозаполнение услуг для кассы
    initCashServiceAutocomplete();
    if (document.getElementById('ordersTable')) {
        initTableSearch('ordersTable');
    }
    if (document.getElementById('partsTable')) {
        initTableSearch('partsTable');
    }

    // Initialize charts if on dashboard
    if (document.getElementById('dashboard')) {
        initDashboardCharts();
    }
});

// Table search functionality
function initTableSearch(tableId) {
    const table = document.getElementById(tableId);
    if (!table) return;

    // Create search input
    const searchContainer = document.createElement('div');
    searchContainer.className = 'mb-3';
    searchContainer.innerHTML = `
        <div class="input-group">
            <span class="input-group-text">
                <i class="bi bi-search"></i>
            </span>
            <input type="text" class="form-control" placeholder="Поиск..." id="search-${tableId}">
        </div>
    `;

    // Insert search before table
    table.parentNode.insertBefore(searchContainer, table);

    // Add search functionality
    const searchInput = document.getElementById(`search-${tableId}`);
    searchInput.addEventListener('keyup', function() {
        const searchTerm = this.value.toLowerCase();
        const rows = table.getElementsByTagName('tbody')[0].getElementsByTagName('tr');

        for (let i = 0; i < rows.length; i++) {
            const row = rows[i];
            const text = row.textContent.toLowerCase();
            
            if (text.includes(searchTerm)) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        }
    });
}

// Dashboard charts
function initDashboardCharts() {
    // This would initialize Chart.js charts if needed
    console.log('Dashboard charts initialized');
}

// API Helper functions
async function apiRequest(url, options = {}) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    const mergedOptions = { ...defaultOptions, ...options };

    try {
        const response = await fetch(url, mergedOptions);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.message || 'Ошибка сервера');
        }
        
        return data;
    } catch (error) {
        console.error('API Error:', error);
        showAlert('Ошибка: ' + error.message, 'danger');
        throw error;
    }
}

// Show alert function
function showAlert(message, type = 'info') {
    const alertContainer = document.createElement('div');
    alertContainer.innerHTML = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;

    // Insert at the top of main content
    const main = document.querySelector('main');
    if (main) {
        main.insertBefore(alertContainer, main.firstChild);
    }

    // Auto-hide after 5 seconds
    setTimeout(() => {
        const alert = alertContainer.querySelector('.alert');
        if (alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }
    }, 5000);
}

// Custom alert function (alias for showAlert)
function customAlert(message, title = '', type = 'info') {
    showAlert(message, type);
}

// Client management functions
async function createClient() {
    const form = document.getElementById('newClientForm');
    const formData = new FormData(form);
    
    const clientData = {
        name: formData.get('clientName') || document.getElementById('clientName').value,
        phone: formData.get('clientPhone') || document.getElementById('clientPhone').value,
        email: formData.get('clientEmail') || document.getElementById('clientEmail').value,
        address: formData.get('clientAddress') || document.getElementById('clientAddress').value,
        notes: formData.get('clientNotes') || document.getElementById('clientNotes').value
    };

    try {
        const result = await apiRequest('/api/clients', {
            method: 'POST',
            body: JSON.stringify(clientData)
        });

        if (result.success) {
            showAlert('Клиент успешно добавлен!', 'success');
            setTimeout(() => location.reload(), 1000);
        }
    } catch (error) {
        showAlert('Ошибка при создании клиента: ' + error.message, 'danger');
    }
}

// Toggle client fields based on client type
function toggleClientFields() {
    const clientType = document.getElementById('clientType')?.value;
    const individualFields = document.getElementById('individualFields');
    const legalFields = document.getElementById('legalFields');
    
    if (individualFields && legalFields) {
        if (clientType === 'individual') {
            individualFields.style.display = 'block';
            legalFields.style.display = 'none';
        } else if (clientType === 'legal') {
            individualFields.style.display = 'none';
            legalFields.style.display = 'block';
        } else {
            individualFields.style.display = 'none';
            legalFields.style.display = 'none';
        }
    }
}

// Order management functions
async function createOrder() {
    const form = document.getElementById('newOrderForm');
    if (!form) {
        console.error('Form not found');
        return;
    }
    
    const orderData = {
        client_type: document.getElementById('clientType')?.value || '',
        client_name: document.getElementById('clientName')?.value || '',
        client_phone: document.getElementById('clientPhone')?.value || '',
        client_address: document.getElementById('clientAddress')?.value || '',
        client_email: document.getElementById('clientEmail')?.value || '',
        organization_name: document.getElementById('organizationName')?.value || '',
        inn: document.getElementById('inn')?.value || '',
        device_type: document.getElementById('deviceType')?.value || '',
        device_brand: document.getElementById('deviceBrand')?.value || '',
        device_model: document.getElementById('deviceModel')?.value || '',
        device_serial_number: document.getElementById('deviceSerialNumber')?.value || '',
        device_imei: document.getElementById('deviceImei')?.value || '',
        device_condition: document.getElementById('deviceCondition')?.value || '',
        problem_description: document.getElementById('problemDescription')?.value || '',
        completeness: document.getElementById('completeness')?.value || ''
    };

    try {
        const result = await apiRequest('/api/orders', {
            method: 'POST',
            body: JSON.stringify(orderData)
        });

        if (result.success) {
            showAlert('Заказ успешно создан!', 'success');
            setTimeout(() => location.reload(), 1000);
        }
    } catch (error) {
        showAlert('Ошибка при создании заказа: ' + error.message, 'danger');
    }
}

// Part management functions
async function createPart() {
    const partData = {
        name: document.getElementById('partName').value,
        article: document.getElementById('partArticle').value,
        quantity: parseInt(document.getElementById('partQuantity').value) || 0,
        price: parseFloat(document.getElementById('partPrice').value),
        supplier: document.getElementById('partSupplier').value,
        description: document.getElementById('partDescription').value
    };

    try {
        const result = await apiRequest('/api/parts', {
            method: 'POST',
            body: JSON.stringify(partData)
        });

        if (result.success) {
            showAlert('Запчасть успешно добавлена!', 'success');
            setTimeout(() => location.reload(), 1000);
        }
    } catch (error) {
        showAlert('Ошибка при создании запчасти: ' + error.message, 'danger');
    }
}

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('ru-RU', {
        style: 'currency',
        currency: 'RUB'
    }).format(amount);
}

function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('ru-RU');
}

// DevTools functionality
function openDevTools() {
    window.open('/devtools', '_blank', 'width=1200,height=800,scrollbars=yes,resizable=yes');
}

// Add DevTools shortcut (Ctrl+Shift+D)
document.addEventListener('keydown', function(e) {
    if (e.ctrlKey && e.shiftKey && e.key === 'D') {
        e.preventDefault();
        openDevTools();
    }
});

// Add DevTools button to admin users
document.addEventListener('DOMContentLoaded', function() {
    // Check if user is admin (this would need to be set by the server)
    const isAdmin = document.body.dataset.userRole === 'admin';
    
    if (isAdmin) {
        // Add DevTools button to the page
        const devToolsButton = document.createElement('button');
        devToolsButton.className = 'btn btn-outline-secondary btn-sm position-fixed';
        devToolsButton.style.cssText = 'bottom: 20px; right: 20px; z-index: 1000;';
        devToolsButton.innerHTML = '<i class="bi bi-tools"></i> DevTools';
        devToolsButton.title = 'Открыть DevTools (Ctrl+Shift+D)';
        devToolsButton.onclick = openDevTools;
        
        document.body.appendChild(devToolsButton);
    }
});

// Custom confirm dialog
function customConfirm(message, title = 'Подтверждение') {
    return new Promise((resolve) => {
        // Create modal HTML
        const modalHtml = `
            <div class="modal fade" id="customConfirmModal" tabindex="-1">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">${title}</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <p>${message}</p>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
                            <button type="button" class="btn btn-primary" id="confirmBtn">Подтвердить</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Add modal to body
        document.body.insertAdjacentHTML('beforeend', modalHtml);
        
        const modal = new bootstrap.Modal(document.getElementById('customConfirmModal'));
        
        // Handle confirm button click
        document.getElementById('confirmBtn').addEventListener('click', () => {
            modal.hide();
            resolve(true);
        });
        
        // Handle cancel or close
        document.getElementById('customConfirmModal').addEventListener('hidden.bs.modal', () => {
            document.getElementById('customConfirmModal').remove();
            resolve(false);
        });
        
        modal.show();
    });
}

// Функция автозаполнения услуг для кассы
function initCashServiceAutocomplete() {
    const descriptionInput = document.getElementById('addDescription');
    if (!descriptionInput) return;

    let services = [];
    let currentSuggestions = [];

    // Загружаем список услуг
    fetch('/api/services/autocomplete')
        .then(response => response.json())
        .then(data => {
            services = data.services || [];
            console.log('Loaded services for autocomplete:', services);
        })
        .catch(error => {
            console.error('Error loading services:', error);
        });

    // Создаем контейнер для подсказок
    const suggestionsContainer = document.createElement('div');
    suggestionsContainer.id = 'service-suggestions';
    suggestionsContainer.style.cssText = `
        position: absolute;
        background: white;
        border: 1px solid #ccc;
        border-radius: 4px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        max-height: 200px;
        overflow-y: auto;
        z-index: 1000;
        display: none;
        width: 100%;
    `;

    // Добавляем контейнер после поля ввода
    descriptionInput.parentNode.style.position = 'relative';
    descriptionInput.parentNode.appendChild(suggestionsContainer);

    // Функция показа подсказок
    function showSuggestions() {
        if (currentSuggestions.length === 0) {
            suggestionsContainer.style.display = 'none';
            return;
        }

        suggestionsContainer.innerHTML = '';
        currentSuggestions.forEach((service, index) => {
            const item = document.createElement('div');
            item.style.cssText = `
                padding: 8px 12px;
                cursor: pointer;
                border-bottom: 1px solid #eee;
            `;
            item.textContent = service;
            item.addEventListener('mouseenter', () => {
                item.style.backgroundColor = '#f5f5f5';
            });
            item.addEventListener('mouseleave', () => {
                item.style.backgroundColor = 'white';
            });
            item.addEventListener('click', () => {
                descriptionInput.value = service;
                suggestionsContainer.style.display = 'none';
                descriptionInput.focus();
            });
            suggestionsContainer.appendChild(item);
        });

        suggestionsContainer.style.display = 'block';
    }

    // Функция скрытия подсказок
    function hideSuggestions() {
        suggestionsContainer.style.display = 'none';
    }

    // Обработчик ввода
    descriptionInput.addEventListener('input', function() {
        const value = this.value.toLowerCase().trim();
        
        if (value.length < 2) {
            hideSuggestions();
            return;
        }

        // Фильтруем услуги по введенному тексту
        currentSuggestions = services.filter(service => 
            service.toLowerCase().includes(value)
        );

        showSuggestions();
    });

    // Скрываем подсказки при потере фокуса
    descriptionInput.addEventListener('blur', function() {
        setTimeout(hideSuggestions, 200);
    });

    // Показываем подсказки при фокусе, если есть текст
    descriptionInput.addEventListener('focus', function() {
        const value = this.value.toLowerCase().trim();
        if (value.length >= 2) {
            currentSuggestions = services.filter(service => 
                service.toLowerCase().includes(value)
            );
            showSuggestions();
        }
    });
}

// Export functions for global use
window.createClient = createClient;
window.createOrder = createOrder;
window.createPart = createPart;
window.showAlert = showAlert;
window.customAlert = customAlert;
window.customConfirm = customConfirm;
window.apiRequest = apiRequest;
window.openDevTools = openDevTools;
