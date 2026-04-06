import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string

# pacotes necessários do NLTK
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

class AcademiaBot:
    def __init__(self):

        # Armazena o que o bot perguntou por último
        self.contexto = None

         # Intent -> (Keywords, Response)
        self.conhecimento = {
            "saudacao": {
                "keywords": ["ola", "olá", "oi", "bom dia", "boa tarde", "boa noite", "salve",  "tudo bem" , "tudo bem?"],
                "resposta": "Olá! Sou seu assistente fitness. Para começarmos, você busca hipertrofia, emagrecimento ou apenas manter a saúde?"
            },
            "emagrecimento": {
                "keywords": ["emagrecer", "perder peso", "queimar gordura", "secar", "dieta", "emagrecimento"],
                "resposta": "Focar em déficit calórico e cardio é essencial. Você prefere fazer exercícios aeróbicos antes ou depois da musculação?",
                "proximo_passo": "esperando_cardio"
            },
            "cardio_sequencia": {
                "keywords": ["antes", "depois", "durante"],
                "resposta": "Boa escolha! Fazer cardio depois preserva seu estoque de glicogênio para o treino de força. Você já faz algum tipo de hiit ou prefere caminhada na esteira?",
                "proximo_passo": "esperando_tipo_cardio"
            },
            "hipertrofia": {
                "keywords": ["ganhar musculo", "hipertrofia", "ganhar", "musculo", "crescer", "ficar forte", "massa muscular"],
                "resposta": "Para ganhar massa, o descanso é tão importante quanto o treino. Você costuma dormir pelo menos 7 horas por noite?",
                "proximo_passo": "esperando_proteina"
            },
            "treino_peito": {
                "keywords": ["peito", "supino", "peitoral"],
                "resposta": "O supino reto é o rei, mas o inclinado ajuda na estética superior. Qual desses você sente mais dificuldade em executar?"
            },
            "suplemento": {
                "keywords": ["whey", "creatina", "pre-treino", "suplemento"],
                "resposta": "Creatina é o suplemento com mais base científica para força. Você já faz uso de algum suplemento ou prefere focar 100% na dieta?"
            },
            "dor_muscular": {
                "keywords": ["dor", "dolorido", "machucado", "lesao"],
                "resposta": "Dor tardia é normal, mas dor articular é um sinal de alerta. Essa dor que você sente é no músculo ou na articulação?"
            },
            "perna": {
                "keywords": ["perna", "agachamento", "legpress", "quadriceps"],
                "resposta": "Treino de pernas eleva muito a testosterona natural. Você prefere agachamento livre ou máquinas como o Leg Press?"
            },
            "costas": {
                "keywords": ["costas", "dorsal", "puxada", "remada"],
                "resposta": "Para costas largas, as puxadas são essenciais. Você já consegue fazer barra fixa ou prefere usar o Pulley?"
            },
            "braco": {
                "keywords": ["braço", "biceps", "triceps", "muque"],
                "resposta": "O tríceps corresponde a 2/3 do volume do braço! Sabia disso? Quer uma dica de exercício para tríceps ou para bíceps?"
            },
            "cardio": {
                "keywords": ["cardio", "esteira", "correr", "bicicleta", "caminhada"],
                "resposta": "O cardio melhora muito seu fôlego na musculação. Você prefere alta intensidade (HIIT) ou uma caminhada constante?"
            },
            "alimentacao": {
                "keywords": ["comer", "comida", "proteina", "ovo", "frango", "carboidrato"],
                "resposta": "A dieta é 70% do resultado. Você costuma preparar suas marmitas ou acaba comendo fora com frequência?"
            },
            "motivacao": {
                "keywords": ["desanimado", "preguica", "desistindo", "cansado"],
                "resposta": "O resultado vem da disciplina, não da motivação. Que tal um treino mais curto hoje só para não perder o ritmo?"
            },
            "abdominal": {
                "keywords": ["abdômen", "barriga", "abdominal", "prancha"],
                "resposta": "Abdominal fortalece o core, mas a definição vem da dieta. Você treina abdômen todo dia ou dia sim, dia não?"
            },
            "alongamento": {
                "keywords": ["alongar", "alongamento", "flexibilidade", "travar"],
                "resposta": "Alongar melhora a amplitude do movimento e evita lesões. Você faz alongamento antes ou depois de treinar?"
            },
            "ombro": {
                "keywords": ["ombro", "deltoide", "desenvolvimento"],
                "resposta": "Ombros fortes dão o aspecto de 'V' no corpo. Você foca mais em elevação lateral ou desenvolvimento com halteres?"
            },
            "creatina": {
                "keywords": ["creatina", "tomar", "dosagem"],
                "resposta": "A creatina deve ser tomada todos os dias, até nos dias de descanso. Você já sabe qual a dose ideal para o seu peso?"
            },
            "jejum": {
                "keywords": ["jejum", "fome", "sem comer"],
                "resposta": "Treinar em jejum funciona para alguns, mas pode causar tontura em outros. Você já tentou treinar sem comer?"
            },
            "horario": {
                "keywords": ["manhã", "noite", "tarde", "melhor horario"],
                "resposta": "O melhor horário é aquele em que você consegue ser constante. Você se sente com mais energia ao acordar ou no fim do dia?"
            },
            "tenis": {
                "keywords": ["tênis", "sapato", "calçado"],
                "resposta": "Para treinos de perna, o ideal é um tênis de solado reto. O seu tênis atual é de corrida ou de solado reto?"
            },
            "tchau": {
                "keywords": ["tchau", "sair", "encerrar", "obrigado", "valeu"],
                "resposta": "Bom treino e foco na missão! Posso te ajudar com mais alguma dúvida sobre exercícios ou nutrição antes de ir?"
            }
            
        }

    def processar_texto(self, texto):
        # NLTK: Tokenização e Limpeza
        tokens = word_tokenize(texto.lower())
        # stop_words = set(stopwords.words('portuguese'))
        return [w for w in tokens if w not in string.punctuation]

    def gerar_resposta(self, mensagem_usuario):
        palavras = self.processar_texto(mensagem_usuario)
        
        # Prioridade total ao contexto atual
        if self.contexto == "esperando_cardio":
            if "depois" in palavras or "pos" in palavras:
                self.contexto = "esperando_tipo_cardio"
                return "Excelente! Deixar o cardio para o final garante que você tenha energia máxima para os pesos. Você gosta de correr ou prefere a escada?"
            elif "antes" in palavras or "pre" in palavras:
                self.contexto = "esperando_tipo_cardio"
                return "Entendi! Um cardio leve antes serve como aquecimento. Mas cuidado para não cansar o músculo principal. Você prefere esteira ou bicicleta?"

        if self.contexto == "esperando_proteina":
            # Verificamos palavras positivas ou negativas
            if any(w in palavras for w in ["sim", "bato", "faço", "faco", "durmo", "sim"]):
                self.contexto = None # Reseta o contexto após concluir o fluxo
                return "Perfeito! A constância no descanso e na dieta é o segredo. Você toma whey protein ou consegue bater a meta só com comida sólida?"
            elif any(w in palavras for w in ["não", "nao", "pouco", "dificuldade"]):
                self.contexto = None
                return "Muitos têm essa dificuldade! O sono regula hormônios como a grelina. Já pensou em ajustar sua rotina para dormir 30min a mais?"

        # --- LÓGICA DE PALAVRAS-CHAVE (Se não houver contexto ou se o usuário mudar de assunto) ---
        for intent, dados in self.conhecimento.items():
            if any(key in palavras for key in dados["keywords"]):
                self.contexto = dados.get("proximo_passo") # Salva o novo contexto
                return dados["resposta"]
        
        # Fallback
        return "Interessante! Não tenho certeza se entendi, mas adoraria saber mais. Você poderia detalhar como é sua rotina atual de exercícios?"