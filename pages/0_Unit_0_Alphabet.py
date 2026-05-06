"""
Unit 0 — Alphabet.

Renders the Belarusian alphabet as a clean grid:
    Cyrillic | Łacinka | IPA | 🔊 | Example word | 🔊

The audio buttons use the audio helper — if a recording exists for
the given letter or word, the button plays it inline (via Streamlit
popover); otherwise, a small placeholder shows where the file would go.

The orthography toggle is intentionally NOT used here. The point of
this page is to *show all three* (Cyrillic, Łacinka, IPA) at once.
That's the lesson: the alphabet has multiple legitimate renderings,
and seeing them aligned is the framework being taught.

A practice drill at the bottom pulls a random word from the alphabet
+ phrase pool and offers a Whisper-powered "say it out loud" widget
so the learner can compare what they said to the target.
"""

import random

import streamlit as st

from content.alphabet import ALPHABET, DIGRAPHS, HISTORY
from content.audio import render_audio_or_placeholder
from content.phrases import PHRASES
from content.transcription import render_transcription_widget


# ---------------------------------------------------------------------------
# CSS — page-specific styling for the alphabet grid
# ---------------------------------------------------------------------------

ALPHABET_CSS = """
<style>
/* Defensive contrast: explicit colors per OS color scheme.
   Streamlit's --text-color doesn't always propagate into custom HTML
   injected via unsafe_allow_html, so we set values directly here. */
.cyr-letter {
    color: #1f2937;
    font-size: 1.7em;
    font-weight: 600;
    line-height: 1;
    text-align: center;
}
.lac-letter {
    font-size: 1.05em;
    font-weight: 400;
    opacity: 0.7;
    font-style: italic;
    text-align: center;
}
.ipa-cell {
    color: #1f2937;
    font-family: 'Charis SIL', 'Lucida Sans Unicode', monospace;
    font-size: 0.95em;
    opacity: 0.9;
    text-align: center;
}
.example-cyr {
    color: #1f2937;
    font-size: 1em;
    font-weight: 500;
}
.example-lac {
    font-size: 0.85em;
    opacity: 0.7;
    font-style: italic;
}
.example-eng {
    font-size: 0.78em;
    opacity: 0.55;
}
.note-cell {
    font-size: 0.82em;
    opacity: 0.75;
    line-height: 1.5;
    border-left: 3px solid rgba(156, 163, 175, 0.4);
    padding-left: 0.7em;
    margin: 0.4em 0 0.6em 0;
}
.audio-placeholder {
    opacity: 0.3;
    font-size: 0.95em;
    cursor: help;
}
.col-header {
    font-size: 0.7em;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    opacity: 0.65;
    font-weight: 600;
    padding-bottom: 0.5em;
    border-bottom: 2px solid rgba(156, 163, 175, 0.25);
    margin-bottom: 0.3em;
}

/* Dark-mode override — kicks in when the OS / browser is in dark mode. */
@media (prefers-color-scheme: dark) {
    .cyr-letter   { color: #f3f4f6; }
    .ipa-cell     { color: #e5e7eb; }
    .example-cyr  { color: #f3f4f6; }
}
</style>
"""

st.markdown(ALPHABET_CSS, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Stork (busel) image — appears above the alphabet title.
# Drop a file at static/images/stork.png to make this render.
# ---------------------------------------------------------------------------
# from content.images import render_image_or_placeholder

# # Center using three columns: small | image | small.
# # The middle column is wider, so the image sits centered.
# left, center, right = st.columns([1, 2, 1])
# with center:
#     render_image_or_placeholder(
#         "static/images/stork.png",
#         description="a stork (busel) flying",
#         use_container_width=True,
#     )


# ---------------------------------------------------------------------------
# Page header
# ---------------------------------------------------------------------------

st.title("Unit 0: Alphabet")
st.caption("32 letters of the modern Belarusian alphabet, in Cyrillic and Łacinka, with IPA and example words")

st.markdown(
    """
    Each row shows a letter in **Cyrillic**, its **Łacinka** equivalent,
    its **IPA** transcription, and an **example word**. 
    **Hint**: Click the 🔊 buttons to hear pronunication!
    """
)

st.divider()


# ---------------------------------------------------------------------------
# Column header
# ---------------------------------------------------------------------------

# Six columns: Cyrillic | Łacinka | IPA | 🔊 sound | Example | 🔊 word
HEADER_COLS = [1.2, 1.2, 1.5, 0.6, 3.0, 0.6]

cols = st.columns(HEADER_COLS)
for col, label in zip(
    cols,
    ["Cyrillic", "Łacinka", "IPA", "🔊", "Example word", "🔊"],
):
    col.markdown(f'<div class="col-header">{label}</div>', unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Letter rows
# ---------------------------------------------------------------------------

def render_letter_row(letter: dict, is_apostrophe: bool = False) -> None:
    """Render one alphabet row. Apostrophe gets slightly different formatting."""
    cols = st.columns(HEADER_COLS)

    # Cyrillic — uppercase + lowercase
    if is_apostrophe:
        cols[0].markdown(
            f'<div class="cyr-letter">{letter["cyrillic_upper"]}</div>',
            unsafe_allow_html=True,
        )
    else:
        cols[0].markdown(
            f'<div class="cyr-letter">{letter["cyrillic_upper"]} {letter["cyrillic_lower"]}</div>',
            unsafe_allow_html=True,
        )

    # Łacinka
    cols[1].markdown(
        f'<div class="lac-letter">{letter["lacinka"]}</div>',
        unsafe_allow_html=True,
    )

    # IPA
    cols[2].markdown(
        f'<div class="ipa-cell">{letter["ipa"]}</div>',
        unsafe_allow_html=True,
    )

    # Audio button for the letter sound
    with cols[3]:
        render_audio_or_placeholder("letters", letter["audio_id"], label="🔊")

    # Example word — Cyrillic, Łacinka, English on three lines
    cols[4].markdown(
        f'<div class="example-cyr">{letter["example_cyr"]}</div>'
        f'<div class="example-lac">{letter["example_lac"]}</div>'
        f'<div class="example-eng">— {letter["example_eng"]}</div>',
        unsafe_allow_html=True,
    )

    # Audio button for the example word
    with cols[5]:
        render_audio_or_placeholder("words", letter["audio_id"], label="🔊")

    # Note row (full width) — only if there's a note
    if letter.get("note"):
        st.markdown(
            f'<div class="note-cell">{letter["note"]}</div>',
            unsafe_allow_html=True,
        )


for letter in ALPHABET:
    is_apos = letter["cyrillic_upper"] == "'"
    render_letter_row(letter, is_apostrophe=is_apos)


# ---------------------------------------------------------------------------
# Digraphs
# ---------------------------------------------------------------------------

st.divider()

st.markdown("### Digraphs — Дж and Дз")
st.caption("Common letter combinations that represent distinctive sounds")

for dg in DIGRAPHS:
    cols = st.columns(HEADER_COLS)
    cols[0].markdown(
        f'<div class="cyr-letter">{dg["cyrillic"]}</div>',
        unsafe_allow_html=True,
    )
    cols[1].markdown(
        f'<div class="lac-letter">{dg["lacinka"]}</div>',
        unsafe_allow_html=True,
    )
    cols[2].markdown(
        f'<div class="ipa-cell">{dg["ipa"]}</div>',
        unsafe_allow_html=True,
    )
    with cols[3]:
        render_audio_or_placeholder("letters", dg["audio_id"], label="🔊")
    cols[4].markdown(
        f'<div class="example-cyr">{dg["example_cyr"]}</div>'
        f'<div class="example-lac">{dg["example_lac"]}</div>'
        f'<div class="example-eng">— {dg["example_eng"]}</div>',
        unsafe_allow_html=True,
    )
    with cols[5]:
        render_audio_or_placeholder("words", dg["audio_id"], label="🔊")

    if dg.get("note"):
        st.markdown(
            f'<div class="note-cell">{dg["note"]}</div>',
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------------------------
# History section
# ---------------------------------------------------------------------------

st.divider()

with st.expander("History (orthographic reforms and the Łacinka tradition)", expanded=False):
    st.markdown(HISTORY)


# ===========================================================================
# Practice — pronounce-the-word drill.
#
# Renders a random word from the alphabet + phrases pool. The student says
# it out loud, optionally records via Whisper, and reveals the answer to
# check.
#
# Word pool combines:
#   - example words from each alphabet entry (cyrillic + lacinka + english,
#     no per-word IPA stored on alphabet entries)
#   - phrase forms from Basic Phrases (cyrillic + lacinka + ipa + english)
#
# The pool rebuilds automatically as you edit alphabet.py / phrases.py —
# nothing here needs touching when you change example words.
# ===========================================================================

st.divider()
st.markdown("### Practice — pronounce the word")
st.caption(
    "A random word from the material so far. Look at the Cyrillic, "
    "say it out loud, then reveal to check yourself."
)


def _build_practice_pool():
    """Combine example words (alphabet) + phrase forms into one pool."""
    pool = []
    # Alphabet example words — no per-word IPA is stored here.
    for letter in ALPHABET:
        if letter.get("example_cyr"):
            pool.append({
                "cyr": letter["example_cyr"],
                "lac": letter.get("example_lac", ""),
                "ipa": "",
                "eng": letter.get("example_eng", ""),
            })
    # Phrase forms — these have full IPA. Walk the categorized structure
    # by flattening across every category's items.
    for category in PHRASES.values():
        for entry in category["items"]:
            for form in entry["forms"]:
                pool.append({
                    "cyr": form["cyrillic"],
                    "lac": form["lacinka"],
                    "ipa": form.get("ipa", ""),
                    "eng": entry["english"],
                })
    return pool


practice_pool = _build_practice_pool()

# Initialize session state for the drill — survives reruns (button clicks)
# but resets when the user reloads or navigates away.
if "practice_word" not in st.session_state:
    st.session_state.practice_word = random.choice(practice_pool)
if "practice_revealed" not in st.session_state:
    st.session_state.practice_revealed = False
if "practice_count" not in st.session_state:
    st.session_state.practice_count = 0

word = st.session_state.practice_word

# Display the Cyrillic prompt — large, centered, lots of breathing room.
st.markdown(
    f'<div style="text-align:center; font-size:2.4em; font-weight:600; '
    f'padding: 1.2em 0 0.8em 0; letter-spacing: 0.02em;">'
    f'{word["cyr"]}</div>',
    unsafe_allow_html=True,
)

# Whisper recording widget — uses the shared helper so the same code path
# is used here, in Phrases in Context, and anywhere else that wants
# transcription. The key_suffix includes practice_count so the recorder
# resets when the user clicks "Next word".
render_transcription_widget(
    target_text=word["cyr"],
    key_suffix=f"alphabet_practice_{st.session_state.practice_count}",
)

# Reveal panel — only shown after the user has tried.
if st.session_state.practice_revealed:
    reveal_lines = []
    if word["lac"]:
        reveal_lines.append(f'**Łacinka:** _{word["lac"]}_')
    if word["ipa"]:
        reveal_lines.append(f'**IPA:** {word["ipa"]}')
    if word["eng"]:
        reveal_lines.append(f'**English:** {word["eng"]}')
    st.success("  \n".join(reveal_lines))
else:
    if st.button("Reveal", use_container_width=True, key="practice_reveal"):
        st.session_state.practice_revealed = True
        st.rerun()

# Next-word button — always available so the student can skip.
if st.button("Next word ▸", use_container_width=True, key="practice_next"):
    # Pick a fresh word; avoid showing the same one twice in a row.
    new_word = random.choice(practice_pool)
    attempts = 0
    while new_word["cyr"] == word["cyr"] and attempts < 10:
        new_word = random.choice(practice_pool)
        attempts += 1
    st.session_state.practice_word = new_word
    st.session_state.practice_revealed = False
    st.session_state.practice_count += 1
    st.rerun()

st.caption(f"Words seen this session: {st.session_state.practice_count}")
