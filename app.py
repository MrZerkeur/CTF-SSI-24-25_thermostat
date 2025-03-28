from flask import Flask, jsonify, request, render_template, redirect, session
import random
import time
import uuid
import sqlite3


app = Flask(__name__)
app.secret_key = '9f92b0f075dbbb40c9ed401a52236191b1cba733893d410bdbf43631c2eff139'

# Simuler des données IoT
devices = [
    {"id": 1, "name": "Living Room Thermostat", "type": "temperature", "value": 22},
    {"id": 2, "name": "Front Door Lock", "type": "lock", "value": "Locked"},
    {"id": 3, "name": "Kitchen Camera", "type": "camera", "value": "Active"},
    {"id": 4, "name": "Garage Door", "type": "door", "value": "Closed"}
]


hidden_flag = "RETRO{3XPLOIT_D@T@BAS3}"

# Logs simulés
logs = []

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uuid TEXT UNIQUE,
            username TEXT UNIQUE
        )
    ''')
    conn.commit()

    admin_uuid = str(uuid.uuid4())
    shortened_admin_uuid = admin_uuid.split('-', 1)[0]
    cursor.execute(
        "INSERT OR IGNORE INTO users (uuid, username) VALUES (?, ?)",
        (shortened_admin_uuid, 'administrator')
    )

    charlie_uuid = str(uuid.uuid4())
    shortened_charlie_uuid = charlie_uuid.split('-', 1)[0]
    cursor.execute(
        "INSERT OR IGNORE INTO users (uuid, username) VALUES (?, ?)",
        (shortened_charlie_uuid, 'Charlie')
    )

    conn.commit()
    conn.close()

def generate_log():
    actions = ["Door opened", "Door closed", "Temperature changed", "Motion detected"]
    return f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {random.choice(actions)}"

def update_device_data():
    for device in devices:
        if device["type"] == "temperature":
            device["value"] = round(random.uniform(18, 26), 1)
        elif device["type"] == "lock":
            device["value"] = random.choice(["Locked", "Unlocked"])
        elif device["type"] == "camera":
            device["value"] = random.choice(["Active", "Standby"])
        elif device["type"] == "door":
            device["value"] = random.choice(["Open", "Closed"])

    logs.append(generate_log())
    if len(logs) > 100:
        logs.pop(0)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/robots.txt')
def robots():
    return "User-agent: *\nDisallow: /very-annoying-path-for-admin-login\n", 200, {'Content-Type': 'text/plain'}

@app.route('/api/devices')
def get_devices():
    update_device_data()
    return jsonify(devices)

@app.route('/api/logs')
def get_logs():
    return jsonify(logs)

@app.route('/api/control', methods=['POST'])
def control_device():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT uuid FROM users WHERE username = ?", ('Charlie',))
    result = cursor.fetchone()
    conn.close()
    charlie_uuid = result[0]
    data = request.json
    if data['uuid'] == charlie_uuid and data['mode'] == "debug":
        return jsonify({"message": f"Debug mode: {hidden_flag}"})
    return jsonify({"error": "Invalid request",
                    'message': 'Awaited format : {"uuid": "*something*", "mode": "*mode here*"}'}), 400

@app.route('/very-annoying-path-for-admin-login', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        cursor.execute(query)
        user = cursor.fetchone()
        conn.close()
        
        if user:
            session['admin'] = True
            return redirect('/very-annoying-path-for-admin-panel')
        else:
            return render_template('admin-login.html', error='Invalid credentials')
    
    return render_template('admin-login.html')

@app.route('/very-annoying-path-for-admin-panel')
def admin_panel():
    if not session.get('admin'):
        return redirect('/very-annoying-path-for-admin-login')
    return render_template('admin-panel.html')

init_db()
