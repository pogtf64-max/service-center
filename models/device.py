"""
Модель устройства
"""
from datetime import datetime
from .database import db

class Device(db.Model):
    """Модель устройства клиента"""
    __tablename__ = 'devices'
    
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    device_type = db.Column(db.String(50), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    serial_number = db.Column(db.String(100))
    imei = db.Column(db.String(20))
    condition = db.Column(db.Text)
    external_description = db.Column(db.Text)
    completeness = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Связи
    orders = db.relationship('Order', backref='device', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Device {self.brand} {self.model}>'
    
    def to_dict(self):
        """Преобразование в словарь для API"""
        return {
            'id': self.id,
            'client_id': self.client_id,
            'device_type': self.device_type,
            'brand': self.brand,
            'model': self.model,
            'serial_number': self.serial_number,
            'imei': self.imei,
            'condition': self.condition,
            'external_description': self.external_description,
            'completeness': self.completeness,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
