"""
=============================================================
 Predictive Maintenance System — Flask Backend
=============================================================
 Endpoints:
   GET  /                  → Main dashboard
   POST /api/predict        → Predict machine condition
   POST /api/chat           → Intelligent chatbot
   GET  /api/digital-twin  → Digital twin simulation
   GET  /api/history        → Prediction history (SQLite)
   GET  /api/stats          → System stats
   GET  /api/metrics        → Model metrics
=============================================================
"""

import os
import json
import random
import sqlite3
import datetime
import numpy as np
import joblib
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# ─────────────────────────────────────────────
# APP INITIALISATION
# ─────────────────────────────────────────────

app = Flask(__name__)
CORS(app)

# ─────────────────────────────────────────────
# LOAD ML MODEL & SCALER
# ─────────────────────────────────────────────

MODEL_PATH  = 'saved_model/xgb_model.pkl'
SCALER_PATH = 'saved_model/scaler.pkl'
METRICS_PATH = 'saved_model/metrics.json'

xgb_model = joblib.load(MODEL_PATH)
scaler    = joblib.load(SCALER_PATH)

with open(METRICS_PATH) as f:
    model_metrics = json.load(f)

print("[✓] Model and scaler loaded successfully")

# ─────────────────────────────────────────────
# SQLITE DATABASE SETUP
# ─────────────────────────────────────────────

DB_PATH = 'logs/maintenance.db'
os.makedirs('logs', exist_ok=True)

def get_db():
    """Return a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Create tables if they do not exist."""
    conn = get_db()
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS predictions (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            temperature REAL,
            vibration   REAL,
            pressure    REAL,
            rpm         REAL,
            condition   TEXT,
            confidence  REAL,
            timestamp   TEXT
        );

        CREATE TABLE IF NOT EXISTS alerts (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            machine_id  TEXT,
            alert_type  TEXT,
            message     TEXT,
            timestamp   TEXT
        );

        CREATE TABLE IF NOT EXISTS chat_history (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            role      TEXT,
            message   TEXT,
            timestamp TEXT
        );
    ''')
    conn.commit()
    conn.close()
    print("[✓] SQLite database initialised")

init_db()

# ─────────────────────────────────────────────
# HELPER: THRESHOLD-BASED ALERT SYSTEM
# ─────────────────────────────────────────────

THRESHOLDS = {
    'temperature': {'warning': 70, 'failure': 90},
    'vibration':   {'warning': 0.6, 'failure': 1.5},
    'pressure':    {'warning': 80, 'failure': 60},   # Below = bad
    'rpm':         {'warning': 1300, 'failure': 1000} # Below = bad
}

def check_thresholds(temp, vib, pres, rpm):
    """Returns list of threshold-based alert messages."""
    alerts = []
    if temp >= THRESHOLDS['temperature']['failure']:
        alerts.append({'sensor': 'temperature', 'level': 'FAILURE',
                       'value': temp, 'msg': f'Critical overheating: {temp:.1f}°C'})
    elif temp >= THRESHOLDS['temperature']['warning']:
        alerts.append({'sensor': 'temperature', 'level': 'WARNING',
                       'value': temp, 'msg': f'Elevated temperature: {temp:.1f}°C'})

    if vib >= THRESHOLDS['vibration']['failure']:
        alerts.append({'sensor': 'vibration', 'level': 'FAILURE',
                       'value': vib, 'msg': f'Severe vibration: {vib:.2f}g'})
    elif vib >= THRESHOLDS['vibration']['warning']:
        alerts.append({'sensor': 'vibration', 'level': 'WARNING',
                       'value': vib, 'msg': f'Abnormal vibration: {vib:.2f}g'})

    if pres <= THRESHOLDS['pressure']['failure']:
        alerts.append({'sensor': 'pressure', 'level': 'FAILURE',
                       'value': pres, 'msg': f'Critical pressure drop: {pres:.1f} PSI'})
    elif pres <= THRESHOLDS['pressure']['warning']:
        alerts.append({'sensor': 'pressure', 'level': 'WARNING',
                       'value': pres, 'msg': f'Low pressure detected: {pres:.1f} PSI'})

    if rpm <= THRESHOLDS['rpm']['failure']:
        alerts.append({'sensor': 'rpm', 'level': 'FAILURE',
                       'value': rpm, 'msg': f'Critical RPM drop: {rpm:.0f} RPM'})
    elif rpm <= THRESHOLDS['rpm']['warning']:
        alerts.append({'sensor': 'rpm', 'level': 'WARNING',
                       'value': rpm, 'msg': f'Low RPM detected: {rpm:.0f} RPM'})

    return alerts

# ─────────────────────────────────────────────
# HELPER: ROOT CAUSE ANALYSIS ENGINE
# ─────────────────────────────────────────────

def root_cause_analysis(temp, vib, pres, rpm, condition):
    """
    Rule-based RCA engine.
    Identifies probable cause, explanation, and recommended action.
    """
    causes = []

    if temp >= 90:
        causes.append({
            'cause':   'Overheating',
            'sensor':  'Temperature',
            'value':   f'{temp:.1f}°C',
            'explanation': 'Motor/bearing temperature exceeds safe limits. '
                           'Possible causes: coolant failure, blocked ventilation, '
                           'excessive load, or lubrication breakdown.',
            'action':  'Shut down immediately. Inspect cooling system, '
                       'check lubricants, and allow cool-down before restart.'
        })
    elif temp >= 70:
        causes.append({
            'cause':   'Elevated Temperature',
            'sensor':  'Temperature',
            'value':   f'{temp:.1f}°C',
            'explanation': 'Temperature in warning range. May indicate early-stage '
                           'lubrication or ventilation issue.',
            'action':  'Schedule inspection. Clean air filters and check oil levels.'
        })

    if vib >= 1.5:
        causes.append({
            'cause':   'Bearing Fault / Imbalance',
            'sensor':  'Vibration',
            'value':   f'{vib:.2f}g',
            'explanation': 'High vibration typically indicates bearing wear, '
                           'shaft imbalance, misalignment, or loose mounting hardware.',
            'action':  'Stop machine. Inspect bearings, check shaft alignment, '
                       'tighten all mechanical fastenings.'
        })
    elif vib >= 0.6:
        causes.append({
            'cause':   'Early Bearing Wear',
            'sensor':  'Vibration',
            'value':   f'{vib:.2f}g',
            'explanation': 'Slightly elevated vibration could indicate early bearing '
                           'degradation or minor imbalance.',
            'action':  'Monitor closely. Schedule bearing inspection within 48 hours.'
        })

    if pres <= 60:
        causes.append({
            'cause':   'Hydraulic/Pneumatic Failure',
            'sensor':  'Pressure',
            'value':   f'{pres:.1f} PSI',
            'explanation': 'Critically low pressure suggests a significant leak, '
                           'pump failure, or blocked line.',
            'action':  'Halt operations. Inspect all pressure lines and seals. '
                       'Check pump output.'
        })
    elif pres <= 80:
        causes.append({
            'cause':   'Pressure Drop',
            'sensor':  'Pressure',
            'value':   f'{pres:.1f} PSI',
            'explanation': 'Below-normal pressure may indicate minor leaks or '
                           'partial blockage in the hydraulic system.',
            'action':  'Inspect for small leaks. Monitor pressure trend.'
        })

    if rpm <= 1000:
        causes.append({
            'cause':   'Motor/Drive Failure',
            'sensor':  'RPM',
            'value':   f'{rpm:.0f} RPM',
            'explanation': 'Severely reduced RPM points to motor malfunction, '
                           'drive belt failure, or overload condition.',
            'action':  'Check motor power, inspect drive belt/coupling, '
                       'verify load conditions.'
        })
    elif rpm <= 1300:
        causes.append({
            'cause':   'Speed Reduction',
            'sensor':  'RPM',
            'value':   f'{rpm:.0f} RPM',
            'explanation': 'Below-target RPM may indicate increased load, '
                           'drive wear, or early motor issues.',
            'action':  'Check drive components and review load requirements.'
        })

    if not causes:
        causes.append({
            'cause':   'No Anomaly Detected',
            'sensor':  'All',
            'value':   'Normal',
            'explanation': 'All sensor readings are within normal operating parameters.',
            'action':  'Continue regular scheduled maintenance.'
        })

    return causes

# ─────────────────────────────────────────────
# HELPER: INTELLIGENT CHATBOT
# ─────────────────────────────────────────────

# In-memory session state for the chatbot
chat_session = {
    'last_prediction': None,
    'history': []
}

def chatbot_response(user_msg, last_pred=None):
    """
    Rule-based NLP chatbot with context awareness.
    Uses the most recent prediction as context.
    """
    msg = user_msg.lower().strip()

    # ── Status queries ────────────────────────
    if any(kw in msg for kw in ['status', 'condition', 'health', 'how is', 'state']):
        if last_pred:
            cond = last_pred['condition']
            conf = last_pred['confidence']
            emoji = {'Healthy': '✅', 'Warning': '⚠️', 'Failure': '🔴'}.get(cond, '❓')
            return (f"{emoji} Current machine status is <strong>{cond}</strong> "
                    f"(confidence: {conf:.1f}%). "
                    + {
                        'Healthy':  "All sensor readings are within normal operating range.",
                        'Warning':  "Some sensors are approaching critical thresholds. Monitor closely.",
                        'Failure':  "Critical sensor anomalies detected! Immediate attention required."
                    }.get(cond, ''))
        return "No prediction data yet. Please run a sensor analysis first."

    # ── Failure probability ───────────────────
    if any(kw in msg for kw in ['probability', 'chance', 'likelihood', 'risk', 'fail']):
        if last_pred:
            probs = last_pred.get('probabilities', {})
            fp = probs.get('Failure', 0)
            wp = probs.get('Warning', 0)
            return (f"📊 Failure probability: <strong>{fp:.1f}%</strong> | "
                    f"Warning probability: <strong>{wp:.1f}%</strong>. "
                    + ("Take immediate action!" if fp > 50 else
                       "Stay vigilant." if fp > 20 else
                       "Risk is currently low."))
        return "Please submit sensor readings first to get failure probabilities."

    # ── Temperature ───────────────────────────
    if 'temperature' in msg or 'temp' in msg or 'heat' in msg or 'overh' in msg:
        if last_pred:
            t = last_pred['inputs']['temperature']
            status = ("🔴 Critical" if t >= 90 else
                      "⚠️ Warning" if t >= 70 else "✅ Normal")
            return (f"🌡️ Current temperature: <strong>{t:.1f}°C</strong> — {status}. "
                    f"Normal range: 40–65°C. "
                    + ("Immediate cooling required!" if t >= 90 else
                       "Schedule inspection." if t >= 70 else
                       "Operating normally."))
        return "Temperature threshold: Warning >70°C, Failure >90°C."

    # ── Vibration ─────────────────────────────
    if 'vibration' in msg or 'bearing' in msg or 'vibrat' in msg or 'shake' in msg:
        if last_pred:
            v = last_pred['inputs']['vibration']
            status = ("🔴 Critical" if v >= 1.5 else
                      "⚠️ Warning" if v >= 0.6 else "✅ Normal")
            return (f"📳 Vibration level: <strong>{v:.2f}g</strong> — {status}. "
                    f"Normal range: 0.1–0.5g. "
                    + ("Bearing fault suspected — stop machine!" if v >= 1.5 else
                       "Possible early bearing wear." if v >= 0.6 else
                       "Vibration is normal."))
        return "Vibration threshold: Warning >0.6g, Failure >1.5g. High vibration suggests bearing faults."

    # ── Pressure ─────────────────────────────
    if 'pressure' in msg or 'psi' in msg or 'hydraulic' in msg:
        if last_pred:
            p = last_pred['inputs']['pressure']
            status = ("🔴 Critical" if p <= 60 else
                      "⚠️ Warning" if p <= 80 else "✅ Normal")
            return (f"🔧 Pressure: <strong>{p:.1f} PSI</strong> — {status}. "
                    f"Normal range: 90–110 PSI. "
                    + ("Critical leak/pump failure!" if p <= 60 else
                       "Check for small leaks." if p <= 80 else
                       "Pressure is normal."))
        return "Pressure threshold: Warning <80 PSI, Failure <60 PSI."

    # ── RPM ──────────────────────────────────
    if 'rpm' in msg or 'speed' in msg or 'motor' in msg or 'rotation' in msg:
        if last_pred:
            r = last_pred['inputs']['rpm']
            status = ("🔴 Critical" if r <= 1000 else
                      "⚠️ Warning" if r <= 1300 else "✅ Normal")
            return (f"⚙️ RPM: <strong>{r:.0f}</strong> — {status}. "
                    f"Normal range: 1400–1600 RPM. "
                    + ("Motor or drive failure likely!" if r <= 1000 else
                       "Monitor drive components." if r <= 1300 else
                       "Speed is normal."))
        return "RPM threshold: Warning <1300, Failure <1000. Low RPM suggests motor/drive issues."

    # ── Maintenance advice ───────────────────
    if any(kw in msg for kw in ['maintenance', 'fix', 'repair', 'action', 'suggest', 'recommend']):
        if last_pred:
            cond = last_pred['condition']
            rcas = last_pred.get('root_causes', [])
            if rcas and rcas[0]['cause'] != 'No Anomaly Detected':
                actions = '; '.join([r['action'] for r in rcas[:2]])
                return f"🔧 Recommended actions based on RCA: {actions}"
            return {
                'Healthy':  "✅ Machine is healthy! Continue regular preventive maintenance schedule.",
                'Warning':  "⚠️ Schedule inspection within 24–48 hours. Check highlighted sensors.",
                'Failure':  "🚨 STOP MACHINE NOW. Call maintenance team immediately. Do not restart without inspection."
            }.get(cond, "Please analyse sensor data first.")
        return ("General maintenance tips: Check lubricant levels weekly, inspect bearings monthly, "
                "calibrate sensors quarterly, and review vibration trends daily.")

    # ── Anomaly ─────────────────────────────
    if any(kw in msg for kw in ['anomal', 'unusual', 'abnormal', 'irregul']):
        if last_pred:
            alerts = last_pred.get('threshold_alerts', [])
            if alerts:
                msgs = [a['msg'] for a in alerts]
                return f"⚠️ {len(alerts)} anomaly/anomalies detected: " + "; ".join(msgs)
            return "✅ No anomalies detected in the latest reading."
        return "Submit sensor readings to check for anomalies."

    # ── Help ─────────────────────────────────
    if any(kw in msg for kw in ['help', 'what can', 'options', 'commands']):
        return ("I can answer questions about:<br>"
                "• <b>Machine status</b> — 'What is the machine status?'<br>"
                "• <b>Failure probability</b> — 'What is the failure risk?'<br>"
                "• <b>Sensor values</b> — 'What is the temperature / vibration / pressure / RPM?'<br>"
                "• <b>Maintenance</b> — 'What action should I take?'<br>"
                "• <b>Anomalies</b> — 'Are there any anomalies?'")

    # ── Greeting ─────────────────────────────
    if any(kw in msg for kw in ['hello', 'hi ', 'hey', 'greet']):
        return ("👋 Hello! I'm the Maintenance AI Assistant. "
                "I can help you monitor machine health, analyse sensor data, "
                "and provide maintenance recommendations. Type 'help' to see what I can do.")

    # ── Default ──────────────────────────────
    return ("I'm not sure I understood that. Try asking about: "
            "<b>machine status</b>, <b>failure probability</b>, "
            "<b>temperature</b>, <b>vibration</b>, <b>pressure</b>, <b>RPM</b>, "
            "or <b>maintenance suggestions</b>. Type 'help' for all options.")


# ─────────────────────────────────────────────
# DIGITAL TWIN SIMULATION HELPER
# ─────────────────────────────────────────────

def simulate_degradation(temp, vib, pres, rpm, steps=24):
    """
    Simulates machine health degradation over `steps` hours.
    Models gradual drift toward failure thresholds.
    """
    np.random.seed(42)
    timeline = []

    for i in range(steps):
        # Gradual drift + random noise
        factor = 1 + (i / steps) * 0.4
        t_sim = min(temp * factor + np.random.normal(0, 1.5),   140)
        v_sim = min(vib  * factor + np.random.normal(0, 0.05),  4.0)
        p_sim = max(pres / factor + np.random.normal(0, 1.5),   30)
        r_sim = max(rpm  / factor + np.random.normal(0, 15),    500)

        # Quick in-memory prediction
        features = np.array([[t_sim, v_sim, p_sim, r_sim]])
        scaled   = scaler.transform(features)
        proba    = xgb_model.predict_proba(scaled)[0]
        pred     = int(np.argmax(proba))
        health   = round(float(proba[0]) * 100, 1)

        timeline.append({
            'hour':        i + 1,
            'temperature': round(t_sim, 1),
            'vibration':   round(v_sim, 3),
            'pressure':    round(p_sim, 1),
            'rpm':         round(r_sim, 0),
            'health':      health,
            'condition':   ['Healthy', 'Warning', 'Failure'][pred]
        })

    return timeline


# ─────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────

@app.route('/')
def index():
    """Serve the main HTML dashboard."""
    return render_template('index.html', metrics=model_metrics)


@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Accept sensor readings, return ML prediction.
    Body (JSON):
      { temperature, vibration, pressure, rpm }
    """
    try:
        data = request.get_json()
        temp = float(data['temperature'])
        vib  = float(data['vibration'])
        pres = float(data['pressure'])
        rpm  = float(data['rpm'])

        # ── Scale and predict ─────────────────
        features = np.array([[temp, vib, pres, rpm]])
        scaled   = scaler.transform(features)
        pred_idx = int(xgb_model.predict(scaled)[0])
        proba    = xgb_model.predict_proba(scaled)[0]

        class_names = ['Healthy', 'Warning', 'Failure']
        condition   = class_names[pred_idx]
        confidence  = round(float(proba[pred_idx]) * 100, 2)
        probabilities = {
            cls: round(float(p) * 100, 2)
            for cls, p in zip(class_names, proba)
        }

        # ── Root cause analysis ───────────────
        root_causes = root_cause_analysis(temp, vib, pres, rpm, condition)

        # ── Threshold alerts ──────────────────
        threshold_alerts = check_thresholds(temp, vib, pres, rpm)

        # ── Log to SQLite ─────────────────────
        ts = datetime.datetime.now().isoformat()
        conn = get_db()
        conn.execute(
            'INSERT INTO predictions (temperature,vibration,pressure,rpm,condition,confidence,timestamp) '
            'VALUES (?,?,?,?,?,?,?)',
            (temp, vib, pres, rpm, condition, confidence, ts)
        )
        if threshold_alerts:
            for alert in threshold_alerts:
                conn.execute(
                    'INSERT INTO alerts (machine_id,alert_type,message,timestamp) VALUES (?,?,?,?)',
                    ('MACHINE-01', alert['level'], alert['msg'], ts)
                )
        conn.commit()
        conn.close()

        result = {
            'condition':        condition,
            'confidence':       confidence,
            'probabilities':    probabilities,
            'root_causes':      root_causes,
            'threshold_alerts': threshold_alerts,
            'inputs': {
                'temperature': temp,
                'vibration':   vib,
                'pressure':    pres,
                'rpm':         rpm
            },
            'timestamp': ts
        }

        # Update chatbot session
        chat_session['last_prediction'] = result

        return jsonify({'success': True, 'result': result})

    except (KeyError, ValueError) as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Rule-based intelligent chatbot endpoint.
    Body: { message: "..." }
    """
    try:
        data    = request.get_json()
        user_msg = data.get('message', '').strip()

        if not user_msg:
            return jsonify({'success': False, 'error': 'Empty message'}), 400

        # Get response using chatbot logic
        reply = chatbot_response(user_msg, chat_session.get('last_prediction'))

        # Save to chat history
        ts = datetime.datetime.now().isoformat()
        conn = get_db()
        conn.execute('INSERT INTO chat_history (role,message,timestamp) VALUES (?,?,?)',
                     ('user', user_msg, ts))
        conn.execute('INSERT INTO chat_history (role,message,timestamp) VALUES (?,?,?)',
                     ('assistant', reply, ts))
        conn.commit()
        conn.close()

        return jsonify({'success': True, 'reply': reply, 'timestamp': ts})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/digital-twin', methods=['POST'])
def digital_twin():
    """
    Simulates machine degradation over 24 hours.
    Body: { temperature, vibration, pressure, rpm }
    """
    try:
        data = request.get_json()
        timeline = simulate_degradation(
            float(data['temperature']),
            float(data['vibration']),
            float(data['pressure']),
            float(data['rpm'])
        )
        return jsonify({'success': True, 'timeline': timeline})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/history', methods=['GET'])
def history():
    """Returns last 50 prediction records."""
    conn = get_db()
    rows = conn.execute(
        'SELECT * FROM predictions ORDER BY id DESC LIMIT 50'
    ).fetchall()
    conn.close()
    return jsonify({'success': True, 'records': [dict(r) for r in rows]})


@app.route('/api/stats', methods=['GET'])
def stats():
    """Returns system statistics from the database."""
    conn = get_db()
    total   = conn.execute('SELECT COUNT(*) FROM predictions').fetchone()[0]
    healthy = conn.execute("SELECT COUNT(*) FROM predictions WHERE condition='Healthy'").fetchone()[0]
    warning = conn.execute("SELECT COUNT(*) FROM predictions WHERE condition='Warning'").fetchone()[0]
    failure = conn.execute("SELECT COUNT(*) FROM predictions WHERE condition='Failure'").fetchone()[0]
    alerts  = conn.execute('SELECT COUNT(*) FROM alerts').fetchone()[0]
    conn.close()
    return jsonify({
        'success': True,
        'stats': {
            'total_predictions': total,
            'healthy': healthy,
            'warning': warning,
            'failure': failure,
            'total_alerts': alerts
        }
    })


@app.route('/api/metrics', methods=['GET'])
def metrics():
    """Returns trained model performance metrics."""
    return jsonify({'success': True, 'metrics': model_metrics})


# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────

if __name__ == '__main__':
    print("\n" + "="*50)
    print("  Predictive Maintenance System — Server")
    print("  Running at: http://localhost:5000")
    print("="*50 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
