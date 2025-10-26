"""
Модель истории изменений статусов заказов
"""
from models.database import db
from datetime import datetime

class OrderStatusHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    old_status = db.Column(db.String(30), nullable=True)
    new_status = db.Column(db.String(30), nullable=False)
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    order = db.relationship('Order', backref=db.backref('status_history', lazy=True))
    user = db.relationship('User', backref=db.backref('status_changes', lazy=True))

    def __repr__(self):
        return f'<OrderStatusHistory {self.id} Order:{self.order_id} NewStatus:{self.new_status}>'

    @staticmethod
    def get_status_display(status_key):
        """Получить отображаемое название статуса на русском для статических вызовов"""
        status_map = {
            'received': 'Принят',
            'diagnosis': 'Диагностика',
            'in_work': 'В работе',
            'requires_approval': 'Требуется согласование',
            'approved': 'Согласовано',
            'ready': 'Готов к выдаче',
            'parts_order': 'Заказ ЗИП',
            'parts_ordered': 'ЗИП заказан',
            'parts_issued': 'ЗИП выдан',
            'completed': 'Выдано',
            'rejected': 'Отказ от ремонта'
        }
        return status_map.get(status_key, status_key)

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'user_id': self.user_id,
            'user_name': self.user.full_name if self.user else 'Неизвестно',
            'old_status': self.old_status,
            'new_status': self.new_status,
            'comment': self.comment,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }