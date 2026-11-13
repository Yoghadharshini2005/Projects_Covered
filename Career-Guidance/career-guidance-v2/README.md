# 🎯 AI Career Guidance System — v2.0

A full-stack AI-powered web application that delivers personalized career recommendations using a trained Machine Learning model. It helps users identify suitable career paths, analyze skill gaps, explore learning resources, and understand career opportunities.

---

## 🆕 What's New in v2.0

| Feature | v1.0 | v2.0 |
|---|---|---|
| Prediction Engine | Rule-based scoring | Random Forest ML model |
| Dataset | None | 496 samples, 9 career domains, 27 features |
| Resume Analyzer | Not available | PDF upload and skill extraction |
| Market Insights | Basic | Salary, demand, growth, and companies |
| Architecture | Single file | Modular Flask blueprints |
| Skill Resources | Not available | Learning links for individual skills |
| Model Comparison | Not available | RF vs GBT vs DT vs LR |
| Admin ML Information | Not available | Model statistics and feature importance |

---

## ✨ Key Features

- **Personalized Career Prediction:** Recommends suitable career domains based on user assessment responses.
- **Machine Learning Integration:** Uses a trained Random Forest classification model.
- **Skill Gap Analysis:** Identifies missing skills required for a recommended career.
- **Resume Analyzer:** Extracts information and skills from uploaded PDF resumes.
- **Career Market Insights:** Provides salary information, job demand, growth trends, and company details.
- **Learning Resources:** Provides useful learning links to improve required skills.
- **Model Comparison:** Compares multiple machine learning algorithms.
- **User Authentication:** Supports registration, login, and logout.
- **Admin Analytics:** Displays model statistics and feature importance.
- **AI Career Mentor:** Provides career-related assistance through a chatbot interface.

---

## 🏗️ Project Structure

```text
career-guidance-v2/
│
├── run.py
├── train.py
├── requirements.txt
│
├── backend/
│   ├── app.py
│   ├── config.py
│   │
│   ├── routes/
│   │   ├── auth_routes.py
│   │   ├── profile_routes.py
│   │   ├── assessment_routes.py
│   │   └── prediction_routes.py
│   │
│   ├── models/
│   │   └── user_model.py
│   │
│   └── ml/
│       ├── train_model.py
│       ├── predictor.py
│       ├── skill_gap.py
│       ├── resume_analyzer.py
│       ├── career_model.pkl
│       └── model_meta.json
│
├── frontend/
│   ├── templates/
│   │   └── index.html
│   └── static/
│
└── dataset/
    ├── generate_dataset.py
    └── career_guidance_dataset_500.csv
```

---

## 🛠️ Technologies Used

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Backend Framework | Flask |
| Machine Learning | Scikit-learn |
| ML Algorithms | Random Forest, Gradient Boosting, Decision Tree, Logistic Regression |
| Data Processing | Pandas, NumPy |
| Model Serialization | Joblib |
| Frontend | HTML, CSS, JavaScript |
| Resume Processing | PDF text extraction |
| Database | SQLite (if configured in the project) |

---

## ⚡ Installation and Setup

### Prerequisites

Make sure the following are installed:

- Python 3.9 or higher
- Git
- pip package manager

### 1. Clone the Repository

```bash
git clone https://github.com/Yoghadharshini2005/Projects_Covered.git
```

### 2. Navigate to the Project Directory

```bash
cd Projects_Covered/Career-Guidance/career-guidance-v2
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

**macOS / Linux:**

```bash
source venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Start the Application

```bash
python run.py
```

### 7. Open the Application

Open your browser and visit:

**http://127.0.0.1:5000**

---

## 🤖 Machine Learning Model Details

The system uses a Random Forest Classifier to predict suitable career domains based on user assessment data.

| Parameter | Details |
|---|---|
| Algorithm | Random Forest Classifier |
| Estimators | 200 |
| Reported Accuracy | 96% |
| Cross-validation Accuracy | 96.2% |
| Number of Features | 27 |
| Number of Career Classes | 9 |
| Dataset Size | 496 samples |

### Model Comparison

The project compares the performance of four machine learning algorithms:

1. Random Forest
2. Gradient Boosting
3. Decision Tree
4. Logistic Regression

### Optional: Retrain the Model

To train the machine learning model again:

```bash
python train.py
```

The training process generates the model and its related metadata files.

---

## 🎯 Career Domains Predicted

The system supports recommendations across nine career domains:

1. Data Science
2. Artificial Intelligence
3. Software Engineering
4. Web Development
5. Cybersecurity
6. Cloud Engineering
7. UI/UX Design
8. Product Management
9. Business Analytics

---

## 📡 REST API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/register` | Create a new account |
| POST | `/api/login` | Authenticate user |
| POST | `/api/logout` | Sign out |
| GET | `/api/session` | Get current session |
| POST | `/api/profile` | Save user profile |
| GET | `/api/profile` | Retrieve user profile |
| POST | `/api/assessment` | Save assessment responses |
| POST | `/api/predict` | Generate ML career prediction |
| GET | `/api/results` | Retrieve prediction results |
| POST | `/api/resume` | Upload and analyze PDF resume |
| POST | `/api/chat` | Interact with career mentor chatbot |
| GET | `/api/admin/stats` | Retrieve admin analytics |

---

## 📊 Application Workflow

1. User registers or logs into the application.
2. User provides profile information.
3. User completes the career assessment.
4. The system processes assessment responses.
5. The trained ML model predicts suitable career domains.
6. The system identifies skill gaps.
7. Users explore learning resources and career market insights.
8. Users can upload resumes for additional skill analysis.

---

## 🔒 Important Notes

- Install all dependencies before starting the application.
- Ensure the dataset and required trained model files are available.
- If model files are missing, run the training script if the project supports generating them.
- Configure any required database or environment settings before running the application.
- Keep credentials and secret keys out of public repositories.

---

## 🚀 Future Enhancements

- Integration with live job market data.
- Advanced resume analysis.
- More personalized learning recommendations.
- Improved career prediction models.
- Cloud deployment and scalable hosting.

---

## 👩‍💻 Author

**Yoghadharshini R**

B.Tech — Artificial Intelligence and Data Science

GitHub: [Yoghadharshini2005](https://github.com/Yoghadharshini2005)

---

⭐ If you find this project useful, consider giving the repository a star!