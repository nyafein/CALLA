"""
Basic Belarusian phrases, organized into themed categories.

Structure:
    PHRASES = {
        "<category_id>": {
            "label_cyr": "<Belarusian Cyrillic header>",
            "label_eng": "<English label, used as fallback or accessibility>",
            "items": [
                {
                    "english": "<English meaning>",
                    "forms": [
                        {
                            "cyrillic": "<Belarusian in Cyrillic>",
                            "lacinka":  "<Belarusian in Łacinka>",
                            "ipa":      "<IPA transcription — first-draft, refine during recording>",
                            "register": "formal" | "informal" | "neutral",
                            "context":  "<short cultural / pragmatic note>",
                        },
                        ...
                    ],
                },
                ...
            ],
        },
        ...
    }

Multiple forms per item where the language distinguishes register.
Categories are rendered with their Cyrillic header so Belarusian remains
the meta-language of instruction.

GENERALIZATION NOTE (for future framework builds): this dict structure is
language-agnostic. Swapping in a new language requires only:
    - a native-speaker pass on items (cyrillic / target-script forms,
      transliteration, ipa, register, context)
    - localized category headers (label_cyr → label_<target_script>)
The pipeline, rendering, and practice machinery downstream do not need
to change. This is the "empty framework" deliverable for the presentation.
"""

PHRASES = {
    # ----------------------------------------------------------------
    "greetings": {
        "label_cyr": "Прывітанні",
        "label_eng": "Greetings",
        "items": [
            {
                "english": "Hello",
                "forms": [
                    {
                        "cyrillic": "Прывітанне",
                        "lacinka": "Pryvitannie",
                        "ipa": "/prɨvʲiˈtaɲɲɛ/",
                        "register": "neutral",
                        "context": (
                            "A general greeting, usable at any time of day. "
                            "Slightly warmer than a strictly business opening."
                        ),
                    },
                ],
            },
            {
                "english": "Good day",
                "forms": [
                    {
                        "cyrillic": "Добры дзень",
                        "lacinka": "Dobry dzień",
                        "ipa": "/ˈdɔbrɨ d͡zʲɛnʲ/",
                        "register": "neutral",
                        "context": (
                            "Literally 'good day'. Common neutral-to-formal "
                            "greeting, appropriate in shops, offices, and "
                            "with strangers throughout the daylight hours."
                        ),
                    },
                ],
            },
            {
                "english": "How are you?",
                "forms": [
                    {
                        "cyrillic": "Як ты?",
                        "lacinka": "Jak ty?",
                        "ipa": "/jak tɨ/",
                        "register": "informal",
                        "context": "For friends, family, peers. A close, warm question.",
                    },
                    {
                        "cyrillic": "Як вы?",
                        "lacinka": "Jak vy?",
                        "ipa": "/jak vɨ/",
                        "register": "formal",
                        "context": (
                            "For anyone you'd address formally. Also: "
                            "'Як справы?' (Jak spravy?) — 'How are things?' — "
                            "works in either register."
                        ),
                    },
                ],
            },
            {
                "english": "Fine, thanks",
                "forms": [
                    {
                        "cyrillic": "Добра, дзякуй",
                        "lacinka": "Dobra, dziakuj",
                        "ipa": "/ˈdɔbra ˈd͡zʲakuj/",
                        "register": "neutral",
                        "context": "",
                    },
                ],
            },
        ],
    },

    # ----------------------------------------------------------------
    "introductions": {
        "label_cyr": "Знаёмства",
        "label_eng": "Introductions",
        "items": [
            {
                "english": "What's your name?",
                "forms": [
                    {
                        "cyrillic": "Як цябе завуць?",
                        "lacinka": "Jak ciabie zavuć?",
                        "ipa": "/jak tsʲaˈbʲɛ zaˈvutsʲ/",
                        "register": "informal",
                        "context": (
                            "Literally 'How do they call you?' — a beautiful "
                            "piece of construction. Informal."
                        ),
                    },
                    {
                        "cyrillic": "Як вас завуць?",
                        "lacinka": "Jak vas zavuć?",
                        "ipa": "/jak vas zaˈvutsʲ/",
                        "register": "formal",
                        "context": "The same construction with the formal pronoun.",
                    },
                ],
            },
            {
                "english": "My name is...",
                "forms": [
                    {
                        "cyrillic": "Мяне завуць...",
                        "lacinka": "Mianie zavuć...",
                        "ipa": "/mʲaˈnʲɛ zaˈvutsʲ/",
                        "register": "neutral",
                        "context": "Mirrors the question — 'They call me...'",
                    },
                ],
            },
            {
                "english": "Nice to meet you",
                "forms": [
                    {
                        "cyrillic": "Прыемна пазнаёміцца",
                        "lacinka": "Pryjemna paznajomicca",
                        "ipa": "/prɨˈjɛmna paznaˈjɔmʲitstsa/",
                        "register": "neutral",
                        "context": (
                            "Literally 'pleasant to get acquainted'. The most "
                            "common standalone 'nice to meet you' — works in "
                            "most everyday introductions, formal or informal."
                        ),
                    },
                ],
            },
            {
                "english": "Pleased to meet you",
                "forms": [
                    {
                        "cyrillic": "Рады сустрэцца з вамі",
                        "lacinka": "Rady sustrecca z vami",
                        "ipa": "/ˈradɨ susˈtrɛtstsa z ˈvamʲi/",
                        "register": "formal",
                        "context": (
                            "The 'з вамі' (with you, formal plural) makes this "
                            "lean formal. With friends or peers, you might "
                            "instead say 'Рады пазнаёміцца' — 'Glad to get "
                            "to know you.'"
                        ),
                    },
                ],
            },
        ],
    },

    # ----------------------------------------------------------------
    "farewells": {
        "label_cyr": "Развітанні",
        "label_eng": "Farewells",
        "items": [
            {
                "english": "Goodbye",
                "forms": [
                    {
                        "cyrillic": "Бывай",
                        "lacinka": "Byvaj",
                        "ipa": "/bɨˈvaj/",
                        "register": "informal",
                        "context": "Casual goodbye, between friends, family, peers.",
                    },
                    {
                        "cyrillic": "Да пабачэння",
                        "lacinka": "Da pabačennia",
                        "ipa": "/da pabaˈtʂɛɲɲa/",
                        "register": "formal",
                        "context": (
                            "The standard polite goodbye — appropriate with "
                            "strangers, in shops, at work."
                        ),
                    },
                ],
            },
            {
                "english": "See you",
                "forms": [
                    {
                        "cyrillic": "Да сустрэчы",
                        "lacinka": "Da sustrečy",
                        "ipa": "/da susˈtrɛtʂɨ/",
                        "register": "neutral",
                        "context": (
                            "Literally 'until [the] meeting'. Warmer than a "
                            "formal 'goodbye' — implies you expect to meet "
                            "again. Common with acquaintances, classmates, "
                            "colleagues you'll see again soon."
                        ),
                    },
                ],
            },
        ],
    },

    # ----------------------------------------------------------------
    # Note: Nya may rename or recategorize this fourth section. It holds
    # courtesies and conversational tools that don't fit the three named
    # headers above. If she moves any items into the prior categories,
    # delete them from here.
    # ----------------------------------------------------------------
    "useful_expressions": {
        "label_cyr": "Карысныя выразы",
        "label_eng": "Useful Expressions",
        "items": [
            {
                "english": "Yes",
                "forms": [
                    {
                        "cyrillic": "Так",
                        "lacinka": "Tak",
                        "ipa": "/tak/",
                        "register": "neutral",
                        "context": "",
                    },
                ],
            },
            {
                "english": "No",
                "forms": [
                    {
                        "cyrillic": "Не",
                        "lacinka": "Nie",
                        "ipa": "/nʲɛ/",
                        "register": "neutral",
                        "context": "",
                    },
                ],
            },
            {
                "english": "Excuse me",
                "forms": [
                    {
                        "cyrillic": "Прабач",
                        "lacinka": "Prabač",
                        "ipa": "/praˈbatʂ/",
                        "register": "informal",
                        "context": (
                            "To a single person you'd address with ты — a "
                            "friend, a child, someone close in age."
                        ),
                    },
                    {
                        "cyrillic": "Прабачце",
                        "lacinka": "Prabačcie",
                        "ipa": "/praˈbatʂtsʲɛ/",
                        "register": "formal",
                        "context": (
                            "To anyone you'd address with вы — strangers, "
                            "elders, in formal settings."
                        ),
                    },
                ],
            },
            {
                "english": "Please / You're welcome",
                "forms": [
                    {
                        "cyrillic": "Калі ласка",
                        "lacinka": "Kali laska",
                        "ipa": "/kaˈlʲi ˈlaska/",
                        "register": "neutral",
                        "context": (
                            "One of those lovely phrases that does double duty "
                            "— it means both 'please' (when asking) and "
                            "'you're welcome' (when responding to thanks)."
                        ),
                    },
                ],
            },
            {
                "english": "Thank you",
                "forms": [
                    {
                        "cyrillic": "Дзякуй",
                        "lacinka": "Dziakuj",
                        "ipa": "/ˈd͡zʲakuj/",
                        "register": "neutral",
                        "context": (
                            "Universal thanks. For warmer thanks, you can say "
                            "шчыра дзякуй (ščyra dziakuj) — 'sincere thanks'."
                        ),
                    },
                ],
            },
            {
                "english": "Do you speak English?",
                "forms": [
                    {
                        "cyrillic": "Вы размаўляеце па-ангельску?",
                        "lacinka": "Vy razmaŭliajecie pa-anhieĺsku?",
                        "ipa": "/vɨ razmaʊˈlʲajɛtsʲɛ pa anˈɣʲɛlʲsku/",
                        "register": "formal",
                        "context": (
                            "The 'вы' form — appropriate when asking a "
                            "stranger or in any public setting."
                        ),
                    },
                ],
            },
            {
                "english": "Do you understand?",
                "forms": [
                    {
                        "cyrillic": "Ты разумееш?",
                        "lacinka": "Ty razumiejеš?",
                        "ipa": "/tɨ razuˈmʲejeʂ/",
                        "register": "informal",
                        "context": "Checking comprehension with someone you know well or a peer.",
                    },
                    {
                        "cyrillic": "Вы разумееце?",
                        "lacinka": "Vy razumiejecie?",
                        "ipa": "/vɨ razuˈmʲejetsʲɛ/",
                        "register": "formal",
                        "context": (
                            "The polite version — for strangers, students "
                            "to teachers, customers in shops."
                        ),
                    },
                ],
            },
            {
                "english": "I understand",
                "forms": [
                    {
                        "cyrillic": "Я разумею",
                        "lacinka": "Ja razumieju",
                        "ipa": "/ja razuˈmʲejʊ/",
                        "register": "neutral",
                        "context": "",
                    },
                ],
            },
            {
                "english": "I don't understand",
                "forms": [
                    {
                        "cyrillic": "Я не разумею",
                        "lacinka": "Ja nie razumieju",
                        "ipa": "/ja nʲɛ razuˈmʲejʊ/",
                        "register": "neutral",
                        "context": (
                            "Useful early. Don't be afraid to use it — "
                            "Belarusian speakers will usually slow down or rephrase."
                        ),
                    },
                ],
            },
        ],
    },
}


# ---------------------------------------------------------------------------
# Compatibility helpers — let downstream code (the practice pool builder, the
# Conversation Partner page, etc.) iterate flat over all phrase items without
# needing to know about the category structure.
# ---------------------------------------------------------------------------

def iter_all_items():
    """Yield every phrase item across all categories, in declared order."""
    for cat in PHRASES.values():
        for item in cat["items"]:
            yield item


def all_items_flat():
    """Return a flat list of all phrase items. Useful for building pools."""
    return list(iter_all_items())
