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
        
        # Guarda o historico da conversa...
        self.historico = []
        
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
        # Varre o JSON para buscar a relação mais próxima com as palavras-chave do usuário
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
        with open("fitbot_prompt.txt", "r", encoding="utf-8") as f:
            prompt =  f.read()

        # Cria a mensagem para o LLM com:
        # Hitórico da conversa
        # Mensagem do usuário
        mensagem = [{
            "role": "system",
            "content": prompt
        }]

        # limitando hitorico
        self.historico = self.historico[-10:]

        mensagem.extend(self.historico)
        mensagem.append({
            "role": "user",
            "content": mensagem_usuario
        })

        payload = {
            "model": self.MODEL,
            "messages": mensagem,
            #"max_tokens": 512,
            "temperature": 0.2
        }

        try:
            response = requests.post(self.HF_API_URL, headers=headers, json=payload)
            response_data = response.json()
            
            if "choices" in response_data and len(response_data["choices"]) > 0:
                resposta_final = response_data["choices"][0]["message"]["content"].strip()

                # Adiciona a pergunta do usuário e resposta ao histórico
                self.historico.append({
                    "role": "user",
                    "content": mensagem_usuario
                })
                self.historico.append({
                    "role": "assistant",
                    "content": resposta_final
                })

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