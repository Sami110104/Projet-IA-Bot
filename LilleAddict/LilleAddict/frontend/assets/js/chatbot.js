// ====================================
// CONFIGURATION
// ====================================
const CONFIG = {
    API_URL: 'http://localhost:8000/api/chat',
    TYPING_DELAY: 1000  // Délai simulation "typing..."
};

// ====================================
// ÉTAT GLOBAL
// ====================================
let conversationId = null;
let isWaitingResponse = false;

// ====================================
// ÉLÉMENTS DOM
// ====================================
const chatToggle = document.getElementById('chat-toggle');
const chatWindow = document.getElementById('chat-window');
const chatClose = document.getElementById('chat-close');
const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

// ====================================
// EVENT LISTENERS
// ====================================

// Toggle chat window
chatToggle.addEventListener('click', openChatbot);

// Close chat window
chatClose.addEventListener('click', closeChatbot);

// Send message on button click
sendBtn.addEventListener('click', sendMessage);

// Send message on Enter key
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Focus input when opening chat
chatWindow.addEventListener('transitionend', () => {
    if (!chatWindow.classList.contains('hidden')) {
        userInput.focus();
    }
});

// ====================================
// FONCTIONS PRINCIPALES
// ====================================

/**
 * Ouvre le chatbot
 */
function openChatbot() {
    chatWindow.classList.remove('hidden');
    userInput.focus();
}

/**
 * Ferme le chatbot
 */
function closeChatbot() {
    chatWindow.classList.add('hidden');
}

/**
 * Envoie un message au chatbot
 */
async function sendMessage() {
    const message = userInput.value.trim();
    
    // Validation
    if (!message || isWaitingResponse) {
        return;
    }
    
    // Désactiver l'input pendant le traitement
    isWaitingResponse = true;
    userInput.value = '';
    userInput.disabled = true;
    sendBtn.disabled = true;
    
    try {
        // 1. Afficher le message de l'utilisateur
        addMessage(message, 'user');
        
        // 2. Afficher l'indicateur de typing
        const typingIndicator = addTypingIndicator();
        
        // 3. Appeler l'API
        const response = await fetch(CONFIG.API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                conversation_id: conversationId
            })
        });
        
        if (!response.ok) {
            throw new Error(`Erreur HTTP: ${response.status}`);
        }
        
        const data = await response.json();
        
        // 4. Retirer l'indicateur de typing
        typingIndicator.remove();
        
        // 5. Afficher la réponse du bot
        addMessage(data.response, 'bot');
        
        // 6. Sauvegarder l'ID de conversation
        if (data.conversation_id) {
            conversationId = data.conversation_id;
        }
        
    } catch (error) {
        console.error('Erreur lors de l\'envoi du message:', error);
        
        // Retirer typing indicator
        const typing = chatMessages.querySelector('.typing');
        if (typing) typing.remove();
        
        // Afficher message d'erreur
        addMessage(
            '😞 Désolé, une erreur est survenue. Vérifie que le backend est démarré (http://localhost:8000).',
            'bot'
        );
    } finally {
        // Réactiver l'input
        isWaitingResponse = false;
        userInput.disabled = false;
        sendBtn.disabled = false;
        userInput.focus();
    }
}

/**
 * Ajoute un message dans le chat
 * @param {string} text - Texte du message
 * @param {string} sender - 'user' ou 'bot'
 */
function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    // Parser le markdown basique (** pour bold, * pour liste)
    const formattedText = formatMessage(text);
    contentDiv.innerHTML = formattedText;
    
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    
    // Scroll vers le bas
    scrollToBottom();
    
    return messageDiv;
}

/**
 * Ajoute un indicateur de "typing..."
 */
function addTypingIndicator() {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot typing';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.innerHTML = '<span class="typing-dots">...</span>';
    
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    
    scrollToBottom();
    
    return messageDiv;
}

/**
 * Formate le texte avec du markdown basique
 * @param {string} text - Texte brut
 * @returns {string} - HTML formaté
 */
function formatMessage(text) {
    // Remplacer les sauts de ligne par <br>
    let formatted = text.replace(/\n/g, '<br>');
    
    // Bold (**texte**)
    formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Emojis common (déjà présents dans le texte)
    
    // Listes simples (- item ou • item)
    formatted = formatted.replace(/^[•\-]\s+(.+)$/gm, '<li>$1</li>');
    
    // Wrapper les listes
    if (formatted.includes('<li>')) {
        formatted = formatted.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');
    }
    
    return formatted;
}

/**
 * Scroll automatique vers le bas du chat
 */
function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

/**
 * Fonction globale pour envoyer un message prédéfini (depuis les boutons de la page)
 * @param {string} message - Message à envoyer
 */
window.askBot = function(message) {
    // Ouvrir le chatbot
    openChatbot();
    
    // Remplir l'input
    userInput.value = message;
    
    // Envoyer après un court délai (effet plus naturel)
    setTimeout(() => {
        sendMessage();
    }, 500);
};

// ====================================
// INITIALISATION
// ====================================

// Générer un ID de session unique
function generateSessionId() {
    return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

// Initialiser au chargement
document.addEventListener('DOMContentLoaded', () => {
    console.log('🤖 Chatbot initialisé');
    console.log('📡 API URL:', CONFIG.API_URL);
});
