from flask import Flask, render_template_string
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Сервисный центр - Работает!</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                min-height: 100vh;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                text-align: center;
            }
            h1 {
                font-size: 3em;
                margin-bottom: 20px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            .status {
                background: rgba(255,255,255,0.1);
                padding: 20px;
                border-radius: 10px;
                margin: 20px 0;
                backdrop-filter: blur(10px);
            }
            .success {
                background: rgba(76, 175, 80, 0.2);
                border: 1px solid rgba(76, 175, 80, 0.5);
            }
            .info {
                background: rgba(33, 150, 243, 0.2);
                border: 1px solid rgba(33, 150, 243, 0.5);
            }
            .warning {
                background: rgba(255, 152, 0, 0.2);
                border: 1px solid rgba(255, 152, 0, 0.5);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔧 Сервисный центр</h1>
            
            <div class="status success">
                <h2>✅ Система работает!</h2>
                <p>Приложение успешно запущено и готово к работе</p>
            </div>
            
            <div class="status info">
                <h3>📊 Статус системы</h3>
                <p><strong>Версия:</strong> 1.0.0</p>
                <p><strong>Статус:</strong> Работает</p>
                <p><strong>База данных:</strong> Настраивается...</p>
                <p><strong>Автоматическое развертывание:</strong> Активно</p>
            </div>
            
            <div class="status warning">
                <h3>⚠️ Временное решение</h3>
                <p>Сейчас работает упрощенная версия приложения</p>
                <p>Полная версия будет восстановлена после настройки базы данных</p>
            </div>
            
            <div class="status">
                <h3>🚀 Возможности</h3>
                <p>• Управление заказами</p>
                <p>• Учет клиентов</p>
                <p>• Складской учет</p>
                <p>• Финансовый учет</p>
                <p>• Автоматическое развертывание</p>
            </div>
            
            <div class="status">
                <h3>🔧 Техническая информация</h3>
                <p><strong>Сервер:</strong> 77.110.127.57</p>
                <p><strong>Контейнер:</strong> Docker</p>
                <p><strong>Веб-сервер:</strong> Nginx</p>
                <p><strong>Приложение:</strong> Flask</p>
            </div>
        </div>
    </body>
    </html>
    ''')

@app.route('/health')
def health():
    return {'status': 'ok', 'message': 'Service Center is running'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
