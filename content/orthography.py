"""
Shared orthography toggle logic.

Used by pages where switching between Cyrillic and Łacinka aids reading
(extended dialogues, multi-turn conversations). NOT used on the alphabet
or basic-phrases reference pages, where seeing both at once is the point.

The selection is stored in st.session_state under the key 'orthography_pref'
and persists across page navigations.
"""

import streamlit as st


# Display labels — used both in the radio and as state values.
ORTHO_BOTH = "Both"
ORTHO_CYR = "Cyrillic only"
ORTHO_LAC = "Łacinka only"


def render_orthography_picker() -> str:
    """
    Render the orthography toggle in the sidebar.
    Returns the current selection: ORTHO_BOTH / ORTHO_CYR / ORTHO_LAC.

    Streamlit handles persistence automatically when we pass a `key=` —
    the radio's value is mirrored into st.session_state[key], and on the
    next page (or rerun) it reads from there to set its initial state.
    """
    return st.sidebar.radio(
        "Orthography",
        options=[ORTHO_BOTH, ORTHO_CYR, ORTHO_LAC],
        key="orthography_pref",
        help=(
            "Switch between scripts. Both Cyrillic and Łacinka are real "
            "Belarusian orthographies — pick whichever helps you read, or "
            "see both at once."
        ),
    )


def show_cyrillic(ortho: str) -> bool:
    """True if Cyrillic should be rendered given the current selection."""
    return ortho in (ORTHO_BOTH, ORTHO_CYR)


def show_lacinka(ortho: str) -> bool:
    """True if Łacinka should be rendered given the current selection."""
    return ortho in (ORTHO_BOTH, ORTHO_LAC)
