import os
BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH    = os.path.join(BASE_DIR, 'career_guidance.db')
SECRET_KEY = 'career_guidance_v2_secret_2024'
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB
