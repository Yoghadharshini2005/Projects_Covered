from flask import Blueprint, request, jsonify, session
from models.user_model import get_db
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DB_PATH
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ml'))
from predictor import CareerPredictor
from resume_analyzer import analyze_resume_text, suggest_careers_from_resume, extract_text_from_pdf_bytes

predict_bp = Blueprint('prediction', __name__)
_predictor = CareerPredictor()

@predict_bp.route('/predict-career', methods=['POST'])
def predict_career_public():
    # Public version - require input directly
    data = request.get_json()
    profile = data.get('profile', {})
    assessment = data.get('assessment', {})
    user_type = data.get('user_type', 'college')
    result = _predictor.predict(profile, assessment, user_type)
    return jsonify(result)

@predict_bp.route('/api/predict', methods=['POST'])
def predict():
    if 'user_id' not in session: return jsonify({'error':'Not authenticated'}), 401
    conn = get_db(DB_PATH)
    pr = conn.execute('SELECT profile_data FROM profiles WHERE user_id=?',(session['user_id'],)).fetchone()
    ar = conn.execute('SELECT responses FROM assessments WHERE user_id=?',(session['user_id'],)).fetchone()
    if not pr or not ar: conn.close(); return jsonify({'error':'Complete profile and assessment first'}), 400
    result = _predictor.predict(json.loads(pr['profile_data']), json.loads(ar['responses']), session['user_type'])
    if conn.execute('SELECT id FROM recommendations WHERE user_id=?',(session['user_id'],)).fetchone():
        conn.execute('''UPDATE recommendations SET primary_career=?,confidence_score=?,all_scores=?,
            skill_gaps=?,skills_have=?,roadmap=?,market_insights=?,model_used=?,model_accuracy=?
            WHERE user_id=?''', (result['primary_career'],result['confidence_score'],
            json.dumps(result['all_scores']),json.dumps(result['skill_gaps']),
            json.dumps(result.get('skills_have',[])),json.dumps(result['roadmap']),
            json.dumps(result.get('market_insights',{})),result.get('model_used',''),
            result.get('model_accuracy',0),session['user_id']))
    else:
        conn.execute('''INSERT INTO recommendations(user_id,primary_career,confidence_score,all_scores,
            skill_gaps,skills_have,roadmap,market_insights,model_used,model_accuracy)
            VALUES(?,?,?,?,?,?,?,?,?,?)''', (session['user_id'],result['primary_career'],
            result['confidence_score'],json.dumps(result['all_scores']),
            json.dumps(result['skill_gaps']),json.dumps(result.get('skills_have',[])),
            json.dumps(result['roadmap']),json.dumps(result.get('market_insights',{})),
            result.get('model_used',''),result.get('model_accuracy',0)))
    conn.commit(); conn.close()
    return jsonify(result)

@predict_bp.route('/api/results')
def get_results():
    if 'user_id' not in session: return jsonify({'error':'Not authenticated'}), 401
    conn = get_db(DB_PATH)
    rec = conn.execute('SELECT * FROM recommendations WHERE user_id=?',(session['user_id'],)).fetchone()
    conn.close()
    if not rec: return jsonify({'results':None})
    return jsonify({
        'primary_career':   rec['primary_career'],
        'confidence_score': rec['confidence_score'],
        'all_scores':       json.loads(rec['all_scores']),
        'skill_gaps':       json.loads(rec['skill_gaps']),
        'skills_have':      json.loads(rec['skills_have'] or '[]'),
        'roadmap':          json.loads(rec['roadmap']),
        'market_insights':  json.loads(rec['market_insights'] or '{}'),
        'model_used':       rec['model_used'],
        'model_accuracy':   rec['model_accuracy'],
    })

@predict_bp.route('/api/resume', methods=['POST'])
def analyze_resume():
    if 'user_id' not in session: return jsonify({'error':'Not authenticated'}), 401
    if 'resume' not in request.files:
        return jsonify({'error':'No file uploaded'}), 400
    file = request.files['resume']
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'error':'Only PDF files are supported'}), 400
    pdf_bytes = file.read()
    text, err = extract_text_from_pdf_bytes(pdf_bytes)
    if err: return jsonify({'error': err}), 400
    if not text or len(text.strip()) < 50:
        return jsonify({'error':'Could not extract text from PDF. Try a text-based PDF.'}), 400
    analysis = analyze_resume_text(text)
    career_suggestions = suggest_careers_from_resume(analysis['found_skills'])
    analysis['career_suggestions'] = [{'career':c,'match':s} for c,s in career_suggestions[:5]]
    conn = get_db(DB_PATH)
    conn.execute('INSERT INTO resume_analyses(user_id,filename,analysis_data) VALUES(?,?,?)',
        (session['user_id'], file.filename, json.dumps(analysis)))
    conn.commit(); conn.close()
    return jsonify({'success':True, 'analysis': analysis})

@predict_bp.route('/api/resume/latest')
def get_latest_resume():
    if 'user_id' not in session: return jsonify({'error':'Not authenticated'}), 401
    conn = get_db(DB_PATH)
    r = conn.execute('SELECT * FROM resume_analyses WHERE user_id=? ORDER BY created_at DESC LIMIT 1',(session['user_id'],)).fetchone()
    conn.close()
    if not r: return jsonify({'resume':None})
    return jsonify({'resume': json.loads(r['analysis_data']), 'filename': r['filename']})

@predict_bp.route('/api/chat', methods=['POST'])
def chat():
    if 'user_id' not in session: return jsonify({'error':'Not authenticated'}), 401
    msg = request.get_json().get('message','').lower().strip()
    conn = get_db(DB_PATH)
    rec = conn.execute('SELECT primary_career FROM recommendations WHERE user_id=?',(session['user_id'],)).fetchone()
    conn.close()
    career = rec['primary_career'] if rec else 'your chosen field'
    return jsonify({'response': _get_chat_response(msg, career)})

def _get_chat_response(msg, career):
    kw_map = {
        'certification': f"Top certifications for **{career}**: AWS/Google Professional certs, Coursera Specializations, LinkedIn Learning, and vendor-specific certificates. Start foundational then advance.",
        'salary':        f"**{career}** salary in India: Entry-level ₹4–8 LPA → Mid-level ₹12–25 LPA → Senior ₹30–60+ LPA. Varies by company, city, and skills stack.",
        'interview':     f"**{career}** interview tips: 1) Practice DSA on LeetCode 2) Build 3 solid projects 3) Know system design basics 4) Study company's tech stack 5) Prepare STAR behavioral stories.",
        'learn':         f"Best platforms for **{career}**: Coursera, Udemy, edX for courses. GitHub for practice. YouTube: Traversy Media, Fireship, Tech With Tim, freeCodeCamp.",
        'skill':         f"Core skills for **{career}**: Strong fundamentals, problem-solving ability, version control (Git), communication, and domain-specific tech stack.",
        'trend':         f"2024-25 **{career}** trends: AI integration everywhere, cloud-first architecture, microservices, DevOps culture, and remote-first hybrid teams dominate.",
        'job':           f"Job hunting for **{career}**: Build GitHub portfolio, optimize LinkedIn headline, contribute to open source, network at meetups, target 3–5 quality applications/day.",
        'roadmap':       f"**{career}** roadmap: Months 1–2 → Core fundamentals | Months 3–4 → Build projects | Month 5 → Open source | Month 6 → Portfolio + job applications.",
        'resume':        f"Resume tips for **{career}**: Use ATS-friendly format, list measurable achievements (not just duties), include GitHub link, quantify impact (e.g., 'reduced load time 40%').",
        'college':       f"During college for **{career}**: Take online certs, build 3–5 projects, contribute to open source, participate in hackathons, and do at least 1 internship.",
        'fresher':       f"As a fresher targeting **{career}**: Start with fundamentals, build 3 projects, create GitHub profile, apply for internships, and network on LinkedIn actively.",
        'switch':        f"Switching to **{career}**: Identify transferable skills, complete 1 relevant certification, build a portfolio project, update LinkedIn, and target bridge roles first.",
    }
    for key, resp in kw_map.items():
        if key in msg:
            return resp
    if any(w in msg for w in ['hi','hello','hey','hii','howdy']):
        return f"Hello! 👋 I'm your AI Career Mentor. I specialise in guidance for **{career}** and can help with certifications, salary info, interview tips, learning resources, job hunting, and career trends. What would you like to explore?"
    if 'help' in msg:
        return "I can help you with: **certifications**, salary expectations, interview preparation, learning resources, skill gap analysis, job hunting strategy, resume tips, and industry trends. What would you like to know?"
    if any(w in msg for w in ['thanks','thank','great','awesome']):
        return f"You're welcome! 😊 Keep pushing towards your **{career}** goals. Consistency is key — small steps every day lead to big results. Anything else I can help you with?"
    return f"That's a strong career question about **{career}**! I can provide a complete answer on certifications, salary expectations, interview preparation, resume best practices, learning resources, job search strategy, or career trends. Tell me what you want to know and I'll help you with it."

@predict_bp.route('/api/admin/stats')
def admin_stats():
    conn = get_db(DB_PATH)
    total  = conn.execute('SELECT COUNT(*) as c FROM users').fetchone()['c']
    s12    = conn.execute("SELECT COUNT(*) as c FROM users WHERE user_type='student12'").fetchone()['c']
    col    = conn.execute("SELECT COUNT(*) as c FROM users WHERE user_type='college'").fetchone()['c']
    emp    = conn.execute("SELECT COUNT(*) as c FROM users WHERE user_type='employee'").fetchone()['c']
    assess = conn.execute('SELECT COUNT(*) as c FROM assessments').fetchone()['c']
    recs   = conn.execute('SELECT primary_career,model_used,confidence_score FROM recommendations').fetchall()
    resumes= conn.execute('SELECT COUNT(*) as c FROM resume_analyses').fetchone()['c']
    conn.close()
    career_dist = {}
    conf_scores = []
    model_usage = {}
    for r in recs:
        c = r['primary_career']; career_dist[c] = career_dist.get(c,0)+1
        if r['confidence_score']: conf_scores.append(r['confidence_score'])
        m = r['model_used'] or 'Unknown'; model_usage[m] = model_usage.get(m,0)+1
    return jsonify({
        'total_users': total,
        'by_type': {'student12':s12,'college':col,'employee':emp},
        'career_distribution': career_dist,
        'total_assessments': assess,
        'total_recommendations': len(recs),
        'total_resumes': resumes,
        'avg_confidence': round(sum(conf_scores)/len(conf_scores),1) if conf_scores else 0,
        'model_usage': model_usage,
    })
