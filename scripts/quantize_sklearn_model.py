import joblib
import numpy as np
import onnx
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType
import onnxruntime as ort

# Load model gốc
model = joblib.load('models/sales_prediction_model.pkl')

# Xác định đầu vào (số feature)
n_features = model.n_features_in_  # hoặc tự xác định
initial_type = [('float_input', FloatTensorType([None, n_features]))]

# Chuyển sang ONNX
onnx_model = convert_sklearn(model, initial_types=initial_type)

# Lưu ONNX
with open('models/sales_prediction_model.onnx', 'wb') as f:
    f.write(onnx_model.SerializeToString())

# Lượng tử hóa ONNX (int8)
from onnxruntime.quantization import quantize_dynamic, QuantType
quantized_model_path = 'models/sales_prediction_model_quantized.onnx'
quantize_dynamic(onnx_model, quantized_model_path, weight_type=QuantType.QInt8)

print("✅ Model đã được lượng tử hóa và lưu tại:", quantized_model_path)

# Kiểm tra kích thước
import os
orig_size = os.path.getsize('models/sales_prediction_model.pkl') / 1024
quant_size = os.path.getsize(quantized_model_path) / 1024
print(f"Kích thước gốc: {orig_size:.2f} KB")
print(f"Sau lượng tử hóa: {quant_size:.2f} KB")
print(f"Giảm: {(1 - quant_size/orig_size)*100:.1f}%")
