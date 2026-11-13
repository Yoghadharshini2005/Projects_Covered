import os, sys
from flask import Blueprint, request, jsonify
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from backend.services.skill_gap_service import analyze_skill_gap

skill_bp = Blueprint('skillgap', __name__, url_prefix='/api')

@skill_bp.route('/skill-gap', methods=['POST'])
def skill_gap():
    data = request.get_json()
    user_skills = data.get('user_skills', [])
    target_career = data.get('target_career')
    result = analyze_skill_gap(user_skills, target_career)
    return jsonify(result)

