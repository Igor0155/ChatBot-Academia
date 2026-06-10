const chatContainer = document.getElementById("chatContainer");
const chatForm = document.getElementById("chatForm");
const messageInput = document.getElementById("messageInput");

const botTypingDelay = 700;

function getDateTimeString() {
  const now = new Date();
  return now.toLocaleString("pt-BR", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });
}

function addMessageToBoard(txt, sender = "bot") {
  const msgEl = document.createElement("div");
  msgEl.className = `message ${sender}`;
  const html = DOMPurify.sanitize(marked.parse(txt));
  msgEl.innerHTML = `
    <div class="message-text">${html}</div>
    <div class="message-time">${getDateTimeString()}</div>
  `;
  chatContainer.appendChild(msgEl);
  chatContainer.scrollTop = chatContainer.scrollHeight;
  return msgEl;
}

chatForm.addEventListener("submit", async (evt) => {
  evt.preventDefault();
  const text = messageInput.value.trim();
  if (!text) return;

  // Mostra mensagem do usuário
  addMessageToBoard(text, "user");
  messageInput.value = "";

  // Mostra "Digitando..."
  const typingMessage = addMessageToBoard("Digitando...", "bot");
  await new Promise((resolve) => setTimeout(resolve, botTypingDelay));

  try {
    // Chamada AJAX para o Flask
    const response = await fetch("/get_response", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text }),
    });

    const data = await response.json();

    // Remove "Digitando" e exibe resposta real
    typingMessage.remove();
    addMessageToBoard(data.reply, "bot");
  } catch (error) {
    typingMessage.remove();
    addMessageToBoard("Erro ao conectar com o servidor.", "bot");
  }
});

messageInput.focus();
