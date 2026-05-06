"""
Audio infrastructure.

The app looks for audio files at conventional paths:
    static/audio/letters/{audio_id}.mp3   — alphabet sound (IPA)
    static/audio/words/{audio_id}.mp3     — example word for that letter
    static/audio/phrases/{phrase_id}.mp3  — basic phrases

If a file exists, we render a Streamlit st.audio control inline.
If not, we render a small "(coming soon)" placeholder so the UI is
visibly intact and the file convention is obvious.

This separation lets Nya record audio at her own pace — drop files
into the right folders and they go live automatically. No code
changes needed.
"""

from pathlib import Path

import streamlit as st


# Project root is the parent of `content/`. Audio lives at
# project_root/static/audio/...
_AUDIO_ROOT = Path(__file__).resolve().parent.parent / "static" / "audio"


def audio_path(category: str, audio_id: str) -> Path:
    """
    Build the canonical audio path for a given category and id.
    Categories: 'letters', 'words', 'phrases'.
    """
    return _AUDIO_ROOT / category / f"{audio_id}.mp3"


def has_audio(category: str, audio_id: str) -> bool:
    """True if a recording exists for this category/id."""
    if not audio_id:
        return False
    return audio_path(category, audio_id).is_file()


def render_audio_or_placeholder(
    category: str,
    audio_id: str,
    label: str = "🔊",
) -> None:
    """
    Render an inline audio control if the file exists, else a small
    placeholder showing where the file would go.

    Wrap in a popover so the audio control doesn't blow up the layout
    when a row has 32 of these on a page.
    """
    if not audio_id:
        return  # silently skip — used for things like the soft sign

    if has_audio(category, audio_id):
        with st.popover(label, use_container_width=False):
            st.audio(str(audio_path(category, audio_id)))
    else:
        st.markdown(
            f'<span class="audio-placeholder" '
            f'title="Audio file expected at static/audio/{category}/{audio_id}.mp3">'
            f'{label}</span>',
            unsafe_allow_html=True,
        )
