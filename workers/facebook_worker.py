import os
import sys
import json
import requests
import hashlib
import hmac
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Thêm đường dẫn gốc để import các module nội bộ
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()

from src.security.policy_checker import can_send_link
from sen_brain import default_brain as brain

# Cấu hình từ biến môi trường
PAGE_ACCESS_TOKEN = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN")
VERIFY_TOKEN = os.getenv("FACEBOOK_VERIFY_TOKEN", "sen_verify_token_2026")  # Thêm dòng này
APP_SECRET = os.getenv("FACEBOOK_APP_SECRET")
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "gemma2:2b")

# Khởi tạo Flask app
app = Flask(__name__)

def ask_ollama(prompt):
    try:
        resp = requests.post(OLLAMA_URL, json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}, timeout=30)
        if resp.status_code == 200:
            return resp.json().get("response", "Xin lỗi, tôi chưa có câu trả lời.")
        else:
            return f"Lỗi Ollama (HTTP {resp.status_code})"
    except Exception as e:
        return f"Lỗi kết nối Ollama: {e}"

def send_message(recipient_id, message_text):
    """Gửi tin nhắn qua Facebook Graph API"""
    url = f"https://graph.facebook.com/v18.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    try:
        resp = requests.post(url, json=payload)
        if resp.status_code != 200:
            print(f"Lỗi gửi tin nhắn: {resp.text}")
        return resp.ok
    except Exception as e:
        print(f"Lỗi kết nối Graph API: {e}")
        return False

def handle_message(sender_id, message_text):
    """Xử lý tin nhắn đến và quyết định có gửi affiliate link hay không"""
    # Phân tích cảm xúc hoặc gọi AI tổng quát
    if brain:
        sentiment = brain.analyze_sentiment(message_text)
        print(f"Sentiment: {sentiment}")
    else:
        sentiment = {"label": "neutral", "score": 0.5}

    # Kiểm tra policy trước khi gửi affiliate link
    if "mua" in message_text.lower() or "giá" in message_text.lower() or "affiliate" in message_text.lower():
        if can_send_link(sender_id, message_text):
            affiliate_message = "Bạn có thể tham khảo sản phẩm tại đây: [link affiliate]"
            send_message(sender_id, affiliate_message)
        else:
            send_message(sender_id, "Rất tiếc, chúng tôi chỉ gửi thông tin này một lần trong 24 giờ. Vui lòng quay lại sau.")
    else:
        # Trả lời bình thường bằng AI
        reply = ask_ollama(message_text)
        send_message(sender_id, reply)

@app.route('/webhook', methods=['GET'])
def verify_webhook():
    """Xác thực webhook với Facebook"""
    received_token = request.args.get('hub.verify_token')
    print(f"🔍 Received verify_token: {received_token}")
    print(f"🔍 Expected VERIFY_TOKEN: {VERIFY_TOKEN}")
    if received_token == VERIFY_TOKEN:
        return request.args.get('hub.challenge')
    return "Verification token mismatch", 403

@app.route('/webhook', methods=['POST'])
def webhook():
    """Nhận sự kiện từ Facebook"""
    data = request.get_json()
    # Kiểm tra signature (nếu có APP_SECRET)
    if APP_SECRET:
        signature = request.headers.get('X-Hub-Signature-256')
        if signature:
            expected = 'sha256=' + hmac.new(APP_SECRET.encode(), request.data, hashlib.sha256).hexdigest()
            if not hmac.compare_digest(signature, expected):
                return "Invalid signature", 403

    if data.get('object') == 'page':
        for entry in data.get('entry', []):
            for messaging in entry.get('messaging', []):
                sender_id = messaging.get('sender', {}).get('id')
                message = messaging.get('message', {})
                if message and 'text' in message:
                    handle_message(sender_id, message['text'])
    return "OK", 200

def start_webhook_server(port=5000):
    app.run(host='0.0.0.0', port=port, debug=False)

if __name__ == "__main__":
    if not PAGE_ACCESS_TOKEN:
        print("❌ Chưa có FACEBOOK_PAGE_ACCESS_TOKEN trong file .env")
        sys.exit(1)
    print(f"✅ Facebook Worker đang chạy, webhook lắng nghe tại port 5000")
    start_webhook_server()