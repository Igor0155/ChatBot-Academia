import json
import requests
import nltk
from nltk.tokenize import word_tokenize
import string

class AcademiaBot:
    def __init__(self):
        self.HF_TOKEN = ""
        self.HF_API_URL = "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-7B-Instruct"
        
        # Carrega a base de dados (Json)
        try:
            with open('base_conhecimento.json', 'r', encoding='utf-8') as f:
                self.base_dados = json.load(f)
        except FileNotFoundError:
            self.base_dados = {}
            print("Aviso: Arquivo base_conhecimento.json não encontrado.")

    def processar_texto(self, texto):
        tokens = word_tokenize(texto.lower())
        return [w for w in tokens if w not in string.punctuation]

    def consultar_base_conhecimento(self, palavras):
        # Varre o JSON para buscar a relação mais próxima com as palavras-chave do usuário
        for categoria, itens in self.base_dados.items():
            for chave, informacao in itens.items():
                if chave in palavras:
                    return f"📚 [Base de Dados] - {chave.title()}:\n{informacao}"
        return None

    def consultar_llm_fallback(self, mensagem_usuario):
        headers = {"Authorization": f"Bearer {self.HF_TOKEN}"}
        
        # O prompt para dá a personalidade de fitness à IA
        prompt = f"""Você é o FitBot, um personal trainer e nutricionista sênior.
        O usuário te fará uma pergunta complexa sobre treinos, fisiologia, biomecânica ou dieta.
        Responda de forma científica, direta e sem inventar dados.
        Usuário: {mensagem_usuario}
        FitBot:"""

        payload = {
            "inputs": prompt,
            "parameters": {"max_new_tokens": 300, "temperature": 0.5} # Temperature baixa para respostas mais exatas
        }

        try:
            response = requests.post(self.HF_API_URL, headers=headers, json=payload)
            response_data = response.json()
            
            if type(response_data) == list and "generated_text" in response_data[0]:
                texto_gerado = response_data[0]["generated_text"]
                resposta_final = texto_gerado.split("FitBot:")[-1].strip()
                return f"🧠 [FitBot IA] - {resposta_final}"
            return "Erro na API. O modelo está indisponível no momento."
        
        except Exception as e:
            return f"Erro de conexão: {str(e)}"

    def gerar_resposta(self, mensagem_usuario):
        palavras = self.processar_texto(mensagem_usuario)
        
        #  Tenta achar na Base Json
        resposta_kb = self.consultar_base_conhecimento(palavras)
        if resposta_kb:
            return resposta_kb
            
        #  Se a base não tiver, o LLM responde
        return self.consultar_llm_fallback(mensagem_usuario)