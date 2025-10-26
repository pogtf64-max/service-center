"""
Модели базы данных
"""
from .database import db
from .service import Service
from .user import User
from .client import Client
from .device import Device
from .order import Order
from .part import Part
from .cash_register import CashRegister

__all__ = ['db', 'Service', 'User', 'Client', 'Device', 'Order', 'Part', 'CashRegister']
