# 🏭 Predictive Maintenance System for Machine Health Monitoring

A machine learning-based predictive maintenance web application that monitors industrial machine health using sensor data such as temperature, vibration, pressure, and RPM.

The system predicts machine conditions, identifies potential failures, provides root cause analysis, and supports maintenance decision-making through an interactive web dashboard.

---

## ✨ Key Features

- **Machine Health Prediction:** Predicts whether a machine is Healthy, Warning, or Failure.
- **Machine Learning Models:** Uses XGBoost and Logistic Regression classifiers.
- **Sensor Monitoring:** Analyzes temperature, vibration, pressure, and RPM.
- **Root Cause Analysis:** Identifies probable reasons behind machine failures.
- **Threshold Alerts:** Highlights sensor readings that exceed defined limits.
- **Digital Twin Simulation:** Simulates machine degradation over a 24-hour period.
- **AI Maintenance Assistant:** Provides maintenance-related answers through a rule-based chatbot.
- **Prediction History:** Stores previous predictions using SQLite.
- **Performance Visualization:** Displays model evaluation and sensor analysis charts.
- **Interactive Dashboard:** Provides machine health insights through a web interface.

---

## 📁 Project Structure

```text
predictive_maintenance_system/
│
├── app.py
├── model.py
├── requirements.txt
├── README.md
│
├── dataset/
│   └── sensor_data.csv
│
├── saved_model/
│   ├── xgb_model.pkl
│   ├── scaler.pkl
│   └── metrics.json
│
├── templates/
│   └── index.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   ├── js/
│   │   └── app.js
│   │
│   └── img/
│       ├── temperature_dist.png
│       ├── vibration_trends.png
│       ├── confusion_matrix.png
│       ├── feature_importance.png
│       └── model_comparison.png
│
└── logs/
    └── maintenance.db
```

*Note: Dataset, trained model files, visualization plots, and database files may be generated automatically when the corresponding scripts or application are executed.*

---

## 🛠️ Tech Stack

| Layer | Technologies |
|---|---|
| Programming Language | Python |
| Machine Learning | XGBoost, Scikit-learn |
| Backend | Flask, Flask-CORS |
| Data Processing | Pandas, NumPy |
| Database | SQLite |
| Visualization | Matplotlib, Seaborn |
| Frontend | HTML5, CSS3, JavaScript |
| Charts | Chart.js |
| Model Persistence | Joblib |

---

## ⚙️ Installation and Setup

### Prerequisites

Make sure you have installed:

- Python 3.9 or higher
- Git
- pip package manager

### 1. Clone the Repository

```bash
git clone https://github.com/Yoghadharshini2005/Projects_Covered.git
```

### 2. Navigate to the Project Directory

```bash
cd Projects_Covered/predictive_maintenance_system
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

### 6. Train the Machine Learning Models

```bash
python model.py
```

The training script is designed to:

- Generate synthetic sensor data (if supported by the script).
- Train XGBoost and Logistic Regression classifiers.
- Evaluate model performance.
- Generate visualization plots.
- Save trained model artifacts and metrics.

### 7. Start the Flask Application

```bash
python app.py
```

### 8. Open the Dashboard

Open your browser and visit:

**http://127.0.0.1:5000**

---

## 🖥️ Dashboard Features

| Module | Description |
|---|---|
| Dashboard | KPI overview, model performance, and sensor thresholds |
| Analyse | Enter sensor values and receive machine predictions with root cause analysis |
| Digital Twin | 24-hour machine degradation simulation with charts |
| AI Assistant | Rule-based chatbot for maintenance-related questions |
| History | View previously stored machine predictions |
| Charts | Explore sensor and model visualization plots |

---

## 🤖 Machine Learning Workflow

The system follows these steps to predict machine health:

1. **Data Generation:** Creates synthetic sensor records labelled as Healthy, Warning, or Failure.
2. **Data Preprocessing:** Handles missing values and prepares sensor features.
3. **Feature Scaling:** Applies StandardScaler to normalize input features.
4. **Model Training:** Trains XGBoost and Logistic Regression classifiers.
5. **Model Evaluation:** Evaluates model performance using classification metrics.
6. **Prediction:** Uses the trained XGBoost classifier to predict machine conditions.
7. **Confidence Estimation:** Uses prediction probabilities to estimate confidence.
8. **Root Cause Analysis:** Applies rule-based sensor thresholds to identify probable failure causes.

### Machine Condition Classes

| Class | Condition | Description |
|---|---|---|
| 0 | Healthy | Sensor readings are within normal operating ranges |
| 1 | Warning | One or more sensor readings are approaching critical limits |
| 2 | Failure | Critical sensor readings indicate a potential machine failure |

---

## 📊 Model Performance

The project evaluates two machine learning algorithms:

- XGBoost Classifier
- Logistic Regression Classifier

**Reported training results:**

| Model | Reported Accuracy |
|---|---:|
| XGBoost | 99.83% |
| Logistic Regression | 99.17% |

*Note: These are the reported results from the project description. Actual performance may vary depending on the dataset, train-test split, and training configuration. Refer to `saved_model/metrics.json` for the generated evaluation metrics.*

---

## 📈 Sample Sensor Values

| Scenario | Temperature | Vibration | Pressure | RPM |
|---|---:|---:|---:|---:|
| Healthy | 52°C | 0.28g | 102 PSI | 1510 |
| Warning | 74°C | 0.72g | 84 PSI | 1260 |
| Failure | 102°C | 1.85g | 55 PSI | 880 |

These values represent example sensor readings for different machine conditions.

---

## 🔌 REST API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Main dashboard interface |
| POST | `/api/predict` | Predict machine condition |
| POST | `/api/chat` | Interact with maintenance assistant |
| POST | `/api/digital-twin` | Run 24-hour simulation |
| GET | `/api/history` | Retrieve recent predictions |
| GET | `/api/stats` | Retrieve system statistics |
| GET | `/api/metrics` | Retrieve model performance metrics |

### 1. Machine Prediction API

**Endpoint:** `POST /api/predict`

Example request:

```bash
curl -X POST http://127.0.0.1:5000/api/predict \
-H "Content-Type: application/json" \
-d '{"temperature":95,"vibration":1.9,"pressure":58,"rpm":870}'
```

Example response:

```json
{
  "success": true,
  "result": {
    "condition": "Failure",
    "confidence": 99.7,
    "probabilities": {
      "Healthy": 0.1,
      "Warning": 0.2,
      "Failure": 99.7
    },
    "root_causes": [
      {
        "cause": "Overheating",
        "sensor": "Temperature",
        "value": "95.0°C",
        "explanation": "Motor or bearing temperature exceeds safe limits.",
        "action": "Inspect the cooling system and follow maintenance safety procedures."
      }
    ],
    "threshold_alerts": [
      {
        "sensor": "temperature",
        "level": "FAILURE",
        "msg": "Critical overheating detected."
      }
    ]
  }
}
```

*The response above is an illustrative example. Actual response fields and values depend on the application implementation.*

### 2. Maintenance Chat API

**Endpoint:** `POST /api/chat`

Example request:

```bash
curl -X POST http://127.0.0.1:5000/api/chat \
-H "Content-Type: application/json" \
-d '{"message":"What is the machine status?"}'
```

---

## 🗄️ Database Design

The application uses SQLite to store machine monitoring information.

The database is designed to maintain:

### Predictions Table

Stores machine sensor readings and prediction results.

| Field | Description |
|---|---|
| id | Unique prediction ID |
| temperature | Temperature reading |
| vibration | Vibration reading |
| pressure | Pressure reading |
| rpm | Rotational speed |
| condition | Predicted machine condition |
| confidence | Prediction confidence |
| timestamp | Prediction date and time |

### Alerts Table

Stores machine threshold alerts and related information.

### Chat History Table

Stores maintenance assistant conversation history.

*The actual database schema depends on the SQLite initialization code in the application.*

---

## 🤖 AI Maintenance Assistant

The maintenance assistant supports questions related to:

- What is the machine status?
- What is the failure probability?
- What is the current temperature?
- What is the vibration level?
- What is the pressure reading?
- What is the RPM?
- Are there any anomalies?
- What maintenance action should I take?
- What are the maintenance recommendations?

---

## 📊 Visualizations

The project includes visualizations to understand machine sensor data and model performance.

- Temperature Distribution
- Vibration Trends
- Confusion Matrix
- Feature Importance
- Model Comparison

---

## 🔮 Future Enhancements

- Real-time IoT sensor integration.
- Live industrial machine monitoring.
- Advanced anomaly detection.
- Remaining Useful Life (RUL) estimation.
- Cloud-based predictive maintenance.
- Automated maintenance scheduling.
- Integration with industrial equipment monitoring systems.

---

## 👩‍💻 Author

**Yoghadharshini R**

B.Tech — Artificial Intelligence and Data Science

GitHub: [Yoghadharshini2005](https://github.com/Yoghadharshini2005)

---

⭐ If you find this project useful, consider giving the repository a star!

*Built as an Engineering Project — Predictive Maintenance Using Machine Learning.*