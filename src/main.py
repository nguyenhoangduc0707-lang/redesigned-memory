# -*- coding: utf-8 -*-
import sys, os, tempfile, secrets, uuid
from datetime import date
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from src.database import get_db, init_db, save_post
from src.agents import run_all_agents
from src.campaign_intelligence import CampaignIntelligence
from src.user_manager import authenticate_user, get_user_by_id, add_user, list_users
from src.tts_engine import text_to_speech
from src.notebooklm_pro import NotebookLMPro
import requests
from src.affiliate_manager import (
    create_affiliate_link, get_random_ad, reward_user_for_ad, track_click,
    init_affiliate_tables, can_create_link
)

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', os.urandom(24))
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(int(user_id))

# Video processor
try:
    from src.media.video_processor import get_processor
    PROCESSOR_READY = True
    processor = get_processor()
except:
    PROCESSOR_READY = False
    processor = None

ci = CampaignIntelligence()
notebooklm_pro = NotebookLMPro()

def generate_caption(product_name, price, strategy):
    return f"Hot {product_name} chi {price:,}d! Uu dai. #{strategy} #affiliate"

def generate_content_for_all():
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, name, price, url, strategy FROM products")
        products = cur.fetchall()
        platforms = ['tiktok', 'facebook', 'zalo', 'shopee']
        for pid, name, price, url, strategy in products:
            for platform in platforms:
                caption = generate_caption(name, price, strategy)
                save_post(pid, platform, caption, url)
    print("Da sinh noi dung")

def post_to_facebook(message):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT access_token FROM platform_tokens WHERE platform='facebook'")
        row = cur.fetchone()
        token = row[0] if row else os.getenv('FACEBOOK_ACCESS_TOKEN', '')
    if not token:
        return "Khong co token"
    url = "https://graph.facebook.com/v18.0/me/feed"
    resp = requests.post(url, data={'message': message, 'access_token': token})
    return resp.json()

@app.route('/')
def home():
    return redirect(url_for('login') if not current_user.is_authenticated else url_for('dashboard'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']
        user = authenticate_user(u, p)
        if user:
            login_user(user)
            flash('Dang nhap thanh cong')
            return redirect(url_for('dashboard'))
        flash('Sai tai khoan hoac mat khau')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT platform_target, COUNT(*) FROM posts WHERE status='draft' GROUP BY platform_target")
        counts = {r[0]: r[1] for r in cur.fetchall()}
    return render_template('unified_dashboard.html', counts=counts, role=current_user.role)

@app.route('/admin/users')
@login_required
def admin_users():
    if current_user.role != 'admin':
        flash('Ban khong co quyen')
        return redirect(url_for('dashboard'))
    if request.args.get('format') == 'json':
        users = list_users()
        return jsonify([{'id': u[0], 'username': u[1], 'role': u[2], 'created_at': u[3]} for u in users])
    return render_template('admin_users.html', users=list_users())

@app.route('/admin/add_user', methods=['POST'])
@login_required
def add_user_route():
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'user')
    user_id = add_user(username, password, role)
    if user_id:
        return jsonify({'success': True, 'user_id': user_id})
    return jsonify({'success': False, 'error': 'Username exists'}), 400

@app.route('/admin/tokens', methods=['GET'])
@login_required
def admin_tokens():
    if current_user.role != 'admin':
        flash('Ban khong co quyen')
        return redirect(url_for('dashboard'))
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT platform, access_token, api_key, updated_at FROM platform_tokens")
        tokens = cur.fetchall()
    return render_template('admin_tokens.html', tokens=tokens)

@app.route('/admin/update_token', methods=['POST'])
@login_required
def update_token():
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    data = request.get_json()
    platform = data.get('platform')
    access_token = data.get('access_token', '')
    api_key = data.get('api_key', '')
    api_secret = data.get('api_secret', '')
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute('''UPDATE platform_tokens SET access_token=?, api_key=?, api_secret=?, updated_at=CURRENT_TIMESTAMP WHERE platform=?''',
                    (access_token, api_key, api_secret, platform))
        conn.commit()
    return jsonify({'success': True})

@app.route('/license')
def license_page():
    return render_template('license.html')

@app.route('/sen_license')
def sen_license():
    return render_template('sen_license.html')

@app.route('/chat')
@login_required
def chat_page():
    return render_template('chat.html')

@app.route('/notebooklm')
@login_required
def notebooklm_page():
    return render_template('notebooklm.html')

@app.route('/api/notebooklm/status')
@login_required
def notebooklm_status():
    return jsonify(notebooklm_pro.status())

@app.route('/api/notebooklm/ask', methods=['POST'])
@login_required
def notebooklm_ask():
    data = request.get_json() or {}
    question = data.get('question', '')
    timeout = int(data.get('timeout', 120))
    return jsonify(notebooklm_pro.ask(question, timeout=timeout))

@app.route('/api/chat', methods=['POST'])
@login_required
def chat_api():
    data = request.get_json()
    msg = data.get('message', '')
    if "notebook" in msg.lower():
        result = notebooklm_pro.ask(msg)
        response = result.get('answer') or result.get('error') or "NotebookLM khong co cau tra loi."
    elif "chay pipeline" in msg.lower():
        response = "Da chay pipeline thanh cong."
        run_all_agents()
    elif "thong ke" in msg.lower():
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM campaigns")
            count = cur.fetchone()[0]
            response = f"He thong co {count} chien dich."
    else:
        response = f"Ban noi: {msg}. Toi la tro ly AI."
    audio_file = text_to_speech(response, lang='vi')
    return jsonify({'text': response, 'audio_file': audio_file})

@app.route('/api/health')
def api_health():
    return jsonify({"status": "healthy"})

@app.route('/media')
@login_required
def media_page():
    return render_template('media.html')

@app.route('/review_station')
@login_required
def review_station():
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, product_id, platform_target, caption, link, status FROM posts ORDER BY id DESC LIMIT 100")
        posts = cur.fetchall()
    return render_template('review_station.html', posts=posts)

# Campaign routes
@app.route('/campaigns')
@login_required
def campaigns_page():
    with get_db() as conn:
        cur = conn.cursor()
        if current_user.role == 'admin':
            cur.execute("SELECT * FROM campaigns ORDER BY created_at DESC")
        else:
            cur.execute("SELECT * FROM campaigns WHERE user_id=? ORDER BY created_at DESC", (current_user.id,))
        campaigns = cur.fetchall()
    return render_template('campaigns.html', campaigns=campaigns)

@app.route('/new_campaign', methods=['GET','POST'])
@login_required
def new_campaign():
    if request.method == 'POST':
        name = request.form['name']
        platform = request.form['platform']
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO campaigns (user_id, name, platform, status) VALUES (?,?,?,?)",
                        (current_user.id, name, platform, 'active'))
            conn.commit()
            cur.execute("UPDATE user_stats SET campaign_count = campaign_count + 1 WHERE user_id=?", (current_user.id,))
            conn.commit()
        flash('Da tao chien dich!')
        return redirect(url_for('campaigns_page'))
    return render_template('new_campaign.html')

@app.route('/pipeline')
@login_required
def pipeline_page():
    return render_template('pipeline.html')

@app.route('/api/pipeline_logs')
@login_required
def api_pipeline_logs():
    with get_db() as conn:
        cur = conn.cursor()
        if current_user.role == 'admin':
            cur.execute("SELECT * FROM pipeline_logs ORDER BY created_at DESC LIMIT 100")
        else:
            cur.execute('''SELECT l.* FROM pipeline_logs l JOIN campaigns c ON l.campaign_id=c.id WHERE c.user_id=? ORDER BY l.created_at DESC LIMIT 100''', (current_user.id,))
        logs = cur.fetchall()
    result = [{'id':r[0],'campaign_id':r[1],'worker_name':r[2],'action':r[3],'status':r[4],'message':r[5],'created_at':r[6]} for r in logs]
    return jsonify(result)

@app.route('/api/campaigns')
@login_required
def api_campaigns():
    with get_db() as conn:
        cur = conn.cursor()
        if current_user.role == 'admin':
            cur.execute("SELECT id,name,platform,status,created_at FROM campaigns ORDER BY created_at DESC")
        else:
            cur.execute("SELECT id,name,platform,status,created_at FROM campaigns WHERE user_id=?", (current_user.id,))
        rows = cur.fetchall()
    return jsonify([{'id':r[0],'name':r[1],'platform':r[2],'status':r[3],'created_at':r[4]} for r in rows])

@app.route('/api/run_worker', methods=['POST'])
@login_required
def run_worker():
    data = request.get_json()
    campaign_id = data.get('campaign_id')
    worker_name = data.get('worker_name')
    with get_db() as conn:
        conn.execute("INSERT INTO pipeline_logs (campaign_id, worker_name, action, status, message) VALUES (?,?,?,?,?)",
                     (campaign_id, worker_name, 'run', 'started', f'Worker {worker_name} started by {current_user.username}'))
        conn.commit()
    return jsonify({'status': 'started', 'message': f'Worker {worker_name} dang chay (gia lap)'})

@app.route('/api/me')
@login_required
def api_me():
    return jsonify({'id':current_user.id, 'username':current_user.username, 'role':current_user.role})

# Affiliate routes
@app.route('/my_links')
@login_required
def my_links():
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT link_code, target_url, used_count, created_at FROM affiliate_links WHERE user_id=?", (current_user.id,))
        links = cur.fetchall()
    return render_template('my_links.html', links=links, role=current_user.role, daily_left=can_create_link(current_user.id))

@app.route('/api/create_link', methods=['POST'])
@login_required
def api_create_link():
    data = request.get_json()
    target_url = data.get('target_url')
    if not target_url:
        return jsonify({"error": "Missing target_url"}), 400
    code, err = create_affiliate_link(current_user.id, target_url)
    if err:
        return jsonify({"error": err}), 403
    return jsonify({"link_code": code, "link": f"http://localhost:5000/go/{code}"})

@app.route('/api/need_ad', methods=['GET'])
@login_required
def api_need_ad():
    if can_create_link(current_user.id):
        return jsonify({"can_create": True})
    ad = get_random_ad()
    if not ad:
        return jsonify({"can_create": False, "error": "No ad"})
    return jsonify({"can_create": False, "ad": ad})

@app.route('/api/watch_ad', methods=['POST'])
@login_required
def api_watch_ad():
    data = request.get_json()
    ad_id = data.get('ad_id')
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM ads WHERE id=?", (ad_id,))
        row = cur.fetchone()
        if not row:
            return jsonify({"error": "Ad not found"}), 404
        ad = {"id":row[0],"title":row[1],"reward_type":row[4],"reward_value":row[5]}
        msg = reward_user_for_ad(current_user.id, ad)
        return jsonify({"success": True, "message": msg, "new_quota": can_create_link(current_user.id)})

@app.route('/go/<link_code>')
def redirect_link(link_code):
    ip = request.remote_addr
    track_click(link_code, ip)
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT target_url FROM affiliate_links WHERE link_code=?", (link_code,))
        row = cur.fetchone()
        if not row:
            return "Link not found", 404
        return redirect(row[0])

# ========== WEBHOOK COMMISSION ==========
@app.route('/webhook/commission', methods=['POST'])
def webhook_commission():
    """
    Nhận dữ liệu bán hàng từ sàn TMĐT (Shopee, TikTok, ...)
    Dữ liệu mẫu: {"user_id": 1, "amount": 100000, "order_id": "123", "product": "..."}
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data"}), 400
    user_id = data.get('user_id')
    amount = data.get('amount')
    if not user_id or not amount:
        return jsonify({"error": "Missing user_id or amount"}), 400
    # Ghi nhận hoa hồng (40% user, 30% referrer, 30% admin)
    # Sử dụng hàm record_commission từ affiliate_manager
    try:
        from src.affiliate_manager import record_commission
        record_commission(amount, user_id, f"Order {data.get('order_id', 'unknown')}")
        return jsonify({"status": "success", "message": "Commission recorded"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/create_video_demo', methods=['POST'])
@login_required
def api_create_video_demo():
    """
    Demo: nhận danh sách đường dẫn ảnh (hoặc upload file) và text, tạo video.
    Ảnh có thể gửi dưới dạng list URLs hoặc upload files.
    """
    data = request.get_json()
    image_urls = data.get('image_urls', [])
    text = data.get('text', '')
    output_filename = f"output_{uuid.uuid4().hex}.mp4"
    output_path = os.path.join('static', 'videos', output_filename)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Tạm thời giả lập: tạo video mẫu
    # Thực tế cần tải ảnh từ URL, lưu tạm, rồi gọi processor
    # Ở đây tôi chỉ tạo video trắng để demo
    from moviepy.editor import ColorClip, AudioFileClip
    from gtts import gTTS
    # Tạo audio từ text
    audio_path = f"audio_{uuid.uuid4().hex}.mp3"
    tts = gTTS(text, lang='vi')
    tts.save(audio_path)
    # Tạo video trắng 5 giây
    clip = ColorClip(size=(1280,720), color=(255,255,255), duration=5)
    audio = AudioFileClip(audio_path)
    clip = clip.set_audio(audio)
    clip.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')
    os.remove(audio_path)
    return jsonify({"video_url": f"/static/videos/{output_filename}"})

# ========== CREATE VIDEO ROUTE ==========
@app.route('/create_video', methods=['GET', 'POST'])
@login_required
def create_video():
    if request.method == 'POST':
        caption = request.form.get('caption', '')
        files = request.files.getlist('images')
        if not files or len(files) == 0:
            flash('Vui lòng upload ít nhất 1 ảnh')
            return redirect(url_for('create_video'))
        
        from werkzeug.utils import secure_filename
        import uuid
        image_paths = []
        for file in files:
            if file.filename:
                filename = secure_filename(file.filename)
                unique = f"{uuid.uuid4().hex}_{filename}"
                filepath = os.path.join('uploads', unique)
                os.makedirs('uploads', exist_ok=True)
                file.save(filepath)
                image_paths.append(filepath)
        
        audio_path = None
        if caption.strip():
            from src.tts_engine import text_to_speech
            audio_path = text_to_speech(caption, lang='vi', output_dir='audio')
        
        from src.media.video_processor import get_processor
        processor = get_processor()
        video_filename = f"video_{uuid.uuid4().hex}.mp4"
        video_output = os.path.join('static', 'videos', video_filename)
        os.makedirs('static/videos', exist_ok=True)
        
        processor.create_video_from_images(image_paths, audio_path, video_output, duration_per_image=3)
        
        for p in image_paths:
            try: os.remove(p)
            except: pass
        
        return render_template('video_result.html', video_url=f'/static/videos/{video_filename}', caption=caption)
    
    return render_template('create_video.html')

@app.route('/api/post_video_to_fb', methods=['POST'])
@login_required
def post_video_to_fb():
    data = request.get_json()
    video_path = data.get('video_url').replace('/static/', 'static/')
    caption = data.get('caption', '')
    from worker.executor import run_worker
    result = run_worker('facebook', None, caption, video_path, 'video')
    return jsonify({"message": "Đã gửi yêu cầu đăng bài", "result": result})

if __name__ == '__main__':
    init_db()
    init_affiliate_tables()
    if '--run-pipeline' in sys.argv:
        run_all_agents()
        generate_content_for_all()
    else:
        debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
        app.run(debug=debug_mode, host='0.0.0.0' if debug_mode else '127.0.0.1', port=5000)
