import json, os, sys
from flask import Blueprint, request, jsonify, session
from backend.models.user_model import get_db
from backend.config import DB_PATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

def is_admin():
    return session.get('is_admin', 0) == 1

@admin_bp.route('/add-job', methods=['POST'])
def add_job():
    if not is_admin(): return jsonify({'error': 'Admin only'}), 403
    data = request.get_json()
    job = data['job_role']
    skills = data['required_skills']
    conn = get_db(DB_PATH)
    conn.execute('INSERT OR REPLACE INTO job_roles (job_role, required_skills) VALUES (?, ?)',
                 (job, json.dumps(skills)))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'job': job})

@admin_bp.route('/add-course', methods=['POST'])
def add_course():
    if not is_admin(): return jsonify({'error': 'Admin only'}), 403
    data = request.get_json()
    course = data['course_name']
    stream = data['stream']
    skills = data['skills_gained']
    conn = get_db(DB_PATH)
    conn.execute('INSERT OR REPLACE INTO courses (course_name, stream, skills_gained) VALUES (?, ?, ?)',
                 (course, stream, json.dumps(skills)))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'course': course})

@admin_bp.route('/add-question', methods=['POST'])
def add_question():
    if not is_admin(): return jsonify({'error': 'Admin only'}), 403
    data = request.get_json()
    conn = get_db(DB_PATH)
    conn.execute('INSERT INTO questions (question, skill, options, answer) VALUES (?, ?, ?, ?)',
                 (data['question'], data['skill'], json.dumps(data['options']), data['answer']))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@admin_bp.route('/users', methods=['GET'])
def list_users():
    if not is_admin(): return jsonify({'error': 'Admin only'}), 403
    conn = get_db(DB_PATH)
    users = conn.execute('SELECT id, name, email, user_type, created_at FROM users').fetchall()
    conn.close()
    return jsonify([dict(u) for u in users])

