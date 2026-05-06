"""
Calla — Context-Aware Language Learning
Landing page (Page 0): Why Belarusian + How to read this app.

Streamlit's multipage convention:
    app.py is the entry point.
    Files in pages/ become additional pages, ordered by their numeric prefix
    and labeled by the rest of the filename.

This file also injects the small bit of custom CSS that the rest of the
pages rely on for rendering Cyrillic and Łacinka side by side.
"""

import streamlit as st


# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
# Only the entry-point file should call set_page_config; subpages inherit it
# from the same Streamlit session, but each page can override its own title.
st.set_page_config(
    page_title="CALLA",
    page_icon="🌱",
    layout="centered",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------------------------
# Global CSS — kept minimal. Streamlit's defaults do most of the work.
# The one styling choice that is *load-bearing* for the pedagogy is the
# Cyrillic-primary / Łacinka-secondary visual hierarchy.
# ---------------------------------------------------------------------------
GLOBAL_CSS = """
<style>
/* Cyrillic — primary script. Inherits the theme's text color so it stays
   readable in both light and dark mode. */
.cyrillic {
    font-size: 1.15em;
    font-weight: 500;
    line-height: 1.4;
}

/* Łacinka — secondary script. Lower opacity (works in both themes),
   italic to mark it as a parallel rendering, not a translation. */
.lacinka {
    font-size: 0.95em;
    font-weight: 300;
    opacity: 0.7;
    font-style: italic;
    line-height: 1.4;
}

/* English gloss — most muted; meant to be read as support, not the
   primary text. Opacity-based so it adapts to either theme. */
.english {
    font-size: 0.85em;
    opacity: 0.55;
    line-height: 1.4;
}

/* Belarusian-language labels (Кірыліца:, Łacinka:, Пераклад...).
   The label is hoverable — native browser tooltip via `title` attr —
   to teach the meaning of the label itself. */
.be-label {
    font-weight: 600;
    opacity: 0.8;
    cursor: help;
    border-bottom: 1px dotted currentColor;
    padding-bottom: 1px;
}

/* Translation row sits in parentheses, slightly muted. */
.translation-line {
    font-size: 0.9em;
    opacity: 0.7;
    margin-top: 0.15em;
}

/* Phrase block — vertical group of label rows. */
.phrase-block {
    margin: 0.7em 0 0.4em 0;
    line-height: 1.5;
}
.phrase-row {
    margin: 0.15em 0;
}

/* Register pill — small inline marker. Three variants. */
.register {
    display: inline-block;
    font-size: 0.7em;
    padding: 0.1em 0.55em;
    border-radius: 999px;
    margin-left: 0.5em;
    font-weight: 500;
    letter-spacing: 0.02em;
    vertical-align: middle;
}
.register-formal   { background: rgba(96, 165, 250, 0.2); color: #93c5fd; }
.register-informal { background: rgba(251, 191, 36, 0.2); color: #fcd34d; }
.register-neutral  { background: rgba(156, 163, 175, 0.2); color: #d1d5db; }

/* Cultural-context note styling — meant to feel like marginalia. */
.context-note {
    font-size: 0.88em;
    opacity: 0.75;
    line-height: 1.55;
    border-left: 3px solid rgba(156, 163, 175, 0.4);
    padding-left: 0.85em;
    margin-top: 0.4em;
    margin-bottom: 0.4em;
}

/* Speaker label inside dialogues. */
.speaker {
    font-size: 0.75em;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    opacity: 0.6;
    font-weight: 600;
    margin-bottom: 0.2em;
}

/* Small heading used inside expanders / cards. */
.small-heading {
    font-size: 0.78em;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    opacity: 0.65;
    font-weight: 600;
    margin-top: 0.6em;
    margin-bottom: 0.2em;
}
</style>
"""

st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Page content
# ---------------------------------------------------------------------------

# Logo + title side by side. The columns split the row so the calla
# illustration sits to the left of the title text.
title_col1, title_col2 = st.columns([1, 6], vertical_alignment="center")
with title_col1:
    st.image("static/images/calla.png", width=90)
with title_col2:
    st.title("CALLA: Беларуская Мова")

st.caption("**C**ontext-**A**ware **L**anguage **L**earning **A**pplication *(a prototype)*")

st.markdown(
    """
    ## Беларуская мова / Biełaruskaja mova 
    ### *The Belarusian Language*

    Belarusian has a deep literary tradition (Kupala,
    Kolas, Bahdanovič, and Bykaŭ, to name a few), has been historically written
    in three scrips (Cyrillic, Łacinka, and - at one point - Arabic), and originates from a country known
    for its rich culture, history, and nature (also referred to as "the lungs of Europe"). 
    Due to the current (and historic) political and social climate in Belarus, speaking
    Belarusian has additional layers of meaning and significance beyond the linguistic itself.
    """
)

st.divider()

st.markdown(
    """
    ### Getting oriented

    Phrases appear in two scripts and three labeled rows. Each Belarusian
    label has its own meaning — hover the label to see what it says in English.
    """
)

# Example phrase block — same markup pattern used everywhere phrases appear.
st.markdown(
    """
    <div class="phrase-block">
      <div class="phrase-row">
        <span class="be-label" title="Cyrillic">Кірыліца:</span>
        <span class="cyrillic">&nbsp;Прывітанне</span>
      </div>
      <div class="phrase-row">
        <span class="be-label" title="Łacinka — the Belarusian Latin alphabet">Łacinka:</span>
        <span class="lacinka">&nbsp;Pryvitannie</span>
      </div>
      <div class="phrase-row translation-line">
        (<span class="be-label" title="Translation into the English language">Пераклад на ангельскую мову</span>: "Hello")
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    **Cyrillic** is the primary orthography. **Łacinka** — the Belarusian Latin
    alphabet — is also present, but appears less frequently in modern usage. 
    Choose whichever you find easier
    to read; ideally, learn to read both.

    Phrases are annotated with **register** (formal / informal / neutral) and
    with **cultural context** wherever the phrase carries meaning beyond its
    dictionary translation.
    """,
)

st.markdown(
    """
    ### What's in here

    **Unit 0: Alphabet.** The Belarusian alphabet in Cyrillic, Łacinka, and
    IPA transliteration, with click-to-hear sounds and example words.

    **Unit 1: Basic conversation.** Three connected pages:

    - *Basic Phrases*: Courtesies and conversation openers, with both
      orthographies, register, and cultural notes.
    - *Phrases in Context*: Three short dialogues built around cultural references.
    - *Conversation Partner*: Practice the phrases in a guided exchange
      with a scripted partner, in three difficulty modes.

    """
)

st.divider()

st.caption(
    "This prototype was built as a demonstration of context-aware "
    "pedagogy. Comments, criticism, and "
    "collaboration welcome."
)
