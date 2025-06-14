
# categorizador.py

from sentence_transformers import SentenceTransformer, util

# Carrega o modelo leve e eficiente para IA semântica
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Mapeamento semântico expandido com 24 categorias
CATEGORIAS_SEMANTICAS = {
    "Assinaturas": "spotify, netflix, globoplay, serviços recorrentes, streaming, assinaturas digitais",
    "Cartão de Crédito": "fatura do cartão, pagamento de cartão de crédito, parcela de cartão",
    "Casa": "aluguel, condomínio, prestação da casa, reforma, manutenção do lar, móveis",
    "Cuidados Pessoais": "barbearia, salão de beleza, manicure, estética, cuidados pessoais, cosméticos",
    "Doações / Presentes": "presente de aniversário, doações, ajuda financeira, lembrança, mimo",
    "Educação": "mensalidade escolar, faculdade, cursinho, material didático, educação, curso online",
    "Impostos": "iptu, ipva, imposto de renda, taxas governamentais, tributos",
    "Lazer": "cinema, parque, festas, sair com amigos, entretenimento, eventos, diversão",
    "Mercado": "compras no mercado, supermercado, feira, alimentos, produtos de limpeza",
    "Outros": "gastos não identificados, categoria desconhecida, sem correspondência clara",
    "Pets": "ração, veterinário, petshop, banho e tosa, cuidados com animais de estimação",
    "Recebimentos": "salário, pix recebido, transferência recebida, entrada de dinheiro",
    "Saúde": "remédios, farmácia, médico, dentista, plano de saúde, exames, consulta",
    "Transporte": "uber, ônibus, combustível, gasolina, táxi, transporte público",
    "Utilidades": "luz, água, energia, telefone, gás, internet, contas fixas",
    "Vestuário": "roupas, sapatos, moda, vestuário, compras em loja de roupa",
    "Viagem": "passagem, hotel, hospedagem, viagem, passeio turístico, férias",
    "Investimentos": "compra de ações, tesouro direto, fundos, investimentos financeiros",
    "Emergências": "socorro, despesa inesperada, reparo urgente, emergência médica ou doméstica",
    "Serviços domésticos": "faxina, diarista, eletricista, encanador, manutenção doméstica",
    "Serviços digitais": "domínio, hospedagem, serviços online, canva, google drive, digital",
    "Trabalho / Profissão": "coworking, uniforme, ferramentas de trabalho, despesa profissional",
    "Reembolsáveis": "gastos para empresa, será reembolsado, viagem a trabalho, adiantamento corporativo"
}

def detectar_categoria_ia(texto):
    """
    Detecta a categoria mais provável de um gasto com IA semântica.
    Usa comparação de similaridade de significado com 24 categorias.
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

        if melhor_score < 0.45:
            return "Outros"
        return melhor_categoria

    except Exception as e:
        print(f"[ERRO IA] {e}")
        return "Outros"
