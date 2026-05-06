"""
Page 2 — Phrases in Context.

Renders the three dialogues (Hrodna, Minsk, Stročycy) with:
    - Setting + register note up top
    - Turn-by-turn rendering: speaker, Cyrillic, Łacinka, English, optional note
    - Optional 🎤 Whisper recording widget per turn so the learner can
      practice saying each line and see what Whisper transcribes
    - Full cultural-context paragraph in an expander at the bottom
"""

import streamlit as st

from content.dialogues import DIALOGUES
from content.orthography import (
    render_orthography_picker,
    show_cyrillic,
    show_lacinka,
)
from content.transcription import render_transcription_widget


# ---------------------------------------------------------------------------
# CSS (defensive re-injection)
# ---------------------------------------------------------------------------

GLOBAL_CSS = """
<style>
.cyrillic { font-size: 1.1em; font-weight: 500; line-height: 1.5; }
.lacinka  { font-size: 0.92em; font-weight: 300; opacity: 0.7; font-style: italic; line-height: 1.5; }
.english  { font-size: 0.85em; opacity: 0.55; line-height: 1.5; }
.context-note { font-size: 0.88em; opacity: 0.75; line-height: 1.55;
                border-left: 3px solid rgba(156, 163, 175, 0.4); padding-left: 0.85em;
                margin-top: 0.4em; margin-bottom: 0.4em; }
.speaker { font-size: 0.7em; text-transform: uppercase; letter-spacing: 0.1em;
           opacity: 0.55; font-weight: 600; margin-bottom: 0.15em; }
.turn-block { margin-bottom: 1.2em; padding-left: 0.5em; border-left: 2px solid transparent; }
.turn-you      { border-left-color: rgba(147, 197, 253, 0.6); padding-left: 0.85em; }
.turn-other    { border-left-color: rgba(252, 211, 77, 0.6); padding-left: 0.85em; }
.setting-block { background: rgba(156, 163, 175, 0.08); border-radius: 6px; padding: 0.9em 1.1em;
                 font-size: 0.92em; opacity: 0.92; margin-bottom: 1em; }
.register-line { font-size: 0.85em; opacity: 0.7; font-style: italic;
                 margin-bottom: 0.6em; }
</style>
"""
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Page header
# ---------------------------------------------------------------------------

st.title("Unit 1.2 — Phrases in Context")
st.caption("Three short dialogues anchored in real Belarusian places")

# Sidebar toggle — choose which scripts to display.
ortho = render_orthography_picker()

st.markdown(
    """
    These dialogues use the phrases from the previous page in actual
    exchanges. Each is set somewhere specific — Hrodna, Minsk,
    Стpoчыцы — and built around real cultural references (food, festival,
    literature).

    Watch how the same courtesy phrases shift in feel depending on the
    setting and the relationship between speakers. That shift *is* the
    cultural context being taught.

    Each turn has an optional 🎤 record-yourself button — say the line
    out loud and Whisper will transcribe it back so you can compare.
    """
)

st.divider()


# ---------------------------------------------------------------------------
# Dialogue selector
# ---------------------------------------------------------------------------

dialogue_titles = [d["title"] for d in DIALOGUES]
selected_title = st.radio(
    "Choose a dialogue:",
    dialogue_titles,
    horizontal=False,
    label_visibility="collapsed",
)
dialogue = next(d for d in DIALOGUES if d["title"] == selected_title)


# ---------------------------------------------------------------------------
# Dialogue rendering
# ---------------------------------------------------------------------------

# Title + setting + register
st.markdown(f"### {dialogue['title']}")
st.markdown(
    f'<div class="setting-block">{dialogue["setting"]}</div>',
    unsafe_allow_html=True,
)
st.markdown(
    f'<div class="register-line">Register: {dialogue["register_note"]}</div>',
    unsafe_allow_html=True,
)
st.markdown("---")

# Each turn — render text + Whisper widget. The widget is wrapped in an
# expander so it doesn't clutter the dialogue flow; learners can open it
# only when they want to practice that specific line.
for turn_idx, turn in enumerate(dialogue["turns"]):
    speaker_class = "turn-you" if turn["speaker"] == "you" else "turn-other"
    speaker_label = turn["speaker"].upper()

    parts = [f'<div class="speaker">{speaker_label}</div>']
    if show_cyrillic(ortho):
        parts.append(f'<div class="cyrillic">{turn["cyrillic"]}</div>')
    if show_lacinka(ortho):
        parts.append(f'<div class="lacinka">{turn["lacinka"]}</div>')
    parts.append(f'<div class="english">— {turn["english"]}</div>')

    st.markdown(
        f'<div class="turn-block {speaker_class}">' + "".join(parts) + "</div>",
        unsafe_allow_html=True,
    )

    if turn.get("note"):
        st.markdown(
            f'<div class="context-note">{turn["note"]}</div>',
            unsafe_allow_html=True,
        )

    # Whisper recording widget for this turn. Targets the Cyrillic.
    # Key includes dialogue id + turn index so each widget is unique.
    render_transcription_widget(
        target_text=turn["cyrillic"],
        key_suffix=f"dialogue_{dialogue['id']}_turn_{turn_idx}",
        target_label="Target line",
    )

# Full cultural-context paragraph
st.markdown("---")
with st.expander("Cultural context — what's happening here", expanded=True):
    st.markdown(dialogue["cultural_context"])
