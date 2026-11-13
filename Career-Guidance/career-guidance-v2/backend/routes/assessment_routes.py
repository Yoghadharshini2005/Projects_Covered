from flask import Blueprint, request, jsonify, session
from models.user_model import get_db
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DB_PATH

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from backend.services.assessment_service import get_questions, evaluate_answers

assess_bp = Blueprint('assessment', __name__, url_prefix='/api')

@assess_bp.route('/assessment', methods=['GET'])
def assessment_questions():
    skill = request.args.get('skill')
    count = int(request.args.get('count', 10))
    questions = get_questions(skill, count)
    return jsonify({'questions': questions})

@assess_bp.route('/submit-assessment', methods=['POST'])
def submit_assessment():
    data = request.get_json()
    result = evaluate_answers(data['answers'])
    return jsonify(result)

@assess_bp.route('/assessment', methods=['POST'])
def save_assessment():
    if 'user_id' not in session: return jsonify({'error':'Not authenticated'}), 401
    d = request.get_json()
    conn = get_db(DB_PATH)
    if conn.execute('SELECT id FROM assessments WHERE user_id=?',(session['user_id'],)).fetchone():
        conn.execute('UPDATE assessments SET responses=? WHERE user_id=?',(json.dumps(d),session['user_id']))
    else:
        conn.execute('INSERT INTO assessments(user_id,responses) VALUES(?,?)',(session['user_id'],json.dumps(d)))
    conn.commit(); conn.close()
    return jsonify({'success':True})

@assess_bp.route('/api/assessment')
def get_assessment():
    if 'user_id' not in session: return jsonify({'error':'Not authenticated'}), 401
    conn = get_db(DB_PATH)
    a = conn.execute('SELECT responses FROM assessments WHERE user_id=?',(session['user_id'],)).fetchone()
    conn.close()
    return jsonify({'responses': json.loads(a['responses']) if a else None})
