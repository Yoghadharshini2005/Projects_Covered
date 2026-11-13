import os, sys
from flask import Blueprint, request, jsonify
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from backend.services.course_recommendation import get_recommended_courses
from backend.services.skill_gap_service import analyze_skill_gap
from backend.models.user_model import get_db
from backend.config import DB_PATH

course_bp = Blueprint('courses', __name__, url_prefix='/api')

@course_bp.route('/recommend-courses', methods=['GET'])
def recommend_courses():
    career = request.args.get('career')
    user_skills = request.args.get('user_skills', '').split(',')
    # Get gaps
    gaps = analyze_skill_gap(user_skills, career)['missing_skills']
    recs = get_recommended_courses(gaps)
    return jsonify({'missing_skills': gaps, 'recommendations': recs})

@course_bp.route('/courses', methods=['GET'])
def list_courses():
    conn = get_db(DB_PATH)
    courses = conn.execute('SELECT * FROM courses').fetchall()
    conn.close()
    return jsonify([dict(course) for course in courses])

