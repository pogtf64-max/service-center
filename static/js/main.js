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

// Order management functions
function viewOrder(orderId) {
    console.log('viewOrder called with ID:', orderId);
    // Загружаем данные заказа
    fetch(`/api/orders/${orderId}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showOrderDetailsModal(data.data);
            } else {
                showAlert('Ошибка при загрузке заказа: ' + data.message, 'danger');
            }
        })
        .catch(error => {
            console.error('Error loading order:', error);
            showAlert('Ошибка при загрузке заказа: ' + error.message, 'danger');
        });
}

function editOrder(orderId) {
    console.log('editOrder called with ID:', orderId);
    // Загружаем данные заказа для редактирования
    fetch(`/api/orders/${orderId}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                openEditOrderModal(data.data);
            } else {
                showAlert('Ошибка при загрузке заказа: ' + data.message, 'danger');
            }
        })
        .catch(error => {
            console.error('Error loading order for edit:', error);
            showAlert('Ошибка при загрузке заказа: ' + error.message, 'danger');
        });
}

function changeStatus(orderId) {
    console.log('changeStatus called with ID:', orderId);
    // Показываем модальное окно изменения статуса
    document.getElementById('changeStatusOrderId').value = orderId;
    const modal = new bootstrap.Modal(document.getElementById('changeStatusModal'));
    modal.show();
}

function changeOrderStatus(orderId, newStatus) {
    console.log('changeOrderStatus called with ID:', orderId, 'newStatus:', newStatus);
    // Обновляем статус заказа
    fetch(`/api/orders/${orderId}/status`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status: newStatus })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAlert('Статус заказа изменен!', 'success');
            setTimeout(() => location.reload(), 1000);
        } else {
            showAlert('Ошибка при изменении статуса: ' + data.message, 'danger');
        }
    })
    .catch(error => {
        console.error('Error changing order status:', error);
        showAlert('Ошибка при изменении статуса: ' + error.message, 'danger');
    });
}

function showAcceptanceAct(orderId) {
    console.log('showAcceptanceAct called with ID:', orderId);
    currentPrintOrderId = orderId;
    
    // Показываем модальное окно предварительного просмотра
    const previewDocumentType = document.getElementById('previewDocumentType');
    const previewDocumentTypeValue = document.getElementById('previewDocumentTypeValue');
    const documentPreviewContent = document.getElementById('documentPreviewContent');
    const modal = document.getElementById('documentPreviewModal');
    
    console.log('Elements found:', {
        previewDocumentType: !!previewDocumentType,
        previewDocumentTypeValue: !!previewDocumentTypeValue,
        documentPreviewContent: !!documentPreviewContent,
        modal: !!modal
    });
    
    if (previewDocumentType) {
        previewDocumentType.textContent = 'Акт приема';
    }
    if (previewDocumentTypeValue) {
        previewDocumentTypeValue.value = 'acceptance_act';
    }
    
    // Показываем загрузку
    if (documentPreviewContent) {
        documentPreviewContent.innerHTML = `
            <div class="text-center py-4">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Загрузка...</span>
                </div>
                <p class="mt-2">Загрузка акта приема...</p>
            </div>
        `;
    }
    
    // Показываем модальное окно
    const modal = document.getElementById('documentPreviewModal');
    if (modal) {
        new bootstrap.Modal(modal).show();
    }
    
    // Загружаем данные заказа
    fetch(`/api/orders/${orderId}`)
        .then(response => response.json())
        .then(orderData => {
            if (orderData.error) {
                if (documentPreviewContent) {
                    documentPreviewContent.innerHTML = `
                        <div class="alert alert-danger">
                            <i class="bi bi-exclamation-triangle"></i>
                            Ошибка загрузки данных заказа: ${orderData.error}
                        </div>
                    `;
                }
                return;
            }
            
            // Генерируем акт приема
            const acceptanceActHtml = generateAcceptanceAct(orderData);
            if (documentPreviewContent) {
                documentPreviewContent.innerHTML = acceptanceActHtml;
            }
        })
        .catch(error => {
            console.error('Error loading order for acceptance act:', error);
            if (documentPreviewContent) {
                documentPreviewContent.innerHTML = `
                    <div class="alert alert-danger">
                        <i class="bi bi-exclamation-triangle"></i>
                        Ошибка загрузки данных заказа: ${error.message}
                    </div>
                `;
            }
        });
}

function takeToWork(orderId) {
    console.log('takeToWork called with ID:', orderId);
    // Обновляем статус заказа на "В работе"
    changeOrderStatus(orderId, 'in_progress');
}

// Modal functions
function showOrderDetailsModal(orderData) {
    // Создать и показать модальное окно с деталями заказа
    const modalHtml = `
        <div class="modal fade" id="orderDetailsModal" tabindex="-1">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Заказ #${orderData.id}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <p><strong>Клиент:</strong> ${orderData.client_name || 'Не указан'}</p>
                        <p><strong>Устройство:</strong> ${orderData.device_type || 'Не указано'}</p>
                        <p><strong>Проблема:</strong> ${orderData.problem_description || 'Не указана'}</p>
                        <p><strong>Статус:</strong> ${orderData.status || 'Не указан'}</p>
                        <p><strong>Стоимость:</strong> ${orderData.cost_estimate || 0} ₽</p>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Удалить существующее модальное окно
    const existingModal = document.getElementById('orderDetailsModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    // Добавить новое модальное окно
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    
    // Показать модальное окно
    const modal = new bootstrap.Modal(document.getElementById('orderDetailsModal'));
    modal.show();
}

function openEditOrderModal(orderData) {
    // Заполнить форму редактирования заказа
    showAlert('Функция редактирования заказа будет добавлена в следующей версии', 'info');
}

function showAcceptanceActModal(actData) {
    // Создаем модальное окно для акта приема
    const modalHtml = `
        <div class="modal fade" id="acceptanceActModal" tabindex="-1">
            <div class="modal-dialog modal-xl">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            <i class="bi bi-file-text"></i> Акт приема оборудования в ремонт
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body" style="max-height: 80vh; overflow-y: auto;">
                        <div id="acceptanceActContent">
                            ${generateAcceptanceAct(actData)}
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                        <button type="button" class="btn btn-primary" onclick="printAcceptanceAct()">
                            <i class="bi bi-printer"></i> Печать
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Удаляем существующее модальное окно
    const existingModal = document.getElementById('acceptanceActModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    // Добавляем новое модальное окно
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    
    // Показываем модальное окно
    const modal = new bootstrap.Modal(document.getElementById('acceptanceActModal'));
    modal.show();
}

// Генерация АКТА ПРИЕМА
function generateAcceptanceAct(data) {
    const currentDate = new Date().toLocaleDateString('ru-RU');
    const currentTime = new Date().toLocaleTimeString('ru-RU', {hour: '2-digit', minute: '2-digit'});
    
    return `
        <html>
        <head>
            <title>Акт приема #${data.id}</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .header { text-align: center; margin-bottom: 30px; }
                .title { font-size: 18px; font-weight: bold; margin-bottom: 10px; }
                .info { margin-bottom: 20px; }
                .info-row { margin-bottom: 10px; }
                .label { font-weight: bold; display: inline-block; width: 150px; }
                .signature { margin-top: 50px; }
                .signature-row { margin-bottom: 20px; }
                .signature-line { border-bottom: 1px solid black; width: 200px; display: inline-block; margin-left: 10px; }
            </style>
        </head>
        <body>
            <div class="header">
                <div class="title">АКТ ПРИЕМА ОБОРУДОВАНИЯ В РЕМОНТ</div>
                <div>№ ${data.id} от ${currentDate}</div>
            </div>
            
            <div class="info">
                <div class="info-row">
                    <span class="label">Клиент:</span> ${data.client_name || 'Не указан'}
                </div>
                <div class="info-row">
                    <span class="label">Телефон:</span> ${data.client_phone || 'Не указан'}
                </div>
                <div class="info-row">
                    <span class="label">Адрес:</span> ${data.client_address || 'Не указан'}
                </div>
                <div class="info-row">
                    <span class="label">Устройство:</span> ${data.device_type || 'Не указано'}
                </div>
                <div class="info-row">
                    <span class="label">Модель:</span> ${data.device_model || 'Не указана'}
                </div>
                <div class="info-row">
                    <span class="label">Серийный номер:</span> ${data.device_serial_number || 'Не указан'}
                </div>
                <div class="info-row">
                    <span class="label">Описание проблемы:</span> ${data.problem_description || 'Не указана'}
                </div>
                <div class="info-row">
                    <span class="label">Внешнее состояние:</span> ${data.device_condition || 'Не указано'}
                </div>
                <div class="info-row">
                    <span class="label">Комплектность:</span> ${data.completeness || 'Не указана'}
                </div>
            </div>
            
            <div class="signature">
                <div class="signature-row">
                    <span>Клиент:</span>
                    <span class="signature-line"></span>
                    <span style="margin-left: 20px;">Дата: ${currentDate}</span>
                </div>
                <div class="signature-row">
                    <span>Принял:</span>
                    <span class="signature-line"></span>
                    <span style="margin-left: 20px;">Дата: ${currentDate}</span>
                </div>
            </div>
        </body>
        </html>
    `;
}

// Глобальная переменная для текущего заказа
let currentPrintOrderId = null;

// Export functions for global use
window.createClient = createClient;
window.createOrder = createOrder;
window.createPart = createPart;
window.showAlert = showAlert;
window.customAlert = customAlert;
window.customConfirm = customConfirm;
window.apiRequest = apiRequest;
window.openDevTools = openDevTools;
window.viewOrder = viewOrder;
window.editOrder = editOrder;
window.changeStatus = changeStatus;
window.changeOrderStatus = changeOrderStatus;
window.showAcceptanceAct = showAcceptanceAct;
window.takeToWork = takeToWork;
