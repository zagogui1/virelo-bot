import openai
import os
from dotenv import load_dotenv

# Carrega a chave da OpenAI do arquivo .env
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Lista oficial de categorias usadas no VIRELO
CATEGORIAS = [
    "Assinaturas", "Cartão de Crédito", "Casa", "Cuidados Pessoais",
    "Doações / Presentes", "Educação", "Impostos", "Lazer e Entretenimento",
    "Mercado", "Outros", "Pets", "Recebimentos", "Saúde", "Transporte",
    "Vestuário", "Viagem", "Investimentos", "Emergências",
    "Serviços Domésticos", "Serviços Digitais", "Trabalho / Profissão"
]

# Prompt que guia o GPT para categorizar corretamente
PROMPT_BASE = f"""
Você é um assistente financeiro chamado VIRELO. Seu trabalho é classificar frases informais de gastos, receitas ou investimentos em uma das seguintes categorias:

{', '.join(CATEGORIAS)}

Responda apenas com o nome exato da categoria. Sem explicações. Se não entender, retorne apenas "Outros".

Exemplos:
- "gastei 20 reais no mercado" → Mercado
- "comprei gás por 130 reais" → Casa
- "recebi meu salário" → Recebimentos
- "comprei bitcoin" → Investimentos

Agora classifique a seguinte frase:
"""

# Função principal de categorização
def classificar_categoria(mensagem):
    try:
        resposta = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {"role": "system", "content": PROMPT_BASE + mensagem}
            ],
            temperature=0.0
        )
        categoria = resposta.choices[0].message.content.strip()
        return categoria
    except Exception as e:
        print(f"[ERRO GPT] {e}")
        return "Outros"
