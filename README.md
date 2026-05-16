# AI_OS Campaign Intelligence System

## Mô tả
Hệ thống tự động tạo chiến dịch affiliate, dự đoán doanh số, đánh giá kết quả và tối ưu thuật toán bằng machine learning.

## Cài đặt
1. Cài Python 3.10+, tạo môi trường ảo.
2. Cài dependencies: `pip install -r requirements.txt`
3. Tạo database: `python -c "from database import init_db; init_db()"`
4. Chạy pipeline lấy sản phẩm mẫu: `python main.py --run-pipeline`

## Sử dụng
- Chạy web app: `python main.py`, truy cập `http://localhost:5000`
- Tài khoản: admin / admin123
- Tạo chiến dịch: Campaign Manager -> New Campaign
- Xem dự đoán, đánh giá kết quả (sau khi chạy thực tế)

## Tối ưu tự động
- Hệ thống tự động điều chỉnh tham số `post_factor`, `like_per_post`, `conversion_rate` dựa trên độ chính xác.
- Chạy `python auto_train_campaigns.py` để tạo nhiều chiến dịch mô phỏng, giúp thuật toán nhanh chóng hội tụ.

## Tích hợp API thật
- **TikTok Shop**: Đăng ký Apify, lấy token, thêm vào .env (APIFY_API_TOKEN)
- **Facebook**: Lấy Page Access Token, thêm vào .env (FACEBOOK_ACCESS_TOKEN)
- Sau đó chạy pipeline để lấy sản phẩm thật và đăng bài thật từ giao diện web.

## Xem biểu đồ độ chính xác
- Chạy `python plot_accuracy.py`

## Liên hệ
[Thông tin của bạn]