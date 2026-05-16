# ==============================================
# KIEM TRA VA FIX TOAN BO HE THONG AI_OS
# ==============================================
$root = "C:\AI_OS_KERNEL_V3"
$dbPath = "$root\affiliate.db"
$errorCount = 0

Write-Host "=== BAT DAU KIEM TRA VA FIX ===" -ForegroundColor Cyan

# 1. Tao thu muc templates neu thieu
if (-not (Test-Path "$root\templates")) {
    New-Item -ItemType Directory -Path "$root\templates" -Force | Out-Null
    Write-Host "[OK] Da tao thu muc templates" -ForegroundColor Green
}

# 2. Kiem tra va tao cac bang database (dung Python)
Write-Host "[1] Kiem tra database..." -ForegroundColor Yellow
python -c "
import sqlite3
conn = sqlite3.connect(r'$dbPath')
conn.execute('''CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT, price REAL, commission REAL, platform TEXT, url TEXT, strategy TEXT)''')
conn.execute('''CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY, product_id INTEGER, platform_target TEXT, caption TEXT, link TEXT, status TEXT DEFAULT 'draft')''')
conn.execute('''CREATE TABLE IF NOT EXISTS campaigns (id INTEGER PRIMARY KEY, name TEXT, platform TEXT, start_date DATE, end_date DATE, budget REAL, goal TEXT, status TEXT DEFAULT 'draft', created_at TIMESTAMP)''')
conn.execute('''CREATE TABLE IF NOT EXISTS campaign_products (campaign_id INTEGER, product_id INTEGER, post_ids TEXT)''')
conn.execute('''CREATE TABLE IF NOT EXISTS campaign_predictions (campaign_id INTEGER, predicted_posts INTEGER, predicted_likes REAL, predicted_sales INTEGER, predicted_revenue REAL, prediction_date TIMESTAMP)''')
conn.execute('''CREATE TABLE IF NOT EXISTS campaign_results (campaign_id INTEGER, actual_posts INTEGER, actual_likes INTEGER, actual_sales INTEGER, actual_revenue REAL, accuracy_percent REAL, result_date TIMESTAMP)''')
conn.execute('''CREATE TABLE IF NOT EXISTS algorithm_adjustments (id INTEGER PRIMARY KEY, platform TEXT, adjustment_reason TEXT, old_params TEXT, new_params TEXT, created_at TIMESTAMP)''')
conn.execute('''CREATE TABLE IF NOT EXISTS algorithm_params (id INTEGER PRIMARY KEY, platform TEXT, param_name TEXT, param_value REAL, updated_at TIMESTAMP)''')
conn.close()
print('OK')
" 2>$null
if ($LASTEXITCODE -eq 0) { Write-Host "[OK] Database ready" -ForegroundColor Green }
else { $errorCount++; Write-Host "[ERROR] Database creation failed" -ForegroundColor Red }

# 3. Kiem tra va tao file .env (neu chua co)
$envFile = "$root\.env"
if (-not (Test-Path $envFile)) {
    @"
SECRET_KEY=af123xyz
FACEBOOK_ACCESS_TOKEN=
APIFY_API_TOKEN=
"@ | Out-File -FilePath $envFile -Encoding utf8
    Write-Host "[OK] Tao file .env (hay dien token sau)" -ForegroundColor Green
}

# 4. Kiem tra va sua encoding trong cac file Python
$filesToFix = @("database.py", "agents.py", "main.py", "campaign_intelligence.py")
foreach ($f in $filesToFix) {
    $full = "$root\$f"
    if (Test-Path $full) {
        $content = Get-Content $full -Raw -Encoding utf8 -ErrorAction SilentlyContinue
        if ($content -match '✅') {
            $newContent = $content -replace '✅', '[OK]' -replace '🔥', '[HOT]' -replace '⚠️', '[WARN]'
            $newContent = $newContent -replace 'Đã', 'Da' -replace 'đã', 'da'
            $newContent = $newContent -replace 'của', 'cua' -replace 'một', 'mot'
            Set-Content -Path $full -Value $newContent -Encoding utf8 -Force
            Write-Host "[FIX] Da sua encoding trong $f" -ForegroundColor Green
        } else {
            Write-Host "[OK] $f da ok encoding" -ForegroundColor Green
        }
    } else {
        Write-Host "[WARN] Thieu file $f" -ForegroundColor Yellow
        $errorCount++
    }
}

# 5. Kiem tra va tao cac file templates (neu thieu)
$templates = @{
    "dashboard.html" = @'
<!DOCTYPE html>
<html>
<head><title>Dashboard</title></head>
<body>
    <h1>Chao {{ session.user }} ({{ role }})</h1>
    <a href="/campaigns">Campaign Manager</a> | <a href="/logout">Logout</a>
    <h2>Kho bai dang</h2>
    <ul>
    {% for platform, count in counts.items() %}
        <li><a href="/posts/{{ platform }}">{{ platform.upper() }} ({{ count }})</a></li>
    {% endfor %}
    </ul>
</body>
</html>
'@
    "posts.html" = @'
<!DOCTYPE html>
<html>
<head><title>Posts</title></head>
<body>
    <h2>Bai dang cho {{ platform.upper() }}</h2>
    <a href="/dashboard">Back</a>
    <ul>
    {% for post in posts %}
        <li>
            <p>{{ post.caption }}</p>
            <small>Link: {{ post.link }}</small>
            <form method="post" action="/post_to_fb">
                <input type="hidden" name="post_id" value="{{ post.id }}">
                <input type="hidden" name="platform" value="{{ platform }}">
                <button type="submit">Dang len Facebook</button>
            </form>
        </li>
    {% endfor %}
    </ul>
</body>
</html>
'@
    "campaigns.html" = @'
<!DOCTYPE html>
<html><head><title>Campaigns</title></head><body>
<h1>Campaign Manager</h1>
<a href="/dashboard">Dashboard</a> | <a href="/campaign/new">New Campaign</a> | <a href="/logout">Logout</a>
<h2>Danh sach chien dich</h2>
<table border=1>
<tr><th>ID</th><th>Name</th><th>Platform</th><th>Budget</th><th>Goal</th><th>Status</th><th>Action</th></tr>
{% for c in campaigns %}
<tr><td>{{ c[0] }}</td><td>{{ c[1] }}</td><td>{{ c[2] }}</td><td>{{ c[5] }}</td><td>{{ c[6] }}</td><td>{{ c[7] }}</td><td><a href="/campaign/{{ c[0] }}/predict">Predict</a></td></tr>
{% endfor %}
</table>
</body></html>
'@
    "new_campaign.html" = @'
<!DOCTYPE html>
<html><head><title>New Campaign</title></head><body>
<h2>New Campaign</h2>
<form method=post>
Name: <input name=name required><br>
Platform: <select name=platform><option>tiktok</option><option>facebook</option><option>shopee</option><option>lazada</option><option>zalo</option><option>alibaba</option></select><br>
Start Date: <input type=date name=start_date><br>
End Date: <input type=date name=end_date><br>
Budget: <input type=number name=budget step=1000 required><br>
Goal: <select name=goal><option>engagement</option><option>sales</option><option>reach</option></select><br>
Products:<br>
{% for p in products %}
    <input type=checkbox name=product_ids value="{{ p[0] }}"> {{ p[1] }} ({{ p[2] }} VND)<br>
{% endfor %}
<button type=submit>Create</button>
</form>
<a href="/campaigns">Back</a>
</body></html>
'@
    "campaign_predict.html" = @'
<!DOCTYPE html>
<html><head><title>Prediction</title></head><body>
<h2>Prediction for Campaign {{ campaign_id }}</h2>
{% if prediction %}
<p>Posts: {{ prediction.predicted_posts }}</p>
<p>Likes: {{ prediction.predicted_likes }}</p>
<p>Sales: {{ prediction.predicted_sales }}</p>
<p>Revenue: {{ prediction.predicted_revenue }} VND</p>
<hr>
<form method=post action="/campaign/{{ campaign_id }}/evaluate">
<h3>Actual results:</h3>
Posts: <input type=number name=actual_posts><br>
Likes: <input type=number name=actual_likes><br>
Sales: <input type=number name=actual_sales><br>
Revenue: <input type=number name=actual_revenue step=1000><br>
<button type=submit>Evaluate</button>
</form>
{% else %}
<p>No prediction</p>
{% endif %}
<a href="/campaigns">Back</a>
</body></html>
'@
}
foreach ($name in $templates.Keys) {
    $full = "$root\templates\$name"
    if (-not (Test-Path $full)) {
        $templates[$name] | Out-File -FilePath $full -Encoding utf8
        Write-Host "[OK] Tao file $name" -ForegroundColor Green
    } else {
        Write-Host "[OK] File $name da ton tai" -ForegroundColor Green
    }
}

# 6. Kiem tra xem co san pham trong database khong
Write-Host "[2] Kiem tra du lieu san pham..." -ForegroundColor Yellow
$productCount = python -c "import sqlite3; conn = sqlite3.connect(r'$dbPath'); cur=conn.cursor(); cur.execute('SELECT COUNT(*) FROM products'); print(cur.fetchone()[0]); conn.close()" 2>$null
if ($productCount -eq 0 -or $productCount -eq "") {
    Write-Host "Chua co san pham. Dang chay pipeline..." -ForegroundColor Yellow
    python main.py --run-pipeline
} else {
    Write-Host "Da co $productCount san pham" -ForegroundColor Green
}

# 7. Khoi dong lai web server
Write-Host "`n=== HOAN TAT ===" -ForegroundColor Cyan
if ($errorCount -eq 0) {
    Write-Host "Moi thu da san sang. Chay: python main.py" -ForegroundColor Green
    Write-Host "Truy cap: http://localhost:5000 (admin/admin123)" -ForegroundColor Yellow
} else {
    Write-Host "Co $errorCount loi. Hay kiem tra lai cac file." -ForegroundColor Red
}