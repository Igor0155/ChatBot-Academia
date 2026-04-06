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
        # Memória de curto prazo do bot
        self.contexto = None 
        
        # Base de Conhecimento Inicial (Gatilhos)
        self.conhecimento = {
            "saudacao": {
                "keywords": ["ola", "olá", "oi", "bom dia", "boa tarde", "boa noite", "salve"],
                "resposta": "Olá! Sou seu assistente fitness. Para começarmos, você busca hipertrofia, emagrecimento ou apenas manter a saúde?"
            },
            "emagrecimento": {
                "keywords": ["emagrecer", "perder peso", "queimar gordura", "secar", "dieta", "emagrecimento"],
                "resposta": "Focar em déficit calórico e cardio é essencial. Você prefere fazer exercícios aeróbicos antes ou depois da musculação?",
                "proximo_passo": "esperando_cardio"
            },
            "hipertrofia": {
                "keywords": ["ganhar musculo", "hipertrofia", "ganhar", "musculo", "crescer", "ficar forte", "massa muscular"],
                "resposta": "Para ganhar massa, o descanso e a proteína são vitais. Você costuma dormir pelo menos 7 horas por noite?",
                "proximo_passo": "esperando_sono"
            },
            "motivacao": {
                "keywords": ["desanimado", "preguica", "desistindo", "cansado", "desanimando", "desânimo"],
                "resposta": "O resultado vem da disciplina, não da motivação. Que tal um treino mais curto hoje só para não perder o ritmo? Topa tentar?",
                "proximo_passo": "esperando_confirmacao_treino"
            },
            "suplemento": {
                "keywords": ["whey", "creatina", "pre-treino", "suplemento", "tomar"],
                "resposta": "Suplementos ajudam, mas a base é a dieta. Você já faz uso de creatina ou whey protein?",
                "proximo_passo": "esperando_detalhe_suplemento"
            },
            "dor_muscular": {
                "keywords": ["dor", "dolorido", "machucado", "lesao", "doendo"],
                "resposta": "Dor tardia é normal, mas dor articular é um sinal de alerta. Essa dor que você sente é no músculo ou na articulação?",
                "proximo_passo": "esperando_tipo_dor"
            },
            "alimentacao": {
                "keywords": ["comer", "comida", "proteina", "ovo", "frango", "carboidrato", "dieta"],
                "resposta": "A dieta é 70% do resultado. Você costuma preparar suas marmitas ou acaba comendo fora com frequência?",
                "proximo_passo": "esperando_marmita"
            },
            "manter_saude": {
                "keywords": ["manter", "saude", "saúde", "bem estar", "qualidade de vida", "viver bem"],
                "resposta": "Excelente objetivo! A longevidade vem do equilíbrio. Você já pratica alguma atividade física regularmente ou está começando agora?",
                "proximo_passo": "esperando_experiencia_saude"
            },
            "tchau": {
                "keywords": ["tchau", "sair", "encerrar", "obrigado", "valeu", "flw", "adeus"],
                "resposta": "Bom treino e foco na missão! Posso te ajudar com mais alguma dúvida antes de ir?"
            }
        }

    def processar_texto(self, texto):
        # Tokenização via NLTK (Não removemos stopwords para manter "sim", "não", "antes", "depois")
        tokens = word_tokenize(texto.lower())
        return [w for w in tokens if w not in string.punctuation]

    def gerar_resposta(self, mensagem_usuario):
        palavras = self.processar_texto(mensagem_usuario)
        
        # --- GERENCIADOR DE CONTEXTO (ÁRVORE DE DECISÃO) ---
        
        # Fluxo de Emagrecimento
        if self.contexto == "esperando_cardio":
            if any(w in palavras for w in ["depois", "pos", "pós"]):
                self.contexto = "esperando_tipo_cardio"
                return "Excelente! Deixar o cardio para o final preserva sua força para os pesos. Você prefere corrida ou escada?"
            self.contexto = "esperando_tipo_cardio"
            return "Entendido. Um cardio leve antes serve como aquecimento. Você prefere esteira ou bicicleta?"

        if self.contexto == "esperando_tipo_cardio":
            self.contexto = "esperando_frequencia"
            return "Boa escolha! E qual a frequência? Pretende fazer todo dia ou apenas 3 vezes na semana?"

        if self.contexto == "esperando_frequencia":
            self.contexto = None
            return "Consistência é a chave! Quer que eu te indique um alimento termogênico para ajudar na queima?"

        # Fluxo de Hipertrofia
        if self.contexto == "esperando_sono":
            if any(w in palavras for w in ["sim", "durmo", "7", "8", "tenho"]):
                self.contexto = "esperando_meta_proteica"
                return "Ótimo, o sono é onde ocorre a síntese proteica. E a dieta? Você consegue comer cerca de 2g de proteína por quilo de peso?"
            self.contexto = "esperando_meta_proteica"
            return "Tente dormir mais, o músculo cresce no descanso! Mas e a comida? Está batendo sua meta de proteínas?"

        if self.contexto == "esperando_meta_proteica":
            self.contexto = "foco_treino"
            return "Entendi. Proteína é essencial. Qual seu foco de treino hoje: Peito, Costas ou Pernas?"

        # Fluxo de Motivação
        if self.contexto == "esperando_confirmacao_treino":
            if any(w in palavras for w in ["sim", "quero", "topo", "bora", "vamos", "ok"]):
                self.contexto = "tipo_treino_curto"
                return "É assim que se fala! Vamos de um treino funcional de 15 minutos ou apenas um aeróbico intenso?"
            self.contexto = None
            return "Sem problemas. O descanso também é importante. Amanhã voltamos com tudo? Me avise se precisar de uma dica de alongamento!"

        if self.contexto == "esperando_tipo_dor":
            if "articulação" in palavras or "articulacao" in palavras or "osso" in palavras:
                self.contexto = None
                return "Cuidado! Dor na articulação pode ser lesão. Recomendo gelo e repouso. Já pensou em procurar um fisioterapeuta?"
            self.contexto = None
            return "Se for muscular, é apenas o ácido lático e a regeneração. Já tomou bastante água hoje para ajudar na recuperação?"

        # Fluxo manter a saude
        if self.contexto == "esperando_experiencia_saude":
            if any(w in palavras for w in ["começando", "começando", "inicio", "sedentário", "parado"]):
                self.contexto = "sugestao_leve"
                return "O importante é o primeiro passo! Que tal começar com 30 minutos de caminhada 3x na semana? Acha que consegue conciliar na sua rotina?"
            else:
                self.contexto = "sugestao_avancada"
                return "Que bom que já se movimenta! Para saúde geral, você foca mais em flexibilidade ou em força muscular?"

        if self.contexto == "sugestao_leve":
            if any(w in palavras for w in ["sim", "consigo", "claro", "topo"]):
                self.contexto = None
                return "Perfeito! Começar devagar evita lesões. Já tem um tênis confortável para essas caminhadas?"
            self.contexto = None
            return "Entendo. Se o tempo está curto, subir escadas em vez de usar o elevador já ajuda muito! Qual outra pequena mudança você poderia fazer hoje?"
        
        
        # --- BUSCA POR INTENÇÕES (PROCURA PALAVRAS-CHAVE SE NÃO HOUVER CONTEXTO) ---
        for intent, dados in self.conhecimento.items():
            if any(key in palavras for key in dados["keywords"]):
                self.contexto = dados.get("proximo_passo")
                return dados["resposta"]
        
        # Resposta padrão caso o bot se perca
        return "Interessante! Não entendi perfeitamente, mas me conte: como está sua rotina de treinos ultimamente?"