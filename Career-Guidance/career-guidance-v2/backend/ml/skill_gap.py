"""
skill_gap.py - Skill Gap Analysis Engine
"""
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

SKILL_RESOURCES = {
    'Python':           {'platform':'Python.org + Codecademy','link':'https://www.python.org/about/gettingstarted/','duration':'4-6 weeks'},
    'SQL':              {'platform':'Mode Analytics + W3Schools','link':'https://mode.com/sql-tutorial/','duration':'2-3 weeks'},
    'Machine Learning': {'platform':'Coursera ML Specialization','link':'https://www.coursera.org/specializations/machine-learning-introduction','duration':'8-10 weeks'},
    'Deep Learning':    {'platform':'fast.ai + deeplearning.ai','link':'https://www.fast.ai/','duration':'8-12 weeks'},
    'React':            {'platform':'React Docs + Scrimba','link':'https://react.dev/learn','duration':'4-6 weeks'},
    'DSA':              {'platform':'NeetCode + LeetCode','link':'https://neetcode.io/','duration':'8-12 weeks'},
    'AWS/Azure/GCP':    {'platform':'A Cloud Guru + Official Docs','link':'https://acloudguru.com/','duration':'8-10 weeks'},
    'Docker':           {'platform':'Docker Docs + TechWorld','link':'https://docs.docker.com/get-started/','duration':'2-3 weeks'},
    'Kubernetes':       {'platform':'KubeAcademy','link':'https://kube.academy/','duration':'4-6 weeks'},
    'Figma':            {'platform':'Figma Tutorials + YouTube','link':'https://www.figma.com/resources/learn-design/','duration':'2-4 weeks'},
    'TensorFlow':       {'platform':'TensorFlow Tutorials','link':'https://www.tensorflow.org/tutorials','duration':'6-8 weeks'},
    'Linux':            {'platform':'Linux Journey','link':'https://linuxjourney.com/','duration':'3-4 weeks'},
    'Networking':       {'platform':'CompTIA Network+ + CBT Nuggets','link':'https://www.comptia.org/training/by-certification/network','duration':'6-8 weeks'},
    'Ethical Hacking':  {'platform':'TryHackMe + HackTheBox','link':'https://tryhackme.com/','duration':'8-12 weeks'},
    'Statistics':       {'platform':'Khan Academy + StatQuest','link':'https://www.khanacademy.org/math/statistics-probability','duration':'4-6 weeks'},
    'Power BI':         {'platform':'Microsoft Learn','link':'https://learn.microsoft.com/en-us/training/powerplatform/power-bi','duration':'3-4 weeks'},
    'Creative Writing': {'platform':'Coursera + edX','link':'https://www.coursera.org/courses?query=creative%20writing','duration':'4-6 weeks'},
    'Public Speaking':  {'platform':'Toastmasters + Udemy','link':'https://www.toastmasters.org/find-a-club','duration':'4-6 weeks'},
    'Research':         {'platform':'edX Research Methods','link':'https://www.edx.org/learn/research','duration':'4-6 weeks'},
    'Visual Design':    {'platform':'Canva + Interaction Design Foundation','link':'https://www.canva.com/learn/design/','duration':'4-6 weeks'},
    'Storytelling':     {'platform':'HubSpot Academy','link':'https://www.hubspot.com/resources/storytelling','duration':'3-5 weeks'},
    'Critical Thinking':{'platform':'FutureLearn','link':'https://www.futurelearn.com/courses/critical-thinking','duration':'3-5 weeks'},
}

def get_skill_gap(career, user_skills):
    """Return list of missing skills for a career"""
    required = REQUIRED_SKILLS.get(career, [])
    user_lower = [s.lower() for s in user_skills]
    missing = []
    for skill in required:
        skill_lower = skill.lower()
        has_skill = any(skill_lower in u or u in skill_lower for u in user_lower)
        if not has_skill:
            missing.append(skill)
    return missing

def get_skill_gap_with_resources(career, user_skills):
    """Return missing skills with learning resources"""
    gaps = get_skill_gap(career, user_skills)
    result = []
    for skill in gaps:
        resource = SKILL_RESOURCES.get(skill, {
            'platform': 'Google + YouTube',
            'link': f'https://www.google.com/search?q=learn+{skill.replace(" ","+")}',
            'duration': '2-4 weeks'
        })
        result.append({'skill': skill, **resource})
    return result

def get_all_required(career):
    return REQUIRED_SKILLS.get(career, [])
