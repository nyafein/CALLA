"""
Structured conversation script for the Basic Phrases page.

The flow is fixed: greeting → name → how-are-you → goodbye.
At each step:
    - The partner's line is given in Cyrillic + Łacinka + English (English
      only revealed if the user clicks "I don't understand").
    - The user is offered button-based response options (also in Cyrillic
      + Łacinka). The "name" step is the one exception — there the user
      types their name into a text input.
    - Each user option is tagged 'good' or 'bad' so the partner can react
      appropriately. Good responses advance the conversation. Bad ones
      stay on the same step with feedback.

The script is data, not logic — it can be swapped wholesale for another
language without changing the conversation_manager.py engine.
"""

CONVERSATION_SCRIPT = [
    # --------------------------------------------------------------
    # Step 0 — Greeting
    # --------------------------------------------------------------
    {
        "step_id": "greeting",
        "step_label_cyr": "Прывітанне",
        "step_label_eng": "Greeting",
        "partner": {
            "cyrillic": "Прывітанне!",
            "lacinka": "Pryvitannie!",
            "english": "Hello!",
            "context": (
                "A neutral greeting, suitable any time of day. Slightly "
                "warmer than a strictly business opening. The exclamation "
                "is friendly, not loud."
            ),
        },
        "user_input_type": "buttons",
        "options": [
            {
                "cyrillic": "Прывітанне!",
                "lacinka": "Pryvitannie!",
                "english": "Hello!",
                "is_good": True,
                "feedback": None,
            },
            {
                "cyrillic": "Добры дзень!",
                "lacinka": "Dobry dzień!",
                "english": "Good day!",
                "is_good": True,
                "feedback": None,
            },
            {
                "cyrillic": "Бывай.",
                "lacinka": "Byvaj.",
                "english": "Goodbye.",
                "is_good": False,
                "feedback": (
                    "That's a goodbye — they've just said hello. Try a "
                    "greeting back."
                ),
            },
        ],
    },

    # --------------------------------------------------------------
    # Step 1 — Name introduction
    # --------------------------------------------------------------
    {
        "step_id": "name",
        "step_label_cyr": "Знаёмства",
        "step_label_eng": "Introduction",
        "partner": {
            "cyrillic": "Як вас завуць?",
            "lacinka": "Jak vas zavuć?",
            "english": "What's your name?",
            "context": (
                "Literally 'How do they call you?' — a beautiful piece of "
                "construction. The 'вы' form is formal/polite, appropriate "
                "with someone you've just met."
            ),
        },
        "user_input_type": "text_with_template",
        "template": {
            # The user types their name; we wrap it in this template for
            # the response. Both scripts are shown so the user can see
            # how the construction works.
            "cyrillic_template": "Мяне завуць {name}.",
            "lacinka_template": "Mianie zavuć {name}.",
            "english_template": "My name is {name}.",
            "input_label": "Type your name:",
            "input_placeholder": "...",
        },
    },

    # --------------------------------------------------------------
    # Step 2 — How are you?
    # --------------------------------------------------------------
    {
        "step_id": "how_are_you",
        "step_label_cyr": "Як справы?",
        "step_label_eng": "How are you?",
        "partner": {
            "cyrillic": "Прыемна пазнаёміцца! Як вы?",
            "lacinka": "Pryjemna paznajomicca! Jak vy?",
            "english": "Nice to meet you! How are you?",
            "context": (
                "Two phrases together: a warm acknowledgment of the "
                "introduction, then a follow-up question. 'Як вы?' uses "
                "the formal pronoun matching the earlier 'вас'."
            ),
        },
        "user_input_type": "buttons",
        "options": [
            {
                "cyrillic": "Добра, дзякуй!",
                "lacinka": "Dobra, dziakuj!",
                "english": "Fine, thanks!",
                "is_good": True,
                "feedback": None,
                "user_state": "well",
            },
            {
                "cyrillic": "Не вельмі добра.",
                "lacinka": "Nie vieĺmi dobra.",
                "english": "Not very well.",
                "is_good": True,
                "feedback": None,
                "user_state": "not_well",
            },
            {
                "cyrillic": "Дзякуй, добра. А вы?",
                "lacinka": "Dziakuj, dobra. A vy?",
                "english": "Thanks, fine. And you?",
                "is_good": True,
                "feedback": None,
                "user_state": "well_reciprocal",
            },
            {
                "cyrillic": "Прабачце, я не разумею.",
                "lacinka": "Prabačcie, ja nie razumieju.",
                "english": "Sorry, I don't understand.",
                "is_good": True,
                "feedback": None,
                "user_state": "confused",
            },
        ],
    },

    # --------------------------------------------------------------
    # Step 3 — Goodbye (final)
    # --------------------------------------------------------------
    {
        "step_id": "goodbye",
        "step_label_cyr": "Развітанне",
        "step_label_eng": "Farewell",
        "partner": {
            # The partner's line varies based on user_state from the prior
            # step. The conversation_manager picks the right one.
            "by_user_state": {
                "well": {
                    "cyrillic": "Цудоўна! Да сустрэчы!",
                    "lacinka": "Cudoŭna! Da sustrečy!",
                    "english": "Wonderful! See you!",
                    "context": (
                        "'Цудоўна' (cudoŭna) means 'wonderful' — a warm "
                        "response to good news. 'Да сустрэчы' implies "
                        "you'll meet again."
                    ),
                },
                "not_well": {
                    "cyrillic": "Шкада. Спадзяюся, заўтра будзе лепш. Да сустрэчы!",
                    "lacinka": "Škada. Spadziajusia, zaŭtra budzie lepš. Da sustrečy!",
                    "english": (
                        "I'm sorry [to hear that]. I hope tomorrow will be "
                        "better. See you!"
                    ),
                    "context": (
                        "'Шкада' (škada) is a sympathetic 'too bad' / "
                        "'I'm sorry'. The hope-for-tomorrow phrasing is a "
                        "common and warm parting in Belarusian."
                    ),
                },
                "well_reciprocal": {
                    "cyrillic": "Таксама добра, дзякуй! Да сустрэчы!",
                    "lacinka": "Taksama dobra, dziakuj! Da sustrečy!",
                    "english": "Also fine, thanks! See you!",
                    "context": (
                        "'Таксама' (taksama) means 'also' — directly "
                        "answering the reciprocal 'А вы?'."
                    ),
                },
                "confused": {
                    "cyrillic": "Без праблем! Да сустрэчы!",
                    "lacinka": "Biez prabliem! Da sustrečy!",
                    "english": "No problem! See you!",
                    "context": (
                        "A gentle, encouraging close — saying 'I don't "
                        "understand' is itself a perfectly polite move "
                        "in Belarusian conversation."
                    ),
                },
            },
        },
        "user_input_type": "buttons",
        "options": [
            {
                "cyrillic": "Да пабачэння!",
                "lacinka": "Da pabačennia!",
                "english": "Goodbye!",
                "is_good": True,
                "feedback": None,
            },
            {
                "cyrillic": "Да сустрэчы!",
                "lacinka": "Da sustrečy!",
                "english": "See you!",
                "is_good": True,
                "feedback": None,
            },
            {
                "cyrillic": "Бывай!",
                "lacinka": "Byvaj!",
                "english": "Bye! (informal)",
                "is_good": True,
                "feedback": None,
            },
        ],
    },
]


# Final acknowledgement after the user clicks goodbye — closes the conversation.
FINAL_MESSAGE = {
    "cyrillic": "Размова скончана. Добра зроблена! 🌷",
    "lacinka": "Razmova skončana. Dobra zrobliena!",
    "english": "Conversation finished. Well done!",
}
