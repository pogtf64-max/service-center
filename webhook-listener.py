from flask import Flask, request
import subprocess
import hmac
import hashlib

app = Flask(__name__)
SECRET = "your-webhook-secret"

@app.route('/webhook', methods=['POST'])
def webhook():
    signature = request.headers.get('X-Hub-Signature-256')
    if not verify_signature(request.data, signature):
        return 'Unauthorized', 401
    
    # Запускаем деплой
    subprocess.Popen(['bash', '/root/deploy-service-center.sh'])
    return 'Deployment started', 200

def verify_signature(payload, signature):
    expected = 'sha256=' + hmac.new(
        SECRET.encode(), payload, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
