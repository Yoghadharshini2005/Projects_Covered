# SmartCare+ 🏥

## Overview

**SmartCare+** is a comprehensive hospital management system designed to connect hospitals, donors, and communities for efficient blood and organ donation coordination. The platform enables seamless management of blood inventory, emergency donation requests, and organ matching across multiple hospitals.

---

## Features

### 🩸 Blood Donation Management
- **Blood Stock Tracking**: Monitor blood inventory by type (A+, A-, B+, B-, AB+, AB-, O+, O-) across hospitals
- **Donation Recording**: Comprehensive form to record blood donations with donor details
- **Expiry Alerts**: Automatic notifications for blood units expiring within specified timeframes
- **CSV Export**: All donations are recorded in a detailed CSV file for auditing and analysis
- **Blood Bank Integration**: Support for multiple hospitals and blood banks

### 🫀 Organ Matching System
- **Donor-Recipient Matching**: Intelligent matching based on blood group compatibility
- **Organ Database**: Track available organs (Kidney, Liver, Heart, Lungs, Pancreas, Cornea) from donors
- **Compatibility Verification**: Ensure blood group compatibility between donors and recipients
- **Real-time Notifications**: Instant alerts when matches are found

### 🚨 Emergency Donation Requests
- **Urgent Requests Management**: Create and manage emergency blood donation requests
- **Urgency Levels**: Categorize requests by urgency (High, Medium, Low)
- **Status Tracking**: Monitor request status (Pending, Processing, Fulfilled, etc.)
- **Contact Information**: Store emergency contact numbers for quick coordination
- **Request History**: View all past and current emergency requests

### 📊 Dashboard & Analytics
- **Live Statistics**: Real-time display of:
  - Total units available
  - Total registered donors
  - Active emergency requests
  - Available organs
  - Today's donations
- **Blood Stock Visualization**: Table view of current blood inventory by hospital
- **Donor Leaderboard**: Top-performing hospitals based on donation volume
- **Hospital Comparison**: Compare blood stock across multiple hospitals

### 🏨 Multi-Hospital Support
- **Hospital Profiles**: Support for both government and private hospitals
- **Pre-configured Hospitals**:
  - Coimbatore Medical College and Hospital – Coimbatore
  - KMCH (Kovai Medical Center and Hospital) – Coimbatore
- **Expandable System**: Easy addition of new hospitals to the network

---

## Project Structure

```
SmartCare+ 2/
├── backend/
│   ├── app.py                    # Flask backend application
│   ├── requirements.txt          # Python dependencies
│   ├── database.db              # SQLite database (auto-created)
│   ├── blood_donations.csv      # Donation records export
│   ├── data/
│   │   └── donors.csv           # Sample donor data
│   └── static/
│       ├── index.html           # Login page
│       ├── dashboard.html       # Main dashboard
│       ├── blood-donation.html  # Blood donation form
│       ├── organ-matching.html  # Organ matching interface
│       ├── emergency-requests.html  # Emergency requests management
│       ├── index.css            # Login page styling
│       ├── dashboard.css        # Dashboard styling
│       ├── blood-donation.css   # Blood donation form styling
│       ├── organ-matching.css   # Organ matching styling
│       ├── emergency-requests.css  # Emergency requests styling
│       └── script.js            # Frontend JavaScript logic
└── README.md                     # This file
```

---

## Technology Stack

### Backend
- **Framework**: Flask 3.1.2
- **Database**: SQLite
- **CORS**: flask-cors 6.0.1
- **Language**: Python 3.x

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Responsive design
- **JavaScript**: Dynamic interactions and API communication
- **JSON**: Data format for API communication

### Key Dependencies
```
Flask==3.1.2
flask-cors==6.0.1
Jinja2==3.1.6
Werkzeug==3.1.3
```

---

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)
- Modern web browser

### Step 1: Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python app.py
```

The application will start on `http://localhost:5000`

### Step 3: Access the Web Interface
Open your browser and navigate to:
```
http://localhost:5000
```

---

## Usage Guide

### 1. Login
- Select hospital type (Government/Private)
- Select hospital name from the dropdown
- Enter email and password
- Click "Login" to access the dashboard

### 2. Dashboard
View real-time statistics:
- Total blood units available
- Registered donors count
- Active emergency requests
- Available organs
- Today's donations

### 3. Blood Donation Management
**Recording a Donation:**
- Navigate to "Blood Donation" section
- Fill in donor details (name, age, gender, blood type)
- Enter contact information and address
- Specify number of units collected
- Automatically calculates 42-day expiry date
- Submit to record the donation

### 4. Emergency Requests
**Creating an Emergency Request:**
- Go to "Emergency Requests"
- Specify hospital, blood type, and units needed
- Set urgency level (High/Medium/Low)
- Provide contact information
- Track request status in real-time

**Managing Requests:**
- View all pending and completed requests
- Update request status as donations arrive
- Monitor urgency-based prioritization

### 5. Organ Matching
**Finding Organ Matches:**
- Navigate to "Organ Matching"
- Enter recipient's blood group
- Specify required organ type
- System searches compatible donors
- View matched donor information

---

## API Endpoints

### Blood Management
- `GET /api/blood_stock` - Retrieve all blood inventory
- `POST /api/add_blood` - Add blood to inventory
- `GET /api/expiry_alerts` - Get blood expiring within X days

### Emergency Requests
- `GET /api/requests` - Get all donation requests
- `POST /api/add_donation_request` - Create emergency request
- `POST /api/update_request_status` - Update request status

### Organ Matching
- `POST /api/add_organ` - Add organ to database
- `POST /api/organ_match` - Find compatible organ matches
- `GET /api/donors` - Get all registered donors

### Donations & Analytics
- `POST /api/add_blood_donation` - Record blood donation
- `POST /api/donate` - Add donor information
- `GET /api/leaderboard` - Get top hospital performers

### Static Files
- `GET /` - Home/Login page
- `GET /dashboard` - Main dashboard
- `GET /blood_donation` - Blood donation page
- `GET /organ_donation` - Organ matching page
- `GET /emergency_request` - Emergency requests page

---

## Database Schema

### hospitals
- `id`: Primary key
- `name`: Hospital name (unique)
- `type`: Hospital type (government/private)

### blood_stock
- `id`: Primary key
- `hospital_name`: Associated hospital
- `blood_type`: Blood type (A+, B+, etc.)
- `units`: Number of units available
- `expiry_date`: Expiry date of blood

### donation_requests
- `id`: Primary key
- `hospital_name`: Requesting hospital
- `blood_type`: Required blood type
- `units_needed`: Number of units requested
- `urgency_level`: Urgency level (High/Medium/Low)
- `date`: Request date
- `contact`: Contact number
- `status`: Request status (Pending/Fulfilled/etc.)

### organ_matching
- `id`: Primary key
- `hospital_name`: Hospital name
- `organ_type`: Type of organ
- `donor_blood`: Donor blood group
- `recipient_blood`: Recipient blood group

### donors
- `id`: Primary key
- `name`: Donor name
- `age`: Donor age
- `blood_group`: Blood group
- `units`: Units donated
- `donation_date`: Date of donation
- `hospital`: Associated hospital
- `organ`: Available organ type

---

## Sample Data

The system comes pre-populated with:
- **Sample Donors**: 7 registered donors with various organs
- **Emergency Requests**: 5 sample requests from different hospitals
- **Hospitals**: Coimbatore Medical College and KMCH

All sample data is automatically initialized when the application starts for the first time.

---

## Features in Detail

### 🔍 Expiry Management
- Tracks expiry dates for all blood units
- Generates alerts for units expiring within 3 days (configurable)
- Helps prevent wastage of precious blood resources

### 📈 Performance Metrics
- Leaderboard showing top 5 hospitals by donation volume
- Track donor participation and contribution
- Monitor emergency request response times

### 🔐 Data Privacy
- Hospital-specific data isolation
- Secure storage of contact information
- CSV export for record keeping and auditing

### 🌐 Multi-Hospital Coordination
- Unified dashboard for network-wide visibility
- Inter-hospital blood transfer coordination
- Organ matching across hospital boundaries

---

## Future Enhancements

- **User Authentication**: Implement secure login with role-based access control
- **SMS/Email Notifications**: Automated alerts for urgent requests
- **Mobile App**: Native mobile application for on-the-go access
- **Advanced Analytics**: Machine learning-based demand forecasting
- **Integration**: Connect with national blood bank networks
- **Report Generation**: Automated health and compliance reports
- **Geolocation**: Map-based hospital and donor location tracking
- **Appointment Scheduling**: Book donation appointments in advance

---

## Troubleshooting

### Database Issues
- Delete `database.db` to reset the database
- Re-run the application to regenerate with sample data

### Port Already in Use
- Change the port in `app.py`: `app.run(debug=True, port=5001)`

### CORS Errors
- Ensure `flask-cors` is installed: `pip install flask-cors`

### Static Files Not Loading
- Verify the `static` folder path is correct
- Check file permissions

---

## Contributing

To contribute to SmartCare+:
1. Review the current codebase
2. Make necessary improvements or bug fixes
3. Test thoroughly
4. Document changes
5. Submit for review

---

## License

This project is developed for educational and healthcare coordination purposes.

---

## Contact & Support

For issues, questions, or suggestions regarding SmartCare+, please contact the development team.

---

## Acknowledgments

Built for efficient coordination between:
- 🏥 Healthcare Institutions
- 👥 Blood Donors
- 🫀 Organ Donors
- 👨‍⚕️ Medical Professionals
- 💙 Communities

**SmartCare+ - Connecting Hearts, Saving Lives** ❤️
