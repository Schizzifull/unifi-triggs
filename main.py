import requests
import os
from flask import Flask

app = Flask(__name__)

USERNAME = os.environ.get("UNIFI_USERNAME")
PASSWORD = os.environ.get("UNIFI_PASSWORD")
SSID_ALVO = "Visitas"  # Altere para o nome da sua rede

@app.route("/")
def index():
    return "UniFi Trigger API ativa."

@app.route("/desativar_wifi")
def desativar_wifi():
    session = requests.Session()

    login_resp = session.post(
        "https://unifi.ui.com/api/auth/login",
        json={"username": USERNAME, "password": PASSWORD}
    )
    if login_resp.status_code != 200:
        return f"Erro ao autenticar: {login_resp.text}", 401

    sites_resp = session.get("https://unifi.ui.com/api/self/sites")
    site_list = sites_resp.json().get("data", [])
    if not site_list:
        return "Nenhum site encontrado.", 404

    site_id = site_list[0]["site_id"]

    wlan_resp = session.get(f"https://unifi.ui.com/proxy/network/api/s/{site_id}/rest/wlanconf")
    wlans = wlan_resp.json()["data"]

    for wlan in wlans:
        if wlan["name"] == SSID_ALVO:
            wlan["enabled"] = False
            session.put(f"https://unifi.ui.com/proxy/network/api/s/{site_id}/rest/wlanconf/{wlan['_id']}", json=wlan)
            return f"Rede '{SSID_ALVO}' desativada com sucesso.", 200

    return "SSID não encontrado.", 404
    if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

