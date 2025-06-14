from sentence_transformers import SentenceTransformer, util

modelo = SentenceTransformer('all-MiniLM-L6-v2')

categorias = {
    "Assinaturas": [
        "spotify", "netflix", "disney", "hbo", "globoplay", "prime video", "deezer", "apple tv", "streaming", "plano mensal"
    ],
    "Cartão de Crédito": [
        "fatura do cartão", "paguei cartão", "parcela cartão", "nubank", "inter", "itaucard", "bradescard", "roxo"
    ],
    "Casa": [
        "aluguel", "condomínio", "reforma", "prestação da casa", "conta de luz", "água", "internet", "telefone", "gás", "tv por assinatura", "net", "vivo", "claro"
    ],
    "Cuidados Pessoais": [
        "barbeiro", "manicure", "pedicure", "cabeleireiro", "estética", "spa", "salão de beleza", "depilação"
    ],
    "Doações / Presentes": [
        "presente de aniversário", "doação igreja", "ajuda alguém", "pix presente", "lembrancinha", "vaquinha", "solidariedade"
    ],
    "Educação": [
        "mensalidade escola", "curso", "faculdade", "paguei cursinho", "plataforma de estudo", "ead", "curso online", "aula particular"
    ],
    "Impostos": [
        "iptu", "ipva", "irpf", "multas", "darf", "contribuição", "dívida ativa", "tributo"
    ],
    "Lazer e Entretenimento": [
        "cinema", "show", "bar", "festa", "passeio", "restaurante com amigos", "balada", "diversão"
    ],
    "Mercado": [
        "supermercado", "pão de açúcar", "extra", "carrefour", "feira", "hortifruti", "mercado", "sacolão", "compras do mês"
    ],
    "Outros": [
        "sem categoria", "não sei", "outro gasto", "diverso", "não classificado"
    ],
    "Pets": [
        "ração", "veterinário", "banho e tosa", "petshop", "consulta pet", "remédio pet"
    ],
    "Recebimentos": [
        "salário", "rendimento", "dinheiro recebido", "recebi pix", "transferência recebida", "freelancer", "depósito"
    ],
    "Saúde": [
        "remédio", "farmácia", "consulta médica", "plano de saúde", "dentista", "cirurgia", "psicólogo", "hospital", "exame"
    ],
    "Transporte": [
        "combustível", "uber", "99", "ônibus", "metrô", "transporte público", "pedágio", "manutenção carro", "gasolina"
    ],
    "Vestuário": [
        "roupa", "calçado", "sapato", "bermuda", "camisa", "tênis", "blusa", "jaqueta", "vestido"
    ],
    "Viagem": [
        "hotel", "passagem", "reserva airbnb", "viagem de férias", "turismo", "trip", "bagagem", "voo"
    ],
    "Investimentos": [
        "tesouro direto", "ações", "fundos imobiliários", "bitcoin", "criptomoeda", "cdb", "renda fixa", "poupança", "renda variável"
    ],
    "Emergências": [
        "gasto inesperado", "urgência", "socorro", "emergência médica", "pneu furado", "vazamento", "pane", "imprevisto"
    ],
    "Serviços Domésticos": [
        "faxina", "diarista", "encanador", "eletricista", "manutenção", "chamei técnico", "dedetização", "montador"
    ],
    "Serviços Digitais": [
        "canva", "cloud", "servidor", "plano pro", "editor de vídeo", "plano anual", "domínio", "gpt", "plano IA"
    ],
    "Trabalho / Profissão": [
        "jaleco", "coworking", "material médico", "assinatura CRM", "instrumento de trabalho", "investi no trabalho", "equipamento profissional"
    ],
    "Reembolsáveis": [
        "gasto reembolsável", "viagem a trabalho", "empresa vai pagar", "adiantamento", "ressarcimento"
    ]
}

def classificar_categoria(mensagem):
    mensagem = mensagem.lower()
    mensagem_embedding = modelo.encode(mensagem, convert_to_tensor=True)

    melhor_categoria = None
    melhor_similaridade = 0.55  # limiar mínimo

    for categoria, exemplos in categorias.items():
        for exemplo in exemplos:
            exemplo_embedding = modelo.encode(exemplo, convert_to_tensor=True)
            similaridade = float(util.pytorch_cos_sim(mensagem_embedding, exemplo_embedding))
            if similaridade > melhor_similaridade:
                melhor_similaridade = similaridade
                melhor_categoria = categoria

    return melhor_categoria if melhor_categoria else "Outros"
