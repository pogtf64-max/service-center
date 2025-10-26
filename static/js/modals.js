/**
 * Кастомные модальные окна для замены стандартных alert, confirm, prompt
 */

// Переменные для хранения промисов
let currentModalPromise = null;
let currentModalResolve = null;

/**
 * Кастомный confirm
 * @param {string} message - Сообщение
 * @param {string} title - Заголовок (опционально)
 * @returns {Promise<boolean>} - true если подтверждено, false если отменено
 */
function customConfirm(message, title = 'Подтвердите действие') {
    return new Promise((resolve) => {
        const modal = document.getElementById('customModal');
        const modalLabel = document.getElementById('customModalLabel');
        const modalMessage = modal.querySelector('.modal-message');
        const confirmBtn = modal.querySelector('.custom-btn-confirm');
        const cancelBtn = modal.querySelector('.custom-btn-cancel');
        
        // Устанавливаем содержимое
        modalLabel.innerHTML = `<i class="bi bi-question-circle"></i> ${title}`;
        modalMessage.textContent = message;
        
        // Обработчики событий
        const handleConfirm = () => {
            bootstrap.Modal.getInstance(modal).hide();
            resolve(true);
            cleanup();
        };
        
        const handleCancel = () => {
            bootstrap.Modal.getInstance(modal).hide();
            resolve(false);
            cleanup();
        };
        
        const cleanup = () => {
            confirmBtn.removeEventListener('click', handleConfirm);
            cancelBtn.removeEventListener('click', handleCancel);
            modal.removeEventListener('hidden.bs.modal', handleCancel);
        };
        
        // Добавляем обработчики
        confirmBtn.addEventListener('click', handleConfirm);
        cancelBtn.addEventListener('click', handleCancel);
        modal.addEventListener('hidden.bs.modal', handleCancel);
        
        // Показываем модальное окно
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
    });
}

/**
 * Кастомный alert
 * @param {string} message - Сообщение
 * @param {string} title - Заголовок (опционально)
 * @param {string} type - Тип уведомления (info, success, warning, error)
 * @returns {Promise<void>}
 */
function customAlert(message, title = 'Уведомление', type = 'info') {
    return new Promise((resolve) => {
        const modal = document.getElementById('alertModal');
        const modalLabel = document.getElementById('alertModalLabel');
        const modalMessage = modal.querySelector('.modal-message');
        const modalIcon = modal.querySelector('.modal-icon i');
        const okBtn = modal.querySelector('.custom-btn-ok');
        
        // Устанавливаем содержимое в зависимости от типа
        let iconClass, iconColor, btnClass;
        
        switch (type) {
            case 'success':
                iconClass = 'bi-check-circle-fill';
                iconColor = '#10b981';
                btnClass = 'custom-btn-ok';
                break;
            case 'warning':
                iconClass = 'bi-exclamation-triangle-fill';
                iconColor = '#f59e0b';
                btnClass = 'custom-btn-ok';
                break;
            case 'error':
                iconClass = 'bi-x-circle-fill';
                iconColor = '#ef4444';
                btnClass = 'custom-btn-ok';
                break;
            default:
                iconClass = 'bi-info-circle-fill';
                iconColor = '#60a5fa';
                btnClass = 'custom-btn-ok';
        }
        
        modalLabel.innerHTML = `<i class="bi bi-${iconClass}"></i> ${title}`;
        modalMessage.textContent = message;
        modalIcon.className = `bi ${iconClass}`;
        modalIcon.style.color = iconColor;
        
        // Обработчик закрытия
        const handleClose = () => {
            bootstrap.Modal.getInstance(modal).hide();
            resolve();
            cleanup();
        };
        
        const cleanup = () => {
            okBtn.removeEventListener('click', handleClose);
            modal.removeEventListener('hidden.bs.modal', handleClose);
        };
        
        // Добавляем обработчики
        okBtn.addEventListener('click', handleClose);
        modal.addEventListener('hidden.bs.modal', handleClose);
        
        // Показываем модальное окно
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
    });
}

/**
 * Кастомный prompt
 * @param {string} message - Сообщение
 * @param {string} defaultValue - Значение по умолчанию
 * @param {string} title - Заголовок (опционально)
 * @returns {Promise<string|null>} - Введенное значение или null если отменено
 */
function customPrompt(message, defaultValue = '', title = 'Введите данные') {
    return new Promise((resolve) => {
        const modal = document.getElementById('promptModal');
        const modalLabel = document.getElementById('promptModalLabel');
        const modalMessage = modal.querySelector('.modal-message');
        const input = modal.querySelector('.custom-prompt-input');
        const confirmBtn = modal.querySelector('.custom-btn-confirm');
        const cancelBtn = modal.querySelector('.custom-btn-cancel');
        
        // Устанавливаем содержимое
        modalLabel.innerHTML = `<i class="bi bi-pencil-square"></i> ${title}`;
        modalMessage.textContent = message;
        input.value = defaultValue;
        
        // Фокус на поле ввода
        setTimeout(() => {
            input.focus();
            input.select();
        }, 300);
        
        // Обработчики событий
        const handleConfirm = () => {
            const value = input.value.trim();
            bootstrap.Modal.getInstance(modal).hide();
            resolve(value);
            cleanup();
        };
        
        const handleCancel = () => {
            bootstrap.Modal.getInstance(modal).hide();
            resolve(null);
            cleanup();
        };
        
        const handleKeyPress = (e) => {
            if (e.key === 'Enter') {
                handleConfirm();
            } else if (e.key === 'Escape') {
                handleCancel();
            }
        };
        
        const cleanup = () => {
            confirmBtn.removeEventListener('click', handleConfirm);
            cancelBtn.removeEventListener('click', handleCancel);
            input.removeEventListener('keypress', handleKeyPress);
            modal.removeEventListener('hidden.bs.modal', handleCancel);
        };
        
        // Добавляем обработчики
        confirmBtn.addEventListener('click', handleConfirm);
        cancelBtn.addEventListener('click', handleCancel);
        input.addEventListener('keypress', handleKeyPress);
        modal.addEventListener('hidden.bs.modal', handleCancel);
        
        // Показываем модальное окно
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
    });
}

/**
 * Замена стандартных функций браузера
 */
function replaceNativeModals() {
    // Заменяем window.confirm
    window.originalConfirm = window.confirm;
    window.confirm = customConfirm;
    
    // Заменяем window.alert
    window.originalAlert = window.alert;
    window.alert = customAlert;
    
    // Заменяем window.prompt
    window.originalPrompt = window.prompt;
    window.prompt = customPrompt;
}

/**
 * Восстановление стандартных функций
 */
function restoreNativeModals() {
    if (window.originalConfirm) window.confirm = window.originalConfirm;
    if (window.originalAlert) window.alert = window.originalAlert;
    if (window.originalPrompt) window.prompt = window.originalPrompt;
}

// Экспорт функций для использования
window.customConfirm = customConfirm;
window.customAlert = customAlert;
window.customPrompt = customPrompt;
window.replaceNativeModals = replaceNativeModals;
window.restoreNativeModals = restoreNativeModals;

// Автоматическая замена при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    // Ждем загрузки Bootstrap
    if (typeof bootstrap !== 'undefined') {
        replaceNativeModals();
    } else {
        // Если Bootstrap еще не загружен, ждем
        setTimeout(replaceNativeModals, 100);
    }
});


