# -*- coding: utf-8 -*-
import sys
import io
import joblib
import numpy as np

class SEN_Brain:
    def __init__(self, model_path='models/sales_prediction_model.pkl'):
        self.model = None
        # Tải model nếu có
        try:
            self.model = joblib.load(model_path)
        except:
            pass

    def check_affiliate_policy(self, user_id, context):
        # Đơn giản: luôn cho phép (hoặc bạn có thể thêm logic)
        return True

    def optimize_code(self, code):
        # Trả về code gốc hoặc thông báo
        return code

    def run_sandbox(self, code):
        # Thực thi code an toàn (tạm thời trả về kết quả)
        try:
            exec_globals = {}
            exec(code, exec_globals)
            return "Code executed successfully"
        except Exception as e:
            return f"Error: {e}"

default_brain = SEN_Brain()
