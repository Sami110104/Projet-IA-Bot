function toggleChat() {
    const chatWindow = document.getElementById('chat-window');
    const notification = document.querySelector('.bot-notification');

    if (chatWindow.style.display === 'flex') {
        chatWindow.style.display = 'none';
    } else {
        chatWindow.style.display = 'flex';
        if(notification) notification.style.display = 'none';
    }
}

function sendMessage(msg) {
    const chatBody = document.getElementById('chat-body');

    // Message utilisateur
    const userDiv = document.createElement('div');
    userDiv.className = 'message user-msg';
    userDiv.textContent = msg;
    chatBody.appendChild(userDiv);

    chatBody.scrollTop = chatBody.scrollHeight;

    // Réponse du bot (simulée)
    setTimeout(() => {
        let botResponse = "";

        if (msg.includes("dalle")) {
            botResponse = "Ah ! Pour un bon welsh, fonce au **George V** ou à **L'Estaminet du Welsh**. Sinon, une petite frite chez Meunier ?";
        } else if (msg.includes("boit")) {
            botResponse = "Santé ! 🍻 Pour une bonne bière, va à **La Capsule** dans le Vieux-Lille. Si tu préfères les cocktails, direction **Le Joker** !";
        } else if (msg.includes("blague")) {
            botResponse = "C'est l'histoire d'un mec qui rentre dans un café à Roubaix... et plouf ! 🌧️ (C'est parce qu'il pleut tout le temps, t'as compris ?)";
        } else {
            botResponse = "J'ai pas tout compris, j'ai du cheddar dans les oreilles !";
        }

        const botDiv = document.createElement('div');
        botDiv.className = 'message bot-msg';
        botDiv.innerHTML = botResponse;
        chatBody.appendChild(botDiv);
        chatBody.scrollTop = chatBody.scrollHeight;

    }, 800);
}
