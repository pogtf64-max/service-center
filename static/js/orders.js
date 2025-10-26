// Orders page specific JavaScript functions

// Функция подсчета общей стоимости АВР для заказа
function calculateOrderWorkReportsTotal(orderId) {
    return new Promise((resolve) => {
        try {
            const workReports = JSON.parse(localStorage.getItem(`workReports_${orderId}`) || '[]');
            const total = workReports.reduce((sum, report) => sum + (parseFloat(report.cost) || 0), 0);
            resolve(total);
        } catch (error) {
            console.error('Ошибка при подсчете суммы АВР:', error);
            return Promise.resolve(0);
        }
    });
}

// Функция обновления стоимости в карточке заказа
function updateOrderCost(orderId) {
    calculateOrderWorkReportsTotal(orderId).then(total => {
        const costElement = document.getElementById(`order-cost-${orderId}`);
        if (costElement && total > 0) {
            costElement.textContent = `${total.toFixed(2)} ₽`;
            costElement.style.color = '#28a745'; // Зеленый цвет для АВР
        }
    });
}

// Функция обновления стоимости для всех заказов на странице
function updateAllOrdersCost() {
    // Находим все карточки заказов и обновляем их стоимость
    const orderCards = document.querySelectorAll('[id^="order-cost-"]');
    orderCards.forEach(card => {
        const orderId = card.id.replace('order-cost-', '');
        updateOrderCost(orderId);
    });
}

// Функция показа уведомлений
function showNotification(title, message, type) {
    // Создаем уведомление
    const notification = document.createElement('div');
    notification.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        <strong>${title}</strong> ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Автоматически удаляем через 5 секунд
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    // Обновляем стоимость всех заказов при загрузке страницы
    updateAllOrdersCost();
    
    // Настраиваем обработчики для модальных окон
    const documentPreviewModal = document.getElementById('documentPreviewModal');
    if (documentPreviewModal) {
        documentPreviewModal.addEventListener('hidden.bs.modal', function() {
            // Очищаем содержимое при закрытии модального окна
            const content = document.getElementById('documentPreviewContent');
            if (content) {
                content.innerHTML = '';
            }
        });
    }
});
