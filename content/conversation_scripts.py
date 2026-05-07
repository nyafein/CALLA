"""
Scripted conversation-partner exchanges.

Each scenario is a sequence of TURNS. At each turn, the user is offered
2-3 choices (Cyrillic + Łacinka + English gloss). Picking one advances
to the partner's response, which carries:
    cyrillic, lacinka, english   — the response itself
    cultural_note                 — the "what just happened culturally?" annotation

Choice schema:
    is_good: True               — choice is acceptable; advances the dialog
    is_good: False              — choice is wrong/awkward; stay on the turn
                                  with feedback shown, don't advance
    feedback (optional)         — string to show the user when is_good=False
    response_if_chosen (opt.)   — full partner response dict to use INSTEAD of
                                  the turn-level response_if_good. Lets a turn
                                  branch on which good choice was picked
                                  (e.g. "What is Kupalle?" → friend explains
                                   vs. "Kupalle! The fern flower?" → friend
                                   confirms with shared knowledge).

The partner is scripted, not LLM-driven. This is deliberate for today's
demo — zero risk of weird outputs, full pedagogical control. The same
structure can later be wired to a live LLM by replacing the lookup with
an API call.

Scenarios mirror the dialogues page so learners practice what they read.
"""

SCENARIOS = {
    "hrodna_market": {
        "title": "Buying mačanka at the Hrodna market",
        "setting": "You approach a vendor's stall.",
        "opening": {
            # Partner speaks first
            "cyrillic": "Добры дзень! Што вы хочаце?",
            "lacinka": "Dobry dzień! Što vy chočacie?",
            "english": "Good day! What would you like?",
            "cultural_note": (
                "She opens with 'Добры дзень' (formal good day) and 'вы хочаце' "
                "(formal 'you want'). The whole exchange will run in formal register."
            ),
        },
        "turns": [
            {
                "step": 1,
                "prompt": "How do you ask if she has mačanka?",
                "choices": [
                    {
                        "id": "a",
                        "cyrillic": "Прабачце, у вас ёсць мачанка?",
                        "lacinka": "Prabačcie, u vas jość mačanka?",
                        "english": "Excuse me, do you have mačanka?",
                        "is_good": True,
                    },
                    {
                        "id": "b",
                        "cyrillic": "Скажыце, калі ласка, ці маеце машыну?",
                        "lacinka": "Skažycie, kali laska, ci majecie мašynu?",
                        "english": "Tell me, please, do you have a car?",
                        "is_good": False,
                        "feedback": (
                            "Hmm... I mean, you could ask this, but don't you have a bus pass?"
                            )
                    },
                    {
                        "id": "c",
                        "cyrillic": "Дай мне мачанку.",
                        "lacinka": "Daj mnie mačanku.",
                        "english": "Give me mačanka.",
                        "is_good": False,
                        "feedback": (
                            "Grammatically fine, but 'дай' is informal-imperative — "
                            "not appropriate to a vendor you don't know. Don't be rude!"
                        ),
                    },
                ],
                "response_if_good": {
                    "cyrillic": "Так, ёсць. Свежая, ранішняя.",
                    "lacinka": "Tak, jość. Sviežaja, ranišniaja.",
                    "english": "Yes, we have it. Fresh, made this morning.",
                    "cultural_note": (
                        "'Ранішняя' — 'morning's,' i.e. made today."
                    ),
                },
            },
            {
                "step": 2,
                "prompt": "She has mačanka. Now ask if she sells the pancakes (бліны) too.",
                "choices": [
                    {
                        "id": "a",
                        "cyrillic": "А з блінамі прадаеце?",
                        "lacinka": "A z blinami pradajecie?",
                        "english": "And do you sell it with pancakes?",
                        "is_good": True,
                        "feedback": (
                            "This is right! So is the other option: 'А бліны таксама ёсць?'"
                            )
                    },
                    {
                        "id": "b",
                        "cyrillic": "А бліны таксама ёсць?",
                        "lacinka": "A bliny taksama jość?",
                        "english": "Are there pancakes too?",
                        "is_good": True,
                        "feedback": (
                            "This is right! So is the other option: 'А з блінамі прадаеце?'"
                            )
                    
                    },
                    {
                        "id": "c",
                        "cyrillic": "Толькі мачанка, дзякуй.",
                        "lacinka": "Toĺki mačanka, dziakuj.",
                        "english": "Just the mačanka, thanks.",
                        "is_good": False,
                        "feedback": (
                            "I mean, technically you can do this, but mačanka without blini is "
                            "incomplete! Don't you want the full experience?"
                        ),
                    },
                ],
                "response_if_good": {
                    "cyrillic": "Канечне. Бліны асобна, мачанка ў слоіку. Колькі вам?",
                    "lacinka": "Kaniečnie. Bliny asobna, mačanka ŭ słoiku. Koĺki vam?",
                    "english": "Of course. Pancakes separately, mačanka in a jar. How much do you want?",
                    "cultural_note": (
                        "'У слоіку' — 'in a jar.' Sold by volume."
                    ),
                },
            },
            {
                "step": 3,
                "prompt": "Close the exchange politely.",
                "choices": [
                    {
                        "id": "a",
                        "cyrillic": "Адзін слоік, калі ласка. Дзякуй.",
                        "lacinka": "Adzin słoik, kali laska. Dziakuj.",
                        "english": "One jar, please. Thank you.",
                        "is_good": True,
                    },
                    {
                        "id": "b",
                        "cyrillic": "Два слоікі, калі ласка. Дзякуй.",
                        "lacinka": "Dva słoiki, kali laska. Dziakuj.",
                        "english": "Two jars, please. Thank you.",
                        "is_good": True,
                        "feedback": "Good move! Mačanka is delicious."

                    },
                    {
                        "id": "c",
                        "cyrillic": "Не, дзякуй. Да пабачэння.",
                        "lacinka": "Nie, dziakuj. Da pabačennia.",
                        "english": "No, thanks. Goodbye.",
                        "is_good": False,
                        "feedback": (
                            "Rude!!!"
                        ),
                    },
                ],
                "response_if_good": {
                    "cyrillic": "Калі ласка. Прыходзьце яшчэ.",
                    "lacinka": "Kali laska. Prychodźcie jaščе.",
                    "english": "You're welcome. Come back again.",
                    "cultural_note": (
                        "'Калі ласка' here means 'you're welcome' (responding to thanks), does it look familiar? "
                        "The same phrase means 'please'! 'Прыходзьце "
                        "яшчэ' — 'come back again' — is a warm market closing."
                    ),
                },
            },
        ],
    },

    "minsk_cafe": {
        "title": "Ordering at a Minsk café",
        "setting": "A small café, mid-afternoon. A barista about your age looks up from the espresso machine.",
        "opening": {
            "cyrillic": "Прывітанне! Што будзеце?",
            "lacinka": "Pryvitannie! Što budziecie?",
            "english": "Hi! What'll you have?",
            "cultural_note": (
                "'Прывітанне' — neutral 'hi.' 'Што будзеце' — informal-leaning 'what'll "
                "you have' (literally 'what will you be?')."
            ),
        },
        "turns": [
            {
                "step": 1,
                "prompt": "Ask if they have kvas!",
                "choices": [
                    {
                        "id": "a",
                        "cyrillic": "Ці ёсць у вас квас?",
                        "lacinka": "Ci jość u vas kvas?",
                        "english": "Do you have kvas?",
                        "is_good": True,
                    },
                    {
                        "id": "b",
                        "cyrillic": "Прывітанне! Квас у вас ёсць?",
                        "lacinka": "Pryvitannie! Kvas u vas jość?",
                        "english": "Hi! Do you have kvas?",
                        "is_good": True,
                    },
                    {
                        "id": "c",
                        "cyrillic": "Ці ёсць у вас кава?",
                        "lacinka": "Ci jość u vas kava?",
                        "english": "Do you have coffee?",
                        "is_good": False,
                        "feedback": (
                            "Functional, but you said you wanted kvas. It's too "
                            "late in the afternoon for coffee anyway!"
                        ),
                    },
                ],
                "response_if_good": {
                    "cyrillic": "Ёсць, хатні. Маленькі ці вялікі?",
                    "lacinka": "Jość, chatni. Mali ci vialiki?",
                    "english": "Yes — homemade. Small or large?",
                    "cultural_note": (
                        "'Хатні' — 'homemade.'"
                        "Note the 'ці' particle! Do you remember what it does? It turns a statement into a yes/no question."
                    ),
                },
            },
            {
                "step": 2,
                "prompt": "Order whichever size you want! Oo, don't forget to ask if they have birch sap.",
                "choices": [
                    {
                        "id": "a",
                        "cyrillic": "Маленькі, дзякуй. І бярозавы сок ёсць?",
                        "lacinka": "Mali, dziakuj. I biarozavy sok jość?",
                        "english": "Small, thanks. And do you have birch sap?",
                        "is_good": True,
                    },
                    {
                        "id": "b",
                        "cyrillic": "вялікі, калі ласка. А бярозавы сок?",
                        "lacinka": "Vialiki, kali laska. A biarozavy sok?",
                        "english": "Large, please. And birch sap?",
                        "is_good": True,
                    },
                    {
                        "id": "c",
                        "cyrillic": "Я перадумаў — нічога не трэба.",
                        "lacinka": "Ja peradumaŭ — ničoha nie treba.",
                        "english": "I changed my mind — I don't want anything.",
                        "is_good": False,
                        "feedback": (
                            "Don't be shy! You're doing great! (:"
                        ),
                    },
                ],
                "response_if_good": {
                    "cyrillic": "Сёння няма, прабач. Прывязуць заўтра.",
                    "lacinka": "Sionnia niama, prabač. Pryviazuć zaŭtra.",
                    "english": "Not today, sorry. They'll bring some tomorrow.",
                    "cultural_note": (
                        "'Прабач' — informal apology. Birch sap is seasonal and supplier-dependent."
                    ),
                },
            },
            {
                "step": 3,
                "prompt": "Aw man... It happens! Let's just buy the kvas and leave.",
                "choices": [
                    {
                        "id": "a",
                        "cyrillic": "Нічога. Тады толькі квас.",
                        "lacinka": "Ničoha. Tady toĺki kvas.",
                        "english": "No worries. Just the kvas, then.",
                        "is_good": True,
                    },
                    {
                        "id": "b",
                        "cyrillic": "Шкада. Заўтра прыйду тады!",
                        "lacinka": "Škada. Zaŭtra pryjdu tady!",
                        "english": "Too bad. I'll come tomorrow then!",
                        "is_good": True,
                    },
                    {
                        "id": "c",
                        "cyrillic": "А чаму няма?",
                        "lacinka": "A čamu niama?",
                        "english": "Why don't you have any?",
                        "is_good": False,
                        "feedback": (
                            "Hey hey, chill out! Don't be *that* person..."
                        ),
                    },
                ],
                "response_if_good": {
                    "cyrillic": "Добра. Зараз прынясу.",
                    "lacinka": "Dobra. Zaraz prynesu.",
                    "english": "Got it. I'll bring it right over.",
                    "cultural_note": (
                        "'Нічога' (literally 'nothing') as 'no worries' "
                        "is a common casual response to an apology. It's like "
                        "saying 'don't mention it' or 'no big deal.'"
                    ),
                },
            },
        ],
    },

    "strochitsy_kupalle": {
        "title": "Walking at Strochitsy near Kupalle",
        "setting": (
            "Late June at Строчыцы (Stročycy), the open-air ethnographic museum "
            "near Minsk. You're walking a forest path with a friend. Kupalle is "
            "approaching."
        ),
        "opening": {
            "cyrillic": "Глядзі, тут грыбы! Лісічкі, здаецца.",
            "lacinka": "Hliadzi, tut hryby! Lisičky, zdajecca.",
            "english": "Look, mushrooms here! Chanterelles, I think.",
            "cultural_note": (
                "'Лісічкі' literally 'little foxes' — for the orange color. "
                "Foraging knowledge is part of the cultural vocabulary, not "
                "specialist jargon."
            ),
        },
        "turns": [
            {
                "step": 1,
                "prompt": "What's your reaction?",
                "choices": [
                    {
                        "id": "a",
                        "cyrillic": "Сапраўды? А ягады тут таксама збіраюць?",
                        "lacinka": "Sapraŭdy? A jahady tut taksama zbirajuć?",
                        "english": "Really? And do they pick berries here too?",
                        "is_good": True,
                    },
                    {
                        "id": "b",
                        "cyrillic": "Лісічкі! Якія прыгожыя.",
                        "lacinka": "Lisičky! Jakija pryhožyja.",
                        "english": "Chanterelles! How beautiful.",
                        "is_good": True,
                    },
                    {
                        "id": "c",
                        "cyrillic": "Я не люблю грыбы.",
                        "lacinka": "Ja nie liubliu hryby.",
                        "english": "I don't like mushrooms.",
                        "is_good": False,
                        "feedback": (
                            "You're missing out."
                        ),
                    },
                ],
                "response_if_good": {
                    "cyrillic": "Чарніцы — улетку. Калi купалле хутка!",
                    "lacinka": "Čarnicy — ŭletku. Kali kupallie chutka!",
                    "english": "Bilberries — in summer. When kupalle is soon!",
                    "cultural_note": (
                        "We're talking about Kupalle now! Strochitsy hosts "
                        "traditional Kupalle celebrations, did you know?"
                    ),
                },
            },
            {
                # NEW step — gives the learner a chance to ASK what Kupalle is.
                # Branches via response_if_chosen on each good option, so the
                # friend's reply differs based on what was asked.
                "step": 2,
                "prompt": "Do you know what Kupalle is? If not, ask!",
                "choices": [
                    {
                        "id": "a",
                        "cyrillic": "А што такое Купалле?",
                        "lacinka": "A što takoje Kupallie?",
                        "english": "What is Kupalle?",
                        "is_good": True,
                        # Friend EXPLAINS — this is the "I don't know, please tell me" path.
                        "response_if_chosen": {
                            "cyrillic": (
                                "Летняе свята. Вогнішчы ноччу, вянкі на ваду, "
                                "шукаюць папараць-кветку ў лесе. Старажытнае і прыгожае..."
                            ),
                            "lacinka": (
                                "Letniaje sviata. Vahniščy nočču, vianki na vadu, "
                                "šukajuć paparać-kvietku ŭ lesie. Staražytnaje i pryhožaje..."
                            ),
                            "english": (
                                "A summer festival. Bonfires at night, wreaths on the "
                                "water, searching for the fern flower in the forest. "
                                "Ancient and beautiful..."
                            ),
                            "cultural_note": (
                                "Asking is the right move when you don't know!"
                                " The name comes from Іван Купала, later layered with the feast "
                                "of John the Baptist."
                            ),
                        },
                    },
                    {
                        "id": "b",
                        "cyrillic": "Купалле! Гэта пра папараць-кветку, праўда?",
                        "lacinka": "Kupallie! Heta pra paparać-kvietku, praŭda?",
                        "english": "Kupalle! That's the one with the fern flower, right?",
                        "is_good": True,
                        # Friend CONFIRMS — this is the "I already know, let me show it"
                        # path. Different response from above.
                        "response_if_chosen": {
                            "cyrillic": (
                                "Так! Ты ведаеш. Кажуць, што калі знойдзеш "
                                "папараць-кветку ў гэтую ноч — атрымаеш жаданае."
                            ),
                            "lacinka": (
                                "Tak! Ty viedaješ. Kažuć, što kali znojdzieš "
                                "paparać-kvietku ŭ hetuju noč — atrymaješ žadanaje."
                            ),
                            "english": (
                                "Yes! You know. They say if you find the fern "
                                "flower that night — you'll get what you wish for."
                            ),
                            "cultural_note": (
                                "Oh, so you've heard of the fern flower (папараць-кветка)! The "
                                "flower supposedly blooms only on Kupalle night and "
                                "is a central image in Belarusian folk tradition."
                            ),
                        },
                    },
                    {
                        "id": "c",
                        "cyrillic": "Я не люблю народных свят.",
                        "lacinka": "Ja nie liubliu narodnych sviat.",
                        "english": "I don't like folk holidays.",
                        "is_good": False,
                        "feedback": (
                            "Is this because you forgot the bug spray?"
                        ),
                    },
                ],
                # Default response (used by all_partner_english_glosses for
                # comprehension distractors). The actual reply branches via
                # response_if_chosen above; this is just a reasonable fallback.
                "response_if_good": {
                    "cyrillic": (
                        "Летняе свята. Вогнішчы ноччу, вянкі на ваду, "
                        "шукаюць папараць-кветку ў лесе."
                    ),
                    "lacinka": (
                        "Letniaje sviata. Vahniščy nočču, vianki na vadu, "
                        "šukajuć paparać-kvietku ŭ lesie."
                    ),
                    "english": (
                        "A summer festival. Bonfires at night, wreaths on the "
                        "water, searching for the fern flower in the forest. "

                    ),
                    "cultural_note": (
                        "Kupalle is a pre-Christian holiday celebrated in mid-summer. Christianized as the "
                        "feast of John the Baptist (Іван Купала), it is still observed."
                    ),
                },
            },
            {
                "step": 3,
                "prompt": "Connect this to literature or song.",
                "choices": [
                    {
                        "id": "a",
                        "cyrillic": "Багдановіч пра гэта пісаў, праўда?",
                        "lacinka": "Bahdanovič pra heta pisaŭ, praŭda?",
                        "english": "Bahdanovič wrote about this, didn't he?",
                        "is_good": True,
                    },
                    {
                        "id": "b",
                        "cyrillic": "А «Купалінка» — гэта народная песня?",
                        "lacinka": "A «Kupalinka» — heta narodnaja piesnia?",
                        "english": "And 'Kupalinka' — is that a folk song?",
                        "is_good": True,
                    },
                    {
                        "id": "c",
                        "cyrillic": "Я не ведаю беларускую літаратуру.",
                        "lacinka": "Ja nie viedaju biełaruskuju litaraturu.",
                        "english": "I don't know Belarusian literature.",
                        "is_good": False,
                        "feedback": "Points for being honest, but c'mon!",
                    },
                ],
                "response_if_good": {
                    "cyrillic": (
                        "Так! Багдановіч пісаў пра гэта ў «Вянку», "
                        "а «Купалінка» — народная песня, якую ўсе ведаюць. "
                       
                    ),
                    "lacinka": (
                        "Tak! Bahdanovič pisaŭ pra heta ŭ «Vianku», "
                        "a «Kupalinka» — narodnaja piesnia, jakuju ŭsie viedajuć. "
                     
                    ),
                    "english": (
                        "Yes! Bahdanovič wrote about this in 'Vianok', and "
                        "'Kupalinka' is a folk song everyone knows."
                    ),
                    "cultural_note": (
                        "'Вянок' (1913) was Bahdanovič's only collection published "
                        "in his lifetime — deeply tied to folk forms. 'Купалінка' "
                        "is a foundational folk song every Belarusian speaker "
                        "knows. Mentioning either lands as cultural fluency."
                    ),
                },
            },
        ],
    },
}
