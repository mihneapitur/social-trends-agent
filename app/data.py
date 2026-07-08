INITIAL_POSTS = [
    # FACEBOOK POSTS
    {
        "id": "fb_1",
        "platform": "facebook",
        "category": "Tech",
        "title": "Viitorul Inteligenței Artificiale în Viața De Zi Cu Zi",
        "description": "Cum vor schimba asistenții AI personali modul în care lucrăm, planificăm și comunicăm în următorul deceniu? Dezbateri interesante despre etică, productivitate și noile interfețe neuronale lansate recent. #AI #Technology #Future #SmartLiving",
        "image_url": "/assets/tech.jpg",
        "tags": ["AI", "Tech", "Future", "SmartLiving"],
        "likes": 120,
        "views": 450,
        "shares": 15
    },
    {
        "id": "fb_2",
        "platform": "facebook",
        "category": "Food",
        "title": "5 Secrete Pentru O Pizza Italiană Autentică La Tine Acasă",
        "description": "Secretele unui aluat perfect dospit timp de 48 de ore, temperatura ideală a cuptorului de casă și cum să alegi sosul de roșii San Marzano pentru o experiență napoletană adevărată. #Cooking #ItalianFood #Pizza #Recipe",
        "image_url": "/assets/cooking.jpg",
        "tags": ["Cooking", "ItalianFood", "Pizza", "Recipe"],
        "likes": 340,
        "views": 980,
        "shares": 45
    },
    {
        "id": "fb_3",
        "platform": "facebook",
        "category": "DIY",
        "title": "Ghid De Amenajare: Cum Să Îți Faci Un Birou Ergonomic Singur",
        "description": "Tutorial pas cu pas pentru construirea unui birou reglabil pe înălțime din materiale accesibile. Economisește sute de lei și scapă de durerile de spate cu acest proiect DIY de weekend. #DIY #Workspace #Ergonomics #HomeImprovement",
        "image_url": "/assets/diy.jpg",
        "tags": ["DIY", "Workspace", "Ergonomics", "HomeImprovement"],
        "likes": 85,
        "views": 320,
        "shares": 8
    },
    {
        "id": "fb_4",
        "platform": "facebook",
        "category": "Fashion",
        "title": "Trendurile Anului 2026: Întoarcerea La Minimalismul Sustenabil",
        "description": "De ce marile case de modă renunță la fast-fashion și adoptă materiale organice reciclabile. Află cum să îți construiești o garderobă capsulă stilată și ecologică. #Fashion #Sustainability #Minimalism #StyleTrends",
        "image_url": "/assets/fashion.jpg",
        "tags": ["Fashion", "Sustainability", "Minimalism", "StyleTrends"],
        "likes": 190,
        "views": 610,
        "shares": 22
    },

    # PINTEREST POSTS
    {
        "id": "pin_1",
        "platform": "pinterest",
        "category": "DIY",
        "title": "Idei Creative Pentru Organizarea Grădinii Verticale De Pe Balcon",
        "description": "Schițe și inspirație pentru a transforma un balcon mic într-o oază verde folosind paleți din lemn reciclați și ghivece suspendate inteligente. Perfect pentru plante aromatice proaspete! #VerticalGarden #BalconyDecor #Upcycling #UrbanJungle",
        "image_url": "/assets/diy.jpg",
        "tags": ["VerticalGarden", "BalconyDecor", "Upcycling", "UrbanJungle"],
        "likes": 42,
        "views": 1250,
        "shares": 310  # Pinterest saves count as shares here
    },
    {
        "id": "pin_2",
        "platform": "pinterest",
        "category": "Fashion",
        "title": "Outfits De Vară: Inspirație Stil Boem Și Culori Pământii",
        "description": "Combinații vestimentare vaporoase din in, accesorii din rafie și nuanțe de bej, teracotă și olive pentru un look relaxat de vară. Salvează pin-ul pentru inspirație zilnică. #BohoStyle #SummerOutfits #LinenLove #Aesthetic",
        "image_url": "/assets/fashion.jpg",
        "tags": ["BohoStyle", "SummerOutfits", "LinenLove", "Aesthetic"],
        "likes": 67,
        "views": 1820,
        "shares": 520
    },
    {
        "id": "pin_3",
        "platform": "pinterest",
        "category": "Decor",
        "title": "Amenajare Living Japandi: Echilibrul Dintre Nordic și Zen Japonez",
        "description": "Paletă cromatică neutră, mobilier minimalist din lemn de stejar deschis, linii curate și multă lumină naturală. Sfaturi practice pentru a aduce calmul în casa ta. #JapandiDesign #LivingRoomDecor #InteriorInspiration #CozySpace",
        "image_url": "/assets/decor.jpg",
        "tags": ["JapandiDesign", "LivingRoomDecor", "InteriorInspiration", "CozySpace"],
        "likes": 110,
        "views": 2500,
        "shares": 740
    },
    {
        "id": "pin_4",
        "platform": "pinterest",
        "category": "Food",
        "title": "Idei De Board-uri Pentru Charcuterie: Gustări Estetice Pentru Oaspeți",
        "description": "Cum să aranjezi brânzeturile fine, fructele confiate, nucile și mezelurile pentru un platou spectaculos vizual. Ghid de asocieri cromatice și arome. #CharcuterieBoard #Entertaining #AestheticFood #CheesePlatter",
        "image_url": "/assets/cooking.jpg",
        "tags": ["CharcuterieBoard", "Entertaining", "AestheticFood", "CheesePlatter"],
        "likes": 53,
        "views": 1400,
        "shares": 390
    }
]

MY_PROFILES_STATS = {
    "facebook": {
        "url": "https://www.facebook.com/mihnea.pitur.18",
        "username": "mihnea.pitur.18",
        "name": "Mihnea Pițur",
        "followers": 363,
        "posts_count": 739,
        "avg_engagement": 4.8,
        "recent_activity": [
            {"date": "Acum 9 ore", "title": "Nu știu dacă ați urmărit faza virală de ieri în care o absolventă a școlii gimnaziale a fost făcută cu ou și cu oțet de reporterul Antenei 1 după Evaluarea Națională. Vezi, Doamne, ce-s cu unghiile alea și cu tatuajul de pe mâna dreaptă?! Apreciez mult sinceritatea și coerența fetei în cauză. Dar mă supără maxim faptul că tembeliziunea difuzează copiii de la școlile mai slabe ca să-i facă muci și să-i subestimeze, în loc să încurajeze gândirea logică. Ați văzut vreodată reporteri care să vină după simulări/examene oficiale la Sava, Vianu, Lazăr? NU! Se duc la licee mai slabe, iar cel din fața micului ecran trage concluzia că tinerii sunt niște ratați fără viitor. Asta face tembeliziunea în goana după audiență: generalizează. Recunosc, râd și eu copios când se difuzează perlele de la examene, dar îmi dau seama că am fost părtaș unui sistem educațional ce nu a promovat gândirea critică și libertatea de exprimare printre elevi. Dacă eu aș fi lucrat în presă într-o mare televiziune comercială și m-ar fi pus cineva să subestimez copiii de la școlile proaste, în secunda 2 mi-aș fi dat demisia. Cât de retard să fii ca reporter să critici vestimentația, aranjatul părului, machiajul, tatuajele de pe corp sau cât de mult a învățat pentru examen. Ca să nu mai zic că știrile care se axează strict pe așa ceva sunt penibile și nu aduc plus valoare unui jurnal de știri. Să le fie rușine ziariștilor de carton! 📺🏫", "views": 190, "likes": 6, "shares": 2},
            {"date": "Acum 10 ore", "title": "Distribuit Carmen Dumitrescu: Au văzut și ei o copilă care făcea mișto de Antena la ieșirea de la examen și au simțit că e momentul să facă pe deștepții în raport cu ”generația asta de ratați”. În primul rând, eu cunosc generația asta bine. Mă întâlnesc des cu ea. Am sute de ore petrecute printre elevi de gimnaziu și liceu. Nu e o generație de ratați. E o generație care nu tocește. Care nu învață comentarii pe de rost. Care nu înțelege sensul acumulării de cunoștințe inutile pe care le poți obține în câteva secunde de pe net. E o generație care nu poate fi prostită de internet, așa cum e generația părinților și bunicilor ei. E o generație care are simțul umorului. Și un bun simț care lipsește generațiilor mele și a celor mai mari decât a mea. Ca atare, lăsați generația în pace! E foarte bine! Vedeți-vă de voi! Și fiți voi deștepți! Dați un exemplu, dacă tot v-ați apucat! Și a înjura o copilă care are simțul umorului nu e o dovadă de deșteptăciune, boșilor! A! Și să presupunem că fata nu face mișto de Antena. Deși eu sunt sigură că asta a făcut. Să presupunem că vorbea serios. Fata vrea să se facă specialist în servicii de înfrumusețare, nu președinte de țară, nu senator, nu medic. Nu o să vă pună niciodată viața în pericol, cum o fac atâția proști din generația voastră sau a mea. Ce e de înjurat aici? Vedeți-vă de voi! 💬📰", "views": 140, "likes": 1, "shares": 0},
            {"date": "Acum 13 ore", "title": "Distribuit Sanda Din Obor: Unul dintre motivele pentru care am plecat din televiziune e (și) ăsta. Ce mocirlă de om să fii să dai un copil la televizor și să comentezi că are unghii și că asta vrea să facă, o meserie și că nu e as la mate și nu știe cum să-și rezolve problemele nerezolvate ale matematicii? Când îmi amintesc că și pe mine mă trimiteau mai-marii perfecți, care aveau (sau nu) copii perfecți, să fac astfel de materiale, mi se face greață de mine că am făcut asta acum 10-15 ani.. să nu uităm de „perlele” din lucrări, ieșite fix amplea uneori de la profesorii care și ei erau perfecți și aveau (sau nu) copii perfecți. Iar când nu existau, se inventau, căci așa cereau mai-marii. Altfel, îți pierdeai jobul, iar banca nu te întreabă dacă ești sau nu integru, ea vrea banii pe rată... *prefecților, vedeți că nevestele voastre se duc la unghii la cineva care nu știe teorema lui Pitagora, dar știe să nu i ftă patul unghial femeii, pentru că știe meserie. Și poate după relaxare la salon doar așa mai aveți și voi parte de ceva în pat, csz 📺✂️", "views": 160, "likes": 2, "shares": 0},
            {"date": "Acum 1 săptămână", "title": "Plimbare de vară și weekend relaxant în Parcul Romanescu din Craiova. 🌳✨", "views": 310, "likes": 64, "shares": 5}
        ]
    },
    "instagram": {
        "url": "https://www.instagram.com/jesuismihnea",
        "username": "jesuismihnea",
        "name": "Mihnea Pițur",
        "followers": 262,
        "posts_count": 66,
        "avg_engagement": 12.4,
        "recent_activity": [
            {"date": "11 iunie", "caption": "This is how you remind me. 🎤✨", "views": 180, "likes": 32, "shares": 3},
            {"date": "7 iunie", "caption": "Și luna-și ascunde răni\nPeste orizont\nȘi sigur și tu, ești om\nDoar un om\nOricât ai vrea să fii mai mult. 🎤🏫", "views": 240, "likes": 42, "shares": 5}
        ]
    },
    "reddit": {
        "url": "https://www.reddit.com/user/Potential-Shirt-7063",
        "username": "Potential-Shirt-7063",
        "name": "Potential-Shirt-7063",
        "karma": 2022,
        "post_karma": 852,
        "comment_karma": 1170,
        "posts_count": 688,
        "recent_activity": [
            {"subreddit": "r/Craiova", "title": "Probleme facturi Premier Energy în Craiova - a mai pățit cineva?", "upvotes": 42, "comments": 18},
            {"subreddit": "r/Craiova", "title": "Recomandări pentru piscine/ștranduri faine în Craiova?", "upvotes": 24, "comments": 15},
            {"subreddit": "r/Craiova", "title": "Taxa de salubritate (gunoi) în Craiova: clarificări plată la primărie", "upvotes": 56, "comments": 29},
            {"subreddit": "r/UniRO", "title": "Întrebări legate de modulul DPPD la Automatică Craiova și examene", "upvotes": 78, "comments": 34},
            {"subreddit": "r/bucuresti", "title": "Experiență neplăcută cu un taximetrist în București", "upvotes": 112, "comments": 47}
        ]
    }
}

