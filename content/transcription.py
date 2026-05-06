"""
Shared speech recording + transcription helper for Calla.

Used by any page that wants to let a learner record themselves saying a
target word or phrase and see what Whisper transcribes back. Wraps:

    - streamlit-mic-recorder for browser audio capture
    - openai-whisper (local) for transcription
    - Loose-match comparison so minor differences don't read as failure

The helper degrades gracefully: if either dependency is missing, the
widget shows install instructions instead of crashing the page.

Usage from a page:

    from content.transcription import render_transcription_widget

    render_transcription_widget(
        target_text="Прывітанне",
        key_suffix="alphabet_practice_1",  # must be unique per widget on page
        target_label="Target",             # optional; defaults to "Target"
        helper_caption=None,               # optional override for the caption
    )

The widget renders inside an st.expander labeled "Try saying it" and
handles its own state. No return value — it's purely a side-effect UI
component.
"""

import os
import re
import tempfile

import streamlit as st


# ---------------------------------------------------------------------------
# Optional dependency probes — done at import time so the helper can show
# clean install instructions instead of crashing pages.
# ---------------------------------------------------------------------------

try:
    from streamlit_mic_recorder import mic_recorder
    _MIC_AVAILABLE = True
except ImportError:
    _MIC_AVAILABLE = False
    mic_recorder = None  # type: ignore

try:
    import whisper as _whisper_check  # noqa: F401  -- presence check only
    _WHISPER_AVAILABLE = True
except ImportError:
    _WHISPER_AVAILABLE = False


# ---------------------------------------------------------------------------
# Whisper model loading — cached for the session so the model loads once.
# ---------------------------------------------------------------------------

@st.cache_resource(show_spinner="Loading Whisper model (one-time, ~244 MB for 'small')...")
def _load_whisper_model(size: str = "small"):
    """
    Load and cache a Whisper model. First call downloads the model into
    ~/.cache/whisper; subsequent calls return the cached instance.

    Sizes: 'tiny' (~39 MB), 'base' (~74 MB), 'small' (~244 MB),
           'medium' (~769 MB), 'large' (~1.5 GB)

    For Belarusian, 'small' is a reasonable demo default. Bump to 'medium'
    if accuracy disappoints; the trade-off is download size and inference
    speed (10–30 sec per clip on CPU vs. 5–15 sec for 'small').
    """
    import whisper
    return whisper.load_model(size)


# ---------------------------------------------------------------------------
# Comparison helpers
# ---------------------------------------------------------------------------

def _normalize_for_compare(text: str) -> str:
    """Loose normalization for matching transcription against target."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", "", text, flags=re.UNICODE)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# ---------------------------------------------------------------------------
# Public API — the widget
# ---------------------------------------------------------------------------

def render_transcription_widget(
    target_text: str,
    *,
    key_suffix: str,
    target_label: str = "Target",
    helper_caption: str | None = None,
    expander_label: str = "🎤 Try saying it (optional — uses local speech recognition)",
    expanded: bool = False,
    model_size: str = "small",
    language_code: str = "be",
) -> None:
    """
    Render a self-contained recording + transcription widget.

    Args:
        target_text: the Cyrillic / Łacinka text the learner is trying to say
        key_suffix: a unique key fragment so multiple widgets on a page don't
                    collide. Should change when target_text changes (the
                    recorder caches by key, so a stale key means the previous
                    recording lingers).
        target_label: header above the target column. Default "Target".
        helper_caption: optional override for the caption beneath the
                        recorder. Defaults to a sensible Belarusian-aware
                        explanation.
        expander_label: text shown on the expander.
        expanded: whether the expander is open by default.
        model_size: Whisper model size ('tiny' to 'large').
        language_code: ISO language hint passed to Whisper. Defaults to 'be'
                       (Belarusian); other low-resource languages just need
                       a different hint here.
    """
    with st.expander(expander_label, expanded=expanded):
        # -- Setup gate ---------------------------------------------------
        if not _MIC_AVAILABLE or not _WHISPER_AVAILABLE:
            missing = []
            if not _MIC_AVAILABLE:
                missing.append("streamlit-mic-recorder")
            if not _WHISPER_AVAILABLE:
                missing.append("openai-whisper")
            st.warning(
                "Speech features need additional setup. Run:\n\n"
                f"```\npip install {' '.join(missing)}\n```\n\n"
                "You'll also need **ffmpeg** installed on your system "
                "(`winget install ffmpeg` on Windows, or download from "
                "https://ffmpeg.org). The first transcription will download "
                "the Whisper model (~244 MB for 'small')."
            )
            return

        # -- Caption ------------------------------------------------------
        if helper_caption is None:
            helper_caption = (
                "Click the microphone, say the word out loud, then click stop. "
                "Transcription quality varies — Belarusian is a low-resource "
                "language for Whisper, so don't take a mismatch as failure."
            )
        st.caption(helper_caption)

        # -- Recorder -----------------------------------------------------
        # Key is critical: must be unique per widget on the page, AND must
        # change when the target changes (so a stale recording from the
        # previous word doesn't get re-transcribed).
        audio = mic_recorder(
            start_prompt="🎤 Record",
            stop_prompt="⏹ Stop",
            just_once=False,
            use_container_width=True,
            key=f"transcribe_{key_suffix}",
        )

        if not (audio and audio.get("bytes")):
            return

        # -- Transcribe ---------------------------------------------------
        transcription = None
        with st.spinner("Transcribing... (5–30 sec on CPU)"):
            # Write recorded bytes to a temp file. The mic_recorder
            # returns webm-format audio, which Whisper decodes via ffmpeg.
            with tempfile.NamedTemporaryFile(
                suffix=".webm", delete=False
            ) as f:
                f.write(audio["bytes"])
                temp_path = f.name

            try:
                model = _load_whisper_model(model_size)
                # Pass language hint so Whisper doesn't misdetect a short
                # utterance as Russian / Ukrainian / Polish.
                result = model.transcribe(temp_path, language=language_code)
                transcription = result["text"].strip()
            except Exception as e:
                st.error(
                    f"Transcription failed: {e}\n\n"
                    "Most common cause: ffmpeg not installed or not on PATH."
                )
            finally:
                try:
                    os.unlink(temp_path)
                except OSError:
                    pass

        if transcription is None:
            return

        # -- Side-by-side compare ----------------------------------------
        target_norm = _normalize_for_compare(target_text)
        heard_norm = _normalize_for_compare(transcription)

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"**{target_label}**")
            st.markdown(
                f'<div style="font-size:1.3em; font-weight:500;">{target_text}</div>',
                unsafe_allow_html=True,
            )
        with col_b:
            st.markdown("**Whisper heard**")
            st.markdown(
                f'<div style="font-size:1.3em; font-weight:500;">'
                f'{transcription if transcription else "(silence)"}'
                f"</div>",
                unsafe_allow_html=True,
            )

        if not transcription:
            st.info("No speech detected — try recording again, closer to the mic.")
        elif heard_norm == target_norm:
            st.success("Match! Whisper heard the same word.")
        else:
            st.info(
                "Doesn't quite match — but Whisper's Belarusian is "
                "imperfect. Use this as a rough check, not a verdict."
            )
