import os
import shutil

import joblib
import numpy as np

from src.config import ROOT_DIR


MODEL_PATH = ROOT_DIR / "models" / "sales_prediction_model.pkl"
FP16_PATH = ROOT_DIR / "models" / "sales_prediction_model_fp16.pkl"
FP16_NEW_PATH = ROOT_DIR / "models" / "sales_prediction_model_fp16.new.pkl"


def ensure_model():
    if MODEL_PATH.exists():
        return

    print("Model not found, creating dummy model for testing")
    from sklearn.ensemble import RandomForestRegressor

    model = RandomForestRegressor(n_estimators=10, random_state=42)
    model.fit(np.random.rand(100, 3), np.random.rand(100))
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)


def quantize_model():
    ensure_model()
    model = joblib.load(MODEL_PATH)

    if hasattr(model, "estimators_"):
        for estimator in model.estimators_:
            if hasattr(estimator, "tree_") and hasattr(estimator.tree_, "value"):
                estimator.tree_.value = estimator.tree_.value.astype(np.float16)

    joblib.dump(model, FP16_NEW_PATH)
    try:
        shutil.move(str(FP16_NEW_PATH), str(FP16_PATH))
        output_path = FP16_PATH
    except PermissionError:
        output_path = FP16_NEW_PATH
        print(f"Could not replace locked model; wrote {FP16_NEW_PATH.name} instead")

    original_size = os.path.getsize(MODEL_PATH) / 1024
    fp16_size = os.path.getsize(output_path) / 1024
    reduction = (1 - fp16_size / original_size) * 100 if original_size else 0
    print(f"Original size: {original_size:.2f} KB")
    print(f"FP16 size: {fp16_size:.2f} KB")
    print(f"Reduction: {reduction:.1f}%")
    return output_path


if __name__ == "__main__":
    quantize_model()
