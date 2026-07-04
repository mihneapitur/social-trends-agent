# Agent AI pentru Identificarea Trendurilor Social Media

Aceasta este o aplicație full-stack (Python + HTML/CSS/JS) dezvoltată ca proiect de practică (stagiu) de 3 săptămâni. Aplicația simulează interacțiunile utilizatorilor în timp real pe platformele **Facebook** și **Pinterest** și identifică trendurile folosind un algoritm matematic de **Time Decay (atenuare temporală)**, asistat de un **Agent AI** interactiv cu care se poate discuta în chat.

---

## Caracteristici Cheie
- **Arhitectură Full-Stack**: Backend robust în Python (FastAPI) și o interfață premium de frontend în HTML/CSS pur cu JavaScript.
- **Algoritm de Time Decay**: Punctajele se degradează în timp real pe măsură ce acțiunile devin mai vechi.
- **Simulator Temporal**: Permite controlarea timpului (grăbirea lui) din interfață pentru a vedea cum scad trendurile inactive.
- **Interfață Premium**: Design închis la culoare (Dark Mode) cu elemente de sticlă mată (glassmorphism), bare de progres luminate și efecte de pulsație la interacțiune.
- **Log de Raționament AI**: O mini-consolă în timp real care ilustrează procesul decizional și calculele matematice ale Agentului AI.
- **Chat Interactiv cu Agentul**: O secțiune în care utilizatorul poate pune întrebări despre ce este în trend și poate primi recomandări de marketing personalizate.

---

## Structura Proiectului
```
social-trends-agent/
├── app/
│   ├── __init__.py
│   ├── main.py          # Serverul FastAPI și definirea endpoint-urilor
│   ├── data.py          # Setul de postări inițiale mock
│   ├── algorithm.py     # Algoritmul de Time Decay
│   ├── agent.py         # Logica de analiză și răspuns a Agentului AI
│   └── models.py        # Modelele de validare a datelor (Pydantic)
├── static/
│   ├── index.html       # Interfața utilizator (Dashboard-ul principal)
│   ├── style.css        # Stilizarea premium (layout, culori, animații)
│   ├── script.js        # Logica de frontend (apeluri API și dinamism)
│   └── assets/          # Resursele vizuale pentru postările din feed
├── requirements.txt     # Dependențele Python necesare
└── README.md            # Ghidul de instalare și documentația
```

---

## Cum se Rulează Proiectul

### 1. Instalarea Dependențelor
Deschide terminalul în directorul proiectului și rulează:
```bash
pip install -r requirements.txt
```
*(Dacă folosești lansatorul standard de Python pe Windows, folosește `py -m pip install -r requirements.txt`)*

### 2. Pornirea Serverului Uvicorn
Rulează comanda următoare pentru a porni serverul local cu reîncărcare automată:
```bash
py -m uvicorn app.main:app --reload
```

### 3. Accesarea Aplicației
După ce serverul a pornit cu succes, deschide browserul preferat și accesează:
`http://127.0.0.1:8000`

---

## Detalii Tehnice: Algoritmul de Trenduri

Fiecare interacțiune a utilizatorului este trimisă la server și primește o greutate inițială:
- **Vizualizare (View)**: 1 punct
- **Apreciere (Like)**: 5 puncte
- **Distribuire / Salvare (Share/Save)**: 10 puncte

Scorul curent al unei postări la timpul $t$ este calculat pe baza tuturor acțiunilor înregistrate pentru acea postare, ponderate cu o funcție de atenuare exponențială:
$$Score(t) = \sum_{i} Weight_i \times e^{-\lambda (t - t_i)}$$

- $\lambda$ (decay rate) este setat implicit la `0.005` (ceea ce înseamnă că relevanța unei acțiuni scade la aproximativ 22% după 5 minute de inactivitate).
- Când avansezi timpul simulat (din sidebar), diferența $t - t_i$ crește artificial, scăzând rapid scorurile postărilor vechi dacă acestea nu primesc interacțiuni proaspete.
