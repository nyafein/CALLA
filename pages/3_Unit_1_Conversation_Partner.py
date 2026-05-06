"""
Page 3 — Conversation Partner.

Scripted interactive exchanges. The user picks the user-side turns from
a small set of options; the partner responds with a Belarusian message
plus an expandable "what just happened culturally?" annotation.

Why scripted (not LLM-driven): for today's demo, full control over the
output and zero risk of weird generation in front of an audience. The
exact same UI structure can later be wired to a Claude API call by
replacing the lookup against SCENARIOS with a /chat endpoint call.

State is tracked in st.session_state because Streamlit re-runs the
script top-to-bottom on every interaction.
"""

import random

import streamlit as st

from content.conversation_scripts import SCENARIOS
from content.orthography import (
    render_orthography_picker,
    show_cyrillic,
    show_lacinka,
)
from content.characters import (
    GENDERED_LANGUAGE_NOTE,
    NONBINARY_NOTE,
    scenario_speaker_indicator,
    scenario_grammar_note,
)


# ---------------------------------------------------------------------------
# CSS (defensive re-injection)
# ---------------------------------------------------------------------------

GLOBAL_CSS = """
<style>
.cyrillic { font-size: 1.05em; font-weight: 500; line-height: 1.45; }
.lacinka  { font-size: 0.9em;  font-weight: 300; opacity: 0.7; font-style: italic; line-height: 1.45; }
.english  { font-size: 0.82em; opacity: 0.55; line-height: 1.45; }
.context-note { font-size: 0.87em; opacity: 0.75; line-height: 1.55;
                border-left: 3px solid rgba(156, 163, 175, 0.4); padding-left: 0.85em; }
.setting-block { background: rgba(156, 163, 175, 0.08); border-radius: 6px; padding: 0.9em 1.1em;
                 font-size: 0.92em; opacity: 0.92; margin-bottom: 1em; }
.prompt-box { background: rgba(251, 191, 36, 0.15); border-radius: 6px; padding: 0.7em 1em;
              font-size: 0.95em; margin-bottom: 0.7em; border-left: 3px solid rgba(251, 191, 36, 0.6); }
.feedback-box { background: rgba(248, 113, 113, 0.15); border-radius: 6px; padding: 0.7em 1em;
                font-size: 0.9em; margin-bottom: 0.7em; border-left: 3px solid rgba(248, 113, 113, 0.6); }
</style>
"""
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------

st.title("Unit 1.3 — Conversation Partner")
st.caption("Pick a scenario. Choose responses. The partner replies in Belarusian.")

st.markdown(
    """
    Each scenario walks through a short, realistic exchange. At each step
    you'll be shown 1–3 ways to say the same thing — the choices reflect
    register, idiom, and cultural fit, not just grammar. The partner's
    reply includes an expandable note explaining what's happening
    culturally beyond the literal translation.

    > **Note:** for today's demo the partner is scripted, not LLM-driven.
    > This gives full pedagogical control. The same interface can be wired
    > to a live model later; the architecture supports it.
    """
)

st.divider()


# ---------------------------------------------------------------------------
# Session state initialization
# ---------------------------------------------------------------------------

if "convo_scenario" not in st.session_state:
    st.session_state.convo_scenario = None  # key into SCENARIOS

if "convo_step" not in st.session_state:
    st.session_state.convo_step = 0  # which turn we're on

if "convo_history" not in st.session_state:
    # List of messages already shown. Each: {role, cyrillic, lacinka,
    # english, cultural_note (optional)}. Role is 'partner' or 'you'.
    st.session_state.convo_history = []

if "convo_feedback" not in st.session_state:
    # If the user picked a 'bad' option last click, hold the feedback string
    # so we can show it before the next render. Cleared on the next click.
    st.session_state.convo_feedback = None

# Difficulty-mode state.
# Easy   = current behavior; partner messages show English gloss inline.
# Medium = partner messages hide English until the user passes a
#          comprehension check ("what did they say?").
# Hard   = reserved for the future LLM-driven version.
if "convo_difficulty" not in st.session_state:
    st.session_state.convo_difficulty = "Easy"

if "convo_comprehended_indices" not in st.session_state:
    # Indices into convo_history of partner messages whose English gloss
    # the user has revealed by passing the comprehension check.
    # The opening message is auto-comprehended on scenario start
    # so the user has at least one anchor.
    st.session_state.convo_comprehended_indices = set()

if "convo_comprehension_feedback" not in st.session_state:
    st.session_state.convo_comprehension_feedback = None

# User's chosen gender for the practice session. Affects the cultural
# notes shown about which grammatical forms apply to them.
if "user_gender" not in st.session_state:
    st.session_state.user_gender = "Feminine"


# Difficulty constants
DIFF_EASY = "Easy"
DIFF_MEDIUM = "Medium"
DIFF_HARD = "Hard (LLM — coming soon)"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def reset_conversation():
    """Clear all conversation state. Used when picking a new scenario."""
    st.session_state.convo_scenario = None
    st.session_state.convo_step = 0
    st.session_state.convo_history = []
    st.session_state.convo_feedback = None
    st.session_state.convo_comprehended_indices = set()
    st.session_state.convo_comprehension_feedback = None


def start_scenario(scenario_key: str):
    """Set up a fresh scenario and seed it with the partner's opening line."""
    st.session_state.convo_scenario = scenario_key
    st.session_state.convo_step = 0
    st.session_state.convo_feedback = None
    st.session_state.convo_comprehension_feedback = None

    opening = SCENARIOS[scenario_key]["opening"]
    st.session_state.convo_history = [
        {
            "role": "partner",
            "cyrillic": opening["cyrillic"],
            "lacinka": opening["lacinka"],
            "english": opening["english"],
            "cultural_note": opening["cultural_note"],
        }
    ]
    # Opening is "free" — comprehension scaffolding starts on subsequent turns.
    # In Medium mode this means the very first message shows English so the
    # learner has a foothold.
    st.session_state.convo_comprehended_indices = {0}


def is_medium_mode() -> bool:
    return st.session_state.convo_difficulty == DIFF_MEDIUM


def latest_partner_index_pending_comprehension() -> int | None:
    """
    In Medium mode, find the index of the most recent partner message that
    the user hasn't yet revealed. Returns None if none pending.
    """
    if not is_medium_mode():
        return None
    history = st.session_state.convo_history
    revealed = st.session_state.convo_comprehended_indices
    for i in range(len(history) - 1, -1, -1):
        msg = history[i]
        if msg["role"] == "partner" and i not in revealed:
            return i
    return None


def all_partner_english_glosses() -> list[str]:
    """
    Pool of all partner English glosses across the active scenario,
    used as distractors in comprehension questions.
    """
    if st.session_state.convo_scenario is None:
        return []
    scenario = SCENARIOS[st.session_state.convo_scenario]
    glosses = [scenario["opening"]["english"]]
    for turn in scenario["turns"]:
        glosses.append(turn["response_if_good"]["english"])
    return glosses


def render_message(msg: dict, idx: int, ortho: str) -> None:
    """Render a single message bubble using Streamlit's chat primitives."""
    avatar = "🤝" if msg["role"] == "partner" else "🧑"

    # Decide whether to show the English gloss for this message.
    show_english = True
    if (
        msg["role"] == "partner"
        and is_medium_mode()
        and idx not in st.session_state.convo_comprehended_indices
    ):
        show_english = False

    with st.chat_message(msg["role"], avatar=avatar):
        parts = []
        if show_cyrillic(ortho):
            parts.append(f'<div class="cyrillic">{msg["cyrillic"]}</div>')
        if show_lacinka(ortho):
            parts.append(f'<div class="lacinka">{msg["lacinka"]}</div>')
        if show_english:
            parts.append(f'<div class="english">— {msg["english"]}</div>')
        else:
            parts.append(
                '<div class="english" style="color:#cbd5e1;font-style:italic;">'
                "— (translate below to reveal)</div>"
            )
        st.markdown("".join(parts), unsafe_allow_html=True)
        # Cultural note attached to partner messages.
        if msg["role"] == "partner" and msg.get("cultural_note"):
            with st.expander("What just happened culturally?", expanded=False):
                st.markdown(
                    f'<div class="context-note">{msg["cultural_note"]}</div>',
                    unsafe_allow_html=True,
                )


def handle_choice(choice: dict, turn: dict):
    """User clicked a choice. Append to history if good, advance the step."""
    if choice["is_good"]:
        # Append user's message
        st.session_state.convo_history.append({
            "role": "you",
            "cyrillic": choice["cyrillic"],
            "lacinka": choice["lacinka"],
            "english": choice["english"],
        })
        # Per-choice response override, if present; else turn-level default.
        # This lets a step branch on which good choice the user picked
        # (e.g. asking "what is Kupalle?" vs. showing existing knowledge
        # of it should produce different partner replies).
        resp = choice.get("response_if_chosen") or turn["response_if_good"]
        # Append partner's response
        st.session_state.convo_history.append({
            "role": "partner",
            "cyrillic": resp["cyrillic"],
            "lacinka": resp["lacinka"],
            "english": resp["english"],
            "cultural_note": resp["cultural_note"],
        })
        # Advance to next step
        st.session_state.convo_step += 1
        st.session_state.convo_feedback = None
    else:
        # Bad choice — capture feedback, don't advance.
        st.session_state.convo_feedback = choice.get(
            "feedback",
            "That choice doesn't quite fit here. Try another."
        )


def render_comprehension_question(partner_idx: int) -> None:
    """
    Medium mode: render a 'what did the partner just say?' multiple-choice
    question for the partner message at history[partner_idx]. The user must
    answer correctly before they can advance to choosing their own response.
    """
    msg = st.session_state.convo_history[partner_idx]
    correct = msg["english"]

    # Build the option set: correct + 2 distractors.
    pool = [g for g in all_partner_english_glosses() if g != correct]
    rng = random.Random(f"{st.session_state.convo_scenario}_{partner_idx}")
    distractors = rng.sample(pool, min(2, len(pool)))
    options = [correct] + distractors
    rng.shuffle(options)

    if st.session_state.convo_comprehension_feedback:
        st.markdown(
            f'<div class="feedback-box">'
            f'{st.session_state.convo_comprehension_feedback}'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="prompt-box"><strong>Comprehension check.</strong> '
        'What did the partner just say?</div>',
        unsafe_allow_html=True,
    )

    for opt in options:
        key = f"comp_{partner_idx}_{abs(hash(opt))}"
        if st.button(opt, key=key, use_container_width=True):
            if opt == correct:
                st.session_state.convo_comprehended_indices.add(partner_idx)
                st.session_state.convo_comprehension_feedback = None
            else:
                st.session_state.convo_comprehension_feedback = (
                    "Not quite — listen again. Look for words you recognize."
                )
            st.rerun()


# ---------------------------------------------------------------------------
# Scenario picker (shown when no scenario is active)
# ---------------------------------------------------------------------------

if st.session_state.convo_scenario is None:
    # ---------------------------------------------------------------
    # Cultural callout — Belarusian is gendered.
    # (Per Nya: no character images / clothing today, but gender
    #  details stay.)
    # ---------------------------------------------------------------
    with st.expander(
        "🪶 Cultural note — Belarusian grammatical gender",
        expanded=False,
    ):
        st.markdown(GENDERED_LANGUAGE_NOTE)
        st.markdown("---")
        st.markdown(NONBINARY_NOTE)

    # ---------------------------------------------------------------
    # User gender selector — affects which grammatical forms get
    # highlighted as "yours" in the scenarios.
    # ---------------------------------------------------------------
    st.markdown("##### Your grammatical gender for practice")
    st.caption(
        "Belarusian past-tense verbs and many adjectives change form "
        "with the speaker's gender. Pick what you'd like to practice with."
    )
    st.radio(
        "User grammatical gender",
        options=[
            "Feminine",
            "Masculine",
        ],
        key="user_gender",
        label_visibility="collapsed",
        horizontal=False,
    )

    st.divider()

    # ---------------------------------------------------------------
    # Difficulty selector
    # ---------------------------------------------------------------
    st.markdown("##### Pick a difficulty")
    st.radio(
        "Difficulty",
        options=[DIFF_EASY, DIFF_MEDIUM, DIFF_HARD],
        key="convo_difficulty",
        label_visibility="collapsed",
        horizontal=True,
        help=(
            "Easy: choices and translations always visible. "
            "Medium: comprehend the partner before responding. "
            "Hard: free-response (LLM-driven, coming soon)."
        ),
    )

    # If Hard is selected, short-circuit with a coming-soon notice.
    if st.session_state.convo_difficulty == DIFF_HARD:
        st.info(
            "**Hard mode is reserved for the LLM-driven version.** "
            "In Hard mode you'll respond freely in Belarusian and the "
            "partner — powered by Claude — will answer back, evaluate "
            "your fit, and explain what's working pragmatically. The "
            "scaffolding for this lives in the codebase already; the "
            "demo today runs Easy and Medium with scripted exchanges."
        )
        st.stop()

    st.markdown("##### Pick a scenario")
    cols = st.columns(len(SCENARIOS))
    for col, (key, scenario) in zip(cols, SCENARIOS.items()):
        with col:
            st.markdown(f"**{scenario['title']}**")
            # Character indicator — who you'll be talking to in this scenario.
            indicator = scenario_speaker_indicator(key)
            if indicator:
                st.caption(f"With: {indicator}")
            st.caption(scenario["setting"])
            if st.button("Start", key=f"start_{key}", use_container_width=True):
                start_scenario(key)
                st.rerun()

    st.stop()


# ---------------------------------------------------------------------------
# Active scenario view
# ---------------------------------------------------------------------------

scenario = SCENARIOS[st.session_state.convo_scenario]

# Sidebar toggle — choose which scripts to display.
ortho = render_orthography_picker()

# Top bar: scenario title + difficulty indicator + reset button
top_col1, top_col2, top_col3 = st.columns([4, 2, 1])
with top_col1:
    st.markdown(f"##### {scenario['title']}")
with top_col2:
    st.caption(f"Difficulty: **{st.session_state.convo_difficulty}**")
with top_col3:
    if st.button("Reset", use_container_width=True):
        reset_conversation()
        st.rerun()

# Character indicator + grammar note — who's speaking and which gendered
# forms apply. Helps the learner anticipate the grammar in this scenario.
indicator = scenario_speaker_indicator(st.session_state.convo_scenario)
grammar_note = scenario_grammar_note(st.session_state.convo_scenario)
if indicator:
    st.markdown(
        f'<div style="opacity:0.85; font-size:0.92em; '
        f'margin: 0.3em 0 0.5em 0;">'
        f'<strong>With:</strong> {indicator}'
        f'</div>',
        unsafe_allow_html=True,
    )
if grammar_note:
    st.info(grammar_note)

# Setting block (always visible while in scenario)
st.markdown(
    f'<div class="setting-block"><strong>Setting.</strong> {scenario["setting"]}</div>',
    unsafe_allow_html=True,
)

# Render conversation history so far
for i, msg in enumerate(st.session_state.convo_history):
    render_message(msg, i, ortho)

# Current turn — show prompt + choices, OR the "scenario complete" state.
turns = scenario["turns"]
step = st.session_state.convo_step

pending_comprehension_idx = latest_partner_index_pending_comprehension()

if pending_comprehension_idx is not None:
    # Medium mode, partner message awaiting comprehension. Render the check.
    render_comprehension_question(pending_comprehension_idx)

elif step < len(turns):
    current_turn = turns[step]

    # Show feedback from previous click if there was one
    if st.session_state.convo_feedback:
        st.markdown(
            f'<div class="feedback-box">{st.session_state.convo_feedback}</div>',
            unsafe_allow_html=True,
        )

    # Prompt for this turn
    st.markdown(
        f'<div class="prompt-box"><strong>Your turn.</strong> '
        f'{current_turn["prompt"]}</div>',
        unsafe_allow_html=True,
    )

    # Choice buttons. The button label respects the orthography toggle.
    for choice in current_turn["choices"]:
        label_parts = []
        if show_cyrillic(ortho):
            label_parts.append(choice["cyrillic"])
        if show_lacinka(ortho):
            label_parts.append(f"_{choice['lacinka']}_")
        label_parts.append(f"— {choice['english']}")
        label = "\n\n".join(label_parts)

        if st.button(
            label,
            key=f"choice_{step}_{choice['id']}",
            use_container_width=True,
        ):
            handle_choice(choice, current_turn)
            st.rerun()

else:
    # Scenario complete
    st.success("Scenario complete. Well done.")
    if st.button("Try another scenario", use_container_width=True):
        reset_conversation()
        st.rerun()
