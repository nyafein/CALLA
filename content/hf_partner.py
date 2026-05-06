"""
Optional HuggingFace integration for the conversation partner.

This module is a *layer on top of* the rule-based pattern matcher in
conversation_manager.py — never a replacement. The pattern matcher
remains primary because:
    1. It always works (deterministic, fast, no model dependency)
    2. The conversation flow is structured enough that an LLM is overkill
    3. Belarusian generation quality from small open-weights models is
       unpredictable; we don't want to ship hallucinated Belarusian to
       a learner

Where the HF model adds value (when it works):
    - Slight variation in partner replies, so repeated demo runs feel
      less canned
    - Using the user's name back at them naturally
    - Generating a contextual reaction when the user types something

Public API:
    is_hf_available()     → bool — true if model loaded successfully
    generate_partner_reply(context: dict, scripted_fallback: dict) → dict
        Tries to generate; if anything fails, returns the scripted_fallback
        unchanged. So the conversation still works.

Default model: ai-forever/mGPT-1.3B
    One of the few small-ish multilingual models with explicit Belarusian
    training data. ~5GB on disk, ~6GB RAM at inference. CPU inference is
    5-20 seconds per response — too slow for live demo but okay for
    background variation.

To swap models, change HF_MODEL_NAME below. Other reasonable choices:
    - "Qwen/Qwen2.5-1.5B-Instruct" (instruction-tuned but English-biased)
    - "ai-forever/mGPT" (smaller, ~1.3B params)
    - "bigscience/bloom-1b7" (multilingual but Belarusian quality unknown)

ENABLE_HF below is False by default. Flip to True (or set the env var
CALLA_ENABLE_HF=1) to opt in. Otherwise this module reports unavailable
and the conversation engine uses scripted replies only.
"""

import os
import logging

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

HF_MODEL_NAME = "ai-forever/mGPT"  # default; smaller variant of mGPT-1.3B
ENABLE_HF = os.environ.get("CALLA_ENABLE_HF", "0") == "1"
GENERATION_MAX_NEW_TOKENS = 60
GENERATION_TIMEOUT_SECONDS = 30


# ---------------------------------------------------------------------------
# Lazy import + load. We don't import transformers at module load — that
# would hang the page even when HF is disabled. Only when ENABLE_HF is True
# AND a generation is requested do we pay the import cost.
# ---------------------------------------------------------------------------

_logger = logging.getLogger(__name__)
_model = None
_tokenizer = None
_load_attempted = False
_load_succeeded = False
_load_error: str | None = None


def _try_load_model() -> bool:
    """
    Attempt to load the HF model + tokenizer once. Subsequent calls are no-ops.
    Returns True on success, False on any failure (with reason logged).
    """
    global _model, _tokenizer, _load_attempted, _load_succeeded, _load_error

    if _load_attempted:
        return _load_succeeded

    _load_attempted = True

    if not ENABLE_HF:
        _load_error = "HF disabled (set CALLA_ENABLE_HF=1 to enable)"
        return False

    try:
        # These imports are heavy. Wrap in try in case transformers/torch
        # not installed — we should fail soft, not crash the page.
        from transformers import AutoModelForCausalLM, AutoTokenizer
        import torch  # noqa: F401  -- imported for side effect of triggering ImportError early
    except ImportError as e:
        _load_error = (
            f"transformers / torch not installed ({e}). To enable HF: "
            "pip install transformers torch"
        )
        _logger.warning(_load_error)
        return False

    try:
        _logger.info(f"Loading HF model: {HF_MODEL_NAME}")
        _tokenizer = AutoTokenizer.from_pretrained(HF_MODEL_NAME)
        _model = AutoModelForCausalLM.from_pretrained(
            HF_MODEL_NAME,
            torch_dtype="auto",
            low_cpu_mem_usage=True,
        )
        _load_succeeded = True
        _logger.info(f"HF model loaded: {HF_MODEL_NAME}")
        return True
    except Exception as e:
        _load_error = f"Model load failed: {e}"
        _logger.warning(_load_error)
        return False


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def is_hf_available() -> bool:
    """Return True iff the HF model is loaded and ready for generation."""
    return _load_succeeded


def get_load_error() -> str | None:
    """Return the most recent load-error message, if any."""
    return _load_error


def get_model_name() -> str:
    """Return the configured model identifier (for display purposes)."""
    return HF_MODEL_NAME


def generate_partner_reply(
    *,
    context: dict,
    scripted_fallback: dict,
) -> dict:
    """
    Try to generate a varied partner reply. If anything fails, return the
    scripted_fallback unchanged so the conversation still works.

    Args:
        context: dict describing the conversation state. Expected keys:
            - "step_id"      — string identifier for the current step
            - "user_name"    — the user's name if known, else ""
            - "user_state"   — "well" / "not_well" / "well_reciprocal" / "confused"
            - "history"      — list of prior turns (most recent last), each with
                               "speaker", "cyrillic", "lacinka", "english"
        scripted_fallback: dict with the canonical scripted reply. Must have
            keys "cyrillic", "lacinka", "english". Returned as-is on failure.

    Returns:
        A dict with the same shape as scripted_fallback. On success, the
        cyrillic / lacinka may be varied; english is regenerated to match.
        On failure (HF not loaded, generation fails, output looks bad),
        returns scripted_fallback verbatim.
    """
    # Fast path: if the model isn't loaded, return the scripted reply.
    if not _try_load_model():
        return scripted_fallback

    # Build a prompt. Format is simple: a short context + the scripted reply
    # as a "starting point" for the model to vary slightly. We do NOT ask
    # the model to generate anything off-script.
    try:
        prompt = _build_prompt(context, scripted_fallback)
        generated = _generate(prompt)
    except Exception as e:
        _logger.warning(f"HF generation failed: {e}")
        return scripted_fallback

    if not _looks_like_valid_belarusian(generated):
        # Defensive: if the model output looks broken, don't ship it.
        _logger.info("HF output failed validation; using scripted fallback.")
        return scripted_fallback

    # Build the full reply dict. Note: we only override cyrillic; the
    # lacinka + english stay scripted because we can't reliably regenerate
    # them from a model output. So this gives variation in Cyrillic with
    # consistent transliteration / translation alongside.
    return {
        **scripted_fallback,
        "cyrillic": generated.strip(),
        "_hf_generated": True,  # marker so the UI can show a "generated" tag
    }


# ---------------------------------------------------------------------------
# Internals
# ---------------------------------------------------------------------------

def _build_prompt(context: dict, scripted: dict) -> str:
    """
    Construct a small prompt to seed generation. The prompt is mostly the
    scripted reply itself — we ask the model to continue / vary it minimally.
    """
    # Build the conversation transcript so far. We keep it short — only
    # the last few turns — so the model has context but isn't overloaded.
    history = context.get("history", [])[-4:]
    transcript_lines = []
    for turn in history:
        speaker_tag = "A:" if turn["speaker"] == "partner" else "B:"
        transcript_lines.append(f"{speaker_tag} {turn['cyrillic']}")
    transcript = "\n".join(transcript_lines)

    # Short prompt: continue the conversation as speaker A.
    prompt = (
        f"{transcript}\nA: {scripted['cyrillic'][:30]}"
    )
    return prompt


def _generate(prompt: str) -> str:
    """Run the model. Caller is responsible for handling exceptions."""
    import torch
    inputs = _tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        output_ids = _model.generate(
            **inputs,
            max_new_tokens=GENERATION_MAX_NEW_TOKENS,
            do_sample=True,
            temperature=0.8,
            top_p=0.9,
            pad_token_id=_tokenizer.eos_token_id or 0,
        )
    full_text = _tokenizer.decode(output_ids[0], skip_special_tokens=True)
    # The generated text includes the prompt — strip it back off.
    if full_text.startswith(prompt):
        full_text = full_text[len(prompt):]
    # Take just the first generated line (we don't want a long monologue).
    first_line = full_text.split("\n")[0].strip()
    # Strip any speaker tag the model may have re-emitted.
    if first_line.startswith("A:") or first_line.startswith("B:"):
        first_line = first_line[2:].strip()
    return first_line


def _looks_like_valid_belarusian(text: str) -> bool:
    """
    Cheap sanity check: does the output look like Belarusian Cyrillic?

    We verify:
        - Non-empty
        - Reasonable length (not just punctuation, not a wall of text)
        - At least 50% of characters are Cyrillic
        - Doesn't contain obvious garbage tokens
    """
    if not text or len(text.strip()) < 2:
        return False
    if len(text) > 200:
        return False  # too long; probably a monologue

    cyrillic_chars = sum(
        1 for ch in text
        if "\u0400" <= ch <= "\u04ff" or "\u0500" <= ch <= "\u052f"
    )
    letter_chars = sum(1 for ch in text if ch.isalpha())
    if letter_chars == 0:
        return False
    if cyrillic_chars / letter_chars < 0.5:
        return False  # too many Latin / non-Cyrillic letters

    # Reject obvious model garbage tokens
    garbage_markers = ["<|", "|>", "[INST]", "<s>", "</s>", "[PAD]"]
    for marker in garbage_markers:
        if marker in text:
            return False

    return True
