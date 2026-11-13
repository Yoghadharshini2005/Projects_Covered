"""
resume_analyzer.py - Extract skills & info from uploaded PDF resumes
"""
import re

SKILL_KEYWORDS = [
    'python','java','javascript','typescript','c++','c#','go','rust','kotlin','swift',
    'react','angular','vue','node.js','express','django','flask','fastapi','spring',
    'sql','mysql','postgresql','mongodb','redis','elasticsearch','cassandra',
    'aws','azure','gcp','docker','kubernetes','terraform','ansible','jenkins',
    'machine learning','deep learning','tensorflow','pytorch','scikit-learn','keras',
    'html','css','tailwind','bootstrap','sass','webpack','git','github','linux',
    'figma','adobe xd','photoshop','illustrator','sketch','invision',
    'agile','scrum','kanban','jira','confluence','trello',
    'excel','power bi','tableau','looker','pandas','numpy','matplotlib','seaborn',
    'nlp','computer vision','data science','data analysis','statistics',
    'networking','cybersecurity','ethical hacking','penetration testing',
    'communication','leadership','teamwork','problem solving','critical thinking'
]

EDUCATION_PATTERNS = [
    r'b\.?tech|b\.?e\.|bachelor of technology',
    r'm\.?tech|master of technology',
    r'b\.?sc|bachelor of science',
    r'mba|master of business',
    r'bca|mca|b\.?c\.?a|m\.?c\.?a',
    r'phd|ph\.?d|doctor',
]

CGPA_PATTERN    = r'(?:cgpa|gpa|percentage)[^\d]*(\d+\.?\d*)'
EMAIL_PATTERN   = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
PHONE_PATTERN   = r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]'
EXP_PATTERN     = r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s+)?(?:experience|exp)'

def extract_text_from_pdf_bytes(pdf_bytes):
    """Extract text from PDF bytes using pypdf/PyPDF2 and optional pdfplumber fallback."""
    try:
        import io
        text = ""
        reader = None
        try:
            from pypdf import PdfReader
            reader = PdfReader(io.BytesIO(pdf_bytes))
        except ImportError:
            try:
                from PyPDF2 import PdfReader
                reader = PdfReader(io.BytesIO(pdf_bytes))
            except ImportError:
                return None, "PDF library not available. Please install pypdf: pip install pypdf"

        if reader:
            for page in reader.pages:
                text += (page.extract_text() or "") + "\n"

        if not text.strip():
            try:
                import pdfplumber
                with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
                    for page in pdf.pages:
                        text += (page.extract_text() or "") + "\n"
            except Exception:
                pass

        if not text.strip():
            return None, "Could not extract text from PDF. Try a text-based PDF or upload a different resume."

        return text.strip(), None
    except Exception as e:
        return None, str(e)

def analyze_resume_text(text):
    """Analyze extracted resume text and return structured info"""
    text_lower = text.lower()
    result = {
        'found_skills':    [],
        'education':       [],
        'cgpa':            None,
        'email':           None,
        'phone':           None,
        'years_experience':None,
        'word_count':      len(text.split()),
        'skill_count':     0,
        'resume_score':    0,
        'suggestions':     [],
    }

    # Skills
    found = [s for s in SKILL_KEYWORDS if re.search(r'\b' + re.escape(s) + r'\b', text_lower)]
    result['found_skills'] = list(dict.fromkeys(found))  # deduplicate preserving order
    result['skill_count']  = len(found)

    # Education
    for pat in EDUCATION_PATTERNS:
        if re.search(pat, text_lower):
            result['education'].append(pat.split('|')[0].replace('\\','').replace('.?','').upper())

    # CGPA
    cgpa_match = re.search(CGPA_PATTERN, text_lower)
    if cgpa_match:
        val = float(cgpa_match.group(1))
        result['cgpa'] = val if val <= 10 else round(val/10, 2)

    # Contact
    email_match = re.search(EMAIL_PATTERN, text)
    if email_match: result['email'] = email_match.group()

    phone_match = re.search(PHONE_PATTERN, text)
    if phone_match: result['phone'] = phone_match.group().strip()

    # Experience
    exp_match = re.search(EXP_PATTERN, text_lower)
    if exp_match: result['years_experience'] = int(exp_match.group(1))

    # Resume Score (0-100)
    score = 0
    if result['skill_count'] >= 10: score += 30
    elif result['skill_count'] >= 5: score += 20
    elif result['skill_count'] >= 2: score += 10
    if result['cgpa']: score += 15
    if result['email']: score += 10
    if result['education']: score += 15
    if result['word_count'] >= 400: score += 15
    elif result['word_count'] >= 200: score += 8
    if result['years_experience']: score += 15
    result['resume_score'] = min(score, 100)

    # Suggestions
    if result['skill_count'] < 5:
        result['suggestions'].append('Add more technical skills to your resume')
    if not result['email']:
        result['suggestions'].append('Include your email address clearly')
    if result['word_count'] < 300:
        result['suggestions'].append('Your resume seems short — add more details about projects and experience')
    if not result['education']:
        result['suggestions'].append('Make your educational qualification clearly visible')
    if not result['years_experience'] and result['word_count'] > 200:
        result['suggestions'].append('Mention your years of experience explicitly')

    return result

def suggest_careers_from_resume(found_skills):
    """Suggest top career matches based on resume skills"""
    from ml.skill_gap import REQUIRED_SKILLS
    scores = {}
    for career, required in REQUIRED_SKILLS.items():
        req_lower  = [r.lower() for r in required]
        found_lower= [s.lower() for s in found_skills]
        overlap    = sum(1 for r in req_lower if any(r in f or f in r for f in found_lower))
        scores[career] = round((overlap / len(required)) * 100, 1)
    return sorted(scores.items(), key=lambda x: -x[1])
