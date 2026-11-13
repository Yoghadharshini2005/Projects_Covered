"""
user_model.py - Database initialization and helper functions
"""
import sqlite3, os, hashlib, json, sys
from datetime import datetime

def get_db(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_path):
    conn = get_db(db_path)
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL, user_type TEXT NOT NULL,
            profile_complete INTEGER DEFAULT 0,
            is_admin INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL UNIQUE,
            profile_data TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL UNIQUE,
            responses TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL UNIQUE,
            primary_career TEXT,
            confidence_score REAL,
            all_scores TEXT, skill_gaps TEXT,
            skills_have TEXT, roadmap TEXT,
            market_insights TEXT, model_used TEXT,
            model_accuracy REAL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS resume_analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            filename TEXT, analysis_data TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS job_roles (
            job_role TEXT PRIMARY KEY,
            required_skills TEXT
        );
        CREATE TABLE IF NOT EXISTS courses (
            course_name TEXT PRIMARY KEY,
            stream TEXT,
            skills_gained TEXT
        );
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            skill TEXT,
            options TEXT,
            answer TEXT
        );
    ''')
    # Seed from CSVs
    try:
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        from utils.csv_loader import seed_db_from_csvs
        seed_db_from_csvs(conn)
        print('[DB] Seeded from CSVs')
    except Exception as e:
        print(f'[DB] CSV seeding skipped: {e}')
    conn.commit()
    conn.close()

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def get_user_by_email(conn, email):
    return conn.execute('SELECT * FROM users WHERE email=?', (email,)).fetchone()

def get_user_by_id(conn, uid):
    return conn.execute('SELECT * FROM users WHERE id=?', (uid,)).fetchone()
