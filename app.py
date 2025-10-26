"""
Главный файл приложения сервисного центра
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
from config import config
from routes import register_blueprints
from routes.service import service_bp
from models import db

def create_app(config_name='default'):
    """Фабрика приложения"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Инициализация расширений
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Пожалуйста, войдите в систему для доступа к этой странице.'
    
    # Загрузчик пользователей
    from models.user import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Регистрация маршрутов
    register_blueprints(app)
    app.register_blueprint(service_bp)
    
    # Создание таблиц и пользователя по умолчанию
    with app.app_context():
        db.create_all()
        create_default_admin()
    
    return app

def create_default_admin():
    """Создание администратора по умолчанию"""
    from models.user import User
    from models.service import Service
    
    # Проверяем, есть ли уже админ
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        # Создаем администратора сначала
        admin = User(
            username='admin',
            password_hash=generate_password_hash('admin123'),
            role='admin',
            full_name='Системный администратор',
            is_active=True,
            is_approved=True
        )
        db.session.add(admin)
        db.session.flush()  # Получаем ID администратора
        
        # Создаем сервис по умолчанию
        default_service = Service(
            name='Административная панель',
            address='Системный сервис',
            service_password=generate_password_hash('admin123'),
            director_id=admin.id
        )
        db.session.add(default_service)
        db.session.flush()  # Получаем ID сервиса
        
        # Обновляем service_id у администратора
        admin.service_id = default_service.id
        
        db.session.commit()
        print("Создан системный администратор: admin/admin123")

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=8080)