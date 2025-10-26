"""
Модель кассы
"""
from datetime import datetime
from .database import db

class CashRegister(db.Model):
    """Модель кассы для отслеживания доходов"""
    __tablename__ = 'cash_register'
    
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Кто выполнил операцию
    amount = db.Column(db.Float, nullable=False)  # Сумма поступления
    description = db.Column(db.String(200), nullable=False)  # Описание операции
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Связи
    service = db.relationship('Service', backref='cash_entries')
    order = db.relationship('Order', backref='cash_entry')
    user = db.relationship('User', backref='cash_operations')
    
    def __repr__(self):
        return f'<CashRegister {self.id}: {self.amount}₽>'
    
    def to_dict(self):
        """Преобразование в словарь для API"""
        return {
            'id': self.id,
            'service_id': self.service_id,
            'order_id': self.order_id,
            'user_id': self.user_id,
            'amount': self.amount,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'user_name': f"{self.user.first_name} {self.user.last_name}" if self.user else "Неизвестно"
        }
    
    @staticmethod
    def get_total_amount(service_id):
        """Получить общую сумму в кассе для сервиса"""
        total = db.session.query(db.func.sum(CashRegister.amount))\
                          .filter_by(service_id=service_id)\
                          .scalar()
        return total or 0.0
    
    @staticmethod
    def get_today_amount(service_id):
        """Получить сумму поступлений за сегодня"""
        today = datetime.utcnow().date()
        total = db.session.query(db.func.sum(CashRegister.amount))\
                          .filter_by(service_id=service_id)\
                          .filter(db.func.date(CashRegister.created_at) == today)\
                          .scalar()
        return total or 0.0
