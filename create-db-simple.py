#!/usr/bin/env python3
import sqlite3
import os

# Создаем директорию instance если её нет
os.makedirs('instance', exist_ok=True)

# Создаем файл базы данных
conn = sqlite3.connect('instance/service_center.db')
conn.close()
print("Database file created successfully")
