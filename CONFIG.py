from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "5000"))
DEBUG = os.getenv("DEBUG", "True").strip().lower() in {"1", "true", "yes", "on"}
SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret")

APP_DIR = BASE_DIR / "app"
MODEL_PATH = str(APP_DIR / "Car_Pred_Model.pkl")
COLUMNS_PATH = str(APP_DIR / "Column.json")
ENCODE_PATH = str(APP_DIR / "encoded_data.json")