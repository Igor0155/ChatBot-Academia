import json
import requests
import nltk
from nltk.tokenize import word_tokenize

import os 
from dotenv import load_dotenv

import string

class AcademiaBot:
    def __init__(self):
        load_dotenv()
        self.HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
        self.HF_API_URL = "https://router.huggingface.co/v1/chat/completions"
        self.MODEL = "Qwen/Qwen2.5-7B-Instruct:together"
        
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

        texto_usuario = " ".join(palavras)
        # Varre o JSON para buscar a relação mais próxima com as palavras-chave do usuári
        for categoria, itens in self.base_dados.items():
            for chave, informacao in itens.items():
                tokens_chave = self.processar_texto(chave)
                chave_limpa = " ".join(tokens_chave)
                if chave_limpa and chave_limpa in texto_usuario:
                    return f"📚 [Base de Dados] - {chave.title()}:\n{informacao}"
                
        return None

    def consultar_llm_fallback(self, mensagem_usuario):
        headers = {"Authorization": f"Bearer {self.HF_TOKEN}"}
        
        # O prompt para dá a personalidade de fitness à IA
        prompt = f"""Você é o FitBot, um personal trainer e nutricionista sênior.
        O usuário te fará uma pergunta complexa sobre treinos, fisiologia, biomecânica ou dieta.
        Responda de forma científica, educada, sem inventar dados e direta (máximo 2 parágrafos). 
        Deixe sempre uma pergunta para o usuário no final da resposta, para manter a conversa fluida.
        FitBot:"""

        payload = {
            "model": self.MODEL,
         "messages": [
                {
                    "role": "system",
                    "content": prompt,
                },
                {
                    "role": "user",
                    "content": mensagem_usuario
                }
            ],
            "max_tokens": 300,
            "temperature": 0.5
        }

        try:
            response = requests.post(self.HF_API_URL, headers=headers, json=payload)
            response_data = response.json()
            
            if "choices" in response_data and len(response_data["choices"]) > 0:
                resposta_final = response_data["choices"][0]["message"]["content"].strip()
                return f"🧠 [FitBot IA] - {resposta_final}"
            else:
                # Retorna o erro exato da API para ajudar a debugar
                return f"Erro na API do Hugging Face: {response_data}"
        
        except Exception as e:
            return f"Erro de conexão com o LLM: {str(e)}"

    def gerar_resposta(self, mensagem_usuario):
        palavras = self.processar_texto(mensagem_usuario)
        
        #  Tenta achar na Base Json
        resposta_kb = self.consultar_base_conhecimento(palavras)
        if resposta_kb:
            return resposta_kb
            
        #  Se a base não tiver, o LLM responde
        return self.consultar_llm_fallback(mensagem_usuario)