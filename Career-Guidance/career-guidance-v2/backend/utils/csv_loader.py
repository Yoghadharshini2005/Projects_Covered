import os, pandas as pd, json
from pathlib import Path

DATASET_DIR = Path(__file__).parent.parent.parent / 'dataset'

def load_csv(filename):
    '''Load CSV from dataset/ -> dict[list] for API use.'''
    path = DATASET_DIR / filename
    if not path.exists():
        print(f"Warning: {path} not found")
        return {}
    df = pd.read_csv(path)
    return {row.iloc[0]: row.iloc[1:].tolist() for _, row in df.iterrows() if len(row) > 1}

def load_courses():
    '''courses.csv -> {course_name: [stream, skills_gained]}'''
    courses_df = pd.read_csv(DATASET_DIR / 'courses.csv')
    return {row['course_name']: [row['stream'], json.loads(row['skills_gained'] or '[]')] 
            for _, row in courses_df.iterrows()}

def seed_db_from_csvs(conn):
    '''Seed DB tables from CSVs.'''
    # jobs
    jobs = load_csv('jobs.csv')
    for job, skills in jobs.items():
        conn.execute('INSERT OR IGNORE INTO job_roles (job_role, required_skills) VALUES (?, ?)',
                     (job, json.dumps(skills)))
    # courses
    courses = load_courses()
    for course, data in courses.items():
        conn.execute('INSERT OR IGNORE INTO courses (course_name, stream, skills_gained) VALUES (?, ?, ?)',
                     (course, data[0], json.dumps(data[1])))
    # TODO: assessment.csv
    conn.commit()

