// State Management
let currentPlatform = 'facebook';
let hoverTimers = {}; // Stores timers for registering hover views

// DOM Elements
const feedPostsContainer = document.getElementById('feed-posts-container');
const trendsListContainer = document.getElementById('trends-list-container');
const simulatedTimeDisplay = document.getElementById('simulated-time-display');
const chatMessagesContainer = document.getElementById('chat-messages-container');
const chatInputForm = document.getElementById('chat-input-form');
const chatInputField = document.getElementById('chat-input-field');
const aiThoughtLog = document.getElementById('ai-thought-log');
const toggleThoughtsBtn = document.getElementById('toggle-thoughts-btn');
const btnFacebook = document.getElementById('btn-facebook');
const btnPinterest = document.getElementById('btn-pinterest');
const btnMyFacebook = document.getElementById('btn-my-facebook');
const btnMyInstagram = document.getElementById('btn-my-instagram');
const btnMyReddit = document.getElementById('btn-my-reddit');
const btnResetSimulation = document.getElementById('btn-reset-simulation');
const feedTitleText = document.getElementById('feed-title-text');
const feedSubtitleText = document.getElementById('feed-subtitle-text');

// Mobile Responsive DOM Elements
const appSidebar = document.getElementById('app-sidebar');
const appAnalytics = document.getElementById('app-analytics');
const bodyOverlay = document.getElementById('body-overlay');
const mobileMenuBtn = document.getElementById('mobile-menu-btn');
const mobileChatBtn = document.getElementById('mobile-chat-btn');
const closeSidebarBtn = document.getElementById('close-sidebar-btn');
const closeAnalyticsBtn = document.getElementById('close-analytics-btn');

// Init
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    refreshAll();

    // Register Service Worker for PWA support
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/sw.js')
            .then(reg => console.log('PWA Service Worker registered:', reg.scope))
            .catch(err => console.error('PWA Service Worker failed:', err));
    }
    
    // Auto-update trend calculations every 3 seconds to simulate real-time decay
    setInterval(() => {
        fetchTrends();
        updateTimeDisplay();
    }, 3000);
});

// Event Listeners Setup
function setupEventListeners() {
    // Platform Switchers
    btnFacebook.addEventListener('click', () => switchPlatform('facebook'));
    btnPinterest.addEventListener('click', () => switchPlatform('pinterest'));
    btnMyFacebook.addEventListener('click', () => switchPlatform('my-facebook'));
    btnMyInstagram.addEventListener('click', () => switchPlatform('my-instagram'));
    btnMyReddit.addEventListener('click', () => switchPlatform('my-reddit'));
    
    // Chat Form
    chatInputForm.addEventListener('submit', handleChatSubmit);
    
    // Simulation Buttons
    document.querySelectorAll('.sim-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const seconds = parseFloat(btn.getAttribute('data-advance'));
            advanceTime(seconds);
        });
    });
    
    // Reset Button
    btnResetSimulation.addEventListener('click', resetSimulation);
    
    // Collapse Thought Log
    toggleThoughtsBtn.addEventListener('click', () => {
        const container = toggleThoughtsBtn.closest('.thought-process-container');
        container.classList.toggle('collapsed');
    });

    // Mobile Responsive Listeners
    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', openSidebar);
    }
    if (mobileChatBtn) {
        mobileChatBtn.addEventListener('click', openAnalytics);
    }
    if (closeSidebarBtn) {
        closeSidebarBtn.addEventListener('click', closeDrawers);
    }
    if (closeAnalyticsBtn) {
        closeAnalyticsBtn.addEventListener('click', closeDrawers);
    }
    if (bodyOverlay) {
        bodyOverlay.addEventListener('click', closeDrawers);
    }
}

// Mobile Drawer Controllers
function openSidebar() {
    if (appSidebar) appSidebar.classList.add('open');
    if (appAnalytics) appAnalytics.classList.remove('open'); // close other
    if (bodyOverlay) bodyOverlay.classList.add('active');
}

// Open Chat Drawer on mobile when clicking Chat topbar button
function openAnalytics() {
    if (appAnalytics) appAnalytics.classList.add('open');
    if (appSidebar) appSidebar.classList.remove('open'); // close other
    if (bodyOverlay) bodyOverlay.classList.add('active');
    
    // Remove unread alert dot when opened
    const pulseDot = document.querySelector('.pulse-dot-small');
    if (pulseDot) pulseDot.style.display = 'none';
}

function closeDrawers() {
    if (appSidebar) appSidebar.classList.remove('open');
    if (appAnalytics) appAnalytics.classList.remove('open');
    if (bodyOverlay) bodyOverlay.classList.remove('active');
}

// Refresh Page Data
function refreshAll() {
    if (currentPlatform === 'my-facebook' || currentPlatform === 'my-instagram' || currentPlatform === 'my-reddit') {
        fetchMySingleProfile(currentPlatform);
    } else {
        fetchFeed();
    }
    fetchTrends();
    updateTimeDisplay();
}

// Switch Active Platform Tab
function switchPlatform(platform) {
    if (currentPlatform === platform) {
        closeDrawers();
        return;
    }
    
    currentPlatform = platform;
    
    // Reset active class on all switchers
    btnFacebook.classList.remove('active');
    btnPinterest.classList.remove('active');
    btnMyFacebook.classList.remove('active');
    btnMyInstagram.classList.remove('active');
    btnMyReddit.classList.remove('active');
    
    if (platform === 'facebook') {
        btnFacebook.classList.add('active');
        feedTitleText.textContent = "Feed Facebook";
        feedSubtitleText.textContent = "Simulează activitatea pentru a influența trendurile în timp real";
        feedPostsContainer.className = "feed-content layout-facebook";
    } else if (platform === 'pinterest') {
        btnPinterest.classList.add('active');
        feedTitleText.textContent = "Board Pinterest";
        feedSubtitleText.textContent = "Salvează pin-uri sau lasă vizualizări pentru a ridica trendurile estetice";
        feedPostsContainer.className = "feed-content layout-pinterest";
    } else if (platform === 'my-facebook') {
        btnMyFacebook.classList.add('active');
        feedTitleText.textContent = "Facebook-ul Meu";
        feedSubtitleText.textContent = "Analiza în timp real a activității și statisticilor tale de Facebook";
        feedPostsContainer.className = "feed-content layout-my-facebook";
        autoTriggerAuditChat('facebook');
    } else if (platform === 'my-instagram') {
        btnMyInstagram.classList.add('active');
        feedTitleText.textContent = "Instagram-ul Meu";
        feedSubtitleText.textContent = "Analiza performanței contului tău de Instagram";
        feedPostsContainer.className = "feed-content layout-my-instagram";
        autoTriggerAuditChat('instagram');
    } else if (platform === 'my-reddit') {
        btnMyReddit.classList.add('active');
        feedTitleText.textContent = "Reddit-ul Meu";
        feedSubtitleText.textContent = "Analiza activității și reputației tale de pe Reddit";
        feedPostsContainer.className = "feed-content layout-my-reddit";
        autoTriggerAuditChat('reddit');
    }
    
    // Clear any active hover timers
    Object.values(hoverTimers).forEach(clearTimeout);
    hoverTimers = {};
    
    closeDrawers(); // Close mobile menus when switching platform
    refreshAll();
}

// ==========================================
// API CALLS & RENDERING
// ==========================================

// Fetch Feed Posts
async function fetchFeed() {
    try {
        const response = await fetch(`/api/feed?platform=${currentPlatform}`);
        if (!response.ok) throw new Error("A eșuat încărcarea feed-ului.");
        const posts = await response.json();
        renderFeed(posts);
    } catch (error) {
        console.error(error);
        feedPostsContainer.innerHTML = `
            <div class="loading-spinner">
                <i class="fa-solid fa-triangle-exclamation" style="color: var(--primary-red)"></i>
                Eroare la conectarea cu serverul Python. Asigură-te că API-ul rulează!
            </div>`;
    }
}

// Render Feed Posts into container
function renderFeed(posts) {
    feedPostsContainer.innerHTML = '';
    
    if (posts.length === 0) {
        feedPostsContainer.innerHTML = '<p class="section-desc">Nu există postări disponibile.</p>';
        return;
    }
    
    posts.forEach(post => {
        const card = document.createElement('div');
        card.className = 'card-wrapper';
        card.id = `card-${post.id}`;
        
        // Add score badge
        card.innerHTML = `
            <div class="score-badge" title="Scor de trend calculat cu Time Decay">
                <i class="fa-solid fa-fire-flame-curved"></i> Scor: <span class="score-val">${post.current_score.toFixed(1)}</span>
            </div>
        `;
        
        if (currentPlatform === 'facebook') {
            card.innerHTML += `
                <div class="fb-post">
                    <div class="fb-post-header">
                        <div class="fb-avatar">${post.category.substring(0,2).toUpperCase()}</div>
                        <div class="fb-meta">
                            <h4>Niche Specialist: ${post.category}</h4>
                            <span>Postat recent</span>
                        </div>
                    </div>
                    <div class="fb-post-body">
                        <h3 class="fb-post-title">${post.title}</h3>
                        <p class="fb-post-desc">${post.description}</p>
                        <div class="fb-post-tags">
                            ${post.tags.map(t => `<a href="#" class="tag-btn">#${t}</a>`).join('')}
                        </div>
                        <img src="${post.image_url}" alt="${post.title}" class="fb-post-image">
                    </div>
                    <div class="fb-post-stats">
                        <span><i class="fa-solid fa-thumbs-up"></i> <span class="likes-count">${post.likes}</span> aprecieri</span>
                        <span>${post.views} vizualizări • ${post.shares} distribuiri</span>
                    </div>
                    <div class="fb-actions">
                        <button class="action-btn btn-like" onclick="interact('${post.id}', 'like')">
                            <i class="fa-regular fa-thumbs-up"></i> Like
                        </button>
                        <button class="action-btn" onclick="interact('${post.id}', 'share')">
                            <i class="fa-solid fa-share"></i> Share
                        </button>
                    </div>
                </div>
            `;
        } else {
            // Pinterest Card
            card.innerHTML += `
                <div class="pin-post">
                    <div class="pin-img-container">
                        <img src="${post.image_url}" alt="${post.title}" class="pin-image">
                        <div class="pin-overlay">
                            <button class="btn-pin-save" onclick="interact('${post.id}', 'save')">
                                <i class="fa-solid fa-thumbtack"></i> Salvează
                            </button>
                            <div class="pin-overlay-bottom">
                                <div class="pin-overlay-stats">
                                    <span><i class="fa-solid fa-thumbtack"></i> ${post.shares}</span>
                                    <span><i class="fa-solid fa-heart"></i> ${post.likes}</span>
                                </div>
                                <button class="btn-pin-like-overlay" onclick="interact('${post.id}', 'like')" title="Apreciază pin">
                                    <i class="fa-solid fa-heart"></i>
                                </button>
                            </div>
                        </div>
                    </div>
                    <div class="pin-details">
                        <span class="pin-category">${post.category}</span>
                        <h3 class="pin-title">${post.title}</h3>
                        <p class="pin-desc">${post.description}</p>
                    </div>
                </div>
            `;
        }
        
        // Setup Hover view simulation (simulates looking at a post for more than 1.5 seconds)
        card.addEventListener('mouseenter', () => {
            hoverTimers[post.id] = setTimeout(() => {
                registerView(post.id);
            }, 1500); // 1.5 seconds hover = view registered
        });
        
        card.addEventListener('mouseleave', () => {
            if (hoverTimers[post.id]) {
                clearTimeout(hoverTimers[post.id]);
                delete hoverTimers[post.id];
            }
        });
        
        feedPostsContainer.appendChild(card);
    });
}

// Fetch Trend Analytics
async function fetchTrends() {
    let platformForTrends = 'facebook';
    if (currentPlatform === 'pinterest') {
        platformForTrends = 'pinterest';
    } else if (currentPlatform === 'my-facebook') {
        platformForTrends = 'facebook';
    } else if (currentPlatform === 'my-instagram') {
        platformForTrends = 'facebook';
    } else if (currentPlatform === 'my-reddit') {
        platformForTrends = 'facebook';
    }
    
    try {
        const response = await fetch(`/api/trends?platform=${platformForTrends}`);
        if (!response.ok) throw new Error("Eroare la preluarea trendurilor.");
        const trends = await response.json();
        renderTrends(trends);
    } catch (error) {
        console.error("Trends error:", error);
    }
}

// Render Trends Graph Progress Bars
function renderTrends(trends) {
    trendsListContainer.innerHTML = '';
    
    if (trends.length === 0) {
        trendsListContainer.innerHTML = '<p class="section-desc">Nicio activitate încă.</p>';
        return;
    }
    
    // Find max score for relative percentage sizing
    const maxScore = Math.max(...trends.map(t => t.score), 10.0); // min divisor of 10.0 to prevent overflow stretch
    
    trends.forEach(trend => {
        const percentage = Math.min((trend.score / maxScore) * 100, 100);
        const barClass = currentPlatform === 'pinterest' ? 'pinterest-bar' : 'facebook-bar';
        
        const item = document.createElement('div');
        item.className = 'trend-item';
        item.innerHTML = `
            <div class="trend-info">
                <span class="trend-name">${trend.category}</span>
                <span class="trend-value">${trend.score.toFixed(1)} pct</span>
            </div>
            <div class="trend-bar-bg">
                <div class="trend-bar-fill ${barClass}" style="width: ${percentage}%"></div>
            </div>
        `;
        
        trendsListContainer.appendChild(item);
    });
}

// Update Simulated Time display in Sidebar
async function updateTimeDisplay() {
    try {
        const response = await fetch('/api/simulate/time');
        const data = await response.json();
        
        const date = new Date(data.current_time * 1000);
        // Format date nicely (HH:MM:SS)
        const timeStr = date.toLocaleTimeString('ro-RO', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
        
        if (data.virtual_offset > 0) {
            const offsetMins = Math.round(data.virtual_offset / 60);
            simulatedTimeDisplay.innerHTML = `${timeStr} <span style="color: var(--primary-red)">(+${offsetMins} min simulate)</span>`;
        } else {
            simulatedTimeDisplay.innerHTML = `${timeStr} <span style="color: var(--text-muted)">(Timp Real)</span>`;
        }
    } catch (error) {
        simulatedTimeDisplay.textContent = "Deconectat";
    }
}

// ==========================================
// ACTIONS AND INTERACTIONS
// ==========================================

// Register Interaction (Like / Share / Save)
async function interact(postId, interactionType) {
    try {
        const card = document.getElementById(`card-${postId}`);
        if (card) {
            // UI Visual Feedback
            card.classList.add('pulse-score-up');
            setTimeout(() => card.classList.remove('pulse-score-up'), 500);
            
            // If it was a like, toggle UI active state locally first
            if (interactionType === 'like') {
                const btn = card.querySelector('.btn-like');
                if (btn) btn.classList.add('btn-like-active');
                const btnOverlay = card.querySelector('.btn-pin-like-overlay');
                if (btnOverlay) btnOverlay.classList.add('active');
            }
        }
        
        const response = await fetch('/api/interact', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ post_id: postId, interaction_type: interactionType })
        });
        
        if (!response.ok) throw new Error("A eșuat înregistrarea interacțiunii.");
        
        const updatedPost = await response.json();
        
        // Dynamic logging in AI Thought console
        logAIThought(`[Eveniment] Inregistrat ${interactionType.toUpperCase()} pe postarea ${postId}.\n[Algoritm] Noul scor calculat: ${updatedPost.current_score.toFixed(1)}`);
        
        // Refresh trends and feed to display new scores
        fetchTrends();
        
        // Fast update stats on card directly without full re-render
        if (card) {
            const scoreVal = card.querySelector('.score-val');
            if (scoreVal) scoreVal.textContent = updatedPost.current_score.toFixed(1);
            
            if (currentPlatform === 'facebook') {
                const likesCount = card.querySelector('.likes-count');
                if (likesCount) likesCount.textContent = updatedPost.likes;
            } else {
                // Update Pinterest saves/likes display
                const overlayStats = card.querySelector('.pin-overlay-stats');
                if (overlayStats) {
                    overlayStats.innerHTML = `
                        <span><i class="fa-solid fa-thumbtack"></i> ${updatedPost.shares}</span>
                        <span><i class="fa-solid fa-heart"></i> ${updatedPost.likes}</span>
                    `;
                }
            }
        }
    } catch (error) {
        console.error(error);
    }
}

// Register passive View (automatically on hover)
async function registerView(postId) {
    try {
        const response = await fetch('/api/interact', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ post_id: postId, interaction_type: 'view' })
        });
        
        if (response.ok) {
            const updatedPost = await response.json();
            logAIThought(`[Passive View] Utilizatorul citește postarea ${postId}.\n[Algoritm] Scorul a crescut la: ${updatedPost.current_score.toFixed(1)}`);
            fetchTrends();
            
            // Update score badge on screen
            const card = document.getElementById(`card-${postId}`);
            if (card) {
                const scoreVal = card.querySelector('.score-val');
                if (scoreVal) scoreVal.textContent = updatedPost.current_score.toFixed(1);
            }
        }
    } catch (e) {
        console.error(e);
    }
}

// Advance Simulation Time
async function advanceTime(seconds) {
    try {
        const response = await fetch(`/api/simulate/advance?seconds=${seconds}`, {
            method: 'POST'
        });
        const data = await response.json();
        
        logAIThought(`[Simulare] Timpul a fost devansat cu ${seconds / 60} minute.\n[Decay] Se calculează deprecierea scorurilor...`);
        
        refreshAll();
    } catch (error) {
        console.error(error);
    }
}

// Reset Simulation
async function resetSimulation() {
    try {
        const response = await fetch('/api/simulate/reset', { method: 'POST' });
        const data = await response.json();
        
        logAIThought("[Sistem] Simularea a fost resetată la starea inițială.");
        
        // Clear chat area except welcome msg
        chatMessagesContainer.innerHTML = `
            <div class="chat-message bot">
                <div class="message-bubble">
                    Simularea a fost resetată. Te rog să interacționezi cu feed-ul pentru a porni algoritmul!
                </div>
            </div>`;
        
        refreshAll();
    } catch (error) {
        console.error(error);
    }
}

// ==========================================
// CHAT FUNCTIONALITY
// ==========================================

async function handleChatSubmit(e) {
    e.preventDefault();
    const query = chatInputField.value.trim();
    if (!query) return;
    
    // Append User Message to UI
    appendChatMessage('user', query);
    chatInputField.value = '';
    
    // Show bot typing placeholder
    const typingBubble = document.createElement('div');
    typingBubble.className = 'chat-message bot typing';
    typingBubble.innerHTML = '<div class="message-bubble"><i class="fa-solid fa-ellipsis fa-bounce"></i> Agentul analizează...</div>';
    chatMessagesContainer.appendChild(typingBubble);
    chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight;
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: query })
        });
        
        typingBubble.remove(); // Remove placeholder
        
        if (!response.ok) throw new Error("A eșuat comunicarea cu Agentul AI.");
        const data = await response.json();
        
        // Append Bot Response
        appendChatMessage('bot', data.response);
        
        // Update Cognitive Log
        if (data.analysis) {
            logAIThought(data.analysis);
        }
    } catch (error) {
        typingBubble.remove();
        appendChatMessage('bot', `Scuze, a apărut o problemă la generarea răspunsului: ${error.message}`);
    }
}

function appendChatMessage(sender, text) {
    const msg = document.createElement('div');
    msg.className = `chat-message ${sender}`;
    msg.innerHTML = `<div class="message-bubble">${text}</div>`;
    chatMessagesContainer.appendChild(msg);
    chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight;
}

// Log thoughts inside terminal window
function logAIThought(thought) {
    aiThoughtLog.textContent = thought;
    aiThoughtLog.scrollTop = aiThoughtLog.scrollHeight;
}

// Auto-trigger Audit chat query for specific platform
function autoTriggerAuditChat(platform) {
    const platformLabel = platform === 'facebook' ? 'Facebook' : platform === 'instagram' ? 'Instagram' : 'Reddit';
    
    // Check if audit was already run recently to avoid duplicate triggers
    const lastMsg = chatMessagesContainer.lastElementChild;
    if (lastMsg && lastMsg.textContent.includes(`Audit AI Profil ${platformLabel}`)) return;
    
    appendChatMessage('user', `Rulează un audit AI pe contul meu de ${platformLabel}.`);
    
    // Typing placeholder
    const typingBubble = document.createElement('div');
    typingBubble.className = 'chat-message bot typing';
    typingBubble.innerHTML = `<div class="message-bubble"><i class="fa-solid fa-ellipsis fa-bounce"></i> Agentul analizează profilul de ${platformLabel}...</div>`;
    chatMessagesContainer.appendChild(typingBubble);
    chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight;
    
    setTimeout(async () => {
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: `audit ${platform}` })
            });
            typingBubble.remove();
            if (response.ok) {
                const data = await response.json();
                appendChatMessage('bot', data.response);
                if (data.analysis) logAIThought(data.analysis);
            }
        } catch (e) {
            typingBubble.remove();
            console.error(e);
        }
    }, 1000);
}

// Fetch My Single Profile Statistics
async function fetchMySingleProfile(platform) {
    try {
        feedPostsContainer.innerHTML = `
            <div class="loading-spinner">
                <i class="fa-solid fa-circle-notch fa-spin"></i> Se încarcă datele pentru ${platform === 'my-facebook' ? 'Facebook' : platform === 'my-instagram' ? 'Instagram' : 'Reddit'}...
            </div>`;
            
        const response = await fetch('/api/my-profiles');
        if (!response.ok) throw new Error("A eșuat încărcarea profilelor.");
        const data = await response.json();
        
        if (platform === 'my-facebook') {
            renderMyFacebookProfile(data.facebook);
        } else if (platform === 'my-instagram') {
            renderMyInstagramProfile(data.instagram);
        } else if (platform === 'my-reddit') {
            renderMyRedditProfile(data.reddit);
        }
    } catch (error) {
        console.error(error);
        feedPostsContainer.innerHTML = `
            <div class="loading-spinner">
                <i class="fa-solid fa-triangle-exclamation" style="color: var(--primary-red)"></i>
                Eroare la preluarea statisticilor de pe serverul Python.
            </div>`;
    }
}

// Render My Facebook Profile
function renderMyFacebookProfile(data) {
    feedPostsContainer.innerHTML = '';
    
    // Create Header Card
    const headerCard = document.createElement('div');
    headerCard.className = 'profile-header-card fb-theme';
    headerCard.innerHTML = `
        <div class="profile-header-top">
            <img class="profile-avatar fb-avatar-glow" src="assets/fb_profile.png" alt="${data.name}">
            <div class="profile-meta-info">
                <h2>${data.name}</h2>
                <a href="${data.url}" target="_blank">@${data.username} <i class="fa-solid fa-external-link"></i></a>
            </div>
        </div>
        <div class="profile-stats-grid">
            <div class="profile-stat-box">
                <span class="stat-num">${data.followers}</span>
                <span class="stat-lbl">Prieteni</span>
            </div>
            <div class="profile-stat-box">
                <span class="stat-num">${data.posts_count}</span>
                <span class="stat-lbl">Postări</span>
            </div>
            <div class="profile-stat-box">
                <span class="stat-num">${data.avg_engagement}%</span>
                <span class="stat-lbl">Engagement Mediu</span>
            </div>
        </div>
    `;
    feedPostsContainer.appendChild(headerCard);
    
    // Create AI recommendation box
    const recommendBox = document.createElement('div');
    recommendBox.className = 'ai-recommendation-box fb-border';
    recommendBox.innerHTML = `
        <div class="ai-box-header">
            <i class="fa-solid fa-robot"></i>
            <h4>Recomandare AI Agent</h4>
        </div>
        <p>Postările tale cu fotografii (cum sunt cele din Parcul Romanescu) obțin cel mai ridicat interes. Algoritmul îți recomandă să crești rata postărilor originale în detrimentul distribuirilor simple de link-uri politice, pentru a menține engagement-ul la o rată ridicată.</p>
    `;
    feedPostsContainer.appendChild(recommendBox);
    
    // Create Recent Posts Feed
    const postsSection = document.createElement('div');
    postsSection.className = 'profile-activity-section';
    postsSection.innerHTML = `<h3>Postări Recente</h3>`;
    
    const activityList = document.createElement('div');
    activityList.className = 'profile-posts-list';
    
    data.recent_activity.forEach(act => {
        const item = document.createElement('div');
        item.className = 'profile-post-card';
        item.innerHTML = `
            <div class="p-post-header" style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                <img src="assets/fb_profile.png" alt="Mihnea Pițur" style="width: 36px; height: 36px; border-radius: 50%; object-fit: cover; border: 1px solid rgba(255,255,255,0.1);">
                <div style="display: flex; flex-direction: column;">
                    <span style="font-weight: 600; font-size: 0.88rem; color: var(--text-primary);">Mihnea Pițur</span>
                    <span class="p-post-date">${act.date}</span>
                </div>
            </div>
            <div class="p-post-body">
                <p>${act.title}</p>
            </div>
            <div class="p-post-footer">
                <div class="p-post-stats">
                    <span><i class="fa-regular fa-eye"></i> ${act.views} vizualizări</span>
                    <span><i class="fa-regular fa-thumbs-up"></i> ${act.likes}</span>
                    <span><i class="fa-solid fa-share"></i> ${act.shares}</span>
                </div>
                <button class="p-post-action-btn fb-btn" onclick="askAIPostAnalysis('Facebook', '${act.title.replace(/'/g, "\\'")}')">
                    <i class="fa-solid fa-wand-magic-sparkles"></i> Analizează cu AI
                </button>
            </div>
        `;
        activityList.appendChild(item);
    });
    
    postsSection.appendChild(activityList);
    feedPostsContainer.appendChild(postsSection);
}

// Render My Instagram Profile
function renderMyInstagramProfile(data) {
    feedPostsContainer.innerHTML = '';
    
    // Create Header Card
    const headerCard = document.createElement('div');
    headerCard.className = 'profile-header-card ig-theme';
    headerCard.innerHTML = `
        <div class="profile-header-top">
            <img class="profile-avatar ig-avatar-glow" src="assets/ig_profile.png" alt="${data.name}">
            <div class="profile-meta-info">
                <h2>${data.name}</h2>
                <a href="${data.url}" target="_blank">@${data.username} <i class="fa-solid fa-external-link"></i></a>
            </div>
        </div>
        <div class="profile-stats-grid">
            <div class="profile-stat-box">
                <span class="stat-num">${data.followers}</span>
                <span class="stat-lbl">Urmăritori</span>
            </div>
            <div class="profile-stat-box">
                <span class="stat-num">${data.posts_count}</span>
                <span class="stat-lbl">Postări</span>
            </div>
            <div class="profile-stat-box">
                <span class="stat-num">${data.avg_engagement}%</span>
                <span class="stat-lbl">Engagement Mediu</span>
            </div>
        </div>
    `;
    feedPostsContainer.appendChild(headerCard);
    
    // Create AI recommendation box
    const recommendBox = document.createElement('div');
    recommendBox.className = 'ai-recommendation-box ig-border';
    recommendBox.innerHTML = `
        <div class="ai-box-header">
            <i class="fa-solid fa-robot"></i>
            <h4>Recomandare AI Agent</h4>
        </div>
        <p>Rata ta de engagement de 12.4% este extraordinară! Comunitatea ta (cum sunt colegii de la Automatică Craiova) reacționează excepțional la momentele din viața de student. Se recomandă postarea de conținut video scurt (Reels) despre viața studențească și proiectele tale.</p>
    `;
    feedPostsContainer.appendChild(recommendBox);
    
    // Create Recent Posts Feed
    const postsSection = document.createElement('div');
    postsSection.className = 'profile-activity-section';
    postsSection.innerHTML = `<h3>Postări Recente</h3>`;
    
    const activityList = document.createElement('div');
    activityList.className = 'profile-posts-list';
    
    data.recent_activity.forEach(act => {
        const item = document.createElement('div');
        item.className = 'profile-post-card';
        item.innerHTML = `
            <div class="p-post-header" style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                <img src="assets/ig_profile.png" alt="Mihnea Pițur" style="width: 36px; height: 36px; border-radius: 50%; object-fit: cover; border: 1px solid rgba(255,255,255,0.1);">
                <div style="display: flex; flex-direction: column;">
                    <span style="font-weight: 600; font-size: 0.88rem; color: var(--text-primary);">Mihnea Pițur</span>
                    <span class="p-post-date">${act.date}</span>
                </div>
            </div>
            <div class="p-post-body">
                <p>${act.caption}</p>
            </div>
            <div class="p-post-footer">
                <div class="p-post-stats">
                    <span><i class="fa-regular fa-eye"></i> ${act.views} vizualizări</span>
                    <span><i class="fa-regular fa-heart"></i> ${act.likes}</span>
                    <span><i class="fa-solid fa-reply"></i> ${act.shares}</span>
                </div>
                <button class="p-post-action-btn ig-btn" onclick="askAIPostAnalysis('Instagram', '${act.caption.replace(/'/g, "\\'")}')">
                    <i class="fa-solid fa-wand-magic-sparkles"></i> Analizează cu AI
                </button>
            </div>
        `;
        activityList.appendChild(item);
    });
    
    postsSection.appendChild(activityList);
    feedPostsContainer.appendChild(postsSection);
}

// Render My Reddit Profile
function renderMyRedditProfile(data) {
    feedPostsContainer.innerHTML = '';
    
    // Create Header Card
    const headerCard = document.createElement('div');
    headerCard.className = 'profile-header-card rd-theme';
    headerCard.innerHTML = `
        <div class="profile-header-top">
            <img class="profile-avatar rd-avatar-glow" src="assets/rd_profile.svg" alt="u/${data.name}">
            <div class="profile-meta-info">
                <h2>u/${data.name}</h2>
                <a href="${data.url}" target="_blank">u/${data.username} <i class="fa-solid fa-external-link"></i></a>
            </div>
        </div>
        <div class="profile-stats-grid">
            <div class="profile-stat-box">
                <span class="stat-num">${data.karma}</span>
                <span class="stat-lbl">Total Karma</span>
            </div>
            <div class="profile-stat-box">
                <span class="stat-num">${data.post_karma}</span>
                <span class="stat-lbl">Post Karma</span>
            </div>
            <div class="profile-stat-box">
                <span class="stat-num">${data.comment_karma}</span>
                <span class="stat-lbl">Comment Karma</span>
            </div>
        </div>
    `;
    feedPostsContainer.appendChild(headerCard);
    
    // Create AI recommendation box
    const recommendBox = document.createElement('div');
    recommendBox.className = 'ai-recommendation-box rd-border';
    recommendBox.innerHTML = `
        <div class="ai-box-header">
            <i class="fa-solid fa-robot"></i>
            <h4>Recomandare AI Agent</h4>
        </div>
        <p>Ești văzut ca un membru de încredere în r/Craiova și r/UniRO. Discuțiile despre situația profesorilor de la Automatică Craiova și subiectele de utilitate publică locală au înregistrat cele mai multe voturi. Continuă să aduci clarificări argumentate.</p>
    `;
    feedPostsContainer.appendChild(recommendBox);
    
    // Create Recent Posts Feed
    const postsSection = document.createElement('div');
    postsSection.className = 'profile-activity-section';
    postsSection.innerHTML = `<h3>Contribuții Recente</h3>`;
    
    const activityList = document.createElement('div');
    activityList.className = 'profile-posts-list';
    
    data.recent_activity.forEach(act => {
        const item = document.createElement('div');
        item.className = 'profile-post-card';
        item.innerHTML = `
            <div class="p-post-header" style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                <img src="assets/rd_profile.svg" alt="u/Potential-Shirt-7063" style="width: 36px; height: 36px; border-radius: 50%; object-fit: cover; border: 1px solid rgba(255,255,255,0.1);">
                <div style="display: flex; flex-direction: column;">
                    <span style="font-weight: 600; font-size: 0.88rem; color: var(--text-primary);">u/Potential-Shirt-7063</span>
                    <span class="p-reddit-subreddit">r/${act.subreddit.replace('r/', '')}</span>
                </div>
            </div>
            <div class="p-post-body">
                <p style="font-weight: 600; font-size: 0.95rem;">${act.title}</p>
            </div>
            <div class="p-post-footer">
                <div class="p-post-stats">
                    <span><i class="fa-solid fa-arrow-up"></i> ${act.upvotes} upvotes</span>
                    <span><i class="fa-solid fa-comment"></i> ${act.comments} comentarii</span>
                </div>
                <button class="p-post-action-btn rd-btn" onclick="askAIPostAnalysis('Reddit', '${act.title.replace(/'/g, "\\'")}')">
                    <i class="fa-solid fa-wand-magic-sparkles"></i> Analizează cu AI
                </button>
            </div>
        `;
        activityList.appendChild(item);
    });
    
    postsSection.appendChild(activityList);
    feedPostsContainer.appendChild(postsSection);
}

// Global helper for Post Analysis through AI Chat
function askAIPostAnalysis(platform, postTitle) {
    chatInputField.value = `Analizează postarea de pe ${platform}: "${postTitle}"`;
    // Dispatch submit event to form
    const event = new Event('submit', { cancelable: true });
    chatInputForm.dispatchEvent(event);
}
