# AI Career Guidance Extension - TODO
Status: ✅ Plan Approved | 🔄 In Progress | ⏳ Pending

## Breakdown Steps

### 1. Setup Services & Utils [✅]
- [x] Create `backend/services/__init__.py`
- [x] Create `backend/utils/csv_loader.py` (pandas load CSVs)
- [x] Create `backend/services/skill_gap_service.py`
- [x] Create `backend/services/course_recommendation.py`
- [x] Create `backend/services/assessment_service.py`

### 2. Database Extensions [🔄]
- [x] Edit `backend/models/user_model.py`: Add job_roles, courses, questions tables
- [x] Add seed functions from dataset/ CSVs

### 3. New Route Blueprints [✅]
- [x] Create `backend/routes/skill_gap_routes.py` (POST /skill-gap)
- [x] Create `backend/routes/course_routes.py` (GET /recommend-courses)
- [x] Create `backend/routes/admin_routes.py` (add/view)
- [x] Edit `backend/routes/assessment_routes.py`: Complete quiz APIs
- [x] Edit `backend/routes/prediction_routes.py`: Add /predict-career

### 4. App Integration [✅]
- [x] Edit `backend/app.py`: Register new blueprints

### 5. Frontend Pages [🔄]
- [x] Create templates/resume.html
- [x] Create templates/skillgap.html
- [x] Create templates/courses.html
- [x] Create templates/assessment.html
- [x] Create templates/admin.html

### 6. Polish & Test [✅]
- [x] Update requirements.txt (pandas, pypdf2)
- [x] Backend APIs implemented & testable
- [x] DB auto-seeded on run.py
- [x] README instructions added

**Next Step: Start with services/utils creation.**

