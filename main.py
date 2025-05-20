from flask import Flask, jsonify
import requests
import urllib3

# Desativa warnings de SSL (caso use IP público sem certificado válido)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

# 🔧 CONFIGURAÇÕES - ALTERE AQUI
UDM_IP = "https://138.59.49.160"  # Ex: https://138.59.xxx.xxx
USERNAME = "schizzifull"           # Usuário da UDM
PASSWORD = "daianschizzi665876"             # Senha da UDM
SSID_ID = "Visitas"         # ID da rede Wi-Fi a ser desativada

@app.route("/desativar_wifi", methods=["GET"])
def desativar_wifi():
    session = requests.Session()
    login_payload = {
        "username": USERNAME,
        "password": PASSWORD
    }

    try:
        # 🔐 Login na UDM
        login_resp = session.post(f"{UDM_IP}/api/auth/login", json=login_payload, verify=False)
        login_resp.raise_for_status()

        # 🔌 Desativar rede Wi-Fi
        disable_payload = { "enabled": False }
        disable_resp = session.put(
            f"{UDM_IP}/proxy/network/api/s/default/rest/wlanconf/{SSID_ID}",
            json=disable_payload,
            verify=False
        )
        disable_resp.raise_for_status()

        return jsonify({"status": "✅ Rede Wi-Fi desativada com sucesso"})

    except requests.exceptions.HTTPError as http_err:
        return jsonify({"erro": "Erro HTTP", "detalhes": str(http_err)}), 500
    except Exception as err:
        return jsonify({"erro": "Erro geral", "detalhes": str(err)}), 500

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "API UDM no ar", "endpoint": "/desativar_wifi"})

# 🚀 Railway inicia por aqui
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
