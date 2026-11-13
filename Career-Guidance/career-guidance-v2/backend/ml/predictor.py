"""
predictor.py - Real ML-based career prediction using trained RandomForest/LR model
"""
import joblib, json, os, numpy as np

ML_DIR  = os.path.dirname(os.path.abspath(__file__))
MODEL   = os.path.join(ML_DIR, 'career_model.pkl')
LE_PATH = os.path.join(ML_DIR, 'career_model_le.pkl')
META    = os.path.join(ML_DIR, 'model_meta.json')

CAREER_SKILLS = {
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

MARKET_INSIGHTS = {
    'Data Science':          {'avg_salary':'₹12-18 LPA','demand':'Very High','growth':'35% YoY','top_companies':['Google','Amazon','Flipkart','Walmart Labs']},
    'Artificial Intelligence':{'avg_salary':'₹15-25 LPA','demand':'Extremely High','growth':'40% YoY','top_companies':['OpenAI','Google DeepMind','Microsoft','Meta AI']},
    'Software Engineering':  {'avg_salary':'₹10-20 LPA','demand':'High','growth':'25% YoY','top_companies':['Google','Amazon','Microsoft','Infosys']},
    'Web Development':       {'avg_salary':'₹6-14 LPA','demand':'High','growth':'20% YoY','top_companies':['Zoho','Freshworks','Razorpay','Swiggy']},
    'Cybersecurity':         {'avg_salary':'₹10-20 LPA','demand':'Very High','growth':'33% YoY','top_companies':['Palo Alto','CrowdStrike','IBM Security','TCS']},
    'Cloud Engineering':     {'avg_salary':'₹12-22 LPA','demand':'Very High','growth':'30% YoY','top_companies':['AWS','Azure','GCP','Accenture']},
    'UI/UX Design':          {'avg_salary':'₹8-16 LPA','demand':'High','growth':'22% YoY','top_companies':['Zomato','CRED','PhonePe','Figma']},
    'Product Management':    {'avg_salary':'₹18-35 LPA','demand':'High','growth':'28% YoY','top_companies':['Google','Flipkart','Paytm','Meesho']},
    'Business Analytics':    {'avg_salary':'₹9-16 LPA','demand':'High','growth':'25% YoY','top_companies':['McKinsey','Deloitte','KPMG','Goldman Sachs']},
    'Arts & Humanities':     {'avg_salary':'₹5-12 LPA','demand':'Rising','growth':'18% YoY','top_companies':['Times Group','Hindustan Times','National Geographic','Tata Literature Live']}
}

ROADMAPS = {
    'Data Science': {'title':'Data Science Roadmap','months':[
        {'month':'Month 1-2','title':'Python & Statistics','tasks':['Learn Python (NumPy, Pandas, Matplotlib)','Descriptive & Inferential Statistics','EDA & Data Cleaning','Platform: Kaggle Learn, Coursera']},
        {'month':'Month 3-4','title':'Machine Learning Core','tasks':['Scikit-learn ML algorithms','Supervised & Unsupervised learning','Cross-validation & Hyperparameter tuning','Build 2 ML projects on Kaggle']},
        {'month':'Month 5','title':'Visualization & SQL','tasks':['Tableau / Power BI','Advanced SQL window functions','Data storytelling techniques','End-to-end analysis project']},
        {'month':'Month 6','title':'Deployment & Jobs','tasks':['Streamlit / Flask for model deployment','GitHub portfolio with 3+ projects','Certification: Google Data Analytics','Apply for DS internships/jobs']}
    ]},
    'Artificial Intelligence': {'title':'AI Engineering Roadmap','months':[
        {'month':'Month 1-2','title':'Math & Python for AI','tasks':['Linear Algebra & Calculus review','Python + NumPy/SciPy','Probability & Information Theory','Platform: fast.ai, deeplearning.ai']},
        {'month':'Month 3-4','title':'Deep Learning','tasks':['Neural Networks from scratch','TensorFlow / PyTorch','CNNs, RNNs, Transformers','Build image classifier + NLP model']},
        {'month':'Month 5','title':'Specialization','tasks':['Choose: NLP / CV / RL / Generative AI','Hugging Face models & fine-tuning','Deploy a demo on HuggingFace Spaces','Publish research or Kaggle notebook']},
        {'month':'Month 6','title':'MLOps & Career','tasks':['MLflow experiment tracking','FastAPI model serving','Certification: TensorFlow Developer','Contribute to open-source AI projects']}
    ]},
    'Software Engineering': {'title':'Software Engineering Roadmap','months':[
        {'month':'Month 1-2','title':'DSA Mastery','tasks':['Data Structures (Arrays, Trees, Graphs, Heaps)','Algorithm patterns (DP, Backtracking, Sliding Window)','LeetCode: 100+ problems (Easy→Medium)','Platform: NeetCode, InterviewBit']},
        {'month':'Month 3','title':'System Design','tasks':['Scalability, Load Balancing, Caching','SQL + NoSQL Databases','Message Queues (Kafka, RabbitMQ)','Design Twitter, Uber, URL Shortener']},
        {'month':'Month 4-5','title':'Backend Engineering','tasks':['Java/Python/Go backend development','REST & GraphQL API design','Microservices & Docker','Build a production-grade backend API']},
        {'month':'Month 6','title':'Interview & Portfolio','tasks':['Mock interviews on Pramp/Interviewing.io','Open source contributions (3+ PRs)','Technical blog on Medium/Dev.to','Apply to product companies & startups']}
    ]},
    'Web Development': {'title':'Full-Stack Web Dev Roadmap','months':[
        {'month':'Month 1-2','title':'HTML, CSS & JavaScript','tasks':['HTML5 semantic markup & accessibility','CSS3, Flexbox, Grid, Animations','JavaScript ES6+ (Promises, Async/Await)','Build 3 responsive static websites']},
        {'month':'Month 3','title':'React & Frontend','tasks':['React.js (Hooks, Context, Router)','State management (Redux / Zustand)','REST API integration','Build a React portfolio SPA']},
        {'month':'Month 4-5','title':'Backend & Database','tasks':['Node.js & Express.js','MongoDB + PostgreSQL','JWT Authentication, Middleware','Full-stack CRUD app with deployment']},
        {'month':'Month 6','title':'DevOps & Launch','tasks':['Git, GitHub, CI/CD with GitHub Actions','Deploy on Vercel / Railway / AWS','Performance optimization','Launch 2 complete projects publicly']}
    ]},
    'Cybersecurity': {'title':'Cybersecurity Professional Roadmap','months':[
        {'month':'Month 1-2','title':'Networking & Linux','tasks':['CompTIA Network+ concepts','Linux CLI mastery (Bash scripting)','TCP/IP, DNS, HTTP/S protocols','Platform: TryHackMe, Cybrary']},
        {'month':'Month 3-4','title':'Ethical Hacking','tasks':['Kali Linux tools (Nmap, Metasploit, Burp)','OWASP Top 10 web vulnerabilities','CTF challenges on HackTheBox','Web application penetration testing']},
        {'month':'Month 5','title':'Defense & SIEM','tasks':['Wireshark packet analysis','Splunk SIEM basics','Incident response process','Build a home lab + write reports']},
        {'month':'Month 6','title':'Certifications','tasks':['CompTIA Security+ exam','CEH or eJPT certification','Write security blog/CTF writeups','Apply: SOC Analyst / Pentester roles']}
    ]},
    'Cloud Engineering': {'title':'Cloud Engineering Roadmap','months':[
        {'month':'Month 1-2','title':'Cloud Fundamentals','tasks':['AWS/Azure/GCP free tier exploration','Core services: EC2, S3, VPC, IAM','Linux & networking basics','Platform: A Cloud Guru, AWS Training']},
        {'month':'Month 3','title':'Infrastructure as Code','tasks':['Terraform fundamentals','AWS CloudFormation templates','Automate multi-tier architecture','Version-control your infra with Git']},
        {'month':'Month 4-5','title':'Containers & K8s','tasks':['Docker containerization','Kubernetes (EKS/GKE/AKS)','CI/CD with GitHub Actions','Deploy microservices application']},
        {'month':'Month 6','title':'Certification','tasks':['AWS Solutions Architect Associate','Cost optimization & FinOps','Security best practices in cloud','Apply for Cloud/DevOps Engineer roles']}
    ]},
    'UI/UX Design': {'title':'UI/UX Designer Roadmap','months':[
        {'month':'Month 1-2','title':'Design Fundamentals','tasks':['Design principles, color theory, typography','Figma from basics to advanced','Gestalt principles & visual hierarchy','Platform: Google UX Design Certificate']},
        {'month':'Month 3','title':'UX Research','tasks':['User interviews & surveys','Personas & user journey mapping','Affinity diagrams & card sorting','Conduct 2 full user research studies']},
        {'month':'Month 4-5','title':'Prototyping & Testing','tasks':['High-fidelity prototypes in Figma','Component libraries & design systems','Usability testing & iteration','Redesign 2 real apps as case studies']},
        {'month':'Month 6','title':'Portfolio & Jobs','tasks':['Behance / Dribbble portfolio','3 detailed case studies with process docs','Learn HTML/CSS basics for handoff','Apply: Junior UX / Product Designer']}
    ]},
    'Product Management': {'title':'Product Management Roadmap','months':[
        {'month':'Month 1-2','title':'PM Fundamentals','tasks':['Product thinking & user empathy','Agile, Scrum, Kanban methodologies','User story & acceptance criteria writing','Book: Inspired by Marty Cagan']},
        {'month':'Month 3','title':'Data & Analytics','tasks':['SQL for product metrics','Google Analytics / Mixpanel / Amplitude','A/B testing concepts & experiment design','Analyze a real product\'s funnel metrics']},
        {'month':'Month 4-5','title':'Strategy & Roadmapping','tasks':['RICE, MoSCoW prioritization frameworks','Competitive analysis & positioning','PRD writing & feature specs','Launch a mini product/feature with users']},
        {'month':'Month 6','title':'Network & Jobs','tasks':['Product School PM Certificate','LinkedIn networking with PMs','Product teardown portfolio (5 analyses)','Apply: APM / Associate PM programs']}
    ]},
    'Business Analytics': {'title':'Business Analytics Roadmap','months':[
        {'month':'Month 1-2','title':'Excel & SQL Mastery','tasks':['Advanced Excel (Pivots, VBA, Power Query)','SQL window functions & CTEs','Business statistics & hypothesis testing','Platform: Mode Analytics, Kaggle']},
        {'month':'Month 3','title':'BI Tools','tasks':['Power BI end-to-end dashboards','Tableau fundamentals & storytelling','KPI design, metrics definition','Build 2 live business dashboards']},
        {'month':'Month 4-5','title':'Python for Analytics','tasks':['Python (Pandas, Seaborn, Plotly)','Predictive analytics & regression','Market basket & cohort analysis','End-to-end business case study']},
        {'month':'Month 6','title':'Certifications','tasks':['Google Data Analytics Certificate','Microsoft PL-300 Power BI cert','Business analytics portfolio (GitHub)','Apply: Analyst / BI Developer roles']}
    ]},
    'Arts & Humanities': {'title':'Arts & Humanities Career Plan','months':[
        {'month':'Month 1-2','title':'Creative Foundation','tasks':['Study creative writing and storytelling','Build strong public speaking skills','Explore art history and cultural studies','Take online courses in visual design']},
        {'month':'Month 3-4','title':'Research & Communication','tasks':['Develop research methods and critical analysis','Create a portfolio of essays/articles','Learn digital media tools like Canva and Adobe Spark','Join debate, theatre, or writing communities']},
        {'month':'Month 5','title':'Specialisation & Projects','tasks':['Choose a humanities focus: Psychology, Literature, Media, Fine Arts','Produce 2-3 case studies or creative projects','Intern or volunteer in education/media/NGO settings','Publish work on blogs, Medium or portfolio site']},
        {'month':'Month 6','title':'Career Launch','tasks':['Prepare a humanities-focused resume and portfolio','Network with professionals in arts, media, education','Apply for internships and entry-level roles','Attend seminars, workshops and cultural events']}
    ]}
}

class CareerPredictor:
    def __init__(self):
        self.model = None
        self.le    = None
        self.meta  = None
        self._load()

    def _load(self):
        try:
            self.model = joblib.load(MODEL)
            self.le    = joblib.load(LE_PATH)
            with open(META) as f:
                self.meta = json.load(f)
            print(f"[ML] Model loaded: {self.meta['best_model']} (accuracy={self.meta['accuracy']})")
        except Exception as e:
            print(f"[ML] Warning: Could not load model ({e}). Using fallback scoring.")

    def _build_feature_vector(self, profile, assessment, user_type):
        """Map profile + assessment → 27-feature vector for the trained model"""
        def g(d, k, default=5.0): 
            v = d.get(k, default)
            try: return float(v) if v not in (None,'',True,False) else (8.0 if v is True else 2.0)
            except: return default

        def yn(d, k): 
            v = d.get(k, False)
            return 8.0 if v in (True,'true','True',1) else 2.0

        def r(d, k): return g(d, k, 5.0)  # rating 1-10

        if user_type == 'student12':
            math  = g(profile,'math_score',70)/10
            phys  = g(profile,'physics_score',70)/10
            cs    = g(profile,'cs_score',70)/10
            logic = g(profile,'logical_reasoning',3)*2
            cgpa  = (g(profile,'twelfth_pct',75)/10)
            feat = [
                cgpa, math, phys, cs, logic,
                7.0 if profile.get('coding_interest') in (True,'true') else 3.0,
                4.0, 5.0, 5.0, 5.0,
                5.0, 4.0,
                8.0 if profile.get('design_interest') in (True,'true') else 3.0,
                g(assessment,'communication',3)*2,
                g(assessment,'leadership_potential',3)*2,
                g(assessment,'creativity',3)*2,
                g(assessment,'problem_solving',3)*2,
                0, 0, 0, 0,
                yn(profile,'coding_interest')*1.2 if profile.get('ai_interest') else g(assessment,'data_interest',3)*2,
                3.0, 3.0,
                8.0 if profile.get('coding_interest') else 3.0,
                8.0 if profile.get('design_interest') else 3.0,
                8.0 if profile.get('business_interest') else 3.0,
            ]
        elif user_type == 'college':
            feat = [
                g(profile,'cgpa',7.5),
                g(profile,'cgpa',7.5)*1.0,
                g(profile,'cgpa',7.5)*0.9,
                g(profile,'cgpa',7.5)*1.1,
                g(assessment,'problem_solving',3)*2,
                g(profile,'python_skill',3)*2,
                4.0, 
                g(profile,'webdev_skill',3)*2,
                g(profile,'sql_skill',3)*2,
                g(profile,'dsa_skill',3)*2,
                8.0 if profile.get('ai_interest') else g(assessment,'ai_ml_interest',3)*2,
                8.0 if profile.get('cloud_interest') else 4.0,
                5.0,
                g(assessment,'communication',3)*2,
                g(assessment,'leadership',3)*2,
                g(assessment,'creativity',3)*2,
                g(assessment,'problem_solving',3)*2,
                g(profile,'projects_count',2),
                1 if profile.get('has_internship') else 0,
                g(profile,'certifications_count',0),
                0,
                9.0 if profile.get('ai_interest') else 4.0,
                9.0 if profile.get('cyber_interest') else 4.0,
                9.0 if profile.get('cloud_interest') else 4.0,
                9.0 if profile.get('web_interest') else 4.0,
                5.0,
                4.0,
            ]
        else:  # employee
            feat = [
                7.5,
                7.0, 6.5, 7.5,
                g(assessment,'problem_solving',3)*2,
                g(profile,'programming_proficiency',3)*2,
                5.0,
                5.5,
                7.0,
                6.5,
                6.0 if profile.get('upskill_interest') else 3.0,
                g(profile,'cloud_experience',3)*2,
                5.0,
                g(assessment,'communication',3)*2,
                g(profile,'leadership_skill',3)*2,
                g(assessment,'creativity',3)*2,
                g(assessment,'problem_solving',3)*2,
                3,
                1 if profile.get('upskill_interest') else 0,
                g(profile,'certifications_count',1),
                g(profile,'years_experience',2),
                8.0 if profile.get('upskill_interest') else 4.0,
                5.0,
                g(profile,'cloud_experience',3)*2,
                5.0, 5.0,
                9.0 if profile.get('management_interest') else 4.0,
            ]
        return np.array(feat, dtype=float).reshape(1, -1)

    def predict(self, profile, assessment, user_type):
        if self.model is None:
            return self._fallback(profile, assessment, user_type)

        fv = self._build_feature_vector(profile, assessment, user_type)
        pred_idx   = self.model.predict(fv)[0]
        proba      = self.model.predict_proba(fv)[0]
        classes    = self.le.classes_

        primary    = classes[pred_idx]
        confidence = round(float(proba[pred_idx]) * 100, 1)
        all_scores = {classes[i]: round(float(p)*100,1) for i,p in enumerate(proba)}
        top_matches= sorted(all_scores.items(), key=lambda x:-x[1])

        user_skills  = self._extract_skills(profile, user_type)
        required     = CAREER_SKILLS.get(primary, [])
        skill_gaps   = [s for s in required if not any(us.lower() in s.lower() or s.lower() in us.lower() for us in user_skills)]
        skill_have   = [s for s in required if s not in skill_gaps]

        return {
            'primary_career':   primary,
            'confidence_score': confidence,
            'all_scores':       dict(top_matches),
            'top_matches':      [{'career':c,'score':s} for c,s in top_matches[:5]],
            'skill_gaps':       skill_gaps,
            'skills_have':      skill_have,
            'roadmap':          ROADMAPS.get(primary, ROADMAPS['Software Engineering']),
            'market_insights':  MARKET_INSIGHTS.get(primary, {}),
            'model_used':       self.meta.get('best_model','ML Model') if self.meta else 'ML Model',
            'model_accuracy':   self.meta.get('accuracy', 0) if self.meta else 0,
        }

    def _extract_skills(self, profile, user_type):
        skills = []
        if user_type == 'college':
            if float(profile.get('python_skill',0)) >= 3: skills.append('Python')
            if float(profile.get('webdev_skill',0)) >= 3: skills.extend(['HTML/CSS','JavaScript'])
            if float(profile.get('sql_skill',0)) >= 3: skills.append('SQL')
            if float(profile.get('dsa_skill',0)) >= 3: skills.append('DSA')
            if 'design' in profile.get('branch','').lower(): skills.append('Design')
        elif user_type == 'employee':
            if float(profile.get('programming_proficiency',0)) >= 3: skills.extend(['Python','Java/C++'])
            if float(profile.get('cloud_experience',0)) >= 3: skills.extend(['AWS/Azure/GCP','Docker'])
            if float(profile.get('leadership_skill',0)) >= 3: skills.extend(['Communication','Leadership'])
        elif user_type == 'student12':
            if float(profile.get('cs_score',0)) >= 70: skills.extend(['Python','HTML/CSS'])
            if float(profile.get('math_score',0)) >= 75: skills.append('Statistics')
            if float(profile.get('logical_reasoning',0)) >= 4: skills.append('Critical Thinking')
            if profile.get('design_interest'): skills.append('Design')
            if profile.get('business_interest'): skills.append('Communication')
            if profile.get('stream') == 'arts' and profile.get('preferred_subjects'):
                skills.append(profile.get('preferred_subjects'))
        return skills

    def _fallback(self, profile, assessment, user_type):
        """Rule-based fallback if model isn't loaded"""
        from ml.skill_gap import get_skill_gap
        scores = {'Software Engineering':50.0,'Web Development':45.0,'Data Science':40.0,
                  'Artificial Intelligence':35.0,'Cybersecurity':30.0,'Cloud Engineering':28.0,
                  'UI/UX Design':25.0,'Product Management':22.0,'Business Analytics':20.0,'Arts & Humanities':26.0}
        primary = 'Software Engineering'
        return {
            'primary_career': primary, 'confidence_score': 50.0,
            'all_scores': scores, 'top_matches': [{'career':k,'score':v} for k,v in list(scores.items())[:5]],
            'skill_gaps': CAREER_SKILLS.get(primary,[])[:4], 'skills_have': [],
            'roadmap': ROADMAPS.get(primary), 'market_insights': MARKET_INSIGHTS.get(primary,{}),
            'model_used': 'Fallback', 'model_accuracy': 0
        }
