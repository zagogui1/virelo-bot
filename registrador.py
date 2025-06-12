from datetime import datetime
from supabase import create_client
import os

# Lê as variáveis de ambiente definidas no Render
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_API_KEY = os.environ.get("SUPABASE_API_KEY")

# Cria o cliente Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_API_KEY)

def registrar_gasto(numero, nome, valor, descricao, categoria="Outros"):
    data = datetime.now().strftime("%d/%m/%Y")
    timestamp = datetime.now().isoformat()

    # Busca o usuário pelo telefone
    usuario = supabase.table("users").select("*").eq("telefone", numero).execute()
    if not usuario.data:
        return f"❌ Usuário {nome} ({numero}) não encontrado no banco."

    user_id = usuario.data[0]["id"]

    # Salva a transação
    supabase.table("transactions").insert({
        "user_id": user_id,
        "valor": float(valor),
        "descricao": descricao,
        "categoria": categoria,
        "data": data,
        "timestamp": timestamp
    }).execute()

    # Retorna a mensagem
    return f"""
💸 *Gasto registrado com sucesso, {nome}!*

📌 *Categoria:* {categoria}
📝 *Descrição:* {descricao}
💰 *Valor:* R$ {float(valor):,.2f}
📅 *Data:* {data}
🔐 *Status:* Confirmado

⚙️ Esses dados já estão organizados na sua planilha do mês!
""".strip()

def adicionar_membro_familia(titular, nome, numero):
    titular_res = supabase.table("users").select("*").eq("telefone", titular).execute()
    if not titular_res.data:
        return f"❌ Titular {titular} não encontrado."

    titular_id = titular_res.data[0]["family_id"]

    supabase.table("users").insert({
        "nome": nome,
        "telefone": numero,
        "family_id": titular_id
    }).execute()

    return f"👨‍👩‍👧 Membro *{nome}* ({numero}) adicionado à família de *{titular_res.data[0]['nome']}* com sucesso!"
