# categorizador.py

from sentence_transformers import SentenceTransformer, util

# Carrega o modelo de IA leve
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Descrições ampliadas para IA sem fallback
CATEGORIAS_SEMANTICAS = {
    "Mercado": "compras em supermercado, feira, alimentos para casa, pão, arroz, leite, produtos de limpeza, mercado local",
    "Transporte": "uber, gasolina, ônibus, transporte público, corridas por aplicativo, táxi, combustível, deslocamento",
    "Alimentação": "restaurante, lanche, janta, almoço, comida fora de casa, fast food, delivery, hamburguer, marmita",
    "Lazer": "cinema, parque, balada, diversão, passeio, viagem, sair com amigos, festas, entretenimento",
    "Saúde": "remédio, farmácia, exame médico, consulta, tratamento de saúde, medicamento, plano de saúde, clínica",
}

def detectar_categoria_ia(texto):
    """
    Detecta a categoria mais provável de um gasto com IA semântica.
    Usa comparação de similaridade de significado.
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

        # Se a similaridade for baixa, considera como "Outros"
        if melhor_score < 0.45:
            return "Outros"
        return melhor_categoria

    except Exception as e:
        print(f"[ERRO IA] {e}")
        return "Outros"
