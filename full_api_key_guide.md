# HƯỚNG DẪN LẤY VÀ CẤU HÌNH API KEY CHO DỰ ÁN AI_OS_KERNEL_V3

## 1. API Key của Claude (Anthropic) – bắt buộc

### Bước 1: Tạo tài khoản nhà phát triển
- Truy cập: https://console.anthropic.com/
- Đăng ký bằng email (nên dùng Gmail/Outlook) hoặc đăng nhập Google.
- Xác thực email qua link gửi về hộp thư.

### Bước 2: Xác thực số điện thoại
- Nhập số điện thoại thật (quốc tế, trả trước hoặc thuê bao chính chủ).
- Nhận mã SMS và nhập vào form.

### Bước 3: Nạp credit (tối thiểu 5 USD)
- Vào mục **"Billing" → "Buy Credits"**.
- Thanh toán bằng thẻ Visa/MasterCard quốc tế hoặc các cổng trung gian (Wise, Depay, v.v.).
- **Lưu ý:** Claude API không có gói miễn phí, cần credit thì mới gọi thành công.

### Bước 4: Tạo API key
- Vào **"API Keys"** → **"Create Key"**.
- Đặt tên (ví dụ: `AI_OS_KERNEL_V3`), bấm **"Create"**.
- Copy key dạng `sk-ant-xxxx...` và **lưu ngay** (chỉ hiện một lần).

### Bước 5: Cấu hình trong dự án
- Trong PowerShell (tại thư mục dự án):
  ```powershell
  $env:ANTHROPIC_API_KEY = "sk-ant-xxxx..."