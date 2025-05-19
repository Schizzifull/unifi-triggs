
from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

@app.route('/desativar_wifi', methods=['GET'])
def desativar_wifi():
    username = os.getenv('UNIFI_USERNAME')
    password = os.getenv('UNIFI_PASSWORD')

    if not username or not password:
        return jsonify({"error": "UNIFI_USERNAME ou UNIFI_PASSWORD não configurados"}), 500

    login_url = "https://unifi.ui.com/api/auth/login"
    payload = {
        "username": username,
        "password": password
    }

    session = requests.Session()
    login_response = session.post(login_url, json=payload)

    if login_response.status_code != 200:
        return jsonify({"error": "Falha no login UniFi", "status": login_response.status_code}), 500

    csrf_token = session.cookies.get("TOKEN")
    headers = {
        "x-csrf-token": csrf_token,
        "Content-Type": "application/json"
    }

    # Substitua esses valores pelos reais
    site_id = "default"
    network_id = "INSIRA_AQUI_O_ID_DA_REDE"
    disable_url = f"https://unifi.ui.com/api/s/default/rest/wlanconf/{network_id}"

    response = session.put(disable_url, headers=headers, json={"enabled": False})

    if response.status_code == 200:
        return jsonify({"status": "Rede Wi-Fi desativada com sucesso"})
    else:
        return jsonify({"error": "Falha ao desativar Wi-Fi", "details": response.text}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
