import streamlit as st

# -----------------------------------------------------------------------------
# Quiz data
# -----------------------------------------------------------------------------
# Add additional minerals here with their own set of questions.
QUIZ_DATA = {
    "Quartz": [
        {
            "question": "What is the chemical formula of Quartz?",
            "options": ["SiO2", "CaCO3", "Fe2O3", "NaCl"],
            "correct": "SiO2",
            "explanation": "Quartz is composed of silicon dioxide (SiO2).",
        },
        {
            "question": "Quartz is commonly found in which type of rock?",
            "options": ["Igneous", "Sedimentary", "Metamorphic", "All of the above"],
            "correct": "All of the above",
            "explanation": "Quartz is common in igneous, sedimentary, and metamorphic rocks.",
        },
        {
            "question": "Which property is Quartz known for?",
            "options": ["Magnetism", "Hardness", "Radioactivity", "High density"],
            "correct": "Hardness",
            "explanation": "Quartz has a hardness of 7 on the Mohs scale.",
        },
    ],
    "Feldspar": [
        {
            "question": "Which element is most abundant in feldspar minerals?",
            "options": ["Sodium", "Potassium", "Calcium", "All of the above"],
            "correct": "All of the above",
            "explanation": "Feldspar minerals contain sodium, potassium, and calcium.",
        },
        {
            "question": "Feldspar is most commonly associated with which rock type?",
            "options": ["Igneous", "Sedimentary", "Metamorphic", "None"],
            "correct": "Igneous",
            "explanation": "Feldspar is a major component of many igneous rocks.",
        },
        {
            "question": "What is a common use of feldspar in industry?",
            "options": ["Glass making", "Fuel", "Fertilizer", "Precious gemstones"],
            "correct": "Glass making",
            "explanation": "Feldspar is widely used in glass and ceramics production.",
        },
    ],
    "Calcite": [
        {
            "question": "What is the chemical formula of Calcite?",
            "options": ["CaCO3", "SiO2", "Fe2O3", "MgO"],
            "correct": "CaCO3",
            "explanation": "Calcite is calcium carbonate (CaCO3).",
        },
        {
            "question": "Calcite reacts with which common chemical?",
            "options": ["Hydrochloric acid", "Water", "Oxygen", "Sodium chloride"],
            "correct": "Hydrochloric acid",
            "explanation": "Calcite effervesces (fizzes) in dilute hydrochloric acid.",
        },
        {
            "question": "Calcite is the primary mineral in which rock?",
            "options": ["Limestone", "Granite", "Basalt", "Shale"],
            "correct": "Limestone",
            "explanation": "Limestone is composed mainly of calcite.",
        },
    ],
}


def get_quiz_for(mineral_name: str):
    """Return quiz questions for the given mineral name.

    The app may pass different casing (e.g., "quartz" vs "Quartz"),
    so we resolve using a normalized key.
    """

    if not mineral_name:
        return []

    key = mineral_name.strip()
    # Try as-is
    if key in QUIZ_DATA:
        return QUIZ_DATA[key]

    # Try capitalized (common display form)
    key_title = key.title()
    if key_title in QUIZ_DATA:
        return QUIZ_DATA[key_title]

    # Try lower-case (common storage form)
    key_lower = key.lower()
    if key_lower in QUIZ_DATA:
        return QUIZ_DATA[key_lower]

    # Fall back: look for case-insensitive match
    for candidate in QUIZ_DATA:
        if candidate.lower() == key_lower:
            return QUIZ_DATA[candidate]

    return []


def render_mineral_quiz(mineral_name: str):
    """Render a mini-quiz for the currently selected mineral."""

    questions = get_quiz_for(mineral_name)
    if not questions:
        return

    # Use a normalized key for session state to avoid case issues
    quiz_key = mineral_name.strip().lower()
    key_prefix = f"quiz_{quiz_key}"

    # Initialize session state for this quiz
    if f"{key_prefix}_submitted" not in st.session_state:
        st.session_state[f"{key_prefix}_submitted"] = False
        st.session_state[f"{key_prefix}_score"] = 0

    if f"{key_prefix}_answers" not in st.session_state:
        st.session_state[f"{key_prefix}_answers"] = {}

    st.divider()

    # Display a normalized display name (e.g., "Quartz") even if the passed name is lowercase
    display_name = mineral_name.strip().title()
    st.markdown(f"### 🧠 Test your knowledge about {display_name}")

    # Render questions
    for idx, question in enumerate(questions, start=1):
        question_key = f"{key_prefix}_q{idx}"
        default = st.session_state[f"{key_prefix}_answers"].get(question_key)

        st.markdown(f"**Question {idx}.** {question['question']}")
        answer = st.radio(
            "",
            options=question["options"],
            index=question["options"].index(default) if default in question["options"] else 0,
            key=question_key,
        )
        st.session_state[f"{key_prefix}_answers"][question_key] = answer

    # Buttons
    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("Submit Quiz", key=f"{key_prefix}_submit"):
            score = 0
            for idx, question in enumerate(questions, start=1):
                question_key = f"{key_prefix}_q{idx}"
                selected = st.session_state[f"{key_prefix}_answers"].get(question_key)
                if selected == question["correct"]:
                    score += 1

            st.session_state[f"{key_prefix}_score"] = score
            st.session_state[f"{key_prefix}_submitted"] = True

    with col2:
        if st.button("Retry Quiz", key=f"{key_prefix}_retry"):
            st.session_state[f"{key_prefix}_submitted"] = False
            st.session_state[f"{key_prefix}_score"] = 0
            st.session_state[f"{key_prefix}_answers"] = {}

    # Feedback after submission
    if st.session_state.get(f"{key_prefix}_submitted"):
        score = st.session_state.get(f"{key_prefix}_score", 0)
        total = len(questions)
        percent = int(score / total * 100) if total else 0

        st.markdown(f"**Your score:** {score}/{total} ({percent}%)")
        st.progress(percent / 100)

        if percent >= 80:
            st.success("Excellent! You really know your minerals.")
        elif percent >= 50:
            st.info("Good job! A little more review will help you master this mineral.")
        else:
            st.warning("Keep trying — review the material and try again.")

        # Show explanations for each question
        for idx, question in enumerate(questions, start=1):
            question_key = f"{key_prefix}_q{idx}"
            selected = st.session_state[f"{key_prefix}_answers"].get(question_key)
            correct = question["correct"]
            is_correct = selected == correct

            if is_correct:
                st.success(f"✅ Question {idx}: Correct — {question['explanation']}")
            else:
                st.error(
                    f"❌ Question {idx}: Incorrect. Correct answer: {correct}. {question['explanation']}"
                )
