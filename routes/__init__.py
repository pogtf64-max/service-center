"""
Маршруты приложения
"""
from .auth import auth_bp
from .dashboard import dashboard_bp
from .clients import clients_bp
from .orders import orders_bp
from .parts import parts_bp
from .services import services_bp
from .devices import devices_bp
from .archive import archive_bp
from .settings import settings_bp

def register_blueprints(app):
    """Регистрация всех blueprint'ов"""
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(clients_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(parts_bp)
    app.register_blueprint(services_bp)
    app.register_blueprint(devices_bp)
    app.register_blueprint(archive_bp)
    app.register_blueprint(settings_bp)