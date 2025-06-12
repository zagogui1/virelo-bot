
from datetime import datetime
import pandas as pd
from supabase import create_client
import json

with open("config.json") as f:
    config = json.load(f)

supabase = create_client(config["SUPABASE_URL"], config["SUPABASE_API_KEY"])

def registrar_gasto(nome, numero, valor, descricao, categoria="Outros"):
    data = datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.now().isoformat()

    # 1. Procurar o usuário no Supabase
    usuario = supabase.table("users").select("*").eq("telefone", numero).execute()

    if not usuario.data:
        return f"❌ Usuário {nome} ({numero}) não encontrado no banco."

    user_id = usuario.data[0]["id"]

    # 2. Gravar transação
    supabase.table("transactions").insert({
        "user_id": user_id,
        "valor": float(valor),
        "descricao": descricao,
        "categoria": categoria,
        "data": data,
        "timestamp": timestamp
    }).execute()

    # 3. Mensagem formatada de retorno
    mensagem = f"""✅ Transação registrada com sucesso, {nome}!

📝 *Descrição:* {descricao}
💰 *Valor:* R$ {float(valor):.2f}
📂 *Categoria:* {categoria}
📅 *Data:* {data}
📌 *Status:* Pago
"""
    return mensagem

def adicionar_membro_familia(nome, numero, titular):
    # Procura o titular pelo número
    titular_res = supabase.table("users").select("*").eq("telefone", titular).execute()
    if not titular_res.data:
        return f"❌ Titular {titular} não encontrado."

    titular_id = titular_res.data[0]["family_id"]
    # Cria um novo usuário vinculado à mesma família
    supabase.table("users").insert({
        "nome": nome,
        "telefone": numero,
        "family_id": titular_id
    }).execute()

    return f"👤 Membro {nome} ({numero}) adicionado com sucesso à família de {titular_res.data[0]['nome']}."
