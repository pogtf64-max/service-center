"""
Модель пользователя
"""
from flask_login import UserMixin
from datetime import datetime
from .database import db

class User(UserMixin, db.Model):
    """Модель пользователя системы"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='employee')
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(20))
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    is_active = db.Column(db.Boolean, default=True)
    is_approved = db.Column(db.Boolean, default=False)  # Подтвержден ли директором
    can_manage_settings = db.Column(db.Boolean, default=False)  # Может ли управлять настройками
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Связи
    orders_as_master = db.relationship('Order', backref='master', lazy='dynamic')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def get_role_display(self):
        """Получить отображаемое название роли на русском"""
        role_map = {
            'director': 'Директор',
            'manager': 'Менеджер',
            'master': 'Мастер',
            'employee': 'Сотрудник'
        }
        return role_map.get(self.role, self.role)
    
    def to_dict(self):
        """Преобразование в словарь для API"""
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
