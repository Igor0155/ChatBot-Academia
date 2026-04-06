# Chatbot Web UI com comportamento inicial “mock” de bot para validação imediata.
## Feito por Davi dos Santos Morais e Luiz Felipe Lamas Mishima
## Funcionalidades
Interface web responsiva para conversar com um chatbot de demonstração.
Layout moderno e responsivo (desktop + mobile)
Área de mensagens com rolamento automático
Input + botão de envio
Respostas de bot simuladas (botReply) com:
reconhecimento de olá, ajuda, tchau.

## Entradas e Saídas usadas como exemplo.
"Olá, Oi e Bom dia" retorna:
Olá! Pronto para treinar hoje? Posso sugerir exercícios, metas e dicas de recuperação.

"Ajuda, como e o que" retorna:
Estou aqui para ajudar no seu plano de treino. Pergunte sobre séries, alimentação ou motivação.

"Tchau e até" retorna:
Bom treino! Volte quando quiser continuar a conversa.

fallback para “ainda em modo de demonstração”
Experiência de digitação (placeholder “Digitando...”)
Acessibilidade básica (aria-live, label no input)

## Como usar
1. Abra `index.html` no navegador a partir da pasta `Interface ChatBot`.
2. Digite uma mensagem e clique em Enviar.
3. Interface responde com mensagens de exemplo.

## Expansão
- Integrar com API real (OpenAI, Rasa, etc.) em `app.js`.
- Substituir `botReply` por chamada fetch para backend.
fetch('/chat', { method:'POST', body: JSON.stringify({msg}) })
- Adicionar persistência de histórico via localStorage ou servidor.

## Integração Interface Web com Python + NLTK
## Arquitetura
- Passo 1: Backend Python com Flask
Você precisará de um servidor que:

Recebe a mensagem do usuário via POST
Processa com NLTK (tokenização, análise, classificação)
Retorna a resposta em JSON
## Estrutura básica:

- Passo 2: Alterar app.js para chamar o backend
No JavaScript, substituir botReply() por uma chamada fetch:

- Passo 3: Processamento NLTK útil para Academia
Exemplos de análise:

Tokenização: Dividir "maior rotina de perna?" em palavras
Classificação: Detectar se é pergunta sobre treino, nutrição ou motivação
Extração: Reconhecer exercícios mencionados ("supino", "agachamento")
Sentimento: Avaliar tom (frustração, entusiasmo)

- Passo 4: Dependências Python
E em Python:
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('vader_lexicon')

## Resumo do fluxo:
Frontend: Usuário digita → app.js coleta mensagem e faz fetch() para /chat
Backend: Flask recebe POST → NLTK processa → lógica gera resposta
Retorno: Backend envia JSON com reply → Frontend exibe no chat