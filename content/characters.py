"""
Conversation partner characters — minimal version.

Per Nya's request: gender details kept, but no character images,
descriptions, or clothing. The CHARACTERS dict carries only the
fields the helpers (and the Conversation Partner page indicators)
actually need: emoji, names, and grammatical-gender label.
"""

CHARACTERS = {
    "girl": {
        "id": "girl",
        "emoji": "👩",
        "name_cyr": "Дзяўчына",
        "name_lac": "Dziaŭčyna",
        "name_eng": "Girl / young woman",
        "grammar": "feminine",
    },
    "boy": {
        "id": "boy",
        "emoji": "👨",
        "name_cyr": "Хлопец",
        "name_lac": "Chłopiec",
        "name_eng": "Boy / young man",
        "grammar": "masculine",
    },
}


# Cultural callout content — about Belarusian grammatical gender.
GENDERED_LANGUAGE_NOTE = """
**Belarusian is a grammatically gendered language.** Verbs in the past
tense, adjectives, and certain pronouns change form depending on the
gender of the speaker (or the noun being modified).

For example, "I went" is:
- **Я пайшоў** (Ja pajšoŭ) — masculine speaker
- **Я пайшла** (Ja pajšla) — feminine speaker

The same is true for many adjectives:
- **Я рады** (Ja rady) — "I'm glad" (masculine)
- **Я рада** (Ja rada) — "I'm glad" (feminine)

In the present and future tenses, most verb forms are gender-neutral
(e.g., **я разумею** "I understand" works for everyone). Gender most
often surfaces in past-tense verbs and predicate adjectives.
"""

# Stub for non-binary considerations — Nya will fill in with research.
NONBINARY_NOTE = """
**Non-binary speakers and Belarusian grammatical gender.**

East Slavic languages including Belarusian assume a binary gender
system in their verb morphology, which presents a real navigation
challenge for non-binary speakers. Strategies vary across the
Belarusian-speaking community and are an active area of discussion.
"""


# Map scenario keys (from conversation_scripts.SCENARIOS) to which
# character(s) appear. Used to render the right indicator and grammar
# callout per scenario.
SCENARIO_CHARACTERS = {
    "hrodna_market":      ["girl"],
    "minsk_cafe":         ["boy"],
    "strochitsy_kupalle": ["girl", "boy"],
}


def scenario_speaker_indicator(scenario_key: str) -> str:
    """Compact emoji + label for the character(s) in a scenario."""
    char_ids = SCENARIO_CHARACTERS.get(scenario_key, [])
    if len(char_ids) == 0:
        return ""
    parts = []
    for cid in char_ids:
        ch = CHARACTERS[cid]
        parts.append(f'{ch["emoji"]} {ch["name_eng"]}')
    return " · ".join(parts)


def scenario_grammar_note(scenario_key: str) -> str:
    """Short grammar-form note for the speaker(s) in a scenario."""
    char_ids = SCENARIO_CHARACTERS.get(scenario_key, [])
    if len(char_ids) == 0:
        return ""
    forms = []
    for cid in char_ids:
        ch = CHARACTERS[cid]
        forms.append(
            f"the {ch['name_eng'].lower()} uses **{ch['grammar']}** grammatical forms"
        )
    return "In this scenario, " + ", and ".join(forms) + "."
