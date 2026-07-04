import os
import re
from typing import Tuple, Optional
from app.algorithm import TrendAlgorithm

try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

class AIAgent:
    def __init__(self, algorithm: TrendAlgorithm):
        self.algo = algorithm
        self.chat_history = []
        self.use_gemini = False
        self.model_name = None
        
        api_key = os.environ.get("GEMINI_API_KEY")
        if HAS_GENAI and api_key:
            try:
                genai.configure(api_key=api_key)
                
                # 1. Attempt dynamic model discovery via API
                discovered_models = []
                try:
                    for m in genai.list_models():
                        if 'generateContent' in m.supported_generation_methods:
                            # Strip the 'models/' prefix if present
                            name = m.name.replace('models/', '')
                            discovered_models.append(name)
                    print(f"Modele descoperite dinamic prin API: {discovered_models}")
                except Exception as list_err:
                    print(f"Avertisment: Nu s-a putut apela list_models ({list_err}). Folosim lista implicită.")
                
                # 2. Combine discovered models with hardcoded fallbacks
                candidate_models = discovered_models + [
                    'gemini-1.5-flash',
                    'gemini-1.5-flash-latest',
                    'gemini-1.5-pro',
                    'gemini-1.5-pro-latest',
                    'gemini-pro'
                ]
                
                # Deduplicate while preserving order
                seen = set()
                candidate_models = [x for x in candidate_models if not (x in seen or seen.add(x))]
                
                # 3. Test candidates and select the first active model
                print("Se testează compatibilitatea modelelor candidate...")
                for model_candidate in candidate_models:
                    try:
                        test_model = genai.GenerativeModel(model_candidate)
                        test_model.generate_content("Ping")
                        self.model = test_model
                        self.model_name = model_candidate
                        self.use_gemini = True
                        print(f"Gemini API configurat cu succes folosind modelul: {model_candidate}")
                        break
                    except Exception as test_err:
                        print(f"Modelul {model_candidate} nu a putut fi utilizat: {test_err}")
                
                if not self.use_gemini:
                    print("Eroare: Niciun model Gemini nu este compatibil cu această cheie API.")
                    
            except Exception as e:
                print(f"Eroare generală la configurarea Gemini API: {e}")

    def clear_chat_history(self):
        self.chat_history = []

    def _get_trends_summary(self, platform: str) -> str:
        trends = self.algo.get_trending_categories(platform)
        if not trends:
            return "nicio activitate înregistrată"
        return ", ".join([f"{t['category']} (scor {t['score']})" for t in trends])

    def respond_to_user(self, user_message: str) -> Tuple[str, str]:
        # Append user message to chat history
        self.chat_history.append({"role": "user", "message": user_message})
        
        current_time = self.algo.get_current_time()
        
        # Fetch current trend data for analysis
        fb_trends = self.algo.get_trending_categories("facebook")
        pin_trends = self.algo.get_trending_categories("pinterest")
        
        fb_posts = self.algo.get_posts_with_scores("facebook")
        pin_posts = self.algo.get_posts_with_scores("pinterest")
        
        all_posts = fb_posts + pin_posts
        all_posts.sort(key=lambda x: x["current_score"], reverse=True)
        
        total_interactions = len(self.algo.interactions)
        recent_interactions = [i for i in self.algo.interactions if current_time - i["timestamp"] < 300] # last 5 min
        
        # Try using Gemini if configured
        if self.use_gemini:
            try:
                # Format current state details
                fb_trends_txt = ", ".join([f"{t['category']} (scor {round(t['score'], 2)})" for t in fb_trends]) if fb_trends else "fără trenduri active"
                pin_trends_txt = ", ".join([f"{t['category']} (scor {round(t['score'], 2)})" for t in pin_trends]) if pin_trends else "fără trenduri active"
                
                posts_list_txt = ""
                for p in all_posts[:8]:
                    posts_list_txt += f"- [{p['platform'].upper()}] '{p['title']}' (Categorie: {p['category']}, Scor: {round(p['current_score'], 2)}, Like-uri: {p['likes']}, Share-uri: {p.get('shares', 0) or p.get('repins', 0)})\n"
                
                # Construct System Prompt
                system_prompt = (
                    "Ești TrendAgent AI, un asistent inteligent de Social Media Analytics creat pentru Mihnea Pițur (un student pasionat de programare, suporter înrăit Universitatea Craiova).\n\n"
                    "Profilurile lui Mihnea:\n"
                    "1. Facebook (Mihnea Pițur): 363 prieteni, 736 postări, 4.8% engagement. Postări recente despre educație, evaluare națională, opinii sociale.\n"
                    "2. Instagram (@jesuismihnea): 262 urmăritori, 66 postări, 12.4% engagement excepțional! Postări de la discursuri la Universitatea din Craiova (cu slide-uri despre Craiova Maxima) și poezie.\n"
                    "3. Reddit (u/Potential-Shirt-7063): 2022 Karma (852 post karma, 1170 comment karma), foarte activ pe r/Craiova și r/UniRO (discuții utile locale sau despre restanțe/profesori la Automatică Craiova).\n\n"
                    "Datele în timp real din aplicație (dashboard):\n"
                    f"- Coeficientul Time Decay (atenuare temporală): λ={self.algo.decay_rate}\n"
                    f"- Timpul simulat curent: {round(current_time, 1)} secunde (offset: {self.algo.virtual_time_offset} secunde)\n"
                    f"- Categoriile în trend pe Facebook: {fb_trends_txt}\n"
                    f"- Categoriile în trend pe Pinterest: {pin_trends_txt}\n"
                    f"- Postările curente cu scorurile lor în timp real:\n{posts_list_txt}\n\n"
                    "Instrucțiuni de comportament:\n"
                    "1. Răspunde prietenos și profesional în limba română (folosește emoticoane, ton cald).\n"
                    "2. Dacă ești întrebat despre profilele utilizatorului, folosește exclusiv datele de mai sus (363 prieteni, 2022 Reddit karma etc.).\n"
                    "3. Răspunsul tău TREBUIE să fie compus din două părți separate EXACT prin delimitatorul '===ANALYSIS===':\n"
                    "   - Partea 1: Răspunsul conversațional adresat utilizatorului (utilizează formatare Markdown frumoasă).\n"
                    "   - Partea 2: Analiza tehnică internă a agentului (care va apărea în consola din dreapta). Scrie-o concis, sub formă de log de sistem.\n"
                    "Exemplu format:\n"
                    "Salut Mihnea! ...\n"
                    "===ANALYSIS===\n"
                    "- Total interacțiuni procesate: 14\n"
                    "- Analiză: ..."
                )
                
                # Format history context
                history_context = "Istoric conversație:\n"
                for h in self.chat_history[-6:-1]: # exclude the user message we just appended
                    role = "Utilizator" if h["role"] == "user" else "TrendAgent AI"
                    history_context += f"{role}: {h['message']}\n"
                
                history_context += f"Utilizator: {user_message}\nTrendAgent AI:"
                
                full_prompt = f"{system_prompt}\n\n{history_context}"
                
                response = self.model.generate_content(full_prompt)
                response_text = response.text
                
                if "===ANALYSIS===" in response_text:
                    parts = response_text.split("===ANALYSIS===")
                    gemini_response = parts[0].strip()
                    gemini_analysis = parts[1].strip()
                else:
                    gemini_response = response_text.strip()
                    gemini_analysis = (
                        f"[AI Process] Scanare bază de date finalizată la t={round(current_time, 1)}.\n"
                        f"- Analiză efectuată prin modelul {self.model_name} (succes)."
                    )
                
                # Save agent response to history
                self.chat_history.append({"role": "agent", "message": gemini_response})
                return gemini_response, gemini_analysis
                
            except Exception as e:
                print(f"Gemini API Execution Error: {e}. Falling back to rule-based agent.")
        
        # Fallback to local rule-based response
        return self._respond_rule_based(
            user_message, current_time, fb_trends, pin_trends, fb_posts, pin_posts, all_posts, total_interactions, recent_interactions
        )

    def _respond_rule_based(self, user_message: str, current_time: float, fb_trends, pin_trends, fb_posts, pin_posts, all_posts, total_interactions, recent_interactions) -> Tuple[str, str]:
        msg = user_message.lower().strip()
        
        analysis = (
            f"[AI Process] Scanare bază de date finalizată la t={round(current_time, 1)}.\n"
            f"- Total interacțiuni în istoric: {total_interactions}\n"
            f"- Activitate recentă (ultimele 5 min simulate): {len(recent_interactions)} evenimente.\n"
            f"- Coeficient curent de atenuare temporală (Time Decay): λ={self.algo.decay_rate}\n"
        )
        
        if all_posts:
            top_post = all_posts[0]
            analysis += f"- Postarea lider în acest moment: '{top_post['title']}' pe {top_post['platform'].capitalize()} cu un scor de {top_post['current_score']}.\n"
        
        # Generate conversational response
        response = ""
        
        # GREETINGS
        if any(greet in msg for greet in ["salut", "buna", "hello", "hei", "salutare"]):
            response = (
                "Salut! Sunt asistentul tău AI pentru analiza trendurilor. "
                "Te pot ajuta să identifici ce subiecte sunt populare acum pe Facebook și Pinterest, "
                "să analizez performanța postărilor sau să îți ofer recomandări de conținut. "
                "Despre ce platformă dorești să vorbim?"
            )
            analysis += "-> Răspuns de întâmpinare generat."
            
        # WHO ARE YOU
        elif any(x in msg for x in ["cine esti", "ce poti sa faci", "scopul tau"]):
            response = (
                "Sunt un Agent AI specializat în Social Media Analytics. "
                "Monitorizez în timp real vizualizările, aprecierile și distribuirile utilizatorilor. "
                "Folosesc un algoritm de atenuare temporală (Time Decay) pentru a diferenția trendurile trecătoare "
                "de interesele stabile ale utilizatorilor și îți pot oferi recomandări de marketing personalizate."
            )
            analysis += "-> Explicare funcționalitate agent."

        # USER'S SOCIAL MEDIA ACCOUNTS (MIHNEA)
        elif any(x in msg for x in ["mihnea", "conturile mele", "profilul meu", "profilele mele", "reddit", "instagram", "facebook", "fb", "insta", "ig", "statisticile mele", "statistici", "audit"]):
            # Check if specific platform is requested
            if any(fb in msg for fb in ["facebook", "fb"]):
                response = (
                    "📊 **Audit AI Profil Facebook (Mihnea Pițur)**\n\n"
                    "• **Audiență**: Ai 363 de prieteni / urmăritori reali.\n"
                    "• **Activitate**: Un volum remarcabil de 736 de postări.\n"
                    "• **Engagement mediu**: 4.8% (o rată de interacțiune solidă pentru un profil personal).\n\n"
                    "🔍 **Analiză conținut**:\n"
                    "Postările tale recente sunt compuse din text original profund și critic despre reacțiile presei și societății față de elevi (cum este opinia ta despre interviul Antena 1: *„Nu știu dacă ați urmărit faza virală de ieri...”*) și din distribuiri de analiză critică conexe (Carmen Dumitrescu și Sanda Din Obor) pe tema virală a evaluării naționale.\n\n"
                    "💡 **Recomandări strategice de la Agentul AI**:\n"
                    "1. **Opinie pe teme sociale virale**: Textul tău original lung critică dur lipsa promovării gândirii critice în educație, obținând 6 like-uri. Algoritmul Facebook favorizează postările cu text original profund pe teme sociale deoarece stimulează comentariile și discuțiile de calitate.\n"
                    "2. **Coerență tematică în distribuiri**: Faptul că ai distribuit două postări conexe (Carmen Dumitrescu și Sanda Din Obor) demonstrează că feed-ul tău susține o linie clară și argumentată pe subiectul analizat, întărindu-ți autoritatea pe acest domeniu."
                )
                analysis += "-> Rulare audit specific pentru profilul de Facebook al lui Mihnea."
            elif any(ig in msg for ig in ["instagram", "insta", "ig"]):
                response = (
                    "📸 **Audit AI Profil Instagram (@jesuismihnea)**\n\n"
                    "• **Audiență**: 262 de urmăritori loiali.\n"
                    "• **Activitate**: 66 de postări estetice.\n"
                    "• **Engagement mediu**: 12.4% (o rată de engagement extrem de ridicată, mult peste media industriei de ~2-3%!).\n\n"
                    "🔍 **Analiză conținut**:\n"
                    "Publicul tău reacționează excepțional la postări de mare impact emoțional și cultural. Postarea ta recentă cu versuri (*„Și luna-și ascunde răni / Peste orizont...”*) și o fotografie de la un discurs pe scena Universității din Craiova a înregistrat 42 de aprecieri reale și felicitări în comentarii.\n\n"
                    "💡 **Recomandări strategice de la Agentul AI**:\n"
                    "1. **Conținut la microfon (Public Speaking)**: Prezența ta pe scenă la Universitatea din Craiova, cu slide-uri despre „Suporter înrăit: Universitatea Craiova”, are reach excelent. Recomandăm încărcarea unor clipuri video scurte (Reels) din timpul acestor discursuri.\n"
                    "2. **Branding personal autentic**: Combinația dintre parcursul tău academic și postările cu tentă artistică/poetică îți oferă un profil unic cu o rată de loialitate a audienței de 12.4%. Păstrează acest mix!"
                )
                analysis += "-> Rulare audit specific pentru profilul de Instagram al lui Mihnea."
            elif any(rd in msg for rd in ["reddit", "rd"]):
                response = (
                    "🔴 **Audit AI Cont Reddit (u/Potential-Shirt-7063)**\n\n"
                    "• **Reputație**: 2,022 Karma totală (852 din postări, 1,170 din comentarii).\n"
                    "• **Activitate**: 688 de contribuții în comunități.\n"
                    "• **Rată de succes**: Postările pe subreddits locale au un impact puternic de nișă.\n\n"
                    "🔍 **Analiză conținut**:\n"
                    "Ești o prezență activă și extrem de utilă în comunitatea **r/Craiova** (sau r/UniRO, unde ai abordat situația profesorilor și a restanțelor de la Automatică Craiova).\n\n"
                    "💡 **Recomandări strategice de la Agentul AI**:\n"
                    "1. **Valoarea de utilitate publică**: Postarea din r/UniRO despre profesorul de la Automatică Craiova a adunat 112 upvotes și 47 de comentarii.\n"
                    "2. **Menține stilul informativ**: Răspunsurile tale argumentate la întrebările altor membri îți aduc în mod constant Comment Karma pozitiv."
                )
                analysis += "-> Rulare audit specific pentru contul de Reddit al lui Mihnea."
            else:
                response = (
                    "Am realizat un audit general al profilelor tale sociale, Mihnea:\n\n"
                    "🔵 **Facebook (Mihnea Pițur)**: 363 prieteni, 736 postări, 4.8% engagement.\n"
                    "📸 **Instagram (@jesuismihnea)**: 262 urmăritori, 66 postări, 12.4% engagement excepțional!\n"
                    "🔴 **Reddit (u/Potential-Shirt-7063)**: 2,022 Karma, 688 contribuții.\n\n"
                    "Selectează o platformă din sidebar pentru o analiză detaliată și recomandări specifice de conținut."
                )
                analysis += "-> Rulare audit AI general pe profilele personale."

        # TRENDS IN GENERAL OR PLATFORM SPECIFIC
        elif "trend" in msg or "popular" in msg or "top" in msg:
            if "facebook" in msg or "fb" in msg:
                summary = self._get_trends_summary("facebook")
                response = f"Pe **Facebook**, topul categoriilor în funcție de scorul recent este: {summary}. "
                if fb_posts:
                    response += f"\nCea mai activă postare este: **\"{fb_posts[0]['title']}\"** (Scor: {fb_posts[0]['current_score']})."
                analysis += "-> Interogare trenduri Facebook."
            elif "pinterest" in msg or "pin" in msg:
                summary = self._get_trends_summary("pinterest")
                response = f"Pe **Pinterest**, categoriile populare bazate pe salvări și vizualizări sunt: {summary}. "
                if pin_posts:
                    response += f"\nPin-ul de top este: **\"{pin_posts[0]['title']}\"** (Scor: {pin_posts[0]['current_score']})."
                analysis += "-> Interogare trenduri Pinterest."
            else:
                fb_summary = self._get_trends_summary("facebook")
                pin_summary = self._get_trends_summary("pinterest")
                response = (
                    f"Iată analiza globală a trendurilor în acest moment:\n\n"
                    f"🔵 **Facebook**: {fb_summary}\n"
                    f"🔴 **Pinterest**: {pin_summary}\n\n"
                    f"Observ o activitate generală mai intensă pe "
                    f"**{ 'Pinterest' if len(pin_posts) > 0 and pin_posts[0]['current_score'] > fb_posts[0]['current_score'] else 'Facebook' }**."
                )
                analysis += "-> Interogare trenduri generale ambele platforme."

        # RECOMMENDATIONS / WHAT TO POST
        elif "recomand" in msg or "ce sa postez" in msg or "idei" in msg or "continut" in msg:
            fb_best = fb_trends[0]["category"] if fb_trends else "Tehnologie"
            pin_best = pin_trends[0]["category"] if pin_trends else "Decor"
            
            response = (
                f"Pe baza activității recente a utilizatorilor, îți recomand următoarea strategie de conținut:\n\n"
                f"1. **Pentru Facebook**: Creează o postare pe nișa **{fb_best}**. Utilizatorii interacționează puternic cu acest tip de conținut recent. "
                f"Încearcă un format de tip discuție/întrebare pentru a stimula comentariile.\n"
                f"2. **Pentru Pinterest**: Nișa **{pin_best}** is în plină ascensiune. Pune accent pe imagini estetice cu rezoluție înaltă "
                f"și adaugă un ghid practic scurt în descriere.\n\n"
                f"Dacă dorești, te pot ajuta să scriem o schiță de postare pentru una dintre aceste categorii!"
            )
            analysis += f"-> Generare recomandări bazate pe categoriile lider: FB={fb_best}, PIN={pin_best}."

        # EXPLAIN A SPECIFIC CATEGORY TREND
        elif any(cat.lower() in msg for cat in ["diy", "tech", "tehnologie", "food", "gastronomie", "fashion", "moda", "decor", "japandi"]):
            matched_cat = None
            for cat in ["DIY", "Tech", "Food", "Fashion", "Decor"]:
                if cat.lower() in msg or (cat == "Tech" and "tehnologie" in msg) or (cat == "Food" and "gastronomie" in msg) or (cat == "Fashion" and "moda" in msg):
                    matched_cat = cat
                    break
            
            if matched_cat:
                cat_posts = [p for p in all_posts if p["category"] == matched_cat]
                total_score = sum([p["current_score"] for p in cat_posts])
                
                response = f" Categoria **{matched_cat}** are un scor total de trend de **{round(total_score, 2)}**. \n"
                if cat_posts:
                    response += "Această creștere este susținută în special de următoarele postări active:\n"
                    for p in cat_posts[:2]:
                        response += f"- **\"{p['title']}\"** (Scor recent: {p['current_score']} pe {p['platform'].capitalize()})\n"
                    response += "\nFiecare vizualizare aduce 1 punct, fiecare Like aduce 5 puncte, iar Distriburile/Salările aduc 10 puncte, ponderate cu vechimea lor."
                else:
                    response += "Momentan nu există postări active pe această nișă care să fi înregistrat interacțiuni recente."
                analysis += f"-> Analiză detaliată solicitată pentru categoria: {matched_cat}."
            else:
                response = "Nu am putut identifica exact categoria menționată. Încearcă să întrebi despre Tech, Food, Fashion, DIY sau Decor."
                analysis += "-> Categoria solicitată nu a fost recunoscută."

        # ANALIZEAZĂ POSTAREA INDIVIDUALĂ
        elif any(x in msg for x in ["analizeaza postarea", "analiză postare", "analizează postarea"]):
            title_match = re.search(r'["\'](.*?)["\']', user_message)
            if not title_match:
                title_match = re.search(r':\s*(.*)', user_message)
            title = title_match.group(1).strip() if title_match else "postarea selectată"
            
            response = (
                f"📊 **Analiză AI Individuală pentru postarea: \"{title}\"**\n\n"
                f"Această postare se încadrează în nișa ta principală de activitate și prezintă elemente puternice de organic reach.\n\n"
                f"• **Relevanță**: Foarte ridicată pentru publicul țintă.\n"
                f"• **Puncte tari**: Subiect autentic, local sau personal.\n"
                f"• **Sfat strategic**: Pentru a maximiza reach-ul organic, adaugă o întrebare deschisă la finalul descrierii."
            )
            analysis += f"-> Generat raport analiză postare individuală: '{title}'."

        # RESET OR SIMULATION
        elif "reset" in msg or "sterge" in msg:
            response = "Pentru a reseta simularea și istoricul chat-ului, te rog să folosești butonul dedicat din panoul de control din stânga."
            analysis += "-> Îndrumare către butonul de reset."

        # DEFAULT FALLBACK
        else:
            response = (
                "Interesantă întrebare! Ca Agent AI, îți pot spune că trendurile se schimbă rapid. "
                "În acest moment, cele mai populare categorii pe Pinterest sunt în zona de decor și modă, "
                "iar pe Facebook vedem interes pe tehnologie și gastronomie. "
                "Încearcă să pui o întrebare specifică, cum ar fi: 'ce recomandări ai?' sau 'ce este în trend pe Pinterest?'."
            )
            analysis += "-> Răspuns generic (fallback)."

        self.chat_history.append({"role": "agent", "message": response})
        return response, analysis
