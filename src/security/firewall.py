import hashlib
from functools import wraps
from flask import request, jsonify

VALID_KEYS_HASH = {
    hashlib.sha256("075097016965".encode()).hexdigest(): "075097016965",
    hashlib.sha256("075088008608".encode()).hexdigest(): "075088008608"
}

def verify_key(provided_key):
    hashed = hashlib.sha256(provided_key.encode()).hexdigest()
    return hashed in VALID_KEYS_HASH

def require_sensitive_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        data = request.get_json(silent=True) or {}
        key = request.headers.get('X-Auth-Key') or request.args.get('key') or data.get('key')
        if not key or not verify_key(key):
            return jsonify({"error": "VUI LÒNG CUNG CẤP KHÓA (KEY) XÁC THỰC HOẶC MÃ CCCD ĐỂ TIẾP TỤC"}), 403
        return f(*args, **kwargs)
    return decorated
