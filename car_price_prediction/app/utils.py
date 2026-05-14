import json
import numpy as np
import pickle
import os
from CONFIG import MODEL_PATH, COLUMNS_PATH, ENCODE_PATH

class Prediction:
    def __init__(self):
        try:
            if not os.path.exists(MODEL_PATH):
                raise FileNotFoundError(f"Model file not found at: {MODEL_PATH}")

            with open(MODEL_PATH, 'rb') as f:
                self.model = pickle.load(f)

            with open(COLUMNS_PATH, 'r') as f:
                self.columns = json.load(f)

            with open(ENCODE_PATH, 'r') as f:
                self.encodings = json.load(f)

        except Exception as e:
            print("❌ Error loading model or config files:", e)
            self.model = None

    def encode_input(self, data):
        encoded = []
        for idx, col in enumerate(self.columns):
            if idx >= len(data):
                raise ValueError(f"Missing value for column: {col}")
            val = data[idx]

            # Skip encoding if already numeric (assumes form values are encoded)
            if col in self.encodings and not isinstance(val, int):
                val = self.encodings[col].get(str(val), -1)

            encoded.append(val)

        print("✅ Encoded Input:", encoded)
        return np.array(encoded).reshape(1, -1)

    def predict(self, data):
        print("📥 Raw Input Data:", data)

        if self.model is None:
            raise RuntimeError("Model is not loaded. Check model path or loading errors.")

        input_encoded = self.encode_input(data)
        print("🧠 Model Input Shape:", input_encoded.shape)

        prediction = self.model.predict(input_encoded)[0]
        print("💰 Predicted Price:", prediction)

        return prediction
