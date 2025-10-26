"""
Модель клиента
"""
from datetime import datetime
from .database import db

class Client(db.Model):
    """Модель клиента сервисного центра"""
    __tablename__ = 'clients'
    
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    client_type = db.Column(db.String(20), nullable=False, default='individual')  # 'individual' или 'legal'
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100))
    address = db.Column(db.Text)
    # Поля для юридических лиц
    organization_name = db.Column(db.String(200))  # Наименование организации
    inn = db.Column(db.String(20))  # ИНН организации
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Связи
    devices = db.relationship('Device', backref='client', lazy='dynamic', cascade='all, delete-orphan')
    orders = db.relationship('Order', backref='client', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Client {self.name}>'
    
    def to_dict(self):
        """Преобразование в словарь для API"""
        return {
            'id': self.id,
            'client_type': self.client_type,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'organization_name': self.organization_name,
            'inn': self.inn,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
