
from datetime import datetime
import pandas as pd
from supabase import create_client
import os

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_API_KEY = os.environ.get("SUPABASE_API_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_API_KEY)

def registrar_gasto(nome, numero, valor, descricao, categoria="Outros"):
    data = datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.now().isoformat()

    usuario = supabase.table("users").select("*").eq("telefone", numero).execute()

    if not usuario.data:
        return f"❌ Usuário {nome} ({numero}) não encontrado no banco."

    user_id = usuario.data[0]["id"]

    supabase.table("transactions").insert({
        "user_id": user_id,
        "valor": float(valor),
        "descricao": descricao,
        "categoria": categoria,
        "data": data,
        "timestamp": timestamp
    }).execute()

    mensagem = f"""✅ Transação registrada com sucesso, {nome}!

📝 *Descrição:* {descricao}
💰 *Valor:* R$ {float(valor):.2f}
📂 *Categoria:* {categoria}
📅 *Data:* {data}
📌 *Status:* Pago
"""
    return mensagem

def adicionar_membro_familia(nome, numero, titular):
    titular_res = supabase.table("users").select("*").eq("telefone", titular).execute()
    if not titular_res.data:
        return f"❌ Titular {titular} não encontrado."

    titular_id = titular_res.data[0]["family_id"]
    supabase.table("users").insert({
        "nome": nome,
        "telefone": numero,
        "family_id": titular_id
    }).execute()

    return f"👤 Membro {nome} ({numero}) adicionado com sucesso à família de {titular_res.data[0]['nome']}."
