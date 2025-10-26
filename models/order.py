"""
Модель заказа
"""
from datetime import datetime
from .database import db

class Order(db.Model):
    """Модель заказа на ремонт"""
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    master_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Статусы заказа
    status = db.Column(db.String(30), nullable=False, default='received')
    
    # Даты
    date_received = db.Column(db.DateTime, default=datetime.utcnow)
    date_diagnosis = db.Column(db.DateTime)
    date_repair_start = db.Column(db.DateTime)
    date_completed = db.Column(db.DateTime)
    date_ready = db.Column(db.DateTime)
    
    # Описание работ
    problem_description = db.Column(db.Text, nullable=False)
    diagnosis = db.Column(db.Text)
    repair_description = db.Column(db.Text)
    work_performed = db.Column(db.Text)
    
    # Финансы
    cost_estimate = db.Column(db.Float, default=0.0)
    final_cost = db.Column(db.Float, default=0.0)
    prepayment = db.Column(db.Float, default=0.0)
    diagnosis_cost = db.Column(db.Float, default=500.0)  # Сумма диагностики для отказов от ремонта
    
    # Гарантия
    warranty_months = db.Column(db.Integer, default=3)
    warranty_until = db.Column(db.DateTime)
    
    # Дополнительно
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Order {self.id}>'
    
    def get_status_display(self):
        """Получить отображаемое название статуса на русском"""
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
        return status_map.get(self.status, self.status)
    
    def get_work_reports_total(self):
        """Получить общую сумму всех АВР для этого заказа"""
        import json
        
        # Получаем все АВР из localStorage (это будет сделано на фронтенде)
        # Здесь возвращаем 0, так как АВР хранятся в localStorage на клиенте
        return 0.0
    
    def to_dict(self):
        """Преобразование в словарь для API"""
        return {
            'id': self.id,
            'device_id': self.device_id,
            'client_id': self.client_id,
            'master_id': self.master_id,
            'status': self.status,
            'status_display': self.get_status_display(),
            'date_received': self.date_received.isoformat() if self.date_received else None,
            'date_diagnosis': self.date_diagnosis.isoformat() if self.date_diagnosis else None,
            'date_repair_start': self.date_repair_start.isoformat() if self.date_repair_start else None,
            'date_completed': self.date_completed.isoformat() if self.date_completed else None,
            'date_ready': self.date_ready.isoformat() if self.date_ready else None,
            'problem_description': self.problem_description,
            'diagnosis': self.diagnosis,
            'repair_description': self.repair_description,
            'work_performed': self.work_performed,
            'cost_estimate': self.cost_estimate,
            'final_cost': self.final_cost,
            'prepayment': self.prepayment,
            'diagnosis_cost': self.diagnosis_cost,
            'warranty_months': self.warranty_months,
            'warranty_until': self.warranty_until.isoformat() if self.warranty_until else None,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            # Добавляем связанные объекты
            'client': self.client.to_dict() if self.client else None,
            'device': self.device.to_dict() if self.device else None,
            'master': self.master.to_dict() if self.master else None
        }
