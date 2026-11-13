from utils.csv_loader import load_courses

COURSES = None

def get_recommended_courses(missing_skills, limit=5):
    """GET /recommend-courses logic."""
    global COURSES
    if COURSES is None:
        COURSES = load_courses()
    
    if not missing_skills:
        return []
    
    recommendations = []
    for course, (stream, skills_gained) in COURSES.items():
        matches = sum(1 for skill in missing_skills if any(s.lower() in skill.lower() or skill.lower() in s.lower() 
                         for s in skills_gained))
        if matches > 0:
            score = matches / len(missing_skills)
            recommendations.append({'course': course, 'stream': stream, 'matches': matches, 'score': round(score*100,1)})
    return sorted(recommendations, key=lambda x: -x['score'])[:limit]

