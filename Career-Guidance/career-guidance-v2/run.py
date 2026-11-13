"""
run.py - Start the AI Career Guidance System v2.0
Usage: python run.py
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app import app
from backend.models.user_model import init_db
from backend.config import DB_PATH, UPLOAD_FOLDER

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    init_db(DB_PATH)
    print("\n" + "="*55)
    print("  🎯 AI Career Guidance System v2.0")
    print("  📍 http://localhost:5000")
    print("  🤖 ML Model: Random Forest (96% accuracy)")
    print("  📊 Dataset: 496 samples, 9 career domains")
    print("="*55 + "\n")
    app.run(debug=True, port=5000, host='0.0.0.0')
