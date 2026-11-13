from flask import Blueprint, request, jsonify, session
from models.user_model import get_db, hash_pw, get_user_by_email
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DB_PATH

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/register', methods=['POST'])
def register():
    d = request.get_json()
    if not all(k in d for k in ['name','email','password','user_type']):
        return jsonify({'error':'All fields required'}), 400
    conn = get_db(DB_PATH)
    if get_user_by_email(conn, d['email']):
        conn.close(); return jsonify({'error':'Email already registered'}), 400
    conn.execute('INSERT INTO users(name,email,password,user_type) VALUES(?,?,?,?)',
        (d['name'].strip(), d['email'].strip().lower(), hash_pw(d['password']), d['user_type']))
    conn.commit()
    user = get_user_by_email(conn, d['email'].strip().lower())
    conn.close()
    session.permanent = True
    session['user_id']=user['id']; session['user_type']=user['user_type']; session['user_name']=user['name']
    return jsonify({'success':True,'user_type':user['user_type'],'name':user['name']})

@auth_bp.route('/api/login', methods=['POST'])
def login():
    d = request.get_json()
    conn = get_db(DB_PATH)
    user = get_user_by_email(conn, d.get('email','').strip().lower())
    if not user or user['password'] != hash_pw(d.get('password','')):
        conn.close(); return jsonify({'error':'Invalid email or password'}), 401
    rec = conn.execute('SELECT id FROM recommendations WHERE user_id=?',(user['id'],)).fetchone()
    conn.close()
    session['user_id']=user['id']; session['user_type']=user['user_type']; session['user_name']=user['name']
    return jsonify({'success':True,'user_type':user['user_type'],'name':user['name'],
        'profile_complete':bool(user['profile_complete']),'has_results':rec is not None})

@auth_bp.route('/api/logout', methods=['POST'])
def logout():
    session.clear(); return jsonify({'success':True})

@auth_bp.route('/api/session')
def get_session():
    if 'user_id' not in session: return jsonify({'logged_in':False})
    conn = get_db(DB_PATH)
    user = conn.execute('SELECT * FROM users WHERE id=?',(session['user_id'],)).fetchone()
    if not user: session.clear(); conn.close(); return jsonify({'logged_in':False})
    rec  = conn.execute('SELECT id FROM recommendations WHERE user_id=?',(user['id'],)).fetchone()
    resume = conn.execute('SELECT id FROM resume_analyses WHERE user_id=? ORDER BY created_at DESC LIMIT 1',(user['id'],)).fetchone()
    conn.close()
    return jsonify({'logged_in':True,'user_type':user['user_type'],'name':user['name'],
        'profile_complete':bool(user['profile_complete']),'has_results':rec is not None,
        'has_resume':resume is not None})
