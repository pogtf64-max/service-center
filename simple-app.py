from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Service Center - Временная версия</title>
        <meta charset="utf-8">
    </head>
    <body>
        <h1>Сервисный центр</h1>
        <p>Приложение временно работает в упрощенном режиме.</p>
        <p>База данных настраивается...</p>
        <p>Статус: Работает</p>
    </body>
    </html>
    ''')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
