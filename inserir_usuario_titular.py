from supabase import create_client
import uuid
from datetime import datetime

SUPABASE_URL = "https://qfjtjzhriylebvhdoxzo.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFmanRqemhyaXlsZWJ2aGRveHpvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDk3NDY0NTEsImV4cCI6MjA2NTMyMjQ1MX0.8j0VPZciTXYn68sF2MNj73iIP5mIcIArMOK6BdyXzQ8"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 🔢 EDITAR AQUI SEU NOME E NÚMERO:
nome_titular = "Zago"
numero_telefone = "5511942885750"

# 1. Criar uma família
nova_familia = {
    "id": str(uuid.uuid4()),
    "nome": f"Família de {nome_titular}",
    "plano_id": "basico",
    "criado_em": datetime.now().isoformat()
}
res_familia = supabase.table("families").insert(nova_familia).execute()
print("✅ Família criada:", res_familia.data)

# 2. Criar o usuário admin vinculado à família
novo_usuario = {
    "id": str(uuid.uuid4()),
    "nome": nome_titular,
    "email": numero_telefone,
    "senha_hash": "",
    "family_id": nova_familia["id"],
    "role": "admin",
    "criado_em": datetime.now().isoformat()
}
res_usuario = supabase.table("users").insert(novo_usuario).execute()
print("✅ Usuário criado:", res_usuario.data)
