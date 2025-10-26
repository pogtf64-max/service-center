"""
Модель сервисного центра
"""
from datetime import datetime
from .database import db

class Service(db.Model):
    """Модель сервисного центра"""
    __tablename__ = 'services'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    short_name = db.Column(db.String(100))  # Сокращенное наименование
    address = db.Column(db.Text)
    legal_address = db.Column(db.Text)  # Юридический адрес
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    website = db.Column(db.String(200))  # Веб-сайт
    working_hours = db.Column(db.String(100))  # Режим работы
    
    # Юридические реквизиты
    inn = db.Column(db.String(20))  # ИНН
    kpp = db.Column(db.String(20))  # КПП
    ogrn = db.Column(db.String(20))  # ОГРН
    okpo = db.Column(db.String(20))  # ОКПО
    okved = db.Column(db.String(50))  # ОКВЭД
    
    # Банковские реквизиты
    bank_name = db.Column(db.String(200))  # Наименование банка
    bank_bik = db.Column(db.String(20))  # БИК
    bank_account = db.Column(db.String(30))  # Расчетный счет
    bank_correspondent_account = db.Column(db.String(30))  # Корреспондентский счет
    
    # Руководство
    director_name = db.Column(db.String(200))  # ФИО директора
    chief_accountant = db.Column(db.String(200))  # ФИО главного бухгалтера
    
    service_password = db.Column(db.String(255), nullable=False)  # Пароль сервиса
    director_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Связи
    director = db.relationship('User', backref='directed_service', foreign_keys=[director_id])
    users = db.relationship('User', backref='service', foreign_keys='User.service_id')
    clients = db.relationship('Client', backref='service')
    orders = db.relationship('Order', backref='service')
    parts = db.relationship('Part', backref='service')
    
    def __repr__(self):
        return f'<Service {self.name}>'
    
    def to_dict(self):
        """Преобразование в словарь для API"""
        return {
            'id': self.id,
            'name': self.name,
            'short_name': self.short_name,
            'address': self.address,
            'legal_address': self.legal_address,
            'phone': self.phone,
            'email': self.email,
            'website': self.website,
            'working_hours': self.working_hours,
            'inn': self.inn,
            'kpp': self.kpp,
            'ogrn': self.ogrn,
            'okpo': self.okpo,
            'okved': self.okved,
            'bank_name': self.bank_name,
            'bank_bik': self.bank_bik,
            'bank_account': self.bank_account,
            'bank_correspondent_account': self.bank_correspondent_account,
            'director_name': self.director_name,
            'chief_accountant': self.chief_accountant,
            'director_id': self.director_id,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
