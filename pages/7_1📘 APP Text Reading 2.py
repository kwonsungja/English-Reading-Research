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

