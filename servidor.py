from flask import Flask, request
import requests
from registrador import registrar_gasto, adicionar_membro_familia
import json
import re

app = Flask(__name__)

# Carrega configurações do config.json
with open("config.json", encoding="utf-8") as f:
    config = json.load(f)

WATI_URL = config["wati"]["url"]
TOKEN = config["wati"]["token"]

@app.route("/webhook", methods=["POST"])
def webhook():
    payload = request.json
    print("🔍 Payload recebido da WATI:")
    print(payload)

    mensagem = payload.get("text", "")
    numero = payload.get("waId", "")
    nome = payload.get("senderName", "Desconhecido")

    print(f"📨 Mensagem recebida de {nome} ({numero}): {mensagem}")

    # Verifica se é comando de cadastro de membro
    if mensagem.startswith("/familia adicionar"):
        partes = mensagem.split()
        if len(partes) >= 4:
            nome_membro = " ".join(partes[2:-1])
            numero_membro = partes[-1]
            resposta = adicionar_membro_familia(numero, nome_membro, numero_membro)
        else:
            resposta = "❌ Formato inválido. Use: /familia adicionar Nome 5511XXXXXXXX"
    else:
        # Detecta valor na mensagem (registro de gasto)
        match = re.search(r"(\d+[.,]?\d*)", mensagem)
        if match:
            valor = match.group(1).replace(",", ".")
            resposta = registrar_gasto(numero, nome, valor, mensagem)
            if not resposta or not resposta.strip():
                resposta = "✅ Gasto registrado com sucesso."
        else:
            resposta = "❌ Nenhum gasto detectado na mensagem."

    print(f"🧾 Resposta a ser enviada: {resposta}")

    payload_envio = {
        "messageText": resposta
    }

    print(f"📤 Form data enviado: {payload_envio}")

    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }

    try:
        response = requests.post(
            f"{WATI_URL}/api/v1/sendSessionMessage/{numero}",
            headers=headers,
            data=payload_envio
        )
        print(f"📤 Resposta enviada. Status: {response.status_code}")
        print(f"📨 Conteúdo da resposta: {response.text}")
    except Exception as e:
        print(f"❌ Erro ao enviar resposta: {e}")

    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)