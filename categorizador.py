from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

# Frases de exemplo realistas para cada categoria
categoria_frases = {
    "Investimentos": [
        "investi 100 reais em ações", "apliquei no tesouro direto", "comprei cripto", "fiz um investimento hoje"
    ],
    "Serviços Digitais": [
        "paguei netflix", "assinei disney+", "hbo max", "spotify", "canva premium", "paguei domínio do site"
    ],
    "Serviços Domésticos": [
        "chamei o encanador", "paguei a faxineira", "manutenção da casa", "serviço de conserto", "paguei o jardineiro"
    ],
    "Reembolsáveis": [
        "empresa vai me reembolsar", "adiantamento para viagem de trabalho", "vou receber esse valor de volta"
    ],
    "Trabalho / Profissão": [
        "paguei coworking", "gastei com jaleco", "ferramentas de trabalho", "comprei material para o serviço"
    ],
    "Emergências": [
        "gasto inesperado", "socorro com pneu", "emergência médica", "urgência no hospital"
    ],
    "Assinaturas": [
        "assinei um serviço", "plano mensal", "assinatura premium", "paguei o pacote mensal"
    ],
    "Cartão de Crédito": [
        "paguei a fatura", "cartão de crédito do banco", "pagamento do cartão"
    ],
    "Casa": [
        "gastei com aluguel", "paguei condomínio", "conserto da geladeira", "reforma da casa"
    ],
    "Cuidados Pessoais": [
        "fui ao salão", "paguei manicure", "comprei cremes", "cortei o cabelo"
    ],
    "Doações / Presentes": [
        "dei um presente", "doei dinheiro", "contribuição para alguém"
    ],
    "Educação": [
        "paguei a escola", "mensalidade da faculdade", "curso online", "comprei livros"
    ],
    "Impostos": [
        "iptu", "ipva", "paguei imposto", "darf", "receita federal"
    ],
    "Lazer e Entretenimento": [
        "fui ao cinema", "paguei ingresso", "comprei jogo", "diversão com amigos"
    ],
    "Mercado": [
        "comprei no mercado", "gastei no pão de açúcar", "fui ao supermercado", "comida da semana"
    ],
    "Outros": [
        "não sei onde encaixar", "gasto diverso"
    ],
    "Pets": [
        "paguei ração", "vacina do cachorro", "pet shop", "consulta veterinária"
    ],
    "Recebimentos": [
        "recebi meu salário", "dinheiro entrou na conta", "renda extra"
    ],
    "Saúde": [
        "paguei consulta médica", "remédio", "fui ao hospital", "plano de saúde"
    ],
    "Transporte": [
        "uber", "ônibus", "gasolina", "estacionamento", "corrida de app"
    ],
    "Utilidades": [
        "conta de luz", "internet", "água", "telefone fixo"
    ],
    "Vestuário": [
        "comprei roupa", "paguei sapato", "nova camiseta", "vestido novo"
    ],
    "Viagem": [
        "hotel", "passagem aérea", "fiz uma viagem", "reserva no booking"
    ]
}

# Vetores prontos
categoria_vetores = {
    categoria: [model.encode(frase) for frase in frases]
    for categoria, frases in categoria_frases.items()
}

def classificar_categoria(mensagem, limiar_similaridade=0.45):
    frase_vetor = model.encode(mensagem)
    melhor_categoria = "Outros"
    maior_similaridade = 0

    for categoria, vetores in categoria_vetores.items():
        for vetor in vetores:
            similaridade = util.cos_sim(frase_vetor, vetor).item()
            if similaridade > maior_similaridade:
                maior_similaridade = similaridade
                melhor_categoria = categoria

    if maior_similaridade >= limiar_similaridade:
        return melhor_categoria
    else:
        return "Outros"
