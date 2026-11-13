# SmartCare+ 🏥

## Overview

**SmartCare+** is a hospital management and healthcare coordination platform designed to connect hospitals, blood donors, and communities for efficient blood and organ donation management.

The system helps manage blood inventory, record donations, handle emergency blood requests, and identify potential organ matches across multiple hospitals through an interactive web interface.

## ✨ Features

### 🩸 Blood Donation Management
- Track blood stock across multiple hospitals.
- Support for all major blood groups (A+, A-, B+, B-, AB+, AB-, O+, O-).
- Record blood donations with donor details.
- Track blood expiry dates.
- Generate expiry alerts for blood units.
- Maintain donation records using CSV files.

### 🫀 Organ Matching System
- Match potential donors and recipients based on blood group compatibility.
- Manage organ information.
- Support different organ categories.
- Display potential donor-recipient matches.

### 🚨 Emergency Donation Requests
- Create emergency blood donation requests.
- Categorize requests by urgency (High, Medium, Low).
- Track request status.
- Store hospital and contact information.
- View existing emergency requests.

### 📊 Dashboard & Analytics
- View blood inventory information.
- Monitor donation records.
- View emergency requests.
- Compare hospital donation performance.
- Display hospital donation leaderboard.

### 🏨 Multi-Hospital Support
- Supports government and private hospitals.
- Includes Coimbatore Medical College and Hospital.
- Includes KMCH (Kovai Medical Center and Hospital).
- Supports adding additional hospitals.

## 📁 Project Structure

```text
SmartCare+/
│
└── backend1/
    ├── app.py
    ├── requirements.txt
    ├── database.db
    ├── blood_donations.csv
    │
    ├── data/
    │   └── donors.csv
    │
    └── static/
        ├── blood-donation.css
        ├── blood-donation.html
        ├── dashboard.css
        ├── dashboard.html
        ├── emergency-requests.css
        ├── emergency-requests.html
        ├── index.css
        ├── index.html
        ├── organ-matching.css
        ├── organ-matching.html
        └── script.js
```

*Note: The SQLite database and CSV files are used for storing application data. The database is initialized by the application.*

## 🛠️ Technology Stack

### Backend
- Python 3
- Flask 3.1.2
- Flask-CORS 6.0.1
- SQLite

### Frontend
- HTML5
- CSS3
- JavaScript
- JSON

### Data Storage
- SQLite Database
- CSV Files

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.9 or higher
- pip package manager
- Git
- Modern web browser

### 1. Clone the Repository

```bash
git clone https://github.com/Yoghadharshini2005/Projects_Covered.git
```

### 2. Navigate to the Project Directory

```bash
cd Projects_Covered/SmartCare+/backend1
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

### 6. Run the Application

```bash
python app.py
```

### 7. Access the Application

Open your browser and visit:

```text
http://127.0.0.1:5000
```

The SmartCare+ application will be available locally.

## 🖥️ Usage Guide

### 1. Login
- Select the hospital type.
- Select the hospital name.
- Enter the required login details.
- Access the application dashboard.

### 2. Dashboard
View hospital and donation-related information through the dashboard.

### 3. Blood Donation Management
- Navigate to the Blood Donation section.
- Enter donor information.
- Provide blood group and donation details.
- Submit the donation record.

### 4. Emergency Requests
- Navigate to Emergency Requests.
- Enter the required blood group and units.
- Select the urgency level.
- Submit and track the request.

### 5. Organ Matching
- Navigate to Organ Matching.
- Enter recipient blood group details.
- Select the required organ.
- View potential matching donors.

## 🔌 API Endpoints

The Flask backend provides the following API routes.

### Blood Management

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/blood_stock` | Retrieve blood inventory |
| POST | `/api/add_blood` | Add blood stock |
| GET | `/api/expiry_alerts` | Retrieve expiry alerts |

### Emergency Requests

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/requests` | Retrieve donation requests |
| POST | `/api/add_donation_request` | Create a donation request |
| POST | `/api/update_request_status` | Update request status |

### Organ Matching

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/add_organ` | Add organ information |
| POST | `/api/organ_match` | Find potential organ matches |
| GET | `/api/donors` | Retrieve donor information |

### Donations & Analytics

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/add_blood_donation` | Record a blood donation |
| POST | `/api/donate` | Add donor information |
| GET | `/api/leaderboard` | Retrieve hospital leaderboard |

### Web Routes

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Login page |
| GET | `/dashboard` | Dashboard |
| GET | `/blood_donation` | Blood donation page |
| GET | `/organ_donation` | Organ matching page |
| GET | `/emergency_request` | Emergency requests page |

## 🗄️ Database

SmartCare+ uses SQLite for storing application information.

The application initializes the following database tables:

- **hospitals** – Hospital information.
- **blood_stock** – Blood inventory details.
- **donation_requests** – Emergency donation requests.
- **organ_matching** – Organ matching information.
- **donors** – Donor information.

The database is stored in `database.db`.

## 📄 Data Files

The project includes CSV files for data management:

- `blood_donations.csv` – Blood donation records.
- `data/donors.csv` – Donor information.

## 🔍 Expiry Management

- Tracks blood unit expiry dates.
- Identifies blood units approaching expiry.
- Provides expiry-related alerts to help reduce blood wastage.

## 📈 Hospital Performance

- Displays hospital donation leaderboard.
- Supports comparison of hospital blood inventory.
- Helps monitor donation activities.

## 🔮 Future Enhancements

- Secure authentication with role-based access control.
- SMS and email notifications.
- Mobile application integration.
- Machine learning-based blood demand forecasting.
- Integration with external blood bank networks.
- Automated report generation.
- Geolocation-based hospital and donor tracking.
- Online donation appointment scheduling.

## 🚀 Troubleshooting

### Database Issues
Check whether the application has permission to access its database file and initialize the database.

### Port Already in Use
If port 5000 is already occupied, configure the Flask application to use another available port.

### Dependency Issues
Install the project dependencies again:

```bash
pip install -r requirements.txt
```

### Static Files Not Loading
Verify that the `static` folder and its files are present in the project directory.

## 👩‍💻 Author

**Yoghadharshini R**

B.Tech – Artificial Intelligence and Data Science

GitHub: [Yoghadharshini2005](https://github.com/Yoghadharshini2005)

## 📌 Project Purpose

Developed as an engineering project to support healthcare coordination through blood donation management, organ matching, and emergency request handling.

**SmartCare+ – Connecting Hearts, Saving Lives ❤️**

⭐ If you find this project useful, consider giving the repository a star!