from flask import Flask, jsonify, request, render_template, redirect, session
import random
import time
import base64
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

# Flag caché (à modifier selon vos besoins)
hidden_flag = "RETRO{H1DD3N_1N_10T_D4T4}"

# Logs simulés
logs = []

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT)''')
    conn.commit()
    cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('admin', 'password123')")  # Weak creds
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
    data = request.json
    if data['uuid'] == "a14118b0-7e79-462f-a365-10848d32624a" and data['mode'] == "debug":
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

if __name__ == '__main__':
    app.run(debug=True)
