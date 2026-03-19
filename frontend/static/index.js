const form = document.getElementById("chat-form");
const input = document.getElementById("question");
const messages = document.getElementById("messages");
const chatHistory = [];

function addMessage(text, role) {
	const bubble = document.createElement("div");
	bubble.className = `bubble ${role}`;
	if (role === "bot" && typeof marked !== "undefined") {
		bubble.innerHTML = marked.parse(text);
	} else {
		bubble.textContent = text;
	}
	messages.appendChild(bubble);
	messages.scrollTop = messages.scrollHeight;
}

function addTypingIndicator() {
	const bubble = document.createElement("div");
	bubble.className = "bubble bot typing";
	bubble.innerHTML = '<span class="dot"></span><span class="dot"></span><span class="dot"></span>';
	messages.appendChild(bubble);
	messages.scrollTop = messages.scrollHeight;
	return bubble;
}

form.addEventListener("submit", async (event) => {
	event.preventDefault();

	const question = input.value.trim();
	if (!question) return;

	addMessage(question, "user");
	chatHistory.push({ role: "user", text: question });
	input.value = "";
	input.disabled = true;

	const typingBubble = addTypingIndicator();

	try {
		const response = await fetch("/chat", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({ message: question, history: chatHistory.slice(-8) }),
		});

		const data = await response.json();
		typingBubble.remove();
		const botText = data.msg || "No response received.";
		addMessage(botText, "bot");
		chatHistory.push({ role: "bot", text: botText });
	} catch (_error) {
		typingBubble.remove();
		addMessage("Something went wrong. Please try again.", "bot");
		chatHistory.push({ role: "bot", text: "Something went wrong. Please try again." });
	} finally {
		input.disabled = false;
		input.focus();
	}
});
