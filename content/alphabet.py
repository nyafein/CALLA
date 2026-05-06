"""
Belarusian alphabet — 32 letters in standard order, plus the apostrophe
and the digraphs Дж / Дз (which are not separate letters but are
pedagogically worth including).

Fields:
    cyrillic_upper, cyrillic_lower
    lacinka            — Łacinka equivalent (lower; uppercase is title-cased
                         where applicable). Where context determines form
                         (e.g. e → je / ie), the most common variant is
                         shown and noted.
    ipa                — IPA representation. Where the letter has both a
                         hard and palatalized form, both are shown.
    example_cyr        — example word in Cyrillic
    example_lac        — example word in Łacinka
    example_eng        — gloss of the example word
    note               — optional notes for special cases (palatalization,
                         iotation, hard-only consonants, etc.)
    audio_id           — file slug used to look up audio under
                         static/audio/letters/{audio_id}.mp3
                         and example word audio under
                         static/audio/words/{audio_id}.mp3
"""

ALPHABET = [
    {"cyrillic_upper": "А", "cyrillic_lower": "а", "lacinka": "A a", "ipa": "/a/",
     "example_cyr": "Аўтобус", "example_lac": "Aŭtobus", "example_eng": "Bus", "note": "", "audio_id": "a"},

    {"cyrillic_upper": "Б", "cyrillic_lower": "б", "lacinka": "B b", "ipa": "/b/",
     "example_cyr": "Бацька", "example_lac": "Baćka", "example_eng": "Father", "note": "", "audio_id": "b"},

    {"cyrillic_upper": "В", "cyrillic_lower": "в", "lacinka": "V v", "ipa": "/v/",
     "example_cyr": "Вада", "example_lac": "Vada", "example_eng": "Water", "note": "", "audio_id": "v"},

    {"cyrillic_upper": "Г", "cyrillic_lower": "г", "lacinka": "H h", "ipa": "/ɣ/, /h/",
     "example_cyr": "Горад", "example_lac": "Horad", "example_eng": "City",
     "note": "Belarusian Г is a fricative, not the stop /ɡ/. Some traditions use Ґ for /ɡ/ in loanwords.",
     "audio_id": "h"},

    {"cyrillic_upper": "Д", "cyrillic_lower": "д", "lacinka": "D d", "ipa": "/d/",
     "example_cyr": "Дом", "example_lac": "Dom", "example_eng": "House", "note": "", "audio_id": "d"},

    {"cyrillic_upper": "Е", "cyrillic_lower": "е", "lacinka": "Je je / ie", "ipa": "/jɛ/, /ʲɛ/",
     "example_cyr": "Ежа", "example_lac": "Ježa", "example_eng": "Food",
     "note": "Word-initially or after a vowel: je. After a consonant: ie (palatalizing the consonant).",
     "audio_id": "je"},

    {"cyrillic_upper": "Ё", "cyrillic_lower": "ё", "lacinka": "Jo jo / io", "ipa": "/jɔ/, /ʲɔ/",
     "example_cyr": "Ёсць", "example_lac": "Jość", "example_eng": "Is / Exists",
     "note": "Always stressed (Example usage: Тут ёсць крама / Tut jość krama — There's a shop here or У мяне ёсць кніга / U mianie jość kniha — I have a book)",
     "audio_id": "jo"},

    {"cyrillic_upper": "Ж", "cyrillic_lower": "ж", "lacinka": "Ž ž", "ipa": "/ʐ/",
     "example_cyr": "Жыццё", "example_lac": "Žyćcio", "example_eng": "Life", "audio_id": "zh"},

    {"cyrillic_upper": "З", "cyrillic_lower": "з", "lacinka": "Z z", "ipa": "/z/",
     "example_cyr": "Зіма", "example_lac": "Zima", "example_eng": "Winter", "note": "", "audio_id": "z"},

    {"cyrillic_upper": "І", "cyrillic_lower": "і", "lacinka": "I i", "ipa": "/i/, /ʲi/",
     "example_cyr": "Імя", "example_lac": "Imia", "example_eng": "Name", "audio_id": "i"},

    {"cyrillic_upper": "Й", "cyrillic_lower": "й", "lacinka": "J j", "ipa": "/j/",
     "example_cyr": "Край", "example_lac": "Kraj", "example_eng": "Edge / Region", "note": "", "audio_id": "j"},

    {"cyrillic_upper": "К", "cyrillic_lower": "к", "lacinka": "K k", "ipa": "/k/",
     "example_cyr": "Кніга", "example_lac": "Kniha", "example_eng": "Book", "note": "", "audio_id": "k"},

    {"cyrillic_upper": "Л", "cyrillic_lower": "л", "lacinka": "Ł ł / L l", "ipa": "/ɫ/, /lʲ/",
     "example_cyr": "Лес", "example_lac": "Les", "example_eng": "Forest",
     "note": "Hard Л = Ł in Łacinka",
     "audio_id": "l"},

    {"cyrillic_upper": "М", "cyrillic_lower": "м", "lacinka": "M m", "ipa": "/m/",
     "example_cyr": "Маці", "example_lac": "Maci", "example_eng": "Mother", "note": "", "audio_id": "m"},

    {"cyrillic_upper": "Н", "cyrillic_lower": "н", "lacinka": "N n", "ipa": "/n/",
     "example_cyr": "Ноч", "example_lac": "Noč", "example_eng": "Night", "note": "", "audio_id": "n"},

    {"cyrillic_upper": "О", "cyrillic_lower": "о", "lacinka": "O o", "ipa": "/ɔ/",
     "example_cyr": "Сонца", "example_lac": "Sonca", "example_eng": "Sun",
     "note": "Belarusian has akanne — unstressed О is reduced to /a/ in pronunciation and spelling.",
     "audio_id": "o"},

    {"cyrillic_upper": "П", "cyrillic_lower": "п", "lacinka": "P p", "ipa": "/p/",
     "example_cyr": "Птушка", "example_lac": "Ptuška", "example_eng": "Bird", "note": "", "audio_id": "p"},

    {"cyrillic_upper": "Р", "cyrillic_lower": "р", "lacinka": "R r", "ipa": "/r/",
     "example_cyr": "Рака", "example_lac": "Raka", "example_eng": "River",
     "note": "Always hard.", "audio_id": "r"},

    {"cyrillic_upper": "С", "cyrillic_lower": "с", "lacinka": "S s", "ipa": "/s/",
     "example_cyr": "Снег", "example_lac": "Snieh", "example_eng": "Snow", "note": "", "audio_id": "s"},

    {"cyrillic_upper": "Т", "cyrillic_lower": "т", "lacinka": "T t", "ipa": "/t/",
     "example_cyr": "Тыдзень", "example_lac": "Tydzień", "example_eng": "Week", "note": "", "audio_id": "t"},

    {"cyrillic_upper": "У", "cyrillic_lower": "у", "lacinka": "U u", "ipa": "/u/",
     "example_cyr": "Урок", "example_lac": "Urok", "example_eng": "Lesson", "note": "", "audio_id": "u"},

    {"cyrillic_upper": "Ў", "cyrillic_lower": "ў", "lacinka": "Ŭ ŭ", "ipa": "/w/",
     "example_cyr": "Воўк", "example_lac": "Voŭk", "example_eng": "Wolf",
     "note": "Unique to Belarusian! Appears only after vowels — it's the neutralization of /v/ and /l/ when no vowel follows.",
     "audio_id": "w"},

    {"cyrillic_upper": "Ф", "cyrillic_lower": "ф", "lacinka": "F f", "ipa": "/f/",
     "example_cyr": "Фабрыка", "example_lac": "Fabryka", "example_eng": "Factory",
     "note": "Belarusian words rarely use Ф; mostly appears in loanwords.", "audio_id": "f"},

    {"cyrillic_upper": "Х", "cyrillic_lower": "х", "lacinka": "Ch ch", "ipa": "/x/",
     "example_cyr": "Хата", "example_lac": "Chata", "example_eng": "Home / Cottage", "note": "", "audio_id": "ch"},

    {"cyrillic_upper": "Ц", "cyrillic_lower": "ц", "lacinka": "C c", "ipa": "/ts/",
     "example_cyr": "Цацка", "example_lac": "Cacka", "example_eng": "toy",
     "note": "Has a palatalized counterpart Ć (after consonants where palatalization applies).",
     "audio_id": "c"},

    {"cyrillic_upper": "Ч", "cyrillic_lower": "ч", "lacinka": "Č č", "ipa": "/tʂ/",
     "example_cyr": "Час", "example_lac": "Čas", "example_eng": "time",
     "note": "Always hard.", "audio_id": "ch_soft"},

    {"cyrillic_upper": "Ш", "cyrillic_lower": "ш", "lacinka": "Š š", "ipa": "/ʂ/",
     "example_cyr": "Школа", "example_lac": "Škoła", "example_eng": "School", "audio_id": "sh"},

    {"cyrillic_upper": "Ы", "cyrillic_lower": "ы", "lacinka": "Y y", "ipa": "/ɨ/",
     "example_cyr": "Сын", "example_lac": "Syn", "example_eng": "Son", "note": "", "audio_id": "y"},

    {"cyrillic_upper": "Ь", "cyrillic_lower": "ь", "lacinka": "(´)", "ipa": "—",
     "example_cyr": "Соль", "example_lac": "Soĺ", "example_eng": "Salt",
     "note": "Soft sign — has no sound of its own. Marks palatalization of the preceding consonant. In Łacinka, palatalization is shown by an acute on the consonant (ć, ń, ś, ź, ĺ).",
     "audio_id": ""},

    {"cyrillic_upper": "Э", "cyrillic_lower": "э", "lacinka": "E e", "ipa": "/ɛ/",
     "example_cyr": "Еўропа", "example_lac": "Eŭropa", "example_eng": "Europe", "note": "", "audio_id": "e"},

    {"cyrillic_upper": "Ю", "cyrillic_lower": "ю", "lacinka": "Ju ju / iu", "ipa": "/ju/, /ʲu/",
     "example_cyr": "Юг", "example_lac": "Juh", "example_eng": "South",
     "note": "Same iotation pattern as е, ё.", "audio_id": "ju"},

    {"cyrillic_upper": "Я", "cyrillic_lower": "я", "lacinka": "Ja ja / ia", "ipa": "/ja/, /ʲa/",
     "example_cyr": "Яблык", "example_lac": "Jabłyk", "example_eng": "Apple",
     "note": "Same iotation pattern as е, ё, ю.", "audio_id": "ja"},

    {"cyrillic_upper": "'", "cyrillic_lower": "'", "lacinka": "—", "ipa": "—",
     "example_cyr": "Сям'я", "example_lac": "Siamja", "example_eng": "Family",
     "note": "Apostrophe (not a letter; doesn't affect alphabetical order). Separates a consonant from a following iotated vowel, blocking palatalization.",
     "audio_id": ""},
]


DIGRAPHS = [
    {"cyrillic": "Дж дж", "lacinka": "Dž dž", "ipa": "/d͡ʐ/",
     "example_cyr": "джала", "example_lac": "džala", "example_eng": "sting",
     "note": "Single affricate sound. Distinguished from prefix-root combinations like пад-жаць where Д and Ж are separate.",
     "audio_id": "dzh"},
    {"cyrillic": "Дз дз", "lacinka": "Dz dz", "ipa": "/d͡z/",
     "example_cyr": "дзень", "example_lac": "dzień", "example_eng": "day",
     "note": "Single affricate sound. The palatalized form Дзь / Dź is one of Belarusian's most distinctive features (dzekanne).",
     "audio_id": "dz"},
]


HISTORY = """
**Modern form (1918):** The Belarusian alphabet as used today was
standardized in 1918 in Branisłaŭ Taraškievič's grammar. Four letters
that had carried over from earlier Cyrillic conventions were dropped;
four, including the distinctive Ў, were added.

**1933 reform:** The Soviet authorities introduced what came to be
called *Narkamaŭka* — a simplified orthography aligning Belarusian
spelling more closely with Russian phonological patterns and
abolishing the letter Ґ (which had marked /ɡ/ in loanwords).

**Today:** These orthographies coexist, sometimes in contention. 
*Narkamaŭka* is the state standard, used in official media and education within Belarus.
*Taraškievica*, the pre-1933 form, often called "classical"
orthography, is favored by the diaspora, independent publishers,
and parts of the democracy-seeking opposition. The choice between them carries political and identity weight.

**Łacinka (the Latin script):** 
Belarusian was written in the Latin script in publications from
the 16th century onward, especially in Catholic and later
nationalist contexts. It was banned by the Russian Empire from
1859 to 1905, restored thereafter, and used in parallel with
Cyrillic in the early 20th century. Today Łacinka has a small but
active community of users, mostly in cultural, academic, and
diaspora contexts.
"""
