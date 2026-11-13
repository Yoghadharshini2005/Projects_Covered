// ------------------- Hospital List -------------------
const hospitals = {
    government: [
        "Coimbatore Medical College and Hospital – Coimbatore",
        "Ganga Hospital – Coimbatore",
        "Government Hospital – Peelamedu",
        "Government Hospital – Mettupalayam",
        "Government Hospital – Sulur",
        "Government Hospital – Singanallur",
        "Government Hospital – RS Puram",
        "Government Hospital – Gandhipuram",
        "Government Hospital – Saibaba Colony",
        "Government Hospital – Ramanathapuram",
        "Government Hospital – Avinashi Road",
        "Government Hospital – Kovaipudur",
        "Government Hospital – Kavundampalayam",
        "Government Hospital – Ukkadam",
        "Government Hospital – Podanur"
    ],
    private: [
        "KMCH (Kovai Medical Center and Hospital) – Coimbatore",
        "PSG Hospitals – Peelamedu, Coimbatore",
        "Sri Ramakrishna Hospital – Sidhapudur, Coimbatore",
        "Royal Care Super Speciality Hospital – Neelambur, Coimbatore",
        "KG Hospital – Arts College Road, Coimbatore",
        "Elce Clinics – Coimbatore",
        "CSR Hospitals – Coimbatore",
        "Ashwin Hospital – Coimbatore",
        "Ganga Hospital (Orthopedics & Trauma) – Coimbatore",
        "KMCH Kovilpalayam Hospital – Kovilpalayam, Coimbatore",
        "Sree Abirami Hospital – Coimbatore",
        "Sree Renga Hospital – Coimbatore",
        "Sree Lakshmi Hospital – Coimbatore",
        "Sree Venkateshwara Hospital – Coimbatore",
        "Sree Krishna Hospital – Coimbatore",
        "Sree Ram Hospital – Coimbatore",
        "Sree Sai Hospital – Coimbatore",
        "Sree Balaji Hospital – Coimbatore",
        "Sree Durga Hospital – Coimbatore",
        "Sree Raghavendra Hospital – Coimbatore",
        "Sree Chandra Hospital – Coimbatore",
        "Sree Ganesh Hospital – Coimbatore",
        "PSG Specialty Hospital – Peelamedu, Coimbatore",
        "KMCH Blood Bank – Coimbatore",
        "PSG Blood Bank – Peelamedu, Coimbatore",
        "GKNM Hospital Blood Bank – Mettupalayam Road, Coimbatore",
        "Sri Ramakrishna Hospital Blood Bank – Sidhapudur, Coimbatore",
        "Royal Care Hospital Blood Bank – Neelambur, Coimbatore",
        "GEM Hospital – Pankaja Mills Rd, Coimbatore",
        "Lotus Eye Hospital and Institute – Coimbatore",
        "Sumith Multi Speciality Hospital – Peelamedu, Coimbatore",
        "VGM Gastro Centre – Singanallur, Coimbatore",
        "Sheela Hospital – Tatabad, Coimbatore",
        "Arun Hospital – Pollachi",
        "FIMS Hospitals – Coimbatore",
        "Coimbatore Kidney Centre & Specialty Hospitals – Coimbatore"
    ]
};

// ------------------- Update Hospital Names in Login -------------------
function updateHospitalNames() {
    const type = document.getElementById("hospitalType").value;
    const select = document.getElementById("hospitalName");
    if (!select) return;
    select.innerHTML = '<option value="">Select Hospital Name</option>';
    if (type && hospitals[type]) {
        hospitals[type].forEach(hospital => {
            const option = document.createElement("option");
            option.value = hospital;
            option.textContent = hospital;
            select.appendChild(option);
        });
    }
}

// ------------------- Populate Hospital Dropdown in Dashboard -------------------
function populateHospitalDropdown() {
    const select = document.getElementById("donorHospital");
    if (!select) return;
    select.innerHTML = '';
    Object.keys(hospitals).forEach(type => {
        hospitals[type].forEach(hospital => {
            const option = document.createElement("option");
            option.value = hospital;
            option.text = hospital;
            select.appendChild(option);
        });
    });
    const logged = localStorage.getItem("loggedHospital");
    if (logged) select.value = logged;
}

// ------------------- Populate Blood Type Dropdown -------------------
function populateBloodTypeDropdown() {
    const donorBlood = document.getElementById("donorBloodType");
    const recipientBlood = document.getElementById("donorBlood") || document.getElementById("recipientBlood");
    const types = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"];
    if (donorBlood) donorBlood.innerHTML = types.map(t => `<option value="${t}">${t}</option>`).join("");
    if (recipientBlood) recipientBlood.innerHTML = types.map(t => `<option value="${t}">${t}</option>`).join("");
}

// ------------------- Login Handling -------------------
function handleLogin(event) {
    event.preventDefault();
    const hospitalType = document.getElementById("hospitalType").value;
    const hospitalName = document.getElementById("hospitalName").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    if (!hospitalType || !hospitalName || !email || !password) {
        alert("Please fill in all fields!");
        return;
    }

    localStorage.setItem("loggedHospital", hospitalName);
    window.location.href = "dashboard.html";
}

// ------------------- Dashboard Auto-Load -------------------
window.onload = () => {
    const hospitalName = localStorage.getItem("loggedHospital") || "SmartCare+ Dashboard";
    const header = document.getElementById("hospitalDisplay");
    if (header) header.textContent = `🏥 ${hospitalName}`;

    populateHospitalDropdown();
    populateBloodTypeDropdown();

    if (document.getElementById("bloodTable")) {
        loadBloodTable();
        loadExpiryAlerts();
        loadStats();
        loadLeaderboard();
        loadDonationRequests();
    }
};

// ------------------- API Calls -------------------
async function loadBloodTable() {
    const res = await fetch("/api/blood_stock");
    const bloodData = await res.json();
    const tbody = document.querySelector("#bloodTable tbody");
    tbody.innerHTML = "";
    bloodData.forEach(b => {
        tbody.innerHTML += `<tr>
            <td>${b.blood_type}</td>
            <td>${b.units}</td>
            <td>${b.expiry_date}</td>
        </tr>`;
    });
}

async function loadExpiryAlerts() {
    const res = await fetch("/api/expiry_alerts?days=3");
    const alertsData = await res.json();
    const alerts = document.getElementById("expiryAlerts");
    alerts.innerHTML = "";
    const today = new Date();
    alertsData.forEach(b => {
        const exp = new Date(b.expiry_date);
        const diff = Math.ceil((exp - today) / (1000 * 60 * 60 * 24));
        alerts.innerHTML += `<li>${b.hospital_name} - ${b.blood_type} expiring in ${diff} days!</li>`;
    });
}

async function loadStats() {
    const res = await fetch("/api/blood_stock");
    const bloodData = await res.json();
    const total = bloodData.reduce((sum, b) => sum + b.units, 0);
    document.getElementById("liveStats").textContent = `Total Units Available: ${total}`;
}

async function loadLeaderboard() {
    const res = await fetch("/api/leaderboard");
    const leaders = await res.json();
    const list = document.getElementById("leaderboard");
    list.innerHTML = "";
    leaders.forEach(l => {
        list.innerHTML += `<li>${l.name} - ${l.donations} Donations</li>`;
    });
}

// ------------------- Add Blood Donation -------------------
document.addEventListener("submit", async (e) => {
    if (e.target.id === "bloodForm") {
        e.preventDefault();
        const hospital = document.getElementById("donorHospital").value;
        const blood_type = document.getElementById("donorBloodType").value;
        const units = document.getElementById("donorUnits").value;
        const expiry = document.getElementById("donorExpiry").value;

        const res = await fetch("/api/add_blood", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ hospital_name: hospital, blood_type, units, expiry_date: expiry })
        });
        const result = await res.json();
        alert(result.message);

        loadBloodTable();
        loadExpiryAlerts();
        loadStats();
        e.target.reset();
    }
});

// ------------------- Emergency Donation -------------------
async function postSampleRequest() {
    const hospital = localStorage.getItem("loggedHospital") || "Sample Hospital";
    const sampleRequests = [
        { blood_type: "O+", units_needed: 2, urgency_level: "High" },
        { blood_type: "A+", units_needed: 3, urgency_level: "Medium" },
        { blood_type: "B+", units_needed: 1, urgency_level: "Low" }
    ];

    for (let req of sampleRequests) {
        await fetch("/api/add_donation_request", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ hospital_name: hospital, ...req })
        });
    }
    loadDonationRequests();
}

// ------------------- Load Donation Requests -------------------
async function loadDonationRequests() {
    const res = await fetch("/api/requests");
    const requests = await res.json();
    const reqs = document.getElementById("donationRequests");
    if (!reqs) return;
    reqs.innerHTML = "";
    requests.forEach(r => {
        reqs.innerHTML += `<li>
            ${r.hospital_name} needs ${r.units_needed} units of ${r.blood_type} (${r.urgency_level})
            <button onclick="acceptRequest(${r.id})">Accept</button>
            <button onclick="declineRequest(${r.id})">Decline</button>
            <span>Status: ${r.status}</span>
        </li>`;
    });
}

// ------------------- Accept / Decline Request -------------------
async function acceptRequest(id) {
    await fetch("/api/update_request_status", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: id, status: "Accepted" })
    });
    loadDonationRequests();
    loadBloodTable();
    loadStats();
}

async function declineRequest(id) {
    await fetch("/api/update_request_status", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: id, status: "Declined" })
    });
    loadDonationRequests();
}

// ------------------- Organ Matching -------------------
document.addEventListener("submit", async (e) => {
    if (e.target.id === "organForm") {
        e.preventDefault();
        const hospital = localStorage.getItem("loggedHospital") || "Sample Hospital";
        const donor = document.getElementById("donorBlood").value;
        const recipient = document.getElementById("recipientBlood").value;
        const organType = document.getElementById("organType").value || "Kidney";

        const res = await fetch("/api/add_organ", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ hospital_name: hospital, organ_type: organType, donor_blood: donor, recipient_blood: recipient })
        });
        const result = await res.json();
        document.getElementById("matchResult").textContent = result.message;
        alert(result.message);
    }
});
