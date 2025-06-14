from sentence_transformers import SentenceTransformer, util
import re

modelo = SentenceTransformer('all-MiniLM-L6-v2')

# Dicionário otimizado com frases padronizadas
categorias = {
    "Assinaturas": [
        "paguei 20 reais no spotify",
        "gastei 30 reais com netflix",
        "paguei 50 reais em streaming",
        "comprei plano mensal da disney",
        "assinei globoplay por 40 reais"
    ],
    "Cartão de Crédito": [
        "paguei 500 da fatura do cartão",
        "quitei o cartão do nubank com 700 reais",
        "paguei 300 reais no itaucard",
        "gastei 250 reais no cartão roxo",
        "comprei roupas no cartão por 600 reais"
    ],
    "Casa": [
        "paguei 1000 reais de aluguel",
        "gastei 250 reais com conta de luz",
        "comprei gás por 130 reais",
        "paguei 300 de condomínio",
        "paguei a internet por 120 reais"
    ],
    "Cuidados Pessoais": [
        "gastei 80 reais no cabeleireiro",
        "paguei 50 na manicure",
        "comprei pacote de spa por 200 reais",
        "fiz depilação por 60 reais"
    ],
    "Doações / Presentes": [
        "doei 100 reais para igreja",
        "dei presente de aniversário de 150 reais",
        "gastei 50 reais em lembrancinha",
        "enviei pix de 200 reais como presente"
    ],
    "Educação": [
        "paguei 1000 reais de mensalidade da faculdade",
        "comprei curso online por 300 reais",
        "assinei plataforma de estudo por 120 reais",
        "gastei 250 reais em aula particular"
    ],
    "Impostos": [
        "paguei 200 de iptu",
        "gastei 600 com imposto de renda",
        "paguei 500 de ipva",
        "quitei 100 reais de multa"
    ],
    "Lazer e Entretenimento": [
        "gastei 100 reais no bar",
        "comprei ingresso de cinema por 50 reais",
        "paguei 200 em festa",
        "fui ao show e gastei 300 reais"
    ],
    "Mercado": [
        "gastei 250 reais no supermercado",
        "comprei 100 reais em feira",
        "fiz compras do mês por 500 reais",
        "comprei comida por 200 reais"
    ],
    "Outros": [
        "não sei a categoria desse gasto",
        "outro tipo de despesa de 100 reais",
        "gasto indefinido de 80 reais",
        "sem classificação"
    ],
    "Pets": [
        "paguei 90 reais em ração",
        "gastei 150 no veterinário",
        "comprei brinquedos pet por 60 reais",
        "banho e tosa por 100 reais"
    ],
    "Recebimentos": [
        "recebi 2000 reais de salário",
        "ganhei 500 reais em transferência",
        "rendimento de 300 reais",
        "recebi 1500 de freelance"
    ],
    "Saúde": [
        "comprei remédio por 80 reais",
        "paguei 200 de consulta médica",
        "gastei 300 no hospital",
        "paguei plano de saúde de 400 reais"
    ],
    "Transporte": [
        "paguei 100 reais em uber",
        "gastei 70 reais com gasolina",
        "comprei bilhete de metrô por 50 reais",
        "paguei manutenção do carro por 300 reais"
    ],
    "Vestuário": [
        "comprei roupa por 150 reais",
        "gastei 200 reais em sapato",
        "paguei 300 reais em tênis",
        "comprei vestido por 180 reais"
    ],
    "Viagem": [
        "comprei passagem por 800 reais",
        "paguei hotel por 1000 reais",
        "reserva de airbnb por 900 reais",
        "gastei 500 em turismo"
    ],
    "Investimentos": [
        "comprei ações por 1000 reais",
        "apliquei 1500 no tesouro direto",
        "investi 2000 reais em cdb",
        "coloquei 500 em bitcoin"
    ],
    "Emergências": [
        "gastei 300 com emergência médica",
        "paguei 200 reais por socorro",
        "gasto inesperado de 400 reais",
        "consertei pane elétrica por 350 reais"
    ],
    "Serviços Domésticos": [
        "paguei 150 reais para diarista",
        "chamei encanador e paguei 200 reais",
        "gastei 180 com dedetização",
        "conserto doméstico por 300 reais"
    ],
    "Serviços Digitais": [
        "assinei plano pro do canva por 90 reais",
        "paguei 120 em servidor cloud",
        "comprei domínio por 60 reais",
        "plano IA por 100 reais"
    ],
    "Trabalho / Profissão": [
        "comprei jaleco por 100 reais",
        "investi 500 reais no consultório",
        "paguei assinatura CRM de 200 reais",
        "gastei 800 com equipamento de trabalho"
    ]
}

# Função de limpeza da frase (preserva emojis)
def limpar_mensagem(msg):
    msg = msg.lower()
    msg = re.sub(r'[^\w\s€$Rr]+', '', msg)  # mantém emojis
    msg = msg.replace("padoca", "padaria")
    msg = msg.replace("reai", "reais").replace("real", "reais")
    msg = re.sub(r'\b(r?\$)?\s?\d+[.,]?\d*\b', 'valor', msg)
    return msg.strip()

# Pré-calcula embeddings das frases de exemplo
vetores_categoria = {
    cat: [modelo.encode(f, convert_to_tensor=True) for f in frases]
    for cat, frases in categorias.items()
}

# Classificador principal com fallback
def classificar_categoria(mensagem, limiar=0.55):
    texto = limpar_mensagem(mensagem)
    emb_msg = modelo.encode(texto, convert_to_tensor=True)

    melhor_categoria = None
    melhor_sim = 0

    for categoria, vetores in vetores_categoria.items():
        for vetor_ref in vetores:
            sim = float(util.pytorch_cos_sim(emb_msg, vetor_ref))
            if sim > melhor_sim:
                melhor_sim = sim
                melhor_categoria = categoria

    return melhor_categoria if melhor_sim >= limiar else "Outros"
