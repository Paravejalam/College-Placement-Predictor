# loader.py
import joblib
from pathlib import Path

MODEL_PATH = Path("model/model.pkl")

def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError("model/model.pkl not found")

    return joblib.load(MODEL_PATH)
