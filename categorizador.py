from sentence_transformers import SentenceTransformer, util
import re

modelo = SentenceTransformer('all-MiniLM-L6-v2')

# Dicionário de categorias com exemplos reais
categorias = {
    "Assinaturas": ["spotify", "netflix", "disney", "hbo", "globoplay", "prime video", "deezer", "apple tv", "streaming", "plano mensal"],
    "Cartão de Crédito": ["fatura do cartão", "paguei cartão", "parcela cartão", "nubank", "inter", "itaucard", "bradescard", "roxo"],
    "Casa": ["aluguel", "condomínio", "reforma", "prestação da casa", "conta de luz", "água", "internet", "telefone", "gás", "tv por assinatura", "net", "vivo", "claro"],
    "Cuidados Pessoais": ["barbeiro", "manicure", "pedicure", "cabeleireiro", "estética", "spa", "salão de beleza", "depilação"],
    "Doações / Presentes": ["presente de aniversário", "doação igreja", "ajuda alguém", "pix presente", "lembrancinha", "vaquinha", "solidariedade"],
    "Educação": ["mensalidade escola", "curso", "faculdade", "paguei cursinho", "plataforma de estudo", "ead", "curso online", "aula particular"],
    "Impostos": ["iptu", "ipva", "irpf", "multas", "darf", "contribuição", "dívida ativa", "tributo"],
    "Lazer e Entretenimento": ["cinema", "show", "bar", "festa", "passeio", "restaurante com amigos", "balada", "diversão"],
    "Mercado": ["supermercado", "pão de açúcar", "extra", "carrefour", "feira", "hortifruti", "mercado", "sacolão", "compras do mês"],
    "Outros": ["sem categoria", "não sei", "outro gasto", "diverso", "não classificado"],
    "Pets": ["ração", "veterinário", "banho e tosa", "petshop", "consulta pet", "remédio pet"],
    "Recebimentos": ["salário", "rendimento", "dinheiro recebido", "recebi pix", "transferência recebida", "freelancer", "depósito"],
    "Saúde": ["remédio", "farmácia", "consulta médica", "plano de saúde", "dentista", "cirurgia", "psicólogo", "hospital", "exame"],
    "Transporte": ["combustível", "uber", "99", "ônibus", "metrô", "transporte público", "pedágio", "manutenção carro", "gasolina"],
    "Vestuário": ["roupa", "calçado", "sapato", "bermuda", "camisa", "tênis", "blusa", "jaqueta", "vestido"],
    "Viagem": ["hotel", "passagem", "reserva airbnb", "viagem de férias", "turismo", "trip", "bagagem", "voo"],
    "Investimentos": ["tesouro direto", "ações", "fundos imobiliários", "bitcoin", "criptomoeda", "cdb", "renda fixa", "poupança", "renda variável"],
    "Emergências": ["gasto inesperado", "urgência", "socorro", "emergência médica", "pneu furado", "vazamento", "pane", "imprevisto"],
    "Serviços Domésticos": ["faxina", "diarista", "encanador", "eletricista", "manutenção", "chamei técnico", "dedetização", "montador"],
    "Serviços Digitais": ["canva", "cloud", "servidor", "plano pro", "editor de vídeo", "plano anual", "domínio", "gpt", "plano IA"],
    "Trabalho / Profissão": ["jaleco", "coworking", "material médico", "assinatura CRM", "instrumento de trabalho", "investi no trabalho", "equipamento profissional"],
    "Reembolsáveis": ["gasto reembolsável", "viagem a trabalho", "empresa vai pagar", "adiantamento", "ressarcimento"]
}

# Pré-processamento da mensagem (sem remover emojis!)
def limpar_mensagem(msg):
    msg = msg.lower()
    msg = re.sub(r'[^\w\s€$Rr]+', '', msg)  # remove pontuações e símbolos (mas mantém emojis)
    msg = msg.replace("padoca", "padaria")
    msg = msg.replace("reai", "reais").replace("real", "reais")
    msg = re.sub(r'\b(r?\$)?\s?\d+[.,]?\d*\b', 'valor', msg)
    return msg.strip()

# Pré-calcula os embeddings dos exemplos
vetores_categoria = {}
for cat, exemplos in categorias.items():
    vetores_categoria[cat] = [modelo.encode(e, convert_to_tensor=True) for e in exemplos]

# Função principal de classificação com fallback
def classificar_categoria(mensagem, limiar=0.55):
    texto = limpar_mensagem(mensagem)
    emb_msg = modelo.encode(texto, convert_to_tensor=True)

    melhor_categoria = None
    melhor_sim = 0

    for categoria, lista_emb in vetores_categoria.items():
        for vetor_ref in lista_emb:
            sim = float(util.pytorch_cos_sim(emb_msg, vetor_ref))
            if sim > melhor_sim:
                melhor_sim = sim
                melhor_categoria = categoria

    return melhor_categoria if melhor_sim >= limiar else "Outros"
