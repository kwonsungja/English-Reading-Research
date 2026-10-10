import html
from io import BytesIO
from pathlib import Path

import pandas as pd
import streamlit as st
from gtts import gTTS

st.set_page_config(page_title="APP Text Reading 2", page_icon="📘", layout="wide")

st.markdown("""
<style>
section[data-testid="stSidebar"] a,
section[data-testid="stSidebar"] a span,
section[data-testid="stSidebar"] a p {font-size:18px !important;font-weight:500 !important;}
.reading-text {font-size:21px !important;line-height:1.9 !important;color:#333 !important;}
.reading-text p {margin-bottom:18px !important;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<h1 style="text-align:center;font-size:36px;margin-bottom:5px;">📘 APP Text Reading 2</h1>
<p style="text-align:center;font-size:18px;color:#555;">미래엔 영어Ⅱ · Main Reading &amp; Read More<br>
Vocabulary → Textbook Reading → Reading Expansion</p>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    csv_path = Path(__file__).resolve().parents[1] / "data" / "english2_reading_full.csv"
    if not csv_path.is_file():
        st.error(f"CSV 파일을 찾을 수 없습니다: {csv_path}")
        st.stop()
    df = pd.read_csv(csv_path, encoding="utf-8-sig").fillna("")
    df.columns = df.columns.str.strip()
    required = {"lesson", "title", "full_text", "further_reading_title", "further_reading_text"}
    missing = required - set(df.columns)
    if missing:
        st.error(f"CSV 필수 열이 없습니다: {', '.join(sorted(missing))}")
        st.stop()
    return df

def render_text(value):
    """Show source paragraphs safely while preserving line breaks."""
    paragraphs = [p.strip() for p in str(value).replace("\r\n", "\n").split("\n\n") if p.strip()]
    body = "".join(f"<p>{html.escape(p).replace(chr(10), '<br>')}</p>" for p in paragraphs)
    st.markdown(f'<div class="reading-text">{body}</div>', unsafe_allow_html=True)

def audio_section(text, button_label, state_key):
    if st.button(button_label, key=f"generate_{state_key}"):
        try:
            with st.spinner("Generating audio..."):
                audio = BytesIO()
                gTTS(text=str(text), lang="en", tld="com").write_to_fp(audio)
                st.session_state[f"audio_{state_key}"] = audio.getvalue()
        except Exception as exc:
            st.error("Audio generation failed. 인터넷 연결을 확인해 주세요.")
            st.caption(str(exc))
    if f"audio_{state_key}" in st.session_state:
        st.audio(st.session_state[f"audio_{state_key}"], format="audio/mp3")

st.header("⚙ Reading Options")
df = load_data()
selected_lesson = st.selectbox("Lesson 선택", df["lesson"].tolist(), index=None, placeholder="Lesson을 선택하세요")
if not selected_lesson:
    st.info("학습할 Lesson을 선택해 주세요.")
    st.stop()

row = df.loc[df["lesson"] == selected_lesson].iloc[0]
lesson_key = str(selected_lesson)
st.markdown(f"## 미래엔 영어Ⅱ · {html.escape(lesson_key)}")
if "lesson_title" in row and str(row["lesson_title"]).strip():
    st.markdown(f"**{row['lesson_title']}**")
st.markdown(f"### {row['title']}")

# These activities appear only after their content is added to the CSV.
if "summary" in row and str(row["summary"]).strip():
    st.subheader("📝 Summary")
    st.info(row["summary"])
if "key_expressions" in row and str(row["key_expressions"]).strip():
    st.subheader("🔑 Key Expressions")
    expressions = [x.strip() for x in str(row["key_expressions"]).split(";") if x.strip()]
    columns = st.columns(2)
    for i, exp in enumerate(expressions):
        columns[i % 2].markdown(f"• {html.escape(exp)}")

st.subheader("📖 Textbook Reading Text")
with st.expander("본문 텍스트 보기"):
    render_text(row["full_text"])
st.markdown("### 🔊 Listen to the Text")
audio_section(row["full_text"], "🎧 Generate American English Audio", f"main_{lesson_key}")

st.subheader("📚 Further Reading")
st.markdown(f"### {row['further_reading_title']}")
with st.expander("Read Further"):
    render_text(row["further_reading_text"])
st.markdown("### 🔊 Listen to the Further Reading")
audio_section(row["further_reading_text"], "🎧 Generate Further Reading Audio", f"more_{lesson_key}")

if "reading_task" in row and str(row["reading_task"]).strip():
    st.subheader("🎯 Reading Task")
    st.success(row["reading_task"])
if "quiz" in row and str(row["quiz"]).strip():
    st.subheader("❓ Comprehension Quiz")
    st.markdown(f"**Q. {row['quiz']}**")
    user_answer = st.text_input("Your answer", key=f"answer_{lesson_key}")
    if st.button("Check Answer", key=f"check_{lesson_key}"):
        answer = str(row.get("answer", "")).strip()
        if not user_answer.strip():
            st.warning("답을 입력해 주세요.")
        elif not answer:
            st.info("아직 모범 답안이 등록되지 않았습니다.")
        elif user_answer.casefold().strip() == answer.casefold():
            st.success("Good job!")
        else:
            st.info("Suggested answer: " + answer)

st.subheader("💬 Reflection")
reflection = st.text_area("오늘 본문에서 새롭게 배운 표현이나 내용을 적어보세요.", height=120, key=f"reflection_{lesson_key}")
if reflection.strip():
    st.success("좋아요. 본문 읽기와 어휘 학습이 잘 연결되고 있어요.")
