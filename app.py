from flask import Flask, jsonify, request, render_template
import random
import time
import base64

app = Flask(__name__)

# Simuler des données IoT
devices = [
    {"id": 1, "name": "Living Room Thermostat", "type": "temperature", "value": 22},
    {"id": 2, "name": "Front Door Lock", "type": "lock", "value": "Locked"},
    {"id": 3, "name": "Kitchen Camera", "type": "camera", "value": "Active"},
    {"id": 4, "name": "Garage Door", "type": "door", "value": "Closed"}
]

# Flag caché (à modifier selon vos besoins)
hidden_flag = "CTF{H1DD3N_1N_10T_D4T4}"

# Logs simulés
logs = []

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

    # Générer un nouveau log
    logs.append(generate_log())
    if len(logs) > 100:  # Garder seulement les 100 derniers logs
        logs.pop(0)

    # Cacher le flag dans les données (exemple simple)
    if random.random() < 0.1:  # 10% de chance à chaque mise à jour
        encoded_char = base64.b64encode(hidden_flag[int(time.time()) % len(hidden_flag)].encode()).decode()
        devices[0]["value"] = f"22.{encoded_char}"

@app.route('/')
def home():
    return render_template('index.html')

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
    if 'id' in data and 'action' in data:
        # Simuler une vulnérabilité : si l'action contient 'FLAG', renvoyer le flag
        if 'FLAG' in data['action'].upper():
            return jsonify({"message": f"Debug mode: {hidden_flag}"})
        return jsonify({"message": f"Action {data['action']} performed on device {data['id']}"})
    return jsonify({"error": "Invalid request"}), 400

if __name__ == '__main__':
    app.run(debug=True)
