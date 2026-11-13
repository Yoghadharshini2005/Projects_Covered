import pandas as pd
import numpy as np
import os

np.random.seed(42)

CAREERS = [
    'Data Science', 'Artificial Intelligence', 'Software Engineering',
    'Web Development', 'Cybersecurity', 'Cloud Engineering',
    'UI/UX Design', 'Product Management', 'Business Analytics',
    'Arts & Humanities'
]

def clamp(val, lo=0, hi=10):
    return round(float(np.clip(val, lo, hi)), 2)

PROFILES = {
    'Data Science':          dict(cgpa=(8.2,.7), math=(8.5,1.0), physics=(7.5,1.2), cs=(8.0,1.0), logic=(8.0,1.0), python=(8.5,.8), java=(5.0,1.5), webdev=(5.0,1.5), sql=(8.0,1.0), dsa=(7.0,1.2), ml=(8.5,.8), cloud=(5.5,1.5), design=(3.5,1.5), comm=(7.0,1.2), lead=(6.0,1.5), creative=(6.5,1.5), ps=(8.5,.8), proj=(4,1.5), intern=.7, cert=(3,1), exp=(1.5,1.5), ai_i=(8.0,1.0), cyber_i=(4.0,1.5), cloud_i=(5.5,1.5), web_i=(4.5,1.5), des_i=(4.0,1.5), biz_i=(5.5,1.5)),
    'Artificial Intelligence': dict(cgpa=(8.5,.6), math=(9.0,.8), physics=(8.0,1.0), cs=(8.5,.8), logic=(9.0,.7), python=(9.0,.7), java=(5.5,1.5), webdev=(4.5,1.5), sql=(7.0,1.2), dsa=(8.0,1.0), ml=(9.5,.5), cloud=(6.0,1.5), design=(3.0,1.5), comm=(7.0,1.2), lead=(6.5,1.5), creative=(7.5,1.2), ps=(9.0,.7), proj=(4,1.5), intern=.75, cert=(3,1), exp=(1.5,1.5), ai_i=(9.5,.5), cyber_i=(4.0,1.5), cloud_i=(6.0,1.5), web_i=(4.0,1.5), des_i=(4.0,1.5), biz_i=(5.0,1.5)),
    'Software Engineering':   dict(cgpa=(8.0,.8), math=(7.5,1.2), physics=(7.0,1.2), cs=(8.5,.8), logic=(8.5,.8), python=(7.5,1.2), java=(8.0,1.0), webdev=(6.0,1.5), sql=(7.5,1.2), dsa=(9.0,.7), ml=(5.0,1.5), cloud=(6.0,1.5), design=(4.0,1.5), comm=(7.0,1.2), lead=(6.5,1.5), creative=(6.5,1.5), ps=(9.0,.7), proj=(5,1.5), intern=.75, cert=(2,1), exp=(2,2), ai_i=(5.5,1.5), cyber_i=(5.0,1.5), cloud_i=(5.5,1.5), web_i=(5.5,1.5), des_i=(4.0,1.5), biz_i=(4.5,1.5)),
    'Web Development':        dict(cgpa=(7.5,1.0), math=(6.5,1.5), physics=(6.0,1.5), cs=(7.5,1.2), logic=(7.0,1.2), python=(6.5,1.5), java=(5.0,1.5), webdev=(9.0,.7), sql=(7.0,1.2), dsa=(6.0,1.5), ml=(4.0,1.5), cloud=(5.5,1.5), design=(7.5,1.2), comm=(7.5,1.2), lead=(6.0,1.5), creative=(8.5,.8), ps=(7.5,1.2), proj=(5,1.5), intern=.7, cert=(2,1), exp=(1.5,1.5), ai_i=(4.5,1.5), cyber_i=(4.5,1.5), cloud_i=(5.5,1.5), web_i=(9.5,.5), des_i=(8.0,1.0), biz_i=(5.0,1.5)),
    'Cybersecurity':          dict(cgpa=(7.8,.9), math=(7.5,1.2), physics=(7.0,1.2), cs=(8.0,1.0), logic=(8.5,.8), python=(7.5,1.2), java=(6.0,1.5), webdev=(5.5,1.5), sql=(7.0,1.2), dsa=(7.5,1.2), ml=(5.0,1.5), cloud=(6.5,1.5), design=(3.5,1.5), comm=(7.0,1.2), lead=(6.5,1.5), creative=(6.0,1.5), ps=(8.5,.8), proj=(3,1.5), intern=.65, cert=(3,1), exp=(2,2), ai_i=(5.0,1.5), cyber_i=(9.5,.5), cloud_i=(6.5,1.5), web_i=(4.5,1.5), des_i=(3.5,1.5), biz_i=(4.5,1.5)),
    'Cloud Engineering':      dict(cgpa=(7.8,.9), math=(7.0,1.2), physics=(7.0,1.2), cs=(8.0,1.0), logic=(8.0,1.0), python=(7.5,1.2), java=(6.5,1.5), webdev=(5.5,1.5), sql=(6.5,1.5), dsa=(7.0,1.2), ml=(5.0,1.5), cloud=(9.5,.5), design=(3.5,1.5), comm=(7.0,1.2), lead=(6.5,1.5), creative=(5.5,1.5), ps=(8.0,1.0), proj=(3,1.5), intern=.7, cert=(4,1), exp=(2,2), ai_i=(5.5,1.5), cyber_i=(6.5,1.5), cloud_i=(9.5,.5), web_i=(4.5,1.5), des_i=(3.5,1.5), biz_i=(4.5,1.5)),
    'UI/UX Design':           dict(cgpa=(7.2,1.0), math=(6.0,1.5), physics=(5.5,1.5), cs=(6.5,1.5), logic=(7.0,1.2), python=(4.0,1.5), java=(3.5,1.5), webdev=(7.0,1.2), sql=(4.5,1.5), dsa=(4.5,1.5), ml=(3.5,1.5), cloud=(4.0,1.5), design=(9.5,.5), comm=(8.5,.8), lead=(7.0,1.2), creative=(9.5,.5), ps=(7.5,1.2), proj=(4,1.5), intern=.7, cert=(2,1), exp=(1.5,1.5), ai_i=(4.5,1.5), cyber_i=(3.0,1.5), cloud_i=(4.0,1.5), web_i=(7.5,1.2), des_i=(9.5,.5), biz_i=(6.0,1.5)),
    'Product Management':     dict(cgpa=(8.0,.8), math=(7.0,1.2), physics=(6.5,1.5), cs=(7.0,1.2), logic=(8.5,.8), python=(5.5,1.5), java=(4.5,1.5), webdev=(5.5,1.5), sql=(7.0,1.2), dsa=(6.0,1.5), ml=(5.5,1.5), cloud=(5.0,1.5), design=(6.5,1.5), comm=(9.5,.5), lead=(9.0,.7), creative=(8.0,1.0), ps=(8.5,.8), proj=(4,1.5), intern=.8, cert=(2,1), exp=(3,2), ai_i=(5.5,1.5), cyber_i=(4.0,1.5), cloud_i=(5.0,1.5), web_i=(5.5,1.5), des_i=(7.0,1.2), biz_i=(9.5,.5)),
    'Business Analytics':     dict(cgpa=(7.8,.9), math=(8.0,1.0), physics=(6.5,1.5), cs=(7.0,1.2), logic=(8.5,.8), python=(6.5,1.5), java=(4.0,1.5), webdev=(4.5,1.5), sql=(8.5,.8), dsa=(5.5,1.5), ml=(6.5,1.5), cloud=(5.0,1.5), design=(5.0,1.5), comm=(8.5,.8), lead=(7.5,1.2), creative=(7.0,1.2), ps=(8.0,1.0), proj=(3,1.5), intern=.7, cert=(3,1), exp=(2,2), ai_i=(6.5,1.5), cyber_i=(4.0,1.5), cloud_i=(5.0,1.5), web_i=(4.5,1.5), des_i=(5.0,1.5), biz_i=(9.0,.7)),
    'Arts & Humanities':     dict(cgpa=(7.2,1.0), math=(6.0,1.2), physics=(5.5,1.5), cs=(5.0,1.5), logic=(7.0,1.2), python=(4.5,1.5), java=(4.0,1.5), webdev=(5.0,1.5), sql=(5.0,1.5), dsa=(4.5,1.5), ml=(4.0,1.5), cloud=(4.5,1.5), design=(8.5,.8), comm=(9.0,.7), lead=(7.0,1.0), creative=(9.5,.5), ps=(8.0,1.0), proj=(3,1.2), intern=.6, cert=(2,1), exp=(1.5,1.2), ai_i=(4.5,1.5), cyber_i=(4.0,1.5), cloud_i=(5.0,1.5), web_i=(6.5,1.2), des_i=(9.5,.5), biz_i=(7.0,1.2)),
}

def make_sample(career):
    p = PROFILES[career]
    n = lambda mu, sd: np.random.normal(mu, sd)
    return {
        'cgpa':             clamp(n(*p['cgpa'])),
        'math_score':       clamp(n(*p['math'])),
        'physics_score':    clamp(n(*p['physics'])),
        'cs_score':         clamp(n(*p['cs'])),
        'logical_reasoning':clamp(n(*p['logic'])),
        'python_skill':     clamp(n(*p['python'])),
        'java_skill':       clamp(n(*p['java'])),
        'webdev_skill':     clamp(n(*p['webdev'])),
        'sql_skill':        clamp(n(*p['sql'])),
        'dsa_skill':        clamp(n(*p['dsa'])),
        'ml_knowledge':     clamp(n(*p['ml'])),
        'cloud_skill':      clamp(n(*p['cloud'])),
        'design_skill':     clamp(n(*p['design'])),
        'communication':    clamp(n(*p['comm'])),
        'leadership':       clamp(n(*p['lead'])),
        'creativity':       clamp(n(*p['creative'])),
        'problem_solving':  clamp(n(*p['ps'])),
        'projects_count':   int(np.clip(n(*p['proj']), 0, 10)),
        'internship':       int(np.random.choice([0,1], p=[1-p['intern'], p['intern']])),
        'certifications':   int(np.clip(n(*p['cert']), 0, 10)),
        'years_experience': clamp(n(*p['exp']), 0, 10),
        'ai_interest':      clamp(n(*p['ai_i'])),
        'cyber_interest':   clamp(n(*p['cyber_i'])),
        'cloud_interest':   clamp(n(*p['cloud_i'])),
        'web_interest':     clamp(n(*p['web_i'])),
        'design_interest':  clamp(n(*p['des_i'])),
        'business_interest':clamp(n(*p['biz_i'])),
        'career': career
    }

if __name__ == '__main__':
    os.makedirs('dataset', exist_ok=True)
    samples = []
    per_class = 500 // len(CAREERS)
    for career in CAREERS:
        for _ in range(per_class + (1 if career == CAREERS[0] else 0)):
            samples.append(make_sample(career))
    df = pd.DataFrame(samples).sample(frac=1, random_state=42).reset_index(drop=True)
    df.to_csv('dataset/career_guidance_dataset_500.csv', index=False)
    print(f"Dataset: {df.shape}")
    print(df['career'].value_counts().to_string())
