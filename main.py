
from flask import Flask

app = Flask(__name__)

@app.route("/desativar_wifi")
def desativar_wifi():
    return "Wi-Fi desativado com sucesso!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
