# Calla — Context-Aware Language Learning

A Streamlit prototype demonstrating context-aware pedagogy as a research
direction. First iteration: Belarusian

## Run it

```bash
pip install -r requirements.txt
streamlit run app.py
```

Streamlit will open the app in your browser at `http://localhost:8501`.

## Architecture

```
calla/
├── app.py                                   # Page 0: Why Calla + framing
├── pages/
│   ├── 0_Unit_0_Alphabet.py                 # Unit 0 — Alphabet
│   ├── 1_Unit_1_Basic_Phrases.py            # Unit 1.1 — Basic Phrases
│   ├── 2_Unit_1_Phrases_in_Context.py       # Unit 1.2 — Dialogues
│   ├── 3_Unit_1_Conversation_Partner.py     # Unit 1.3 — Guided practice
│   └── 4_About_Me.py                        # Bio
├── content/
│   ├── phrases.py                           # Phrase data
│   ├── dialogues.py                         # Dialogue scripts
│   └── conversation_scripts.py              # Conversation-partner scenarios
├── requirements.txt
└── README.md
```

Streamlit's multipage convention: `app.py` is the entry point; each
file in `pages/` becomes a sidebar navigation item, ordered by the
numeric prefix.

## Pedagogical commitments encoded in the architecture (For Belarusian Studies)

- **Cyrillic primary, Łacinka secondary.** Both are Belarusian orthographic systems!
- **Register pairing visible.** Where the language distinguishes formal
  and informal, both forms are shown.
- **Cultural context as a first-class layer.** Every phrase, every
  dialogue turn, every partner response carries an annotation explaining
  the cultural-pragmatic move; what's being signaled beyond the literal
  translation.

## Future work

- LLM integration. Today the conversation partner is scripted for
  pedagogical control and demo reliability. The same UI can be wired to
  an API call by replacing the `SCENARIOS` lookup with a `/chat`
  request.
- Add audio
- Idioms with explicit moral-framing annotation, drawing on the CIS-MFT
  framework from the parent research project.
- Full curriculum coverage: grammar, extended vocabulary, longer-form
  cultural texts (songs, poems, prose excerpts -- Belarusian curriculum based on the textbook RAMZA)
- Multilingual discourse-marker analysis as
  the empirical instrument for scoring context-fit at scale.
- Add the community-interactive element (and distribution to topics)
- Create the fillable framework to connect to textbooks (reach out to language departments)