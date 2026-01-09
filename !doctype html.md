<!doctype html>  
<html lang="fr-FR">  
<head>  
    <meta charset="UTF-8">  
    <meta name="viewport" content="width=device-width, initial-scale=1">  
    <title>Lille Addict | Bons plans & Le Bot Welsh</title>  
    <link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@400;700;900&display=swap" rel="stylesheet">  
      
    <style>  
        /* --- VARIABLES GLOBALES (Tirées du site original) --- */  
        :root {  
            --lille-rouge: #cf2e2e;  
            --lille-bleu: #1D2965;  
            --lille-blanc: #ffffff;  
            --lille-bg-gris: #f5f5f5;  
            --font-main: 'Quicksand', sans-serif;  
        }  
  
        body {  
            font-family: var(--font-main);  
            margin: 0;  
            padding: 0;  
            background-color: var(--lille-blanc);  
            color: #333;  
            overflow-x: hidden;  
        }  
  
        a { text-decoration: none; color: inherit; }  
  
        /* --- HEADER --- */  
        header {  
            background: var(--lille-blanc);  
            padding: 15px 20px;  
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);  
            position: sticky;  
            top: 0;  
            z-index: 100;  
            display: flex;  
            justify-content: space-between;  
            align-items: center;  
        }  
  
        .logo img {  
            height: 60px;  
        }  
  
        .nav-buttons {  
            display: flex;  
            gap: 15px;  
        }  
  
        .btn {  
            padding: 10px 20px;  
            border-radius: 999px;  
            font-weight: 900;  
            border: 2px solid;  
            transition: all 0.3s;  
            cursor: pointer;  
        }  
  
        .btn-rouge {  
            background-color: var(--lille-rouge);  
            color: white;  
            border-color: var(--lille-rouge);  
        }  
        .btn-rouge:hover { background: transparent; color: var(--lille-rouge); }  
  
        /* --- HERO SECTION (Que faire à Lille) --- */  
        .hero {  
            background-color: #f9f9f9;  
            padding: 40px 20px;  
            text-align: center;  
            border-bottom: 1px solid #eee;  
        }  
  
        .hero h1 {  
            color: var(--lille-bleu);  
            font-size: 2.5rem;  
            margin-bottom: 10px;  
        }  
  
        .qce-lille-text {  
            color: var(--lille-rouge);  
            font-weight: 900;  
        }  
  
        /* --- GRILLE D'ARTICLES (Simulation) --- */  
        .container {  
            max-width: 1240px;  
            margin: 40px auto;  
            padding: 0 20px;  
        }  
  
        h2.section-title {  
            font-family: var(--font-main);  
            font-weight: 900;  
            font-size: 24px;  
            margin-bottom: 20px;  
            color: var(--lille-bleu);  
        }  
  
        .grid {  
            display: grid;  
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));  
            gap: 20px;  
        }  
  
        .card {  
            background: white;  
            border-radius: 24px;  
            overflow: hidden;  
            box-shadow: 0 10px 30px rgba(0,0,0,0.08);  
            border: 3px solid transparent;  
            transition: 0.3s;  
            display: flex;  
            flex-direction: column;  
        }  
  
        .card:hover {  
            border-color: var(--lille-rouge);  
            transform: translateY(-5px);  
        }  
  
        .card-img {  
            height: 200px;  
            background-color: #ddd;  
            background-size: cover;  
            background-position: center;  
            position: relative;  
        }  
  
        .pastille {  
            position: absolute;  
            top: 15px;  
            right: 15px;  
            background: var(--lille-rouge);  
            color: white;  
            padding: 5px 12px;  
            border-radius: 99px;  
            font-size: 12px;  
            font-weight: bold;  
        }  
  
        .card-content {  
            padding: 20px;  
            flex-grow: 1;  
            display: flex;  
            flex-direction: column;  
            justify-content: space-between;  
        }  
  
        .card h3 {  
            margin: 0 0 10px 0;  
            font-size: 18px;  
            line-height: 1.4;  
            color: var(--lille-bleu);  
        }  
  
        .card-meta {  
            font-size: 13px;  
            color: #888;  
            margin-bottom: 15px;  
        }  
  
        /* --- LE BOT WELSH (STYLES) --- */  
        #welsh-bot-container {  
            position: fixed;  
            bottom: 30px;  
            right: 30px;  
            z-index: 9999;  
            font-family: var(--font-main);  
        }  
  
        /* L'avatar du Welsh */  
        #welsh-avatar {  
            width: 80px;  
            height: 80px;  
            background-color: #FFA500; /* Couleur Cheddar */  
            border-radius: 50%;  
            border: 4px solid var(--lille-bleu);  
            box-shadow: 0 5px 20px rgba(0,0,0,0.3);  
            cursor: pointer;  
            display: flex;  
            align-items: center;  
            justify-content: center;  
            transition: transform 0.2s;  
            position: relative;  
            overflow: hidden;  
        }  
  
        #welsh-avatar:hover {  
            transform: scale(1.1) rotate(-5deg);  
        }  
  
        #welsh-avatar img {  
            width: 100%;  
            height: 100%;  
            object-fit: cover;  
        }  
  
        /* Bulle de notification */  
        .bot-notification {  
            position: absolute;  
            top: -5px;  
            right: -5px;  
            background: var(--lille-rouge);  
            color: white;  
            width: 25px;  
            height: 25px;  
            border-radius: 50%;  
            display: flex;  
            align-items: center;  
            justify-content: center;  
            font-weight: bold;  
            font-size: 14px;  
            animation: bounce 2s infinite;  
        }  
  
        /* Fenêtre de chat */  
        #chat-window {  
            position: absolute;  
            bottom: 100px;  
            right: 0;  
            width: 320px;  
            background: white;  
            border-radius: 20px;  
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);  
            display: none; /* Caché par défaut */  
            flex-direction: column;  
            overflow: hidden;  
            border: 2px solid var(--lille-bleu);  
        }  
  
        .chat-header {  
            background: var(--lille-bleu);  
            color: white;  
            padding: 15px;  
            font-weight: bold;  
            display: flex;  
            align-items: center;  
            gap: 10px;  
        }  
  
        .chat-body {  
            padding: 15px;  
            height: 250px;  
            overflow-y: auto;  
            background: #fff;  
            display: flex;  
            flex-direction: column;  
            gap: 10px;  
        }  
  
        .message {  
            padding: 10px 15px;  
            border-radius: 15px;  
            font-size: 14px;  
            max-width: 80%;  
            line-height: 1.4;  
        }  
  
        .bot-msg {  
            background: #f1f1f1;  
            align-self: flex-start;  
            border-bottom-left-radius: 2px;  
        }  
  
        .user-msg {  
            background: var(--lille-rouge);  
            color: white;  
            align-self: flex-end;  
            border-bottom-right-radius: 2px;  
        }  
  
        .chat-options {  
            padding: 10px;  
            border-top: 1px solid #eee;  
            display: flex;  
            flex-wrap: wrap;  
            gap: 5px;  
            background: #fafafa;  
        }  
  
        .option-btn {  
            background: white;  
            border: 1px solid var(--lille-bleu);  
            color: var(--lille-bleu);  
            padding: 5px 10px;  
            border-radius: 15px;  
            font-size: 12px;  
            cursor: pointer;  
            transition: 0.2s;  
        }  
  
        .option-btn:hover {  
            background: var(--lille-bleu);  
            color: white;  
        }  
  
        @keyframes bounce {  
            0%, 20%, 50%, 80%, 100% {transform: translateY(0);}  
            40% {transform: translateY(-10px);}  
            60% {transform: translateY(-5px);}  
        }  
  
        /* Icône de fermeture */  
        .close-chat {  
            margin-left: auto;  
            cursor: pointer;  
            font-size: 20px;  
        }  
  
    </style>  
</head>  
<body>  
  
    <header id="header">  
        <div class="logo">  
            <a href="https://lilleaddict.fr">  
                <img src="https://lilleaddict.fr/wp-content/uploads/2020/11/logo-rouge.svg" alt="Lille Addict Logo">  
            </a>  
        </div>  
        <div class="nav-buttons">  
            <a href="#" class="btn btn-rouge">Événements</a>  
            <a href="#" class="btn btn-rouge" style="background:white; color:var(--lille-bleu); border-color:var(--lille-bleu);">Mon Compte</a>  
        </div>  
    </header>  
  
    <section class="hero">  
        <h1>Que faire à <span class="qce-lille-text">Lille</span> ?</h1>  
        <p>Découvre le meilleur de la métropole lilloise : bons plans, activités et actus.</p>  
    </section>  
  
    <main class="container">  
          
        <h2 class="section-title">Nos derniers articles à ne pas rater !</h2>  
        <div class="grid">  
            <article class="card">  
                <div class="card-img" style="background-image: url('https://lilleaddict.fr/wp-content/uploads/2025/01/capture-decran-2026-01-07-a-15.17.15-1024x998.png');">  
                    <span class="pastille">Actus</span>  
                </div>  
                <div class="card-content">  
                    <div class="card-meta">Il y a 2 jours</div>  
                    <h3>Carnaval de Dunkerque 2026 : l'agenda complet</h3>  
                    <div style="margin-top:auto;">  
                        <a href="#" class="btn btn-rouge" style="padding: 5px 15px; font-size:12px;">Lire la suite</a>  
                    </div>  
                </div>  
            </article>  
  
            <article class="card">  
                <div class="card-img" style="background-image: url('https://lilleaddict.fr/wp-content/uploads/2025/11/village-de-noel-moyenne.jpeg');">  
                    <span class="pastille">Sortir</span>  
                </div>  
                <div class="card-content">  
                    <div class="card-meta">Il y a 3 jours</div>  
                    <h3>Que faire à Lille et aux alentours pour le Nouvel An ?</h3>  
                    <div style="margin-top:auto;">  
                        <a href="#" class="btn btn-rouge" style="padding: 5px 15px; font-size:12px;">Lire la suite</a>  
                    </div>  
                </div>  
            </article>  
  
            <article class="card">  
                <div class="card-img" style="background-image: url('https://lilleaddict.fr/wp-content/uploads/2025/11/ben09508-moyenne.jpeg');">  
                    <span class="pastille">Miam</span>  
                </div>  
                <div class="card-content">  
                    <div class="card-meta">Il y a 1 semaine</div>  
                    <h3>Les meilleurs Welshs de Lille selon les Lillois</h3>  
                    <div style="margin-top:auto;">  
                        <a href="#" class="btn btn-rouge" style="padding: 5px 15px; font-size:12px;">Lire la suite</a>  
                    </div>  
                </div>  
            </article>  
  
             <article class="card">  
                <div class="card-img" style="background-image: url('https://lilleaddict.fr/wp-content/uploads/2023/11/image_7-29-e1746191577679.webp');">  
                    <span class="pastille">Sport</span>  
                </div>  
                <div class="card-content">  
                    <div class="card-meta">Il y a 2 semaines</div>  
                    <h3>Les meilleures salles d'escalade à Lille</h3>  
                    <div style="margin-top:auto;">  
                        <a href="#" class="btn btn-rouge" style="padding: 5px 15px; font-size:12px;">Lire la suite</a>  
                    </div>  
                </div>  
            </article>  
        </div>  
  
    </main>  
  
    <div id="welsh-bot-container">  
        <div id="chat-window">  
            <div class="chat-header">  
                <span>🧀 Welly le Welsh</span>  
                <span class="close-chat" onclick="toggleChat()">×</span>  
            </div>  
            <div class="chat-body" id="chat-body">  
                <div class="message bot-msg">  
                    Salut biloute ! 👋 Moi c'est Welly. Je suis chaud comme un welsh sortant du four. Tu cherches quoi ?  
                </div>  
            </div>  
            <div class="chat-options">  
                <button class="option-btn" onclick="sendMessage('J\'ai la dalle !')">🍔 J'ai la dalle</button>  
                <button class="option-btn" onclick="sendMessage('On boit un coup ?')">🍻 On boit un coup ?</button>  
                <button class="option-btn" onclick="sendMessage('Une blague Ch\'ti')">🤡 Raconte une blague</button>  
            </div>  
        </div>  
  
        <div id="welsh-avatar" onclick="toggleChat()">  
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Welsh_rabbit_%2834038476632%29.jpg/640px-Welsh_rabbit_%2834038476632%29.jpg" alt="Welsh Bot">  
            <div class="bot-notification">1</div>  
        </div>  
    </div>  
  
    <script>  
        function toggleChat() {  
            const chatWindow = document.getElementById('chat-window');  
            const notification = document.querySelector('.bot-notification');  
              
            if (chatWindow.style.display === 'flex') {  
                chatWindow.style.display = 'none';  
            } else {  
                chatWindow.style.display = 'flex';  
                if(notification) notification.style.display = 'none'; // Cache la notif une fois ouvert  
            }  
        }  
  
        function sendMessage(msg) {  
            const chatBody = document.getElementById('chat-body');  
              
            // Message utilisateur  
            const userDiv = document.createElement('div');  
            userDiv.className = 'message user-msg';  
            userDiv.textContent = msg;  
            chatBody.appendChild(userDiv);  
  
            // Scroll vers le bas  
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
                botDiv.innerHTML = botResponse; // innerHTML pour gérer le gras si besoin  
                chatBody.appendChild(botDiv);  
                chatBody.scrollTop = chatBody.scrollHeight;  
  
            }, 800); // Petit délai pour faire naturel  
        }  
    </script>  
  
</body>  
</html>  
