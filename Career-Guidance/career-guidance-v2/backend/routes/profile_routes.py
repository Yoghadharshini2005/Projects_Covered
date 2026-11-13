from flask import Blueprint, request, jsonify, session
from models.user_model import get_db
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DB_PATH

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/api/profile', methods=['POST'])
def save_profile():
    if 'user_id' not in session: return jsonify({'error':'Not authenticated'}), 401
    d = request.get_json()
    conn = get_db(DB_PATH)
    if conn.execute('SELECT id FROM profiles WHERE user_id=?',(session['user_id'],)).fetchone():
        conn.execute('UPDATE profiles SET profile_data=? WHERE user_id=?',(json.dumps(d),session['user_id']))
    else:
        conn.execute('INSERT INTO profiles(user_id,profile_data) VALUES(?,?)',(session['user_id'],json.dumps(d)))
    conn.execute('UPDATE users SET profile_complete=1 WHERE id=?',(session['user_id'],))
    conn.commit(); conn.close()
    return jsonify({'success':True})

@profile_bp.route('/api/profile')
def get_profile():
    if 'user_id' not in session: return jsonify({'error':'Not authenticated'}), 401
    conn = get_db(DB_PATH)
    p = conn.execute('SELECT profile_data FROM profiles WHERE user_id=?',(session['user_id'],)).fetchone()
    conn.close()
    return jsonify({'profile':json.loads(p['profile_data']) if p else None})
