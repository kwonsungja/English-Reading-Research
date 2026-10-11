import streamlit as st
import pandas as pd
from pathlib import Path
from gtts import gTTS
from io import BytesIO
import html
import re
import random

# =====================================================
# 1. Page Configuration
# =====================================================

st.set_page_config(
    page_title="Grade 2 Vocabulary Flashcards",
    page_icon="📗",
    layout="wide"
)

# =====================================================
# 2. CSS - Flashcard Design
# =====================================================

st.markdown("""
<style>

/* Sidebar */
section[data-testid="stSidebar"] a,
section[data-testid="stSidebar"] a span,
section[data-testid="stSidebar"] a p {
    font-size: 18px !important;
    font-weight: 500 !important;
}

/* Main Title */
.main-title {
    font-size: 32px;
    font-weight: 700;
    color: #2E7D32;
    margin-bottom: 10px;
}

/* Flashcard */
.flashcard {
    background-color: #E8F5E9;
    border: 2px solid #A5D6A7;
    border-radius: 16px;
    padding: 20px;
    min-height: 260px;
    text-align: center;
    box-shadow: 0 4px 8px rgba(0,0,0,0.08);
    margin-bottom: 10px;
    overflow-wrap: anywhere;
}

/* Front */
.card-front {
    font-size: 25px;
    font-weight: 700;
    color: #1B5E20;
    margin-top: 70px;
}

/* Back */
.card-word {
    font-size: 24px;
    font-weight: 700;
    color: #1B5E20;
    margin-bottom: 12px;
}

.card-meaning {
    font-size: 19px;
    color: #333;
    margin-bottom: 12px;
}

.card-definition {
    font-size: 17px;
    color: #444;
    margin-bottom: 12px;
    line-height: 1.6;
}

.card-example {
    font-size: 17px;
    color: #333;
    line-height: 1.6;
    margin-bottom: 10px;
}

.card-translation {
    font-size: 16px;
    color: #555;
    line-height: 1.6;
}

.highlight {
    color: #D32F2F;
    font-weight: 700;
}

/* Buttons */
div.stButton > button {
    font-size: 18px !important;
    min-height: 48px;
    border-radius: 10px;
}

/* Mobile */
@media (max-width: 768px) {

    .main-title {
        font-size: 26px;
    }

    .flashcard {
        min-height: 220px;
        padding: 15px;
    }

    .card-front {
        font-size: 22px;
        margin-top: 55px;
    }

    .card-word {
        font-size: 21px;
    }

    .card-meaning {
        font-size: 18px;
    }

    .card-definition,
    .card-example {
        font-size: 16px;
    }

    .card-translation {
        font-size: 15px;
    }
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# 3. Load CSV
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

CSV_PATH = (
    BASE_DIR
    / "data"
    / "miraen_english2_vocabulary_flashcards_L1-L5.csv"
)


@st.cache_data
def load_data():

    if not CSV_PATH.exists():
        st.error("Vocabulary CSV file not found.")
        st.stop()

    df = pd.read_csv(CSV_PATH, encoding="utf-8-sig")

    required_columns = [
        "lesson",
        "lesson_title",
        "word",
        "meaning",
        "english_definition",
        "example",
        "example_ko"
    ]

    missing = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing:
        st.error(f"Missing columns: {missing}")
        st.stop()

    df["lesson"] = pd.to_numeric(
        df["lesson"],
        errors="coerce"
    )

    df = df.dropna(subset=["lesson", "word"])

    df["lesson"] = df["lesson"].astype(int)

    text_columns = [
        "lesson_title",
        "word",
        "meaning",
        "english_definition",
        "example",
        "example_ko"
    ]

    for col in text_columns:
        df[col] = df[col].fillna("").astype(str)

    return df.reset_index(drop=True)


df = load_data()

# =====================================================
# 4. TTS
# =====================================================

@st.cache_data(show_spinner=False)
def generate_audio(text):

    audio = BytesIO()

    tts = gTTS(
        text=text,
        lang="en",
        tld="com"
    )

    tts.write_to_fp(audio)

    return audio.getvalue()


# =====================================================
# 5. Highlight Vocabulary in Example
# =====================================================

def highlight_word(sentence, word):

    safe_sentence = html.escape(sentence)

    if not word.strip():
        return safe_sentence

    safe_word = html.escape(word)

    pattern = re.compile(
        rf"(?<!\\w){re.escape(safe_word)}(?!\\w)",
        re.IGNORECASE
    )

    return pattern.sub(
        lambda match:
        f'<span class="highlight">{match.group(0)}</span>',
        safe_sentence
    )


# =====================================================
# 6. Session State
# =====================================================

if "flashcard_lesson" not in st.session_state:
    st.session_state.flashcard_lesson = None

if "flashcard_flipped" not in st.session_state:
    st.session_state.flashcard_flipped = {}

if "flashcard_favorites" not in st.session_state:
    st.session_state.flashcard_favorites = set()

if "flashcard_order" not in st.session_state:
    st.session_state.flashcard_order = []

if "flashcard_page" not in st.session_state:
    st.session_state.flashcard_page = 0


# =====================================================
# 7. Title
# =====================================================

st.markdown(
    '<div class="main-title">'
    '📗 Grade 2 MiraeN English II Vocabulary Flashcards'
    '</div>',
    unsafe_allow_html=True
)

st.write(
    "Learn vocabulary through interactive flashcards."
)

st.divider()

# =====================================================
# 8. Lesson Selection
# =====================================================

lesson_options = sorted(df["lesson"].unique())

lesson = st.selectbox(
    "📘 Select Lesson",
    options=lesson_options,
    index=None,
    placeholder="Choose Lesson 1–5",
    format_func=lambda x: f"Lesson {x}"
)

if lesson is None:
    st.info("Please select a lesson to begin.")
    st.stop()


lesson_df = df[
    df["lesson"] == lesson
].copy().reset_index(drop=True)

lesson_title = lesson_df["lesson_title"].iloc[0]

st.subheader(
    f"Lesson {lesson}: {lesson_title}"
)

# =====================================================
# 9. Reset State When Lesson Changes
# =====================================================

if st.session_state.flashcard_lesson != lesson:

    st.session_state.flashcard_lesson = lesson

    st.session_state.flashcard_flipped = {}

    st.session_state.flashcard_order = list(
        range(len(lesson_df))
    )

    st.session_state.flashcard_page = 0


# =====================================================
# 10. Learning Controls
# =====================================================

total_words = len(lesson_df)

st.write(f"📚 Total Vocabulary: **{total_words} words**")

control1, control2, control3 = st.columns(3)

with control1:

    if st.button(
        "🔀 Shuffle Cards",
        use_container_width=True
    ):

        random.shuffle(
            st.session_state.flashcard_order
        )

        st.session_state.flashcard_page = 0
        st.session_state.flashcard_flipped = {}

        st.rerun()


with control2:

    if st.button(
        "🔄 Reset Cards",
        use_container_width=True
    ):

        st.session_state.flashcard_order = list(
            range(total_words)
        )

        st.session_state.flashcard_page = 0
        st.session_state.flashcard_flipped = {}

        st.rerun()


with control3:

    favorites_only = st.toggle(
        "⭐ Favorites Only",
        value=False
    )


# =====================================================
# 11. Filter Cards
# =====================================================

order = st.session_state.flashcard_order.copy()

if favorites_only:

    order = [
        i for i in order
        if (lesson, lesson_df.iloc[i]["word"])
        in st.session_state.flashcard_favorites
    ]


if not order:

    st.info("No flashcards available.")
    st.stop()


# =====================================================
# 12. Pagination
# =====================================================

CARDS_PER_PAGE = 12

total_pages = (
    len(order) + CARDS_PER_PAGE - 1
) // CARDS_PER_PAGE

if st.session_state.flashcard_page >= total_pages:
    st.session_state.flashcard_page = 0

page = st.session_state.flashcard_page

start = page * CARDS_PER_PAGE
end = start + CARDS_PER_PAGE

current_cards = order[start:end]

st.write(
    f"Page **{page + 1} / {total_pages}**"
)

st.progress(
    min((page + 1) / total_pages, 1.0)
)

st.divider()

# =====================================================
# 13. Display Flashcards
# =====================================================

# Streamlit columns: 4 cards per row

for row_start in range(0, len(current_cards), 4):

    row_indices = current_cards[
        row_start:row_start + 4
    ]

    cols = st.columns(
        len(row_indices)
    )

    for col, card_index in zip(cols, row_indices):

        row = lesson_df.iloc[card_index]

        word = row["word"]
        meaning = row["meaning"]
        definition = row["english_definition"]
        example = row["example"]
        example_ko = row["example_ko"]

        card_key = f"{lesson}_{card_index}"

        flipped = st.session_state.flashcard_flipped.get(
            card_key,
            False
        )

        favorite_key = (lesson, word)

        with col:

            # ---------------------------------
            # Card Front / Back
            # ---------------------------------

            if not flipped:

                card_html = f"""
                <div class="flashcard">
                    <div class="card-front">
                        {html.escape(word)}
                    </div>
                </div>
                """

            else:

                highlighted_example = highlight_word(
                    example,
                    word
                )

                card_html = f"""
                <div class="flashcard">

                    <div class="card-word">
                        {html.escape(word)}
                    </div>

                    <div class="card-meaning">
                        {html.escape(meaning)}
                    </div>

                    <div class="card-definition">
                        <b>Definition</b><br>
                        {html.escape(definition)}
                    </div>

                    <div class="card-example">
                        <b>Example</b><br>
                        {highlighted_example}
                    </div>

                    <div class="card-translation">
                        {html.escape(example_ko)}
                    </div>

                </div>
                """

            st.markdown(
                card_html,
                unsafe_allow_html=True
            )

            # ---------------------------------
            # Flip Button
            # ---------------------------------

            if st.button(
                "🔄 Flip Card",
                key=f"flip_{card_key}",
                use_container_width=True
            ):

                st.session_state.flashcard_flipped[
                    card_key
                ] = not flipped

                st.rerun()

            # ---------------------------------
            # Favorite Button
            # ---------------------------------

            is_favorite = (
                favorite_key
                in st.session_state.flashcard_favorites
            )

            star_label = (
                "⭐ Saved"
                if is_favorite
                else "☆ Favorite"
            )

            if st.button(
                star_label,
                key=f"favorite_{card_key}",
                use_container_width=True
            ):

                if is_favorite:

                    st.session_state.flashcard_favorites.remove(
                        favorite_key
                    )

                else:

                    st.session_state.flashcard_favorites.add(
                        favorite_key
                    )

                st.rerun()

            # ---------------------------------
            # Pronunciation
            # ---------------------------------

            with st.expander("🔊 Pronunciation"):

                if st.button(
                    "▶ Play",
                    key=f"audio_button_{card_key}",
                    use_container_width=True
                ):

                    try:

                        audio_bytes = generate_audio(word)

                        st.audio(
                            audio_bytes,
                            format="audio/mp3"
                        )

                    except Exception:

                        st.warning(
                            "Audio is temporarily unavailable."
                        )

    st.write("")


# =====================================================
# 14. Page Navigation
# =====================================================

st.divider()

nav1, nav2, nav3 = st.columns([1, 2, 1])

with nav1:

    if st.button(
        "⬅ Previous",
        disabled=(page == 0),
        use_container_width=True
    ):

        st.session_state.flashcard_page -= 1

        st.rerun()


with nav2:

    st.markdown(
        f"""
        <div style="
            text-align:center;
            font-size:20px;
            padding-top:10px;
        ">
        {page + 1} / {total_pages}
        </div>
        """,
        unsafe_allow_html=True
    )


with nav3:

    if st.button(
        "Next ➡",
        disabled=(page >= total_pages - 1),
        use_container_width=True
    ):

        st.session_state.flashcard_page += 1

        st.rerun()


# =====================================================
# 15. Learning Summary
# =====================================================

st.divider()

favorite_count = sum(
    1
    for item in st.session_state.flashcard_favorites
    if item[0] == lesson
)

st.success(
    f"⭐ Saved Vocabulary: {favorite_count} words"
)

st.caption(
    "English Opens Your World | "
    "Grade 2 MiraeN English II Vocabulary Learning"
)
