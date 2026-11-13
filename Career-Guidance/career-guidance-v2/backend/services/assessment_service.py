import random
from utils.csv_loader import load_csv

def get_questions(skill=None, count=10):
    """GET /assessment?skill=XX&count=10"""
    questions = load_csv('assessment.csv')
    if skill:
        filtered = {k:v for k,v in questions.items() if skill.lower() in k.lower()}
        filtered_list = list(filtered.values())
        return filtered_list[:count] if filtered_list else []
    questions_list = list(questions.values())
    sample_size = min(count, len(questions_list))
    return random.sample(questions_list, sample_size) if sample_size > 0 else []

def evaluate_answers(answers, skill=None):
    """POST /submit-assessment {answers: [{question_id, selected}]}"""
    questions = load_csv('assessment.csv')
    score = 0
    total = len(answers)
    feedback = []
    for ans in answers:
        qid = ans.get('question_id')
        if qid is None:
            continue
        question_data = questions.get(qid, [''])
        correct = question_data[-1] if question_data else ''
        if ans.get('selected') == correct:
            score += 1
        else:
            feedback.append(f"Q{qid}: Expected {correct}, got {ans.get('selected')}")
    pct = round(score / total * 100, 1) if total else 0
    return {'score': score, 'total': total, 'percentage': pct, 'feedback': feedback}
