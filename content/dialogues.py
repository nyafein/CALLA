"""
Three scripted dialogues, each anchored in a real Belarusian place
and built around culturally specific food and reference points.

Each dialogue has:
    setting        — short description of the scene
    register_note  — what register is operating, and why
    turns          — list of {speaker, cyrillic, lacinka, english, note}
                     where 'note' (optional) explains a word or move
    cultural_context — longer paragraph on what's happening culturally

Anchors:
    Hrodna     — formal market exchange, hearty everyday foods
    Minsk      — casual café, drinks
    Strochitsy — ethnographic museum, Kupalle context, foraging,
                 Bahdanovič reference
"""

DIALOGUES = [
    {
        "id": "hrodna",
        "title": "У Гродне на рынку — At the Hrodna market",
        "setting": "A weekday morning at a covered market in Hrodna. You're approaching a vendor's stall to ask about мачанка (mačanka) — meat in gravy, traditionally served with pancakes.",
        "register_note": "Formal throughout. You don't know the vendor; she's older than you; this is a public exchange.",
        "turns": [
            {
                "speaker": "you",
                "cyrillic": "Прабачце, у вас ёсць мачанка?",
                "lacinka": "Prabačcie, u vas jość mačanka?",
                "english": "Excuse me, do you have mačanka?",
                "note": "'Прабачце' opens politely. 'У вас ёсць...?' literally 'Do you have...?' (the standard polite ask)."
            },
            {
                "speaker": "vendor",
                "cyrillic": "Так, ёсць. Свежая, ранішняя.",
                "lacinka": "Tak, jość. Sviežaja, ranišniaja.",
                "english": "Yes, we have it. Fresh, made this morning.",
                "note": "'Ранішняя' — 'morning's', i.e. made today."
            },
            {
                "speaker": "you",
                "cyrillic": "А з блінамі прадаеце?",
                "lacinka": "A z blinami pradajecie?",
                "english": "And do you sell it with pancakes?",
                "note": "Mačanka without blini is incomplete!"
            },
            {
                "speaker": "vendor",
                "cyrillic": "Канечне. Бліны асобна, мачанка ў слоіку. Колькі вам?",
                "lacinka": "Kaniečnie. Bliny asobna, mačanka ŭ słoiku. Koĺki vam?",
                "english": "Of course. Pancakes separately, mačanka in a jar. How much do you want?",
                "note": "'У слоіку' — 'in a jar.' Sold by volume, not weight — typical at markets."
            },
            {
                "speaker": "you",
                "cyrillic": "Адзін слоік, калі ласка. Дзякуй.",
                "lacinka": "Adzin słoik, kali laska. Dziakuj.",
                "english": "One jar, please. Thank you.",
                "note": ""
            },
        ],
        "cultural_context": (
            "Mačanka pork or sausage in a thick, "
            "sour-cream-and-flour gravy, eaten by tearing pieces of pancake and dipping. "
            "Verašvčaka and draniki are the other "
            "two standards you'd encounter at the same stall."
        ),
    },
    {
        "id": "minsk",
        "title": "У мінскай кавярні — At a Minsk café",
        "setting": "A small café in Minsk, mid-afternoon. You're meeting a friend who suggested it. They're at a corner table; you're ordering before sitting down.",
        "register_note": "Casual throughout. The barista is around your age; the friend is close.",
        "turns": [
            {
                "speaker": "you",
                "cyrillic": "Прывітанне! Ці ёсць у вас квас?",
                "lacinka": "Pryvitannie! Ci jość u vas kvas?",
                "english": "Hi! Do you have kvas?",
                "note": "'Ці' is the interrogative particle — turns a statement into a yes/no question. Useful to know!"
            },
            {
                "speaker": "barista",
                "cyrillic": "Ёсць, хатні. Маленькі ці вялікі?",
                "lacinka": "Jość, chatni. Mali ci vialiki?",
                "english": "We do — homemade. Small or large?",
                "note": "'Хатні' — 'homemade.' Do you see the word 'хата' (house) in there?"
            },
            {
                "speaker": "you",
                "cyrillic": "Маленькі, дзякуй. І бярозавы сок ёсць?",
                "lacinka": "Mali, dziakuj. I biarozavy sok jość?",
                "english": "Small, thanks. And do you have birch sap?",
                "note": "Birch sap (бярозавы сок) is a seasonal drink and best consumed in the spring!"
            },
            {
                "speaker": "barista",
                "cyrillic": "Сёння няма, прабач. Прывязуць заўтра.",
                "lacinka": "Sionnia niama, prabač. Pryviazuć zaŭtra.",
                "english": "Not today, sorry. They'll bring some tomorrow.",
                "note": "'Прабач' — informal apology."
            },
            {
                "speaker": "you",
                "cyrillic": "Нічога. Тады толькі квас.",
                "lacinka": "Ničoha. Tady toĺki kvas.",
                "english": "No worries. Just the kvas, then.",
                "note": "'Нічога' — literally 'nothing' but functions as 'no worries' / 'never mind.' Useful phrase!"
            },
        ],
        "cultural_context": (
            "Kvas is a popular fermented bread drink. "
            "Birch sap (бярозавы сок) is more seasonal."
        ),
    },
    {
        "id": "strochitsy",
        "title": "У Строчыцах на Купалле — At Strochitsy on Kupalle",
        "setting": (
            "Строчыцы (Stročycy) — the open-air ethnographic museum near Minsk, "
            "preserving traditional Belarusian rural architecture and craft. "
            "It's late June, around Kupalle (the mid-summer holiday, also called Kupala night). You're walking with friends along "
            "a forest path on the museum grounds."
        ),
        "register_note": "Mostly informal — you're with friends!",
        "turns": [
            {
                "speaker": "friend",
                "cyrillic": "Глядзі, тут грыбы! Лісічкі, здаецца.",
                "lacinka": "Hliadzi, tut hryby! Lisičky, zdajecca.",
                "english": "Look, mushrooms here! Chanterelles, I think.",
                "note": "'Лісічкі' — chanterelles, literally 'little foxes' for the orange color. Foraging knowledge runs deep in Belarusian rural tradition."
            },
            {
                "speaker": "you",
                "cyrillic": "Сапраўды? А ягады тут таксама збіраюць?",
                "lacinka": "Sapraŭdy? A jahady tut taksama zbirajuć?",
                "english": "Really? And do they pick berries here too?",
                "note": "'Сапраўды' — 'really / truly.' Common in conversation as a soft surprise marker."
            },
            {
                "speaker": "friend",
                "cyrillic": "Чарніцы — улетку. А зараз — Купалле хутка.",
                "lacinka": "Čarnicy — ŭletku. A zaraz — Kupallie chutka.",
                "english": "Bilberries — in summer. And right now — Kupalle is coming soon.",
                "note": "'Купалле' is a midsummer festival. Strochitsy hosts traditional Kupalle celebrations."
            },
            {
                "speaker": "you",
                "cyrillic": "Багдановіч пра гэта пісаў, праўда?",
                "lacinka": "Bahdanovič pra heta pisaŭ, praŭda?",
                "english": "Bahdanovič wrote about this, didn't he?",
                "note": "Maksim Bahdanovič (1891–1917) drew heavily on folk tradition. Mentioning him here lands."
            },
            {
                "speaker": "friend",
                "cyrillic": "Так! У 'Вянку'. Ён увесь з гэтага.",
                "lacinka": "Tak! U 'Viankú'. Jon uviеś z hetaha.",
                "english": "Yes! In 'Vianok' [The Wreath]. The whole thing comes from this.",
                "note": "'Вянок' (1913) — Bahdanovič's only collection published in his lifetime, deeply rooted in Belarusian folk forms."
            },
        ],
        "cultural_context": (
            "Strochitsy preserves what Bahdanovič wrote into modern Belarusian "
            "literary identity: rural craft, folk calendar, the relationship "
            "between language and forest. Kupalle — celebrated near the summer "
            "solstice — is one of the most culturally dense moments in the "
            "Belarusian year: bonfires, wreaths floated on water, the mythical "
            "'fern flower' that blooms only on Kupalle night. Seasonal nature "
            " vocabulary — грыбы, ягады, чарніцы."
        ),
    },
]
