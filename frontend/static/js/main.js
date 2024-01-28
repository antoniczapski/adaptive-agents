
let conversationHistory = [];

fetch('static/instructions.txt')
  .then(response => response.text())
  .then(data => {
    conversationHistory = [{sender: 'system', message: data}];
    document.getElementById('agent-instructions-textarea').value = data;
  });


async function sendMessage() {
    var prompt = document.getElementById('prompt-textarea').value;
    document.getElementById('prompt-textarea').value = '';
    displayMessage('user', prompt);

    conversationHistory.push({ sender: 'user', message: prompt });

    try {
        const response = await generateChatbotResponse(conversationHistory);
        displayMessage('assistant', response)
        conversationHistory.push({ sender: 'assistant', message: response });
    } catch (error) {
        console.error('Error:', error);
    }
}

function displayMessage(sender, message) {
    if (sender === 'system') {
        return;
    }
    var chatDiv = document.getElementById('chat');
    var messageDiv = document.createElement('div');
    var imageDiv = document.createElement('img');
    var textDiv = document.createElement('div');
    
    var senderTextNode = document.createElement('div');
    var messageTextNode = document.createElement('div');

    senderTextNode.className = 'chat-sender';
    messageTextNode.className = sender === 'user' ? 'chat-message-text-user' : 'chat-message-text-bot';

    senderTextNode.textContent = sender;
    if (sender === 'user') {
        messageTextNode.textContent = message;
    }
    else {
        var formattedMessage = message.replace(/\n/g, '<br>');
        formattedMessage = formattedMessage.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        messageTextNode.innerHTML = formattedMessage;
    }

    textDiv.appendChild(senderTextNode);
    textDiv.appendChild(messageTextNode);

    textDiv.className = 'chat-text';

    let userImg = document.body.getAttribute('data-user-img');
    let botImg = document.body.getAttribute('data-bot-img');

    imageDiv.src = sender === 'user' ? userImg : botImg;
    imageDiv.className = 'chat-image';

    messageDiv.className = 'chat-message';
    messageDiv.appendChild(imageDiv);
    messageDiv.appendChild(textDiv);

    chatDiv.appendChild(messageDiv);

    messageDiv.scrollIntoView({ behavior: 'smooth' });
}

async function generateChatbotResponse(conversationHistory) {
    const response = await fetch('/run_script', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(conversationHistory)
    });

    if (response.ok) {
        const result = await response.json();
        return result;
    } else {
        console.error('Error calling Python script:', response.status, response.statusText);
    }
}

var textarea = document.getElementById('prompt-textarea');
textarea.addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        sendMessage();
    }
});