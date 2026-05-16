import sys
from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import get_db, init_db, save_post
from agents import run_all_agents
from campaign_intelligence import CampaignIntelligence
import requests
import os

app = Flask(__name__)
app.secret_key = 'affiliate-secret'
USERS = {'admin': 'admin123', 'user1': 'user123'}
ci = CampaignIntelligence()

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
    token = os.getenv('FACEBOOK_ACCESS_TOKEN', '')
    if not token:
        return "Khong co token"
    url = "https://graph.facebook.com/v18.0/me/feed"
    resp = requests.post(url, data={'message': message, 'access_token': token})
    return resp.json()

@app.route('/')
def home():
    return redirect(url_for('login') if not session.get('user') else url_for('dashboard'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']
        if u in USERS and USERS[u] == p:
            session['user'] = u
            session['role'] = 'admin' if u == 'admin' else 'user'
            flash('Dang nhap thanh cong')
            return redirect(url_for('dashboard'))
        flash('Sai tai khoan hoac mat khau')
    return '''
        <h2>Dang nhap</h2>
        <form method=post>
            <input name=username placeholder=admin><br>
            <input name=password type=password><br>
            <button>Dang nhap</button>
        </form>
    '''

@app.route('/dashboard')
def dashboard():
    if not session.get('user'):
        return redirect(url_for('login'))
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT platform_target, COUNT(*) FROM posts WHERE status='draft' GROUP BY platform_target")
        counts = {r[0]: r[1] for r in cur.fetchall()}
    return render_template('dashboard.html', counts=counts, role=session.get('role'))

@app.route('/posts/<platform>')
def posts(platform):
    if not session.get('user'):
        return redirect(url_for('login'))
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, caption, link FROM posts WHERE platform_target=? AND status='draft'", (platform,))
        posts = [{'id':r[0], 'caption':r[1], 'link':r[2]} for r in cur.fetchall()]
    return render_template('posts.html', platform=platform, posts=posts)

@app.route('/post_to_fb', methods=['POST'])
def post_to_fb():
    post_id = request.form['post_id']
    platform = request.form['platform']
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT caption, link FROM posts WHERE id=?", (post_id,))
        row = cur.fetchone()
        if not row:
            flash('Khong tim thay bai dang')
            return redirect(url_for('posts', platform=platform))
        caption, link = row
        message = f"{caption}\nLink: {link}"
        result = post_to_facebook(message)
        if 'id' in result:
            cur.execute("UPDATE posts SET status='published' WHERE id=?", (post_id,))
            conn.commit()
            flash('Da dang len Facebook thanh cong!')
        else:
            flash(f'Loi: {result}')
    return redirect(url_for('posts', platform=platform))

@app.route('/run_pipeline')
def run_pipeline():
    if session.get('role') != 'admin':
        flash('Chi admin moi duoc chay')
        return redirect(url_for('dashboard'))
    run_all_agents()
    generate_content_for_all()
    flash('Pipeline da chay xong!')
    return redirect(url_for('dashboard'))

# ========== CAMPAIGN MANAGEMENT ROUTES ==========
@app.route('/campaigns')
def list_campaigns():
    if not session.get('user'):
        return redirect(url_for('login'))
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM campaigns ORDER BY created_at DESC")
        campaigns = cur.fetchall()
    return render_template('campaigns.html', campaigns=campaigns)

@app.route('/campaign/new', methods=['GET','POST'])
def new_campaign():
    if session.get('role') != 'admin':
        flash('Chi admin moi duoc tao')
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        name = request.form['name']
        platform = request.form['platform']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        budget = float(request.form['budget'])
        goal = request.form['goal']
        product_ids = request.form.getlist('product_ids')
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO campaigns (name, platform, start_date, end_date, budget, goal, status) VALUES (?,?,?,?,?,?,'draft')",
                        (name, platform, start_date, end_date, budget, goal))
            campaign_id = cur.lastrowid
            for pid in product_ids:
                cur.execute("INSERT INTO campaign_products (campaign_id, product_id) VALUES (?,?)", (campaign_id, pid))
            conn.commit()
        pred = ci.predict_campaign(campaign_id)
        flash(f"Tao chien dich thanh cong! Du doan: {pred['predicted_posts']} bai, {pred['predicted_sales']} don hang.")
        return redirect(url_for('list_campaigns'))
    else:
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, name, price FROM products")
            products = cur.fetchall()
        return render_template('new_campaign.html', products=products)

@app.route('/campaign/<int:campaign_id>/predict')
def show_prediction(campaign_id):
    if not session.get('user'):
        return redirect(url_for('login'))
    pred = ci.predict_campaign(campaign_id)
    return render_template('campaign_predict.html', prediction=pred, campaign_id=campaign_id)

@app.route('/campaign/<int:campaign_id>/evaluate', methods=['POST'])
def evaluate_campaign(campaign_id):
    if session.get('role') != 'admin':
        flash('Admin only')
        return redirect(url_for('dashboard'))
    actual_posts = int(request.form['actual_posts'])
    actual_likes = int(request.form['actual_likes'])
    actual_sales = int(request.form['actual_sales'])
    actual_revenue = float(request.form['actual_revenue'])
    result = ci.evaluate_campaign(campaign_id, actual_posts, actual_likes, actual_sales, actual_revenue)
    if result.get('need_optimization'):
        opt = ci.optimize_algorithm(campaign_id)
        flash(f"Danh gia hoan tat. Do chinh xac: {result['accuracy_percent']:.2f}%. Da toi uu thuat toan.")
    else:
        flash(f"Danh gia hoan tat. Do chinh xac: {result['accuracy_percent']:.2f}%. Tot!")
    return redirect(url_for('list_campaigns'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--run-pipeline':
        init_db()
        run_all_agents()
        generate_content_for_all()
        print("Pipeline hoan tat.")
    else:
        init_db()
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM products")
            if cur.fetchone()[0] == 0:
                run_all_agents()
                generate_content_for_all()
        app.run(debug=True, host='0.0.0.0', port=5000)