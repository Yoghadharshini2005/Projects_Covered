"""
app.py - Main Flask application entry point
Career Guidance AI System v2.0
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template
from routes.auth_routes import auth_bp
from routes.profile_routes import profile_bp
from routes.assessment_routes import assess_bp
from routes.prediction_routes import predict_bp
from routes.skill_gap_routes import skill_bp
from routes.course_routes import course_bp
from routes.admin_routes import admin_bp
from models.user_model import init_db
from config import SECRET_KEY, DB_PATH, UPLOAD_FOLDER

app = Flask(__name__,
    template_folder=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend', 'templates'),
    static_folder=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend', 'static'))

app.secret_key = SECRET_KEY

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(assess_bp)
app.register_blueprint(predict_bp)
app.register_blueprint(skill_bp)
app.register_blueprint(course_bp)
app.register_blueprint(admin_bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    init_db(DB_PATH)
    print("\n" + "="*55)
    print("  AI Career Guidance System v2.0")
    print("  Running at: http://localhost:5000")
    print("="*55 + "\n")
    app.run(debug=True, port=5000)
