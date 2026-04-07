import nltk
from nltk.tokenize import word_tokenize
import string

# Downloads necessários
nltk.download('punkt')
nltk.download('punkt_tab')

class AcademiaBot:
    def __init__(self):
        self.contexto = None 
        
        # BASE DE CONHECIMENTO (GATILHOS INICIAIS)
        self.conhecimento = {
            "saudacao": {
                "keywords": ["ola", "olá", "oi", "bom dia", "boa tarde", "boa noite", "salve"],
                "resposta": "Olá! Sou seu assistente fitness virtual. Para eu personalizar nosso papo, qual é o seu objetivo principal hoje: hipertrofia (ganho de massa), emagrecimento ou melhorar sua saúde geral?",
                "proximo_passo": None
            },
            "emagrecimento": {
                "keywords": ["emagrecer", "perder", "peso", "gordura", "secar", "dieta", "emagrecimento"],
                "resposta": "Para emagrecer de forma saudável, o segredo não é parar de comer, mas sim manter um 'Déficit Calórico'. Você já tem o hábito de calcular suas calorias diárias ou come de forma mais intuitiva?",
                "proximo_passo": "esperando_dieta_emagrecimento"
            },
            "hipertrofia": {
                "keywords": ["ganhar", "musculo", "hipertrofia", "crescer", "forte", "massa", "volume"],
                "resposta": "A hipertrofia exige três pilares: Treino até a falha, ingestão adequada de proteínas e sono profundo. Qual desses três fatores você sente que é o seu ponto mais fraco hoje?",
                "proximo_passo": "esperando_pilar_hipertrofia"
            },
            "manter_saude": {
                "keywords": ["manter", "saude", "saúde", "bem estar", "qualidade", "vida", "longevidade"],
                "resposta": "Excelente! A longevidade se baseia em articulações fortes e saúde cardiovascular. Você passa muito tempo sentado durante o dia ou tem uma rotina mais ativa?",
                "proximo_passo": "esperando_rotina_saude"
            },
            "motivacao": {
                "keywords": ["desanimado", "preguica", "cansado", "desistindo", "desânimo", "motivação"],
                "resposta": "A motivação é passageira, o que traz resultado é a disciplina. Topa tentar a 'Regra dos 5 Minutos'? Prometa a si mesmo ir treinar por apenas 5 minutos hoje. Aceita o desafio?",
                "proximo_passo": "esperando_regra_5min"
            },
            # --- NOVOS TEMAS ESPECÍFICOS ADICIONADOS AQUI ---
            "abdominal": {
                "keywords": ["abdomen", "abdômen", "barriga", "tanquinho", "abdominal", "core"],
                "resposta": "Para ver os 'gominhos', você precisa de duas coisas: hipertrofiar o músculo e ter o percentual de gordura baixo. Você costuma treinar abdômen com pesos (polia/máquina) ou só no colchonete?",
                "proximo_passo": "esperando_tipo_abdominal"
            },
            "perna": {
                "keywords": ["perna", "coxa", "gluteo", "agachamento", "inferiores", "legpress", "leg press"],
                "resposta": "Treino de pernas é vital para a liberação natural de testosterona! Seu foco atual é mais em quadríceps (parte da frente) ou na cadeia posterior (glúteos e posterior de coxa)?",
                "proximo_passo": "esperando_foco_perna"
            },
            "jejum_horario": {
                "keywords": ["jejum", "fome", "horario", "horário", "vazio", "cedo", "acordar"],
                "resposta": "Treinar em jejum otimiza a sensibilidade à insulina, mas pode reduzir a força máxima em treinos pesados. Você sente tontura ou fraqueza quando treina de barriga vazia?",
                "proximo_passo": "esperando_sintoma_jejum"
            },
            "dor_lesao": {
                "keywords": ["dor", "lesao", "machucado", "doendo", "ombro", "joelho", "lombar"],
                "resposta": "Sinal de alerta! Dor tardia (aquela do dia seguinte) é normal, mas dor aguda na hora do exercício não é. Essa dor que você sente é no 'meio' do músculo ou bem na articulação/osso?",
                "proximo_passo": "esperando_tipo_dor"
            },
            "tchau": {
                "keywords": ["tchau", "sair", "encerrar", "obrigado", "valeu", "flw", "adeus"],
                "resposta": "Foi um prazer ajudar! Lembre-se: constância é melhor que intensidade. Bom treino e até a próxima!",
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
        
        # ---------------- FLUXO: ABDOMINAL (NOVO) ----------------
        if self.contexto == "esperando_tipo_abdominal":
            if self.tem_palavra(palavras, ["peso", "pesos", "maquina", "máquina", "polia", "carga"]):
                self.contexto = None
                return "Excelente! O abdômen é um músculo como qualquer outro e precisa de sobrecarga progressiva para crescer. Continue progredindo carga e ajustando a dieta que o tanquinho aparece!"
            else:
                self.contexto = None
                return "Fazer só com o peso do corpo melhora a resistência, mas não engrossa tanto o músculo. Tente abraçar uma anilha na próxima vez! Ah, e lembre-se: a definição real do abdômen é construída na cozinha. Mais alguma dúvida?"

        # ---------------- FLUXO: TREINO DE PERNAS (NOVO) ---------
        if self.contexto == "esperando_foco_perna":
            if self.tem_palavra(palavras, ["frente", "quadriceps", "quadríceps", "coxa"]):
                self.contexto = None
                return "Para quadríceps, exercícios como Agachamento Búlgaro e Cadeira Extensora são os melhores. Foque em descer o peso devagar (fase excêntrica) para recrutar o máximo de fibras! Quer saber de outro grupo muscular?"
            else:
                self.contexto = None
                return "Para a cadeia posterior, o Stiff e a Elevação Pélvica são os reis. Um erro comum no Stiff é dobrar muito o joelho; lembre-se de jogar o quadril bem para trás! Qual seu próximo treino?"

        # ---------------- FLUXO: JEJUM E HORÁRIO (NOVO) ----------
        if self.contexto == "esperando_sintoma_jejum":
            if self.tem_palavra(palavras, ["sim", "tontura", "fraqueza", "passo", "mal", "ruim"]):
                self.contexto = None
                return "Isso é um sinal clássico de hipoglicemia. Não force! Tente comer um carboidrato de rápida absorção (como uma banana ou doce de leite) uns 30 minutos antes do treino para ter energia rápida."
            else:
                self.contexto = None
                return "Que genética privilegiada! Se você se sente bem e com força, pode continuar. Apenas garanta que vai ingerir todas as suas calorias e proteínas necessárias dentro da sua janela de alimentação diária."

        # ---------------- FLUXO: DOR E LESÃO (NOVO) --------------
        if self.contexto == "esperando_tipo_dor":
            if self.tem_palavra(palavras, ["articulação", "articulacao", "osso", "junta"]):
                self.contexto = None
                return "Cuidado extremo! Dor articular indica que a carga está passando do músculo para o tendão/osso. Reduza o peso imediatamente, revise sua execução e considere procurar um fisioterapeuta."
            else:
                self.contexto = None
                return "Se for dor no ventre do músculo, provavelmente é só ácido lático ou microlesões boas do treino. Um bom alongamento e bastante água ajudam na recuperação. Em qual músculo está essa dor?"

        # ---------------- FLUXO: EMAGRECIMENTO -----------------
        if self.contexto == "esperando_dieta_emagrecimento":
            if self.tem_palavra(palavras, ["calculo", "conto", "calorias", "sim", "app", "aplicativo"]):
                self.contexto = "esperando_cardio_emagrecimento"
                return "Isso é excelente! Ter controle dos macronutrientes acelera o processo. Falando nisso, você prefere fazer seu treino de cardio (aeróbico) antes ou depois do treino de força?"
            else:
                self.contexto = "esperando_cardio_emagrecimento"
                return "Comer de forma intuitiva é bom, mas pode esconder calorias extras. Tente focar em proteínas! Mudando para o treino: você costuma fazer cardio antes ou depois da musculação?"

        if self.contexto == "esperando_cardio_emagrecimento":
            if self.tem_palavra(palavras, ["depois", "pos", "pós", "final"]):
                self.contexto = "esperando_tipo_cardio"
                return "A ciência apoia sua escolha! Fazer cardio depois preserva seu glicogênio muscular. Você prefere algo intenso como o HIIT ou constante como a esteira inclinada?"
            elif self.tem_palavra(palavras, ["antes", "pre", "pré", "inicio"]):
                self.contexto = "esperando_tipo_cardio"
                return "Fazer antes funciona como aquecimento. Apenas tome cuidado para não gastar toda sua energia antes de levantar os pesos! Prefere esteira ou bicicleta?"

        if self.contexto == "esperando_tipo_cardio":
            self.contexto = None 
            return "Perfeito! A melhor máquina é aquela que você tem consistência em usar. Mantenha o ritmo, beba água e o resultado vem. Posso ajudar com mais algum tema?"

        # ---------------- FLUXO: HIPERTROFIA -------------------
        if self.contexto == "esperando_pilar_hipertrofia":
            if self.tem_palavra(palavras, ["treino", "falha", "força", "peso", "carga"]):
                self.contexto = "esperando_sobrecarga"
                return "Muitos erram aí! Para o músculo crescer, é preciso 'Sobrecarga Progressiva' (aumentar peso ou repetições). Você anota as cargas que levanta?"
            elif self.tem_palavra(palavras, ["proteina", "comida", "dieta", "alimentação"]):
                self.contexto = "esperando_suplemento"
                return "Sem material, a casa não sobe! A recomendação é de 1.6g a 2g de proteína por quilo. Já pensou em usar Whey Protein ou Creatina para facilitar?"
            elif self.tem_palavra(palavras, ["sono", "dormir", "descanso", "noite"]):
                self.contexto = None
                return "O sono é inegociável. É na fase profunda que o GH (hormônio do crescimento) é liberado. Tente evitar telas 1h antes de deitar. Como posso te ajudar em outro aspecto?"

        if self.contexto == "esperando_sobrecarga":
            self.contexto = None
            return "Anotar o treino muda o jogo! Ver sua evolução de força é o maior motivador que existe. Quer tirar dúvidas sobre algum exercício específico?"

        if self.contexto == "esperando_suplemento":
            self.contexto = None
            return "A Creatina ajuda muito na explosão muscular, e o Whey é ótimo pela praticidade. Vale a pena pesquisar! Mais alguma dúvida sobre treinos?"

        # ---------------- FLUXO: SAÚDE E BEM-ESTAR -------------
        if self.contexto == "esperando_rotina_saude":
            if self.tem_palavra(palavras, ["sentado", "cadeira", "escritorio", "computador"]):
                self.contexto = "esperando_mobilidade"
                return "A 'Síndrome da Cadeira' causa dor na lombar. Adicionar 10 minutos de alongamento pela manhã ajudaria. O que acha da ideia?"
            else:
                self.contexto = "esperando_mobilidade"
                return "Ter uma rotina ativa é ótimo! Para blindar o corpo contra o envelhecimento, o treino de força é crucial. Você prefere levantar pesos (musculação) ou usar o peso do corpo (calistenia/pilates)?"

        if self.contexto == "esperando_mobilidade":
            self.contexto = None
            return "Sua saúde articular vai agradecer muito no futuro. Lembre-se: investir tempo no corpo hoje é economizar na farmácia amanhã!"

        # ---------------- FLUXO: MOTIVAÇÃO ---------------------
        if self.contexto == "esperando_regra_5min":
            if self.tem_palavra(palavras, ["sim", "topo", "vamos", "ok", "claro", "bora"]):
                self.contexto = None
                return "Essa é a atitude! Coloque a roupa de treino e vá. Aposto que a endorfina vai te fazer ficar o treino todo!"
            else:
                self.contexto = None
                return "Compreensível. O corpo precisa de descanso também. Faça uma boa refeição e amanhã você recomeça. Deseja saber algo sobre alimentação?"

        # BUSCA INICIAL DE INTENÇÕE
        for intent, dados in self.conhecimento.items():
            if self.tem_palavra(palavras, dados["keywords"]):
                self.contexto = dados.get("proximo_passo")
                return dados["resposta"]
        
        # Resposta padrão
        return "Confesso que não peguei essa! Minha especialidade é falar sobre treinos específicos (pernas, abdômen), hipertrofia, emagrecimento, dor, jejum e saúde geral. Qual assunto quer explorar agora?"