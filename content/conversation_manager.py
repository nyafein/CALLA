"""
Conversation manager — a small state machine that drives the structured
Basic Phrases dialogue.

Engine is rule-based. It reads CONVERSATION_SCRIPT (a list of step dicts)
and renders the appropriate UI for each step:
    - "buttons" steps offer 2-4 button responses, each tagged good/bad.
    - "text_with_template" steps offer a free text input wrapped in a
      template (e.g. user types "Анна" → "Мяне завуць Анна").

User can always click "🙋 I don't understand" to reveal the English
translation of the partner's current line.

Why no LLM here:
    The flow is fully scripted. Adding an LLM would (a) require Belarusian-
    capable inference (rare in small models), (b) introduce latency and
    failure modes, and (c) buy nothing pedagogically — the conversation is
    *meant* to be tightly structured.

If you later want richer behavior (free-form responses, off-script turns),
add an LLM hook at handle_response() — but ship the rule-based version
first because it's reliable and demo-ready today.

Public API:
    render_basic_phrases_conversation(orthography="both")

The orthography parameter controls Cyrillic/Łacinka display:
    "both" → both shown (default for learners just starting)
    "cyrillic" → Cyrillic only
    "lacinka" → Łacinka only
"""

import streamlit as st

from content.basic_phrases_conversation import (
    CONVERSATION_SCRIPT,
    FINAL_MESSAGE,
)

# Optional HF model for partner-reply variation. The conversation always
# works without it — see hf_partner.py for the design rationale.
try:
    from content.hf_partner import (
        generate_partner_reply,
        is_hf_available,
        get_load_error,
        get_model_name,
    )
    _HF_HOOK_AVAILABLE = True
except ImportError:
    _HF_HOOK_AVAILABLE = False
    def generate_partner_reply(*, context, scripted_fallback):  # type: ignore
        return scripted_fallback
    def is_hf_available(): return False
    def get_load_error(): return "HF helper module missing"
    def get_model_name(): return "(none)"


# ---------------------------------------------------------------------------
# Session state initialization
# ---------------------------------------------------------------------------

def _init_state():
    """Set up session state keys used by the conversation manager."""
    if "bp_convo_step" not in st.session_state:
        st.session_state.bp_convo_step = 0  # index into CONVERSATION_SCRIPT
    if "bp_convo_history" not in st.session_state:
        st.session_state.bp_convo_history = []  # list of rendered turns
    if "bp_convo_user_state" not in st.session_state:
        # Tracks whether the user said they're well / not / etc — used so
        # the partner can react appropriately at goodbye.
        st.session_state.bp_convo_user_state = "well"
    if "bp_convo_feedback" not in st.session_state:
        st.session_state.bp_convo_feedback = None
    if "bp_convo_show_english" not in st.session_state:
        st.session_state.bp_convo_show_english = False
    if "bp_convo_user_name" not in st.session_state:
        st.session_state.bp_convo_user_name = ""
    if "bp_convo_finished" not in st.session_state:
        st.session_state.bp_convo_finished = False


def _reset_conversation():
    """Reset the conversation to step 0."""
    st.session_state.bp_convo_step = 0
    st.session_state.bp_convo_history = []
    st.session_state.bp_convo_user_state = "well"
    st.session_state.bp_convo_feedback = None
    st.session_state.bp_convo_show_english = False
    st.session_state.bp_convo_user_name = ""
    st.session_state.bp_convo_finished = False


# ---------------------------------------------------------------------------
# Rendering helpers — turn one bilingual line into HTML
# ---------------------------------------------------------------------------

def _render_belarusian_line(
    cyrillic: str,
    lacinka: str,
    english: str | None,
    *,
    orthography: str = "both",
    show_english: bool = False,
    speaker: str = "partner",
) -> str:
    """
    Build the HTML for one conversational line.

    speaker: "partner" or "you" — affects styling.
    """
    color_class = "convo-partner" if speaker == "partner" else "convo-you"
    parts = [f'<div class="convo-bubble {color_class}">']

    if orthography in ("both", "cyrillic"):
        parts.append(f'<div class="convo-cyr">{cyrillic}</div>')
    if orthography in ("both", "lacinka"):
        parts.append(f'<div class="convo-lac">{lacinka}</div>')
    if show_english and english:
        parts.append(f'<div class="convo-eng">[{english}]</div>')

    parts.append("</div>")
    return "".join(parts)


# ---------------------------------------------------------------------------
# CSS — injected once per call
# ---------------------------------------------------------------------------

_CONVO_CSS = """
<style>
.convo-bubble {
    border-radius: 12px;
    padding: 0.7em 1em;
    margin: 0.4em 0;
    max-width: 85%;
    line-height: 1.45;
}
.convo-partner {
    background: rgba(252, 211, 77, 0.18);
    border-left: 3px solid rgba(252, 211, 77, 0.7);
    margin-right: auto;
}
.convo-you {
    background: rgba(147, 197, 253, 0.18);
    border-left: 3px solid rgba(147, 197, 253, 0.7);
    margin-left: auto;
}
.convo-cyr { font-size: 1.1em; font-weight: 500; }
.convo-lac { font-size: 0.95em; font-weight: 300; opacity: 0.7; font-style: italic; }
.convo-eng { font-size: 0.85em; opacity: 0.6; margin-top: 0.3em; font-style: italic; }
.convo-progress { font-size: 0.75em; opacity: 0.6; text-transform: uppercase;
                  letter-spacing: 0.08em; margin: 0.5em 0 0.3em 0; font-weight: 600; }
</style>
"""


# ---------------------------------------------------------------------------
# Step renderers
# ---------------------------------------------------------------------------

def _resolve_partner_line(step: dict, user_state: str) -> dict:
    """
    Some steps (the goodbye step) have partner lines that vary by user_state.
    Resolve to a flat dict.
    """
    partner = step["partner"]
    if "by_user_state" in partner:
        return partner["by_user_state"].get(
            user_state, list(partner["by_user_state"].values())[0]
        )
    return partner


def _resolve_and_maybe_vary(step: dict, user_state: str, history: list) -> dict:
    """
    Resolve the scripted partner line for this step, then optionally pass
    it through the HF model for slight variation. The HF model is opt-in
    (CALLA_ENABLE_HF=1) and falls back to the scripted line on any failure.

    The pattern matcher / scripted reply is always the source of truth —
    HF is purely an optional variation layer.
    """
    scripted = _resolve_partner_line(step, user_state)

    # Build context for the HF helper. Includes step ID, user state, name,
    # and the recent conversation history for prompting.
    context = {
        "step_id": step["step_id"],
        "user_state": user_state,
        "user_name": st.session_state.get("bp_convo_user_name", ""),
        "history": history,
    }

    # Call the HF helper. If HF is not enabled / loaded / generation fails,
    # this returns scripted unchanged.
    return generate_partner_reply(context=context, scripted_fallback=scripted)


def _render_history(orthography: str) -> None:
    """Render all completed turns from history."""
    for turn in st.session_state.bp_convo_history:
        st.markdown(
            _render_belarusian_line(
                turn["cyrillic"],
                turn["lacinka"],
                turn["english"],
                orthography=orthography,
                show_english=turn.get("show_english", False),
                speaker=turn["speaker"],
            ),
            unsafe_allow_html=True,
        )


def _render_step_buttons(step: dict, orthography: str) -> None:
    """Render button-based response options for a step."""
    options = step["options"]

    # Two-column grid for the buttons (or single column on mobile width)
    cols = st.columns(2)
    for i, opt in enumerate(options):
        col = cols[i % 2]
        with col:
            # Button label — show whichever script(s) the user wants.
            if orthography == "cyrillic":
                label = opt["cyrillic"]
            elif orthography == "lacinka":
                label = opt["lacinka"]
            else:
                label = f'{opt["cyrillic"]}\n{opt["lacinka"]}'

            if st.button(
                label,
                key=f"bp_convo_opt_{step['step_id']}_{i}",
                use_container_width=True,
            ):
                _handle_button_response(step, opt)
                st.rerun()


def _render_step_text(step: dict, orthography: str) -> None:
    """Render text input for the name step."""
    template = step["template"]
    name_input = st.text_input(
        template["input_label"],
        value=st.session_state.bp_convo_user_name,
        placeholder=template["input_placeholder"],
        key=f"bp_convo_name_input_{step['step_id']}",
    )

    # Show a preview of how the response will look
    if name_input.strip():
        preview_cyr = template["cyrillic_template"].format(name=name_input.strip())
        preview_lac = template["lacinka_template"].format(name=name_input.strip())
        preview_eng = template["english_template"].format(name=name_input.strip())

        st.markdown(
            _render_belarusian_line(
                preview_cyr,
                preview_lac,
                preview_eng,
                orthography=orthography,
                show_english=False,
                speaker="you",
            ),
            unsafe_allow_html=True,
        )

        if st.button(
            "Send →",
            use_container_width=True,
            key=f"bp_convo_send_{step['step_id']}",
        ):
            st.session_state.bp_convo_user_name = name_input.strip()
            _handle_text_response(step, name_input.strip())
            st.rerun()


def _handle_button_response(step: dict, option: dict) -> None:
    """Process a button click."""
    if not option["is_good"]:
        st.session_state.bp_convo_feedback = option.get(
            "feedback", "Try a different choice."
        )
        return

    # Append user's turn to history
    st.session_state.bp_convo_history.append({
        "cyrillic": option["cyrillic"],
        "lacinka": option["lacinka"],
        "english": option["english"],
        "show_english": False,
        "speaker": "you",
    })

    # Track user_state if this option has one (used at goodbye step)
    if "user_state" in option:
        st.session_state.bp_convo_user_state = option["user_state"]

    # Append partner's next line (if there is one) to history
    next_step_idx = st.session_state.bp_convo_step + 1
    if next_step_idx < len(CONVERSATION_SCRIPT):
        next_step = CONVERSATION_SCRIPT[next_step_idx]
        next_partner = _resolve_and_maybe_vary(
            next_step,
            st.session_state.bp_convo_user_state,
            st.session_state.bp_convo_history,
        )
        st.session_state.bp_convo_history.append({
            "cyrillic": next_partner["cyrillic"],
            "lacinka": next_partner["lacinka"],
            "english": next_partner["english"],
            "show_english": False,
            "speaker": "partner",
            "context": next_partner.get("context", ""),
        })
        st.session_state.bp_convo_step = next_step_idx
        st.session_state.bp_convo_show_english = False
        st.session_state.bp_convo_feedback = None
    else:
        # Past the last step — conversation is finished.
        st.session_state.bp_convo_finished = True


def _handle_text_response(step: dict, name: str) -> None:
    """Process a text input response (the name step)."""
    template = step["template"]
    cyr = template["cyrillic_template"].format(name=name)
    lac = template["lacinka_template"].format(name=name)
    eng = template["english_template"].format(name=name)

    st.session_state.bp_convo_history.append({
        "cyrillic": cyr,
        "lacinka": lac,
        "english": eng,
        "show_english": False,
        "speaker": "you",
    })

    # Advance and append next partner line.
    next_step_idx = st.session_state.bp_convo_step + 1
    if next_step_idx < len(CONVERSATION_SCRIPT):
        next_step = CONVERSATION_SCRIPT[next_step_idx]
        next_partner = _resolve_and_maybe_vary(
            next_step,
            st.session_state.bp_convo_user_state,
            st.session_state.bp_convo_history,
        )
        st.session_state.bp_convo_history.append({
            "cyrillic": next_partner["cyrillic"],
            "lacinka": next_partner["lacinka"],
            "english": next_partner["english"],
            "show_english": False,
            "speaker": "partner",
            "context": next_partner.get("context", ""),
        })
        st.session_state.bp_convo_step = next_step_idx
        st.session_state.bp_convo_show_english = False
        st.session_state.bp_convo_feedback = None


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def render_basic_phrases_conversation(orthography: str = "both") -> None:
    """
    Render the entire Basic Phrases conversation widget.

    Args:
        orthography: "both" | "cyrillic" | "lacinka" — what scripts to show.
    """
    _init_state()
    st.markdown(_CONVO_CSS, unsafe_allow_html=True)

    # Optional: show a small indicator of whether the HF variation layer
    # is active. The conversation works either way; this is just info
    # for the demo-er.
    if _HF_HOOK_AVAILABLE:
        if is_hf_available():
            st.caption(
                f"🤖 AI partner variation active "
                f"(model: `{get_model_name()}`)"
            )
        else:
            err = get_load_error()
            if err and "disabled" not in err:
                with st.expander("AI partner status (info only)"):
                    st.caption(
                        f"HF model not loaded — using scripted replies. "
                        f"Reason: {err}"
                    )

    # Header / progress
    if not st.session_state.bp_convo_finished:
        current_step = CONVERSATION_SCRIPT[st.session_state.bp_convo_step]
        progress_label = (
            f"Step {st.session_state.bp_convo_step + 1} of "
            f"{len(CONVERSATION_SCRIPT)} — {current_step['step_label_cyr']} "
            f"({current_step['step_label_eng']})"
        )
        st.markdown(
            f'<div class="convo-progress">{progress_label}</div>',
            unsafe_allow_html=True,
        )

    # If history is empty, seed it with the partner's opening line.
    if not st.session_state.bp_convo_history and not st.session_state.bp_convo_finished:
        first_step = CONVERSATION_SCRIPT[0]
        first_partner = _resolve_and_maybe_vary(
            first_step,
            st.session_state.bp_convo_user_state,
            st.session_state.bp_convo_history,
        )
        st.session_state.bp_convo_history.append({
            "cyrillic": first_partner["cyrillic"],
            "lacinka": first_partner["lacinka"],
            "english": first_partner["english"],
            "show_english": False,
            "speaker": "partner",
            "context": first_partner.get("context", ""),
        })

    # Render the full history (each turn is a bubble).
    _render_history(orthography)

    # Toggle "I don't understand" — sets show_english on the most recent
    # partner turn so the user can see the translation.
    if (
        not st.session_state.bp_convo_finished
        and st.session_state.bp_convo_history
        and st.session_state.bp_convo_history[-1]["speaker"] == "partner"
    ):
        # Find the index of the most recent partner turn
        last_partner_idx = None
        for i in range(len(st.session_state.bp_convo_history) - 1, -1, -1):
            if st.session_state.bp_convo_history[i]["speaker"] == "partner":
                last_partner_idx = i
                break

        if last_partner_idx is not None:
            already_revealed = st.session_state.bp_convo_history[
                last_partner_idx
            ].get("show_english", False)
            if not already_revealed:
                if st.button("🙋 I don't understand", key="bp_convo_idk"):
                    st.session_state.bp_convo_history[last_partner_idx][
                        "show_english"
                    ] = True
                    st.rerun()

    # Show feedback if a bad choice was made on the last turn
    if st.session_state.bp_convo_feedback:
        st.warning(st.session_state.bp_convo_feedback)

    # Render the input UI for the current step
    if not st.session_state.bp_convo_finished:
        current_step = CONVERSATION_SCRIPT[st.session_state.bp_convo_step]
        st.markdown("&nbsp;", unsafe_allow_html=True)
        if current_step["user_input_type"] == "buttons":
            _render_step_buttons(current_step, orthography)
        elif current_step["user_input_type"] == "text_with_template":
            _render_step_text(current_step, orthography)

    # Final state — show the completion message
    if st.session_state.bp_convo_finished:
        st.success(
            f'**{FINAL_MESSAGE["cyrillic"]}**\n\n'
            f'_{FINAL_MESSAGE["lacinka"]}_\n\n'
            f'[{FINAL_MESSAGE["english"]}]'
        )
        if st.button("↺ Start a new conversation", use_container_width=True):
            _reset_conversation()
            st.rerun()
        return

    # Cultural-context expander for the most recent partner turn (if it has
    # any context to show). This is where the pedagogical depth lives.
    last_partner_turn = next(
        (t for t in reversed(st.session_state.bp_convo_history)
         if t["speaker"] == "partner"),
        None,
    )
    if last_partner_turn and last_partner_turn.get("context"):
        with st.expander("💭 Cultural context for what they just said"):
            st.write(last_partner_turn["context"])

    # Reset button at the bottom for use mid-conversation
    st.markdown("&nbsp;", unsafe_allow_html=True)
    if st.button(
        "↺ Restart conversation",
        key="bp_convo_restart",
        use_container_width=False,
    ):
        _reset_conversation()
        st.rerun()
