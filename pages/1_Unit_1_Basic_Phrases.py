"""
Page 1 — Basic Phrases.

Renders the phrase data from content.phrases with:
    - Cyrillic primary, Łacinka secondary
    - Register pill (formal / informal / neutral)
    - Cultural-context note where present

Phrases are now organized into categories (Прывітанні / Знаёмства /
Развітанні / Карысныя выразы), each rendered with a Belarusian Cyrillic
header so Belarusian remains the meta-language of instruction.

A scripted conversation widget at the bottom lets the learner practice
the phrases in a short, branching exchange (greeting → name → how-are-
you → goodbye). The partner reacts based on the user's chosen state.
"""

import streamlit as st

from content.phrases import PHRASES
from content.audio import render_audio_or_placeholder
from content.conversation_manager import render_basic_phrases_conversation


def phrase_audio_id(english: str, register: str) -> str:
    """
    Derive a deterministic audio file slug from a phrase's English meaning
    and register. Used so the same phrase always looks for the same file.

    Example:
        "How are you?" + "informal"  ->  "how_are_you_informal"
        "Hello"        + "neutral"   ->  "hello"
    """
    slug = (
        english.lower()
        .replace("?", "")
        .replace(",", "")
        .replace(".", "")
        .replace("'", "")
        .replace("/", "_or_")
        .strip()
        .replace(" ", "_")
    )
    if register != "neutral":
        slug = f"{slug}_{register}"
    return slug


# ---------------------------------------------------------------------------
# CSS (defensive re-injection — same block as in app.py)
# ---------------------------------------------------------------------------

GLOBAL_CSS = """
<style>
.cyrillic { font-size: 1.15em; font-weight: 500; line-height: 1.4; }
.lacinka  { font-size: 0.95em; font-weight: 300; opacity: 0.7; font-style: italic; line-height: 1.4; }
.english  { font-size: 0.85em; opacity: 0.55; line-height: 1.4; }
.be-label { font-weight: 600; opacity: 0.8; cursor: help;
            border-bottom: 1px dotted currentColor; padding-bottom: 1px; }
.translation-line { font-size: 0.9em; opacity: 0.7; margin-top: 0.15em; }
.phrase-block { margin: 0.7em 0 0.4em 0; line-height: 1.5; }
.phrase-row { margin: 0.15em 0; }
.ipa-inline { font-family: 'Charis SIL', 'Lucida Sans Unicode', monospace;
              font-size: 0.92em; opacity: 0.85; }
.register { display: inline-block; font-size: 0.7em; padding: 0.1em 0.55em; border-radius: 999px;
            margin-left: 0.5em; font-weight: 500; letter-spacing: 0.02em; vertical-align: middle; }
.register-formal   { background: rgba(96, 165, 250, 0.2); color: #93c5fd; }
.register-informal { background: rgba(251, 191, 36, 0.2); color: #fcd34d; }
.register-neutral  { background: rgba(156, 163, 175, 0.2); color: #d1d5db; }
.context-note { font-size: 0.88em; opacity: 0.75; line-height: 1.55;
                border-left: 3px solid rgba(156, 163, 175, 0.4); padding-left: 0.85em;
                margin-top: 0.4em; margin-bottom: 0.4em; }
.small-heading { font-size: 0.78em; text-transform: uppercase; letter-spacing: 0.06em;
                 opacity: 0.65; font-weight: 600; margin-top: 0.6em; margin-bottom: 0.2em; }
@media (prefers-color-scheme: dark) {
    .cyrillic { color: #f3f4f6; }
}
</style>
"""
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)




# ---------------------------------------------------------------------------
# Page header
# ---------------------------------------------------------------------------

st.title("Unit 1.1: Basic Phrases")
st.caption("Courtesies and conversation openers")

st.markdown(
    """
    Each phrase appears below in **Cyrillic** and **Łacinka**. 
    Where the language distinguishes formal and informal forms,
    both are shown.

    Click the **Cultural context** expander under any phrase to see what the
    phrase means in context beyond the dictionary definition!
    """
)

st.divider()


# ---------------------------------------------------------------------------
# Renderer for a single form (one Cyrillic + Łacinka + optional context)
# ---------------------------------------------------------------------------

def render_form(form: dict, english: str) -> None:
    """
    Render one Belarusian form using the labeled vertical structure:
        Кірыліца:        <cyrillic>           [register pill]    [🔊 audio]
        Łacinka:         <lacinka>
        Транскрыпцыя:    <ipa>
        (Пераклад на ангельскую мову: "english")

    The Belarusian labels (Кірыліца, Łacinka, Транскрыпцыя, Пераклад на
    ангельскую мову) are themselves hoverable — native browser tooltip
    via the title attr — so a learner who doesn't yet know what those
    words mean can read them by hovering. This keeps Belarusian as the
    meta-language of instruction instead of routing everything through
    English.
    """
    register = form["register"]
    register_pill = (
        f'<span class="register register-{register}">{register}</span>'
    )
    audio_id = phrase_audio_id(english, register)

    # IPA row — only shown if the data has one (defensive against partial
    # entries you might add without IPA later).
    ipa_row = ""
    if form.get("ipa"):
        ipa_row = (
            f'<div class="phrase-row">'
            f'  <span class="be-label" title="Phonetic transcription (IPA)">Транскрыпцыя:</span>'
            f'  <span class="ipa-inline">&nbsp;{form["ipa"]}</span>'
            f'</div>'
        )

    # Two-column layout: phrase block on the left, audio button on the right.
    main_col, audio_col = st.columns([10, 1])

    with main_col:
        st.markdown(
            f'''
            <div class="phrase-block">
              <div class="phrase-row">
                <span class="be-label" title="Cyrillic">Кірыліца:</span>
                <span class="cyrillic">&nbsp;{form["cyrillic"]}</span>
                {register_pill}
              </div>
              <div class="phrase-row">
                <span class="be-label" title="Łacinka — the Belarusian Latin alphabet">Łacinka:</span>
                <span class="lacinka">&nbsp;{form["lacinka"]}</span>
              </div>
              {ipa_row}
              <div class="phrase-row translation-line">
                (<span class="be-label" title="Translation into the English language">Пераклад на ангельскую мову</span>: "{english}")
              </div>
            </div>
            ''',
            unsafe_allow_html=True,
        )

    with audio_col:
        # Vertical alignment with the phrase block — small top margin
        st.markdown('<div style="margin-top: 0.7em;">', unsafe_allow_html=True)
        render_audio_or_placeholder("phrases", audio_id, label="🔊")
        st.markdown('</div>', unsafe_allow_html=True)

    # Cultural context only shown if the entry has one.
    if form.get("context"):
        with st.expander("Cultural context", expanded=False):
            st.markdown(
                f'<div class="context-note">{form["context"]}</div>',
                unsafe_allow_html=True,
            )


# ---------------------------------------------------------------------------
# Main loop — iterate categories (each with a Cyrillic header) and then
# the items within. The category label_cyr is a Belarusian-language
# section header; label_eng appears as a small caption underneath.
# ---------------------------------------------------------------------------

for cat_id, category in PHRASES.items():
    # Cyrillic header for the section + English caption underneath.
    st.markdown(f"## {category['label_cyr']}")
    st.caption(category["label_eng"])
    st.markdown("&nbsp;", unsafe_allow_html=True)

    for entry in category["items"]:
        # English gloss as the sub-header for this phrase entry.
        st.markdown(f"#### {entry['english']}")

        # If there's only one form, render it inline. If there are two
        # (formal/informal), render both — register pairing is part of
        # what we're teaching here.
        for form in entry["forms"]:
            render_form(form, entry["english"])

        st.markdown("&nbsp;", unsafe_allow_html=True)  # small spacer

    st.divider()


st.caption(
    "Note on coverage: this page demonstrates the annotation framework on "
    "courtesy phrases. Full curriculum coverage (phonetics, grammar, extended "
    "vocabulary) follows the same pattern — each unit annotated with register "
    "and cultural context. The category structure (Прывітанні / Знаёмства / "
    "Развітанні / Карысныя выразы) generalizes to any target language: a "
    "native-speaker pass instantiates the cells, the framework stays the same."
)


# ---------------------------------------------------------------------------
# Practice the conversation — uses the conversation_manager engine.
# 4-turn flow: greeting → name (text input) → how-are-you → goodbye.
# Reactive partner reply at goodbye based on user's chosen state.
# "🙋 I don't understand" reveals English on the partner's most recent line.
# ---------------------------------------------------------------------------

st.divider()
st.markdown("## Practice the conversation")
st.caption(
    "A short scripted conversation using the phrases above. Click "
    "responses in Belarusian — toggle between Cyrillic and Łacinka in "
    "the sidebar. If you don't understand the partner's line, click "
    "'I don't understand' for the English translation."
)

# Sidebar orthography toggle. Reuses the same key namespace pattern as
# the rest of the app so multiple pages don't clash.
orthography = st.sidebar.radio(
    "Conversation script:",
    options=["both", "cyrillic", "lacinka"],
    format_func=lambda x: {
        "both": "Both Cyrillic and Łacinka",
        "cyrillic": "Cyrillic only",
        "lacinka": "Łacinka only",
    }[x],
    key="bp_convo_orthography",
)

render_basic_phrases_conversation(orthography=orthography)
