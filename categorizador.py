# categorizador.py

from sentence_transformers import SentenceTransformer, util

# Carrega o modelo de IA leve (apenas na primeira vez faz download)
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Dicionário de descrições semânticas por categoria
CATEGORIAS_SEMANTICAS = {
    "Mercado": "supermercado, compras de comida, feira, pão de açúcar",
    "Transporte": "gastos com uber, gasolina, ônibus, aplicativo de transporte",
    "Lazer": "cinema, parque, festas, viagem, entretenimento",
    "Alimentação": "restaurante, lanche, almoço, jantar, pizzaria",
    "Saúde": "farmácia, remédio, consulta médica, exame",
}

# Palavras-chave alternativas para fallback
PALAVRAS_CHAVE = {
    "Mercado": ["mercado", "supermercado", "compras", "feira"],
    "Transporte": ["uber", "gasolina", "ônibus", "transporte", "99"],
    "Alimentação": ["pizza", "lanche", "restaurante", "almoço", "jantar"],
    "Saúde": ["farmácia", "remédio", "consulta", "exame"],
    "Lazer": ["cinema", "parque", "viagem", "bar", "balada"],
}


def detectar_categoria_ia(texto):
    """
    Detecta a categoria mais provável de um gasto com IA semântica.
    Se houver erro ou baixa confiança, usa o fallback por palavras-chave.
    """
    try:
        texto_embedding = model.encode(texto, convert_to_tensor=True)
        melhor_score = -1
        melhor_categoria = "Outros"

        for categoria, descricao in CATEGORIAS_SEMANTICAS.items():
            descricao_embedding = model.encode(descricao, convert_to_tensor=True)
            score = util.cos_sim(texto_embedding, descricao_embedding).item()
            if score > melhor_score:
                melhor_score = score
                melhor_categoria = categoria

        # Se o score for muito baixo, considerar como "Outros"
        if melhor_score < 0.45:
            return detectar_categoria_palavras(texto)  # Fallback
        return melhor_categoria

    except Exception as e:
        print(f"[ERRO IA] {e}")
        return detectar_categoria_palavras(texto)


def detectar_categoria_palavras(texto):
    """
    Fallback simples com palavras-chave caso a IA falhe.
    """
    texto = texto.lower()
    for categoria, palavras in PALAVRAS_CHAVE.items():
        if any(p in texto for p in palavras):
            return categoria
    return "Outros"
