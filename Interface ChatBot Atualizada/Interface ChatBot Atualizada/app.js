const chatContainer = document.getElementById("chatContainer");
const chatForm = document.getElementById("chatForm");
const messageInput = document.getElementById("messageInput");

const botTypingDelay = 700;

function getDateTimeString() {
  const now = new Date();
  return now.toLocaleString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  });
}

function addMessageToBoard(txt, sender = "bot") {
  const msgEl = document.createElement("div");
  msgEl.className = `message ${sender}`;
  msgEl.innerHTML = `
    <div class="message-text">${txt}</div>
    <div class="message-time">${getDateTimeString()}</div>
  `;
  chatContainer.appendChild(msgEl);
  chatContainer.scrollTop = chatContainer.scrollHeight;
  return msgEl;
}

function botReply(userText) {
  const lowercase = userText.trim().toLowerCase();

  if (!lowercase) return "Desculpe, não entendi. Pode repetir?";

  if (lowercase.includes("olá") || lowercase.includes("oi") || lowercase.includes("bom dia")) {
    return "Olá! Pronto para treinar hoje? Posso sugerir exercícios, metas e dicas de recuperação.";
  }

  if (lowercase.includes("ajuda") || lowercase.includes("como") || lowercase.includes("o que")) {
    return "Estou aqui para ajudar no seu plano de treino. Pergunte sobre séries, alimentação ou motivação.";
  }

  if (lowercase.includes("tchau") || lowercase.includes("até")) {
    return "Bom treino! Volte quando quiser continuar a conversa.";
  }

  return `Você disse: "${userText}". Ainda estou em modo de demonstração e posso ser ampliado para consultas reais.`;
}

chatForm.addEventListener("submit", async (evt) => {
  evt.preventDefault();
  const text = messageInput.value.trim();
  if (!text) return;

  addMessageToBoard(text, "user");
  messageInput.value = "";
  messageInput.focus();

  const typingMessage = addMessageToBoard("Digitando...", "bot");
  await new Promise((resolve) => setTimeout(resolve, botTypingDelay));

  if (typingMessage && typingMessage.parentNode) {
    typingMessage.remove();
  }

  const answer = botReply(text);
  addMessageToBoard(answer, "bot");
});

messageInput.focus();
