from datetime import datetime
from supabase import create_client
import json

# Carrega config
with open("config.json", encoding="utf-8") as f:
    config = json.load(f)

supabase = create_client(config["SUPABASE_URL"], config["SUPABASE_API_KEY"])

def registrar_gasto(numero, nome, valor, descricao, categoria="Outros"):
    data = datetime.now().strftime("%d/%m/%Y")
    timestamp = datetime.now().isoformat()

    # Busca o usuário
    usuario = supabase.table("users").select("*").eq("telefone", numero).execute()
    if not usuario.data:
        return f"❌ Usuário {nome} ({numero}) não encontrado no banco."

    user_id = usuario.data[0]["id"]

    # Salva transação
    supabase.table("transactions").insert({
        "user_id": user_id,
        "valor": float(valor),
        "descricao": descricao,
        "categoria": categoria,
        "data": data,
        "timestamp": timestamp
    }).execute()

    # Mensagem personalizada
    mensagem = f"""
💸 *Gasto registrado com sucesso, {nome}*!

📌 *Categoria:* {categoria}
📝 *Descrição:* {descricao}
💰 *Valor:* R$ {float(valor):,.2f}
📅 *Data:* {data}
🔐 *Status:* Confirmado

⚙️ Esses dados já estão organizados na sua planilha do mês!
"""
    return mensagem.strip()

def adicionar_membro_familia(titular, nome, numero):
    # Busca o titular
    titular_res = supabase.table("users").select("*").eq("telefone", titular).execute()
    if not titular_res.data:
        return f"❌ Titular {titular} não encontrado."

    titular_id = titular_res.data[0]["family_id"]

    # Adiciona novo membro
    supabase.table("users").insert({
        "nome": nome,
        "telefone": numero,
        "family_id": titular_id
    }).execute()

    return f"👨‍👩‍👧 Membro *{nome}* ({numero}) adicionado à família de *{titular_res.data[0]['nome']}* com sucesso!"
