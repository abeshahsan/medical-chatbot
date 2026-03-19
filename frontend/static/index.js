const form = document.getElementById("chat-form");
const input = document.getElementById("question");
const messages = document.getElementById("messages");

function addMessage(text, role) {
	const bubble = document.createElement("div");
	bubble.className = `bubble ${role}`;
	bubble.textContent = text;
	messages.appendChild(bubble);
	messages.scrollTop = messages.scrollHeight;
}

form.addEventListener("submit", async (event) => {
	event.preventDefault();

	const question = input.value.trim();
	if (!question) return;

	addMessage(question, "user");
	input.value = "";

	try {
		const response = await fetch("/chat", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({ message: question }),
		});

		const data = await response.json();
		const botText = data.msg || "No response received.";
		addMessage(botText, "bot");
	} catch (_error) {
		addMessage("Something went wrong. Please try again.", "bot");
	}
});
