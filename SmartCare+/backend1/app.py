from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
import sqlite3
import os
import csv
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

DB_FILE = "database.db"

# ------------------- Initialize Database -------------------
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # Hospitals table
    c.execute('''
        CREATE TABLE IF NOT EXISTS hospitals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            type TEXT
        )
    ''')

    # Blood stock table
    c.execute('''
        CREATE TABLE IF NOT EXISTS blood_stock (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hospital_name TEXT,
            blood_type TEXT,
            units INTEGER,
            expiry_date TEXT
        )
    ''')

    # Blood donation requests table
    c.execute('''
        CREATE TABLE IF NOT EXISTS donation_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hospital_name TEXT,
            blood_type TEXT,
            units_needed INTEGER,
            urgency_level TEXT,
            date TEXT,
            contact TEXT,
            status TEXT DEFAULT 'Pending'
        )
    ''')

    # Organ matching table (requests)
    c.execute('''
        CREATE TABLE IF NOT EXISTS organ_matching (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hospital_name TEXT,
            organ_type TEXT,
            donor_blood TEXT,
            recipient_blood TEXT
        )
    ''')

    # Donors table (with organ field)
    c.execute('''
        CREATE TABLE IF NOT EXISTS donors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            blood_group TEXT,
            units INTEGER,
            donation_date DATE,
            hospital TEXT,
            organ TEXT
        )
    ''')

    # Sample hospitals
    hospitals = [
        ("Coimbatore Medical College and Hospital – Coimbatore", "government"),
        ("KMCH (Kovai Medical Center and Hospital) – Coimbatore", "private")
    ]
    for name, htype in hospitals:
        try:
            c.execute("INSERT INTO hospitals (name, type) VALUES (?,?)", (name, htype))
        except sqlite3.IntegrityError:
            pass

    conn.commit()
    conn.close()

# ------------------- Seed Sample Donors -------------------
def seed_donors():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    sample_donors = [
        ("Arun Kumar", 28, "A+", 1, "2025-10-01", "KMCH (Kovai Medical Center and Hospital) – Coimbatore", "Kidney"),
        ("Priya R", 34, "B+", 1, "2025-09-28", "Coimbatore Medical College and Hospital – Coimbatore", "Liver"),
        ("Suresh M", 45, "O+", 1, "2025-09-15", "KMCH (Kovai Medical Center and Hospital) – Coimbatore", "Heart"),
        ("Divya S", 26, "AB+", 1, "2025-10-05", "Coimbatore Medical College and Hospital – Coimbatore", "Lungs"),
        ("Karthik N", 32, "A-", 1, "2025-09-20", "KMCH (Kovai Medical Center and Hospital) – Coimbatore", "Cornea"),
        ("Meena V", 29, "B-", 1, "2025-09-25", "Coimbatore Medical College and Hospital – Coimbatore", "Kidney"),
        ("Ravi T", 40, "O-", 1, "2025-09-30", "KMCH (Kovai Medical Center and Hospital) – Coimbatore", "Pancreas"),
        ("Anjali P", 36, "AB-", 1, "2025-09-18", "Coimbatore Medical College and Hospital – Coimbatore", "Liver"),
        ("Ganesh K", 30, "A+", 1, "2025-10-07", "KMCH (Kovai Medical Center and Hospital) – Coimbatore", "Heart"),
        ("Lakshmi S", 27, "O+", 1, "2025-10-09", "Coimbatore Medical College and Hospital – Coimbatore", "Kidney")
    ]

    for d in sample_donors:
        try:
            c.execute("""
                INSERT INTO donors (name, age, blood_group, units, donation_date, hospital, organ)
                VALUES (?,?,?,?,?,?,?)
            """, d)
        except sqlite3.IntegrityError:
            pass

    conn.commit()
    conn.close()

# ------------------- Seed Sample Emergency Requests -------------------
def seed_emergency_requests():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    sample_requests = [
        ("Coimbatore Medical College and Hospital – Coimbatore", "O+", 3, "High", "2025-10-15", "9876543210", "Pending"),
        ("KMCH (Kovai Medical Center and Hospital) – Coimbatore", "B+", 2, "High", "2025-10-16", "9876543211", "Pending"),
        ("PSG Hospitals – Peelamedu, Coimbatore", "A+", 4, "Medium", "2025-10-17", "9876543212", "Pending"),
        ("Ganga Hospital – Coimbatore", "AB-", 1, "Low", "2025-10-18", "9876543213", "Pending"),
        ("Sri Ramakrishna Hospital – Sidhapudur, Coimbatore", "O-", 2, "High", "2025-10-19", "9876543214", "Pending"),
    ]

    for req in sample_requests:
        try:
            c.execute("""
                INSERT INTO donation_requests (hospital_name, blood_type, units_needed, urgency_level, date, contact, status)
                VALUES (?,?,?,?,?,?,?)
            """, req)
        except sqlite3.IntegrityError:
            pass

    conn.commit()
    conn.close()

# Run DB init + seed donors + seed emergency requests once
init_db()
seed_donors()
seed_emergency_requests()

# ------------------- Serve Static Pages -------------------
@app.route("/")
def serve_index():
    return send_from_directory('static', 'index.html')

@app.route("/dashboard")
def serve_dashboard():
    return render_template("dashboard.html")

@app.route("/blood_donation")
def serve_blood_donation():
    return send_from_directory('static', 'blood-donation.html')

@app.route("/organ_donation")
def serve_organ_donation():
    return send_from_directory('static', 'organ-matching.html')

@app.route("/emergency_request")
def serve_emergency_request():
    return send_from_directory('static', 'emergency-requests.html')

@app.route("/<path:path>")
def serve_file(path):
    return send_from_directory('static', path)

# ------------------- API: Blood Stock -------------------
@app.route("/api/blood_stock")
def get_blood_stock():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT hospital_name, blood_type, units, expiry_date FROM blood_stock")
    rows = c.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

# ------------------- API: Add Blood -------------------
@app.route("/api/add_blood", methods=["POST"])
def add_blood():
    data = request.json
    hospital_name = data.get("hospital_name")
    blood_type = data.get("blood_type")
    units = int(data.get("units", 0))
    expiry_date = data.get("expiry_date")

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO blood_stock (hospital_name, blood_type, units, expiry_date) VALUES (?,?,?,?)",
              (hospital_name, blood_type, units, expiry_date))
    conn.commit()
    conn.close()
    return jsonify({"message": f"{units} units of {blood_type} added for {hospital_name}!"})

# ------------------- API: Expiry Alerts -------------------
@app.route("/api/expiry_alerts")
def expiry_alerts():
    days = int(request.args.get("days", 3))
    limit_date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT hospital_name, blood_type, expiry_date FROM blood_stock WHERE expiry_date <= ?", (limit_date,))
    rows = c.fetchall()
    conn.close()
    return jsonify([{"hospital_name": r[0], "blood_type": r[1], "expiry_date": r[2]} for r in rows])

# ------------------- API: Emergency Donation Requests -------------------
@app.route("/api/add_donation_request", methods=["POST"])
def add_request():
    data = request.json
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        INSERT INTO donation_requests (hospital_name, blood_type, units_needed, urgency_level, date, contact, status)
        VALUES (?,?,?,?,?,?,?)
    """, (data.get("hospital_name"), data.get("blood_type"), data.get("units_needed"), data.get("urgency_level"), 
          data.get("date"), data.get("contact"), data.get("status", "Pending")))
    conn.commit()
    conn.close()
    return jsonify({"message": "Emergency donation request posted!"})

@app.route("/api/requests")
def get_requests():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT id, hospital_name, blood_type, units_needed, urgency_level, date, contact, status FROM donation_requests ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route("/api/update_request_status", methods=["POST"])
def update_request_status():
    data = request.json
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE donation_requests SET status=? WHERE id=?", (data.get("status"), data.get("id")))
    conn.commit()
    conn.close()
    return jsonify({"message": "Request status updated!"})

# ------------------- API: Organ Matching -------------------
@app.route("/api/add_organ", methods=["POST"])
def add_organ():
    data = request.json
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        INSERT INTO organ_matching (hospital_name, organ_type, donor_blood, recipient_blood)
        VALUES (?,?,?,?)
    """, (data.get("hospital_name"), data.get("organ_type"), data.get("donor_blood"), data.get("recipient_blood")))
    conn.commit()
    conn.close()
    return jsonify({"message": "Organ matching data saved!"})

@app.route("/api/organ_match", methods=["POST"])
def organ_match():
    data = request.json
    blood_group = data["blood_group"]
    organ_needed = data["organ_needed"]

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT name, hospital FROM donors WHERE blood_group=? AND organ=? LIMIT 1",
              (blood_group, organ_needed))
    donor = c.fetchone()
    conn.close()

    if donor:
        return jsonify({"message": f"✅ Match found! Donor: {donor[0]} (Hospital: {donor[1]})"})
    else:
        return jsonify({"message": "❌ No match available right now."})

# ------------------- API: Leaderboard -------------------
@app.route("/api/leaderboard")
def leaderboard():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT hospital_name, SUM(units) as total_donations FROM blood_stock GROUP BY hospital_name ORDER BY total_donations DESC LIMIT 5")
    rows = c.fetchall()
    conn.close()
    return jsonify([{"name": r[0], "donations": r[1]} for r in rows])

# ------------------- API: Blood Donation + CSV -------------------
@app.route("/api/add_blood_donation", methods=["POST"])
def add_blood_donation():
    data = request.json or {}

    # Accept multiple possible field names coming from the extended form
    donor_name = data.get("donor_name")
    phone = data.get("phone") or data.get("alt_phone")
    address = data.get("address")
    place = data.get("place") or data.get("city")
    hospital_name = data.get("hospital_name")
    # blood_type fallback order: original field, collected type, blood_group
    blood_type = data.get("blood_type") or data.get("collected_blood_type") or data.get("blood_group") or "Unknown"

    # Safely parse units
    try:
        units = int(data.get("units") or 0)
    except (ValueError, TypeError):
        units = 0

    donation_date = data.get("donation_date") or datetime.now().strftime("%Y-%m-%d")
    expiry_date = data.get("expiry_date") or (datetime.now() + timedelta(days=42)).strftime("%Y-%m-%d")

    # Insert into blood_stock (keep schema expectations)
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("""
            INSERT INTO blood_stock (hospital_name, blood_type, units, expiry_date)
            VALUES (?,?,?,?)
        """, (hospital_name, blood_type, units, expiry_date))
        conn.commit()
    finally:
        conn.close()

    # Append a comprehensive CSV row with many fields (non-blocking)
    csv_file = "blood_donations.csv"
    file_exists = os.path.isfile(csv_file)
    headers = [
        "Donor Name", "Age", "Gender", "DOB", "Phone", "Alt Phone", "Email", "Emergency Name", "Emergency Phone",
        "Address", "City", "District", "State", "Pincode", "Nearest Bank",
        "Hospital", "Blood Bank", "License No", "Technician", "Donation Location",
        "Collected Blood Type", "Units", "Collection Method", "Bag Barcode", "Storage Temp", "Expiry Date", "Blood Status",
        "Hemoglobin", "BP", "Pulse", "Temperature", "Medical History", "Current Medications", "Eligibility",
        "HIV", "HBsAg", "HCV", "Syphilis", "Malaria",
        "Verified By", "Verified At", "Consent", "Privacy Accepted", "Notify Pref", "Recorded At"
    ]

    row = [
        donor_name, data.get("age"), data.get("gender"), data.get("dob"), phone, data.get("alt_phone"), data.get("email"), data.get("emergency_name"), data.get("emergency_phone"),
        address, data.get("city"), data.get("district"), data.get("state"), data.get("pincode"), data.get("nearest_bank"),
        hospital_name, data.get("blood_bank_name"), data.get("license_no"), data.get("technician"), data.get("donation_location"),
        blood_type, units, data.get("collection_method"), data.get("bag_barcode"), data.get("storage_temp"), expiry_date, data.get("blood_status"),
        data.get("hemoglobin"), data.get("bp"), data.get("pulse"), data.get("temperature"), data.get("medical_history"), data.get("current_medications"), data.get("eligibility"),
        data.get("hiv"), data.get("hbsag"), data.get("hcv"), data.get("syphilis"), data.get("malaria"),
        data.get("verified_by"), data.get("verified_at"), data.get("consent"), data.get("privacy_accept"), data.get("notify_pref"), datetime.now().isoformat()
    ]

    try:
        with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(headers)
            writer.writerow(row)
    except Exception:
        # CSV write errors should not break the API call
        pass

    return jsonify({"message": "Blood donation successfully recorded!"})

# ------------------- API: Donors -------------------
@app.route('/api/donors')
def get_donors():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM donors")
    rows = c.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/api/donate', methods=['POST'])
def donate():
    data = request.json
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        INSERT INTO donors (name, age, blood_group, units, donation_date, hospital, organ)
        VALUES (?,?,?,?,?,?,?)
    """, (data.get("name"), data.get("age"), data.get("blood_group"), data.get("units"),
          data.get("donation_date"), data.get("hospital"), data.get("organ")))
    conn.commit()
    conn.close()
    return jsonify({"message": "Donation added successfully!"}), 201

# ------------------- Run App -------------------
if __name__ == "__main__":
    app.run(debug=True)
