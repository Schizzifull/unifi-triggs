# UniFi Triggs API

Projeto em Flask para desativar uma rede Wi-Fi UniFi (via Cloud Controller) usando variáveis de ambiente.

## Como usar

1. Defina as variáveis de ambiente:
   - `UNIFI_USERNAME`
   - `UNIFI_PASSWORD`

2. Instale dependências:
```
pip install -r requirements.txt
```

3. Rode:
```
python main.py
```

4. Acesse em:
```
http://localhost:5000/desativar_wifi
```
