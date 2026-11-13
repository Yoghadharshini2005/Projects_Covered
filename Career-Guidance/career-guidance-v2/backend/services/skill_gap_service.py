import json
from ..utils.csv_loader import load_csv

REQUIRED_SKILLS = {
    'Data Science':          ['Python','Statistics','Machine Learning','SQL','Pandas','NumPy','Tableau','Data Visualization'],
    'Artificial Intelligence':['Python','Deep Learning','TensorFlow','PyTorch','NLP','Computer Vision','Math','Research'],
    'Software Engineering':  ['DSA','System Design','Java/C++','Git','Testing','Agile','REST APIs','Databases'],
    'Web Development':       ['HTML/CSS','JavaScript','React','Node.js','REST APIs','Git','Responsive Design','Databases'],
    'Cybersecurity':         ['Networking','Linux','Python','Ethical Hacking','Cryptography','SIEM','Risk Analysis','Firewalls'],
    'Cloud Engineering':     ['AWS/Azure/GCP','Docker','Kubernetes','Terraform','Linux','Networking','CI/CD','IaC'],
    'UI/UX Design':          ['Figma','User Research','Prototyping','CSS','Typography','Usability Testing','Adobe XD','Wireframing'],
    'Product Management':    ['Communication','Strategy','Data Analysis','Roadmapping','Stakeholder Mgmt','Agile','SQL','Market Research'],
    'Business Analytics':    ['SQL','Excel','Power BI','Statistics','Communication','Python','Data Storytelling','Tableau'],
    'Arts & Humanities':     ['Creative Writing','Public Speaking','Research','Visual Design','Storytelling','Critical Thinking','Communication','Cultural Studies']
}

def analyze_skill_gap(user_skills, target_career=None):
    '''POST /skill-gap {user_skills, target_career} → matched, missing, %'''
    jobs = load_csv('jobs.csv')
    required = REQUIRED_SKILLS.get(target_career, jobs.get(target_career, REQUIRED_SKILLS['Software Engineering']))
    user_lower = [s.lower() for s in user_skills or []]
    matched = []
    missing = []
    for skill in required:
        has = any(skill.lower() in u or u.lower() in s.lower() for s in user_skills)
        if has:
            matched.append(skill)
        else:
            missing.append(skill)
    match_pct = round(len(matched) / len(required) * 100, 1) if required else 0
    return {
        'target_career': target_career or 'Software Engineering',
        'required_skills': required,
        'matched_skills': matched,
        'missing_skills': missing,
        'match_percentage': match_pct
    }

