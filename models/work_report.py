"""
Модель акта выполненных работ (АВР)
"""
from models.database import db
from datetime import datetime
import json

class WorkReport(db.Model):
    """Модель акта выполненных работ"""
    __tablename__ = 'work_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=True)  # Может быть привязан к заказу
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Кто создал АВР
    
    # Даты
    work_start_date = db.Column(db.Date, nullable=False)
    work_end_date = db.Column(db.Date, nullable=False)
    
    # Описание работ
    work_description = db.Column(db.Text, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    
    # Финансы
    total_cost = db.Column(db.Float, nullable=False, default=0.0)
    
    # Гарантия
    warranty_period = db.Column(db.Integer, default=30)  # в днях
    
    # Запчасти и услуги (храним в JSON)
    parts = db.Column(db.Text, nullable=True)  # JSON массив
    services = db.Column(db.Text, nullable=True)  # JSON массив
    
    # Метаданные
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    order = db.relationship('Order', backref=db.backref('work_reports', lazy=True))
    device = db.relationship('Device', backref=db.backref('work_reports', lazy=True))
    user = db.relationship('User', backref=db.backref('work_reports', lazy=True))
    
    def __repr__(self):
        return f'<WorkReport {self.id} Device:{self.device_id} Order:{self.order_id}>'
    
    def get_parts(self):
        """Получить список запчастей из JSON"""
        try:
            return json.loads(self.parts) if self.parts else []
        except:
            return []
    
    def get_services(self):
        """Получить список услуг из JSON"""
        try:
            return json.loads(self.services) if self.services else []
        except:
            return []
    
    def set_parts(self, parts_list):
        """Установить список запчастей (сохранить в JSON)"""
        self.parts = json.dumps(parts_list, ensure_ascii=False) if parts_list else None
    
    def set_services(self, services_list):
        """Установить список услуг (сохранить в JSON)"""
        self.services = json.dumps(services_list, ensure_ascii=False) if services_list else None
    
    def to_dict(self):
        """Преобразование в словарь для API"""
        return {
            'id': self.id,
            'order_id': self.order_id,
            'device_id': self.device_id,
            'user_id': self.user_id,
            'user_name': self.user.full_name if self.user else 'Неизвестно',
            'work_start_date': self.work_start_date.isoformat() if self.work_start_date else None,
            'work_end_date': self.work_end_date.isoformat() if self.work_end_date else None,
            'work_description': self.work_description,
            'notes': self.notes,
            'total_cost': self.total_cost,
            'warranty_period': self.warranty_period,
            'parts': self.get_parts(),
            'services': self.get_services(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

