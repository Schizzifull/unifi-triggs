import os
import requests
from flask import Flask

app = Flask(__name__)

UNIFI_USER = os.environ.get("UNIFI_USER")
UNIFI_PASS = os.environ.get("UNIFI_PASS")
SITE_ID = "default"
BASE_URL = "https://138.59.49.160"  # Substitua pelo seu IP público real se for diferente

@app.route("/desativar_wifi")
def desativar_wifi():
    try:
        # 1. Autentica
        login_url = f"{BASE_URL}/api/login"
        session = requests.Session()
        response = session.post(login_url, json={"username": UNIFI_USER, "password": UNIFI_PASS}, verify=False)

        if response.status_code != 200 or "csrf_token" not in session.cookies.get_dict():
            return "Falha no login na UniFi Cloud."

        # 2. Desativa todas as redes Wi-Fi do site
        wlan_url = f"{BASE_URL}/proxy/network/api/s/{SITE_ID}/rest/wlanconf"
        redes = session.get(wlan_url, verify=False).json()['data']

        for rede in redes:
            rede['enabled'] = False
            session.put(f"{wlan_url}/{rede['_id']}", json=rede, verify=False)

        return "Redes Wi-Fi desativadas com sucesso!"

    except Exception as e:
        return f"Erro: {str(e)}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
