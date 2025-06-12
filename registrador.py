import pandas as pd
import os
import json
from datetime import datetime

def atualizar_clientes_json(numero, nome):
    caminho = "clientes/clientes.json"
    os.makedirs("clientes", exist_ok=True)

    if os.path.exists(caminho):
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                dados = json.load(f)
        except json.JSONDecodeError:
            dados = {}
    else:
        dados = {}

    dados.pop("", None)
    dados[numero] = f"{nome} ({numero})"

    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

def identificar_membro(numero_remetente):
    base = "clientes"
    if not os.path.exists(base):
        return None, None

    for titular in os.listdir(base):
        caminho_membros = os.path.join(base, titular, "membros.json")
        if os.path.exists(caminho_membros):
            with open(caminho_membros, "r", encoding="utf-8") as f:
                membros = json.load(f)
                if numero_remetente in membros:
                    return titular, membros[numero_remetente]["nome"]

    return None, None

def registrar_gasto(numero, nome, valor, categoria="Outros"):
    try:
        atualizar_clientes_json(numero, nome)

        # Verifica se é membro de uma família
        titular, nome_membro = identificar_membro(numero)

        if titular and nome_membro:
            pasta = f"clientes/{titular}/{nome_membro}"
            os.makedirs(pasta, exist_ok=True)
            nome_arquivo = datetime.now().strftime("%Y-%m") + ".json"
            caminho_individual = os.path.join(pasta, nome_arquivo)
            caminho_consolidado = os.path.join(f"clientes/{titular}", f"consolidado_{nome_arquivo}")
            nome_exibicao = f"{nome_membro} (familiar)"
        else:
            pasta = f"planilhas/{nome} ({numero})"
            os.makedirs(pasta, exist_ok=True)
            nome_arquivo = datetime.now().strftime("%Y-%m") + ".json"
            caminho_individual = os.path.join(pasta, nome_arquivo)
            caminho_consolidado = None
            nome_exibicao = nome

        novo_dado = {
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "valor": float(valor),
            "categoria": categoria
        }

        # Salva dado individual
        if os.path.exists(caminho_individual):
            df = pd.read_json(caminho_individual)
        else:
            df = pd.DataFrame(columns=["data", "valor", "categoria"])

        df = pd.concat([df, pd.DataFrame([novo_dado])], ignore_index=True)
        df.to_json(caminho_individual, orient="records", indent=2)

        # Se for familiar, atualiza consolidado do titular
        if caminho_consolidado:
            if os.path.exists(caminho_consolidado):
                df_c = pd.read_json(caminho_consolidado)
            else:
                df_c = pd.DataFrame(columns=["data", "valor", "categoria", "membro"])
            novo_dado["membro"] = nome_membro
            df_c = pd.concat([df_c, pd.DataFrame([novo_dado])], ignore_index=True)
            df_c.to_json(caminho_consolidado, orient="records", indent=2)

        return f"✅ Gasto de R$ {valor} registrado com sucesso para {nome_exibicao}!"
    except Exception as e:
        return f"❌ Erro ao registrar o gasto: {str(e)}"

def adicionar_membro_familia(numero_titular, nome_membro, numero_membro):
    try:
        pasta_titular = f"clientes/{numero_titular}"
        caminho_arquivo = os.path.join(pasta_titular, "membros.json")

        os.makedirs(pasta_titular, exist_ok=True)

        if os.path.exists(caminho_arquivo):
            with open(caminho_arquivo, "r", encoding="utf-8") as f:
                membros = json.load(f)
        else:
            membros = {}

        membros[numero_membro] = {
            "nome": nome_membro,
            "titular": numero_titular
        }

        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            json.dump(membros, f, indent=2, ensure_ascii=False)

        return f"👤 Membro \"{nome_membro}\" ({numero_membro}) adicionado com sucesso à família!"
    except Exception as e:
        return f"❌ Erro ao adicionar membro: {str(e)}"
