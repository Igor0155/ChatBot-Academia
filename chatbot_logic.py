import nltk
from nltk.tokenize import word_tokenize
import string

# Downloads necessários
nltk.download('punkt')
nltk.download('punkt_tab')

class AcademiaBot:
    def __init__(self):
        self.contexto = None 
        
        # =========================================================
        # BASE DE CONHECIMENTO COMPLETA (TODOS COM GANCHOS)
        # =========================================================
        self.conhecimento = {
            "saudacao": {
                "keywords": ["ola", "olá", "oi", "bom dia", "boa tarde", "boa noite", "salve"],
                "resposta": "Olá! Sou seu assistente fitness virtual. Para eu personalizar nosso papo, qual é o seu objetivo principal hoje: hipertrofia (ganho de massa), emagrecimento definitivo ou melhorar sua saúde e longevidade?",
                "proximo_passo": None
            },
            "emagrecimento": {
                "keywords": ["emagrecer", "perder", "peso", "gordura", "secar", "dieta", "emagrecimento"],
                "resposta": "Para emagrecer de verdade, o segredo é a 'Densidade Calórica' (comer muito volume com pouca caloria). O que mais te sabota na dieta: a fome constante ao longo do dia, ou a vontade de comer doces/besteiras à noite?",
                "proximo_passo": "esperando_sabotador_dieta"
            },
            "hipertrofia": {
                "keywords": ["ganhar", "musculo", "hipertrofia", "crescer", "forte", "massa", "volume"],
                "resposta": "A hipertrofia exige três pilares: Treino com progressão de carga, ingestão de proteínas e sono profundo. Qual desses três fatores você sente que é o seu maior gargalo hoje?",
                "proximo_passo": "esperando_pilar_hipertrofia"
            },
            "manter_saude": {
                "keywords": ["manter", "saude", "saúde", "bem estar", "qualidade", "vida", "longevidade", "condicionamento"],
                "resposta": "Excelente! A longevidade se baseia em articulações fortes e saúde cardiovascular. O maior inimigo da saúde moderna é o sedentarismo. Você passa muito tempo sentado durante o dia (trabalho/estudos) ou tem uma rotina mais ativa?",
                "proximo_passo": "esperando_rotina_saude"
            },
            "motivacao": {
                "keywords": ["desanimado", "preguica", "cansado", "desistindo", "desânimo", "motivação"],
                "resposta": "A motivação é passageira, a disciplina fica. Um truque neurocientífico é a 'Regra dos 5 Minutos': prometa a si mesmo ir treinar por apenas 5 minutos. Isso quebra a barreira da dopamina. Topa tentar hoje?",
                "proximo_passo": "esperando_regra_5min"
            },
            "abdominal": {
                "keywords": ["abdomen", "abdômen", "barriga", "tanquinho", "abdominal", "core"],
                "resposta": "Para ver os 'gominhos', você precisa de hipertrofia do músculo e percentual de gordura baixo. Você costuma treinar abdômen com pesos (polia/máquina) ou só com o peso do corpo no colchonete?",
                "proximo_passo": "esperando_tipo_abdominal"
            },
            "perna": {
                "keywords": ["perna", "pernas", "biomecanica", "biomecânica", "coxa", "gluteo", "agachamento", "inferiores", "legpress"],
                "resposta": "Treino de pernas libera testosterona natural por envolver grandes grupos musculares. Seu foco atual é mais em quadríceps (parte da frente) ou na cadeia posterior (glúteos e posterior de coxa)?",
                "proximo_passo": "esperando_foco_perna"
            },
            "jejum_horario": {
                "keywords": ["jejum", "fome", "horario", "horário", "vazio", "cedo", "acordar"],
                "resposta": "Treinar em jejum melhora a sensibilidade à insulina, mas pode faltar energia para força máxima. Você sente tontura, fraqueza ou enjoo quando treina de barriga vazia?",
                "proximo_passo": "esperando_sintoma_jejum"
            },
            "dor_lesao": {
                "keywords": ["dor", "lesao", "machucado", "doendo", "ombro", "joelho", "lombar"],
                "resposta": "Sinal de alerta! Dor muscular tardia é boa, dor articular é perigosa. Essa dor que você sente é no 'meio' do músculo ou bem na articulação/junta (onde os ossos se encontram)?",
                "proximo_passo": "esperando_tipo_dor"
            },
            "tchau": {
                "keywords": ["tchau", "sair", "encerrar", "obrigado", "valeu", "flw", "adeus"],
                "resposta": "Foi um prazer ajudar! O resultado que você quer está na rotina que você ignora. Bom treino e até a próxima! Se mudar de ideia, é só mandar um 'Oi' de novo!",
                "proximo_passo": None
            }
        }

    def processar_texto(self, texto):
        tokens = word_tokenize(texto.lower())
        return [w for w in tokens if w not in string.punctuation]

    def tem_palavra(self, palavras_usuario, lista_alvos):
        return any(w in palavras_usuario for w in lista_alvos)

    def gerar_resposta(self, mensagem_usuario):
        palavras = self.processar_texto(mensagem_usuario)
        
        # =========================================================
        # ÁRVORE DE DIÁLOGO (TODOS OS NÓS COM GANCHOS!)
        # =========================================================

        # ---------------- 3. FLUXO: SAÚDE E BEM-ESTAR ----------------
        if self.contexto == "esperando_rotina_saude":
            if self.tem_palavra(palavras, ["sentado", "cadeira", "escritorio", "computador", "trabalho", "estudo"]):
                self.contexto = "esperando_dores_saude"
                return "Cuidado com a 'Síndrome da Cadeira'! Ficar sentado encurta o músculo Iliopsoas e 'desliga' os glúteos, causando dores na lombar. Você já sente dores nas costas ou rigidez no pescoço?"
            else:
                self.contexto = "esperando_cardio_saude"
                return "Que excelente! O corpo humano foi feito para o movimento. Para quem já é ativo, o próximo passo é melhorar o VO2 Máx (capacidade do coração e pulmões). Você faz treinos aeróbicos focados em suar bastante na semana?"

        if self.contexto == "esperando_dores_saude":
            if self.tem_palavra(palavras, ["sim", "sinto", "muito", "doem", "costas", "lombar"]):
                self.contexto = None
                return "Isso é um pedido de socorro do seu corpo. A recomendação médica é: a cada 1 hora sentado, levante por 5 minutos. Exercícios de fortalecimento do Core são urgentes. Quer que eu te indique um exercício bom para lombar ou prefere falar sobre dieta?"
            else:
                self.contexto = None
                return "Que sorte! Mas não espere a dor chegar. Adicionar 10 minutos de alongamento ao acordar vai manter suas articulações jovens. Pensando em rotina, você tem alguma dúvida específica sobre hipertrofia ou emagrecimento?"

        if self.contexto == "esperando_cardio_saude":
            self.contexto = None
            return "Perfeito! A recomendação da OMS é de 150 a 300 minutos de atividade aeróbica moderada por semana para blindar o coração. Mantendo essa saúde em dia, qual é o seu próximo desafio fitness: ganhar mais força ou definir a musculatura?"

        # ---------------- 1. FLUXO: EMAGRECIMENTO -----------------
        if self.contexto == "esperando_sabotador_dieta":
            if self.tem_palavra(palavras, ["fome", "toda", "hora", "beliscar", "estômago"]):
                self.contexto = "esperando_cardio_emagrecimento"
                return "Use o 'Efeito Térmico dos Alimentos'. Proteínas e fibras demoram horas para serem digeridas, mantendo seu estômago cheio e gastando calorias. Coma sempre uma bacia de salada *antes* do prato principal. E sobre o treino: prefere fazer cardio antes ou depois da musculação?"
            elif self.tem_palavra(palavras, ["doce", "açúcar", "noite", "ansiedade", "besteira", "chocolate"]):
                self.contexto = "esperando_cardio_emagrecimento"
                return "A estratégia ideal é o 'Encaixe Flexível'. Reserve 10% das suas calorias para um docinho. O segredo é comer sempre *logo após* a refeição, para as fibras impedirem o pico de insulina! Falando em gastar essas calorias extras, você foca mais na musculação ou no aeróbico?"
            else:
                self.contexto = "esperando_cardio_emagrecimento"
                return "Foque em comida de verdade (descascar mais, desembalar menos). Aliado à dieta, o exercício acelera a queima. Pensando nisso, você costuma fazer seu cardio antes ou depois da musculação?"

        if self.contexto == "esperando_cardio_emagrecimento":
            self.contexto = None
            return "Lembre-se: emagrecimento é uma maratona, não um sprint. Beba muita água e foque em dormir bem, pois é à noite que a queima de gordura ocorre com mais força. Falando em sono, você costuma ter dificuldades para dormir ou apaga rápido?"

        # ---------------- 2. FLUXO: HIPERTROFIA -------------------
        if self.contexto == "esperando_pilar_hipertrofia":
            if self.tem_palavra(palavras, ["treino", "falha", "força", "peso", "carga"]):
                self.contexto = "esperando_sobrecarga"
                return "A chave é a 'Sobrecarga Progressiva'. Se você pegar 10kg no supino hoje e daqui a 6 meses continuar pegando 10kg, seu músculo não cresce. Você tem o costume de anotar suas cargas para tentar bater seu próprio recorde?"
            elif self.tem_palavra(palavras, ["proteina", "comida", "dieta", "alimentação"]):
                self.contexto = "esperando_suplemento"
                return "Sem tijolos, o pedreiro não faz a parede! Consuma cerca de 1.6g a 2g de proteína por quilo de peso corporal. Você já usa algum suplemento como Whey ou Creatina para ajudar nessa meta?"
            elif self.tem_palavra(palavras, ["sono", "dormir", "descanso", "noite"]):
                self.contexto = None
                return "Treinar apenas 'machuca' o músculo; ele cresce na cama. Tente expor seus olhos ao sol logo que acordar e evite luz azul de celular 1h antes de dormir. Fora o sono, qual grupo muscular você tem mais dificuldade de desenvolver?"

        if self.contexto == "esperando_sobrecarga":
            self.contexto = None
            return "Anotar o treino é o divisor de águas! Além disso, focar na descida do peso (fase excêntrica) causa mais microlesões hipertróficas. Qual exercício você considera o mais difícil na sua rotina hoje?"

        if self.contexto == "esperando_suplemento":
            self.contexto = None
            return "O Whey é praticidade, mas a Creatina é obrigatória para força, pois recarrega o ATP intramuscular. Vale o investimento! Qual outra dúvida sobre treinos ou dietas eu posso esclarecer para você?"

        # ---------------- 5. FLUXO: ABDOMINAL ----------------
        if self.contexto == "esperando_tipo_abdominal":
            if self.tem_palavra(palavras, ["peso", "pesos", "maquina", "polia", "carga"]):
                self.contexto = None
                return "Excelente! O reto abdominal precisa de sobrecarga para criar 'gomos' profundos. Continue progredindo carga. Lembre-se: abdômen se define na cozinha. Como está seu foco na dieta ultimamente?"
            else:
                self.contexto = None
                return "Peso do corpo melhora resistência, mas não hipertrofia tanto. Tente abraçar uma anilha de 5kg ou 10kg no próximo treino! Vai arder, mas o resultado vem. Quer uma dica de outro exercício para adicionar na rotina?"

        # ---------------- 6. FLUXO: PERNAS -------------------------
        if self.contexto == "esperando_foco_perna":
            if self.tem_palavra(palavras, ["frente", "quadriceps", "coxa"]):
                self.contexto = None
                return "Para quadríceps, Agachamento Búlgaro e Cadeira Extensora são incríveis. Uma dica de biomecânica: ao fazer o agachamento, quanto mais o joelho for para frente, mais recruta a coxa! Você costuma sentir dor no joelho quando treina perna?"
            else:
                self.contexto = None
                return "Para glúteos e posterior, Stiff e Elevação Pélvica reinam. No Stiff, empurre o quadril o máximo para trás, como se fosse fechar uma porta com o bumbum. Você vai sentir repuxar muito mais! Tem facilidade em sentir o glúteo trabalhando ou acaba sentindo mais a lombar?"

        # ---------------- 7. FLUXO: JEJUM --------------------------
        if self.contexto == "esperando_sintoma_jejum":
            if self.tem_palavra(palavras, ["sim", "tontura", "fraqueza", "passo", "mal"]):
                self.contexto = None
                return "Isso é hipoglicemia de esforço. Não force! Coma um carboidrato simples (uma banana com mel) 30 minutos antes. Isso vai te dar o 'pump' de energia sem pesar no estômago. Qual é a sua refeição pré-treino favorita no momento?"
            else:
                self.contexto = None
                return "Se você rende bem, ótimo! O corpo induz a quebra de gordura mais rápido. Apenas garanta que vai bater suas metas de proteínas na hora que quebrar o jejum. Você sabe calcular a quantidade de proteína que precisa no dia?"

        # ---------------- 8. FLUXO: DOR E LESÃO --------------------
        if self.contexto == "esperando_tipo_dor":
            if self.tem_palavra(palavras, ["articulação", "articulacao", "osso", "junta"]):
                self.contexto = None
                return "PARE O EXERCÍCIO! Dor articular significa que a carga está indo para o tendão/ligamento. Reduza o peso ou busque um fisioterapeuta. Já pensou em focar em alongamento e mobilidade para proteger essa articulação?"
            else:
                self.contexto = None
                return "Se for dor no meio do músculo no dia seguinte, é a famosa DOMS (Dor Muscular Tardia). Muito alongamento leve e água aceleram a recuperação. Qual grupo muscular está te incomodando mais hoje?"

        # ---------------- 4. FLUXO: MOTIVAÇÃO ---------------------
        if self.contexto == "esperando_regra_5min":
            if self.tem_palavra(palavras, ["sim", "topo", "vamos", "ok", "bora"]):
                self.contexto = None
                return "Essa é a atitude de quem tem resultados! Vá treinar. Se após 5 minutos quiser voltar, volte. Mas a endorfina sempre te faz ficar. E quando você voltar, quer que eu te ajude a pensar em uma boa refeição pós-treino?"
            else:
                self.contexto = None
                return "Compreensível, o descanso mental também importa. Não deixe que um dia ruim vire uma semana parada. Volte com tudo amanhã! Quer aproveitar o dia off para falarmos sobre estratégias de dieta?"

        # =========================================================
        # BUSCA INICIAL DE INTENÇÕES (FALLBACK PARA NOVO ASSUNTO)
        # =========================================================
        for intent, dados in self.conhecimento.items():
            if self.tem_palavra(palavras, dados["keywords"]):
                self.contexto = dados.get("proximo_passo")
                return dados["resposta"]
        
        # Resposta padrão inteligente
        return "Minha base de dados não pegou essa palavra exata! Mas adoro explicar sobre a ciência da hipertrofia, biomecânica de pernas, dores, estratégias de emagrecimento e longevidade. Sobre qual desses temas você quer que a gente converse agora?"