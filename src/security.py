# src/security.py
import os
from werkzeug.security import check_password_hash

# Danh sách CCCD hợp lệ (chỉ lưu hash, nhưng đơn giản thì dùng plain)
VALID_CCCD = ['075097016965', '075088008608']

def verify_cccd(cccd):
    """Kiểm tra CCCD có hợp lệ không"""
    return cccd in VALID_CCCD

def get_sensitive_info(cccd):
    """Chỉ trả về thông tin nhạy cảm nếu CCCD đúng"""
    if cccd == '075097016965':
        return {
            'fullname': 'Nguyễn Hoàng Đức',
            'dob': '07/07/1997',
            'phone': '0326014497',
            'role': 'Sáng lập, thiết kế chính',
            'cccd': '075097016965'
        }
    elif ccd == '075088008608':
        return {
            'fullname': 'Nguyễn Thanh Tiến',
            'dob': '16/10/1988',
            'phone': '0971136712',
            'role': 'Đồng sáng lập',
            'cccd': '075088008608'
        }
    return None

def get_public_info():
    """Thông tin công khai, không nhạy cảm"""
    return {
        'system_name': 'AI_OS_KERNEL_V3',
        'founders': 'Đồng sáng lập dự án SEN',
        'description': 'Nhân hệ điều hành AI mô-đun cho tự động hóa Affiliate'
    }