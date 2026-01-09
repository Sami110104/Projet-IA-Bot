// ====================================
// MAIN.JS - Welsh BOT - Lille Addict Style
// ====================================

document.addEventListener('DOMContentLoaded', () => {
    console.log('🧀 Welsh BOT - Lille Addict Style');
    loadEventsPreview();
});

// ====================================
// LOAD EVENTS PREVIEW
// ====================================
async function loadEventsPreview() {
    const container = document.getElementById('events-preview');
    if (!container) return;

    try {
        const response = await fetch('http://localhost:8000/api/events/preview');

        if (!response.ok) throw new Error('API error');

        const data = await response.json();

        if (data.events && data.events.length > 0) {
            container.innerHTML = '';
            data.events.forEach((event, i) => {
                container.innerHTML += createArticleCard(event, i);
            });
        } else {
            container.innerHTML = `
                <div class="loading-message">
                    <p>Aucun événement disponible.</p>
                    <p>Clique sur <strong>Welsh BOT</strong> pour découvrir Lille ! 🤖</p>
                </div>
            `;
        }
    } catch (error) {
        console.error('Erreur:', error);
        container.innerHTML = `
            <div class="loading-message">
                <p>Impossible de charger les événements.</p>
                <p style="font-size: 13px; color: #999;">Backend: http://localhost:8000</p>
            </div>
        `;
    }
}

// ====================================
// CREATE ARTICLE CARD
// ====================================
function createArticleCard(event, index) {
    const colors = [
        'linear-gradient(135deg, #D62825 0%, #FF6B6B 100%)',
        'linear-gradient(135deg, #1D2965 0%, #4A6FA5 100%)',
        'linear-gradient(135deg, #F0A500 0%, #FFD93D 100%)',
        'linear-gradient(135deg, #6B4984 0%, #A855F7 100%)'
    ];

    const tags = ['Événement', 'Sortie', 'Concert', 'Marché'];
    const times = ['Il y a 2 jours', 'Il y a 3 jours', 'Il y a 1 semaine'];

    const emoji = getEventEmoji(event.title);
    const color = colors[index % colors.length];
    const tag = tags[index % tags.length];
    const time = times[index % times.length];

    return `
        <article class="article-card" onclick="askBot('Parle-moi de ${escapeHtml(event.title)}')">
            <span class="article-tag">${tag}</span>
            <span class="article-date">${time}</span>
            <div class="article-image-placeholder" style="background: ${color}">
                <span>${emoji}</span>
            </div>
            <h3 class="article-title">${escapeHtml(event.title)}</h3>
            <p class="article-excerpt">${escapeHtml(event.description || '')}</p>
            <div class="article-btn">
                <span>lire la suite</span>
                <svg width="40" height="17" viewBox="0 0 41 18" fill="none">
                    <path d="M1.71464 17.4751C1.18433 17.5404 0.678377 17.2134 0.550487 16.6996C0.414905 16.1453 0.768828 15.5877 1.34163 15.4523L30.281 8.57269C30.8565 8.43691 31.4309 8.77366 31.5662 9.32544C31.7018 9.87978 31.3478 10.4373 30.775 10.5728L1.83598 17.4549C1.79418 17.4653 1.75472 17.4727 1.71495 17.4776L1.71464 17.4751Z" fill="#D62825"/>
                    <path d="M31.8501 16.3531C31.6353 16.3796 31.413 16.3446 31.2087 16.2374C30.6934 15.9661 30.5033 15.3406 30.789 14.8408C32.2649 12.2476 34.3317 9.97099 36.2956 7.93028C33.697 6.54506 31.0671 4.70945 29.0633 2.86421C28.6382 2.47272 28.6251 1.82023 29.0344 1.40642C29.4437 0.992604 30.1198 0.974214 30.5449 1.36571C32.7252 3.37609 35.7037 5.3764 38.5119 6.71504C38.815 6.85939 39.0263 7.13187 39.0848 7.45431C39.1431 7.77418 39.041 8.10343 38.8066 8.34254C36.6682 10.5397 34.2454 13.0289 32.6566 15.8203C32.4841 16.1244 32.1762 16.3129 31.8474 16.3534L31.8501 16.3531Z" fill="#D62825"/>
                </svg>
            </div>
        </article>
    `;
}

// ====================================
// UTILITIES
// ====================================
function getEventEmoji(title) {
    const t = (title || '').toLowerCase();
    if (t.includes('concert') || t.includes('jazz') || t.includes('musique')) return '🎵';
    if (t.includes('marché') || t.includes('créateur')) return '🛍️';
    if (t.includes('escape') || t.includes('jeu')) return '🎮';
    if (t.includes('spectacle') || t.includes('cirque')) return '🎪';
    if (t.includes('expo') || t.includes('musée')) return '🖼️';
    if (t.includes('festival')) return '🎉';
    if (t.includes('sport') || t.includes('trail')) return '🏃';
    return '📅';
}

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ====================================
// SEARCH BAR
// ====================================
const searchInput = document.getElementById('search-input');
if (searchInput) {
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            const query = searchInput.value.trim();
            if (query) {
                askBot(query);
                searchInput.value = '';
            }
        }
    });
}
