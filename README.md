# AI_OS Campaign Intelligence System

## Mô tả
Hệ thống tự động tạo chiến dịch affiliate, dự đoán doanh số, đánh giá kết quả và tối ưu thuật toán bằng machine learning.

## Cài đặt
1. Cài Python 3.10+, tạo môi trường ảo.
2. Cài dependencies: `pip install -r requirements.txt`
3. Tạo database: `python -c "from src.database import init_db; init_db()"`
4. Chạy pipeline lấy sản phẩm mẫu: `python -m src.main --run-pipeline`

## Sử dụng
- Chạy web app: `python -m src.main`, truy cập `http://localhost:5000`
- Tài khoản: admin / admin123
- Tạo chiến dịch: Campaign Manager -> New Campaign
- Xem dự đoán, đánh giá kết quả (sau khi chạy thực tế)

## Môi Trường Ảo Riêng
- Tạo môi trường riêng cho dự án:
  `powershell -ExecutionPolicy Bypass -File .\scripts\setup_project_venv.ps1`
- Kích hoạt:
  `.\.venv_aios\Scripts\Activate.ps1`
- Kiểm tra cấu trúc:
  `python scripts\validate.py`

## NotebookLM Pro
- Trang web: `/notebooklm`
- API trạng thái: `GET /api/notebooklm/status`
- API hỏi đáp: `POST /api/notebooklm/ask`
- Nếu có `nlm` CLI và `NOTEBOOKLM_NOTEBOOK_ID`, hệ thống dùng NotebookLM thật.
- Nếu chưa cấu hình NotebookLM, hệ thống fallback sang file export local `AI_OS_KERNEL_V3_FULL_EXPORT.md`.

## Local-First AI Controller
- `src.agents` now uses Local LLM as the primary logic controller through `LOCAL_LLM_COMMAND`.
- Default local command: `ollama run llama3.2`.
- External APIs such as DeepSeek/OpenAI are fallback only.
- CRM assistant: `src/agents/crm_bot.py`.

## Quản Lý API Key
- Audit key không lộ secret:
  `python scripts\audit_api_keys.py`
- Báo cáo sinh ra tại `API_KEY_AUDIT.md`.
- Nhập key thủ công an toàn:
  `python scripts\credential_agent.py set FACEBOOK_PAGE_ACCESS_TOKEN`
- Tool này không thu thập cookie hoặc scrape credential từ nền tảng khác.

## Tối ưu tự động
- Hệ thống tự động điều chỉnh tham số `post_factor`, `like_per_post`, `conversion_rate` dựa trên độ chính xác.
- Chạy `python auto_train_campaigns.py` để tạo nhiều chiến dịch mô phỏng, giúp thuật toán nhanh chóng hội tụ.

## Tích hợp API thật
- **TikTok Shop**: Đăng ký Apify, lấy token, thêm vào .env (APIFY_API_TOKEN)
- **Facebook**: Lấy Page Access Token, thêm vào .env (FACEBOOK_ACCESS_TOKEN)
- Sau đó chạy pipeline để lấy sản phẩm thật và đăng bài thật từ giao diện web.

## Xem biểu đồ độ chính xác
- Chạy `python plot_accuracy.py`

## DevWeb F12 Agent
- Phân tích console, network, DOM, storage keys, performance và tạo báo cáo:
  `python scripts\devweb_f12_agent.py http://localhost:5000 --headed`
- Tool tự động redact cookie, authorization header và token trong query string.
- Báo cáo nằm trong `reports/devweb/` dưới dạng JSON và Markdown.

## Quick & Full Build Modules
- Media image generation: `src/media/image_gen.py`
- Review Station: `/review_station`
- Marketplace workers: `worker/lazada_worker.py`, `worker/amazon_worker.py`, `worker/tiktok_shop_api.py`
- Intelligence sandbox: `src/ml/algo_simulator.py`
- Market mood tracking: `src/learning/sentiment_analyzer.py`

## Liên hệ
[Thông tin của bạn]
