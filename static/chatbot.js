document.addEventListener('DOMContentLoaded', () => {
    const messageInput = document.getElementById('message');
    const sendButton = document.getElementById('send');
    const messagesContainer = document.getElementById('messages');
    const messageForm = document.getElementById('message-form');
    const username = localStorage.getItem("username") || "guest";

    function addBubble(text, className) {
        const bubble = document.createElement('div');
        bubble.className = className;
        bubble.textContent = text;
        messagesContainer.appendChild(bubble);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    async function sendMessage() {
        const text = messageInput.value.trim();
        if (!text) return;

        addBubble(text, 'user-bubble');
        messageInput.value = '';

        try {
            const res = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: text,
                    username: username
                })
            });

            const data = await res.json();
            addBubble(data.reply || 'No reply from AI.', 'bot-bubble');
        } catch (error) {
            console.error('Error:', error);
            addBubble('Oops! Server error occurred.', 'bot-bubble');
        }
    }

    if (sendButton) sendButton.addEventListener('click', sendMessage);

    if (messageInput) {
        messageInput.addEventListener('keydown', event => {
            if (event.key === 'Enter') {
                event.preventDefault();
                sendMessage();
            }
        });
    }

    if (messageForm) {
        messageForm.addEventListener('submit', event => {
            event.preventDefault();
            sendMessage();
        });
    }

    addBubble('Hello! I am your healthcare assistant. How can I help you today?', 'bot-bubble');
});