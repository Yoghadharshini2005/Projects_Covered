# 🎯 AI Career Guidance System — v2.0

A production-grade full-stack AI web application delivering personalized career
predictions using a **real trained Machine Learning model (96% accuracy)**.

## 🆕 What's New in v2.0
| Feature | v1.0 | v2.0 |
|---|---|---|
| Prediction Engine | Rule-based scoring | **Real ML (Random Forest, 96% acc)** |
| Dataset | None | **496 samples, 9 careers, 27 features** |
| Resume Analyzer | ❌ | **✅ PDF upload → skill extraction** |
| Market Insights | Basic | **Salary, demand, growth, companies** |
| Architecture | Single file | **Modular blueprints (routes/models/ml)** |
| Skill Resources | ❌ | **✅ Direct learning links per skill** |
| Model Comparison | ❌ | **✅ RF vs GBT vs DT vs LR** |
| Admin ML Info | ❌ | **✅ Model stats & feature importance** |

## 🏗️ Project Structure
```
career-guidance-v2/
├── run.py                    ← Start app here
├── train.py                  ← Retrain ML model
├── requirements.txt
│
├── backend/
│   ├── app.py                ← Flask app + blueprint registration
│   ├── config.py             ← Paths & settings
│   │
│   ├── routes/
│   │   ├── auth_routes.py    ← Register / Login / Logout
│   │   ├── profile_routes.py ← Save / Get profile
│   │   ├── assessment_routes.py ← Save assessment
│   │   └── prediction_routes.py ← Predict / Results / Chat / Admin
│   │
│   ├── models/
│   │   └── user_model.py     ← DB init & helper functions
│   │
│   └── ml/
│       ├── train_model.py    ← Train & compare 4 ML algorithms
│       ├── predictor.py      ← Real ML prediction with joblib
│       ├── skill_gap.py      ← Skill gap engine + resources
│       ├── resume_analyzer.py← PDF text extraction & analysis
│       ├── career_model.pkl  ← Trained model (auto-generated)
│       └── model_meta.json   ← Model metadata & accuracy
│
├── frontend/
│   ├── templates/
│   │   └── index.html        ← Complete SPA (1177 lines)
│   └── static/
│
└── dataset/
    ├── generate_dataset.py   ← Generate 500-row training data
    └── career_guidance_dataset_500.csv
```

## ⚡ Quick Start
```bash
# 1. Install dependencies
pip install flask scikit-learn pandas numpy joblib

# 2. (Optional) Retrain the model
python train.py

# 3. Start the app
python run.py

# 4. Open browser
open http://localhost:5000
```

## 🤖 ML Model Details
- **Algorithm**: Random Forest Classifier (200 estimators)
- **Accuracy**: 96% on test set (5-fold CV: 96.2%)
- **Features**: 27 (CGPA, skills, interests, experience, etc.)
- **Classes**: 9 career domains
- **Dataset**: 496 realistic synthetic samples
- **Comparison**: RF vs Gradient Boosting vs Decision Tree vs Logistic Regression

## 🎯 Career Domains Predicted
Data Science · Artificial Intelligence · Software Engineering ·
Web Development · Cybersecurity · Cloud Engineering ·
UI/UX Design · Product Management · Business Analytics

## 📡 REST API Endpoints
| Method | Endpoint | Description |
|---|---|---|
| POST | /api/register | Create account |
| POST | /api/login | Authenticate |
| POST | /api/logout | Sign out |
| GET | /api/session | Get current session |
| POST | /api/profile | Save profile |
| GET | /api/profile | Get profile |
| POST | /api/assessment | Save answers |
| POST | /api/predict | Run ML prediction |
| GET | /api/results | Get saved results |
| POST | /api/resume | Upload & analyze PDF |
| POST | /api/chat | AI mentor chatbot |
| GET | /api/admin/stats | Admin analytics |
