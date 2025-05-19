import os
import requests
from flask import Flask

app = Flask(__name__)

UNIFI_USER = os.environ.get("schizzi2010@gmail.com")
UNIFI_PASS = os.environ.get("daianschizzi665876")
SITE_ID = "default"
BASE_URL = "https://unifi.ui.com"

@app.route("/desativar_wifi")
def desativar_wifi():
    try:
        # Login na nuvem UniFi
        session = requests.Session()
        login = session.post(f"{BASE_URL}/api/auth/login", json={
            "username": UNIFI_USER,
            "password": UNIFI_PASS
        })

        if login.status_code != 200:
            return "Falha no login na UniFi Cloud.", 401

        # Pega a lista de redes Wi-Fi
        wlans = session.get(f"{BASE_URL}/proxy/network/api/s/{SITE_ID}/rest/wlanconf").json()["data"]
        visitas = next((w for w in wlans if w["name"] == "Visitas"), None)

        if not visitas:
            return "Rede 'Visitas' não encontrada.", 404

        # Desativar a rede "Visitas"
        visitas_id = visitas["_id"]
        visitas["enabled"] = False

        update = session.put(
            f"{BASE_URL}/proxy/network/api/s/{SITE_ID}/rest/wlanconf/{visitas_id}",
            json=visitas
        )

        if update.status_code == 200:
            return "Rede 'Visitas' desativada com sucesso!"
        else:
            return f"Erro ao desativar: {update.status_code}", 500

    except Exception as e:
        return f"Erro inesperado: {str(e)}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
