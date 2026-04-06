from flask import Flask, render_template, request, jsonify
from chatbot_logic import AcademiaBot

app = Flask(__name__)
bot = AcademiaBot()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    data = request.json
    user_message = data.get("message")
    
    if not user_message:
        return jsonify({"reply": "Ops, não recebi nada!"})

    # Chama a lógica do NLTK
    resposta_bot = bot.gerar_resposta(user_message)
    
    return jsonify({"reply": resposta_bot})

if __name__ == '__main__':
    app.run(debug=True)