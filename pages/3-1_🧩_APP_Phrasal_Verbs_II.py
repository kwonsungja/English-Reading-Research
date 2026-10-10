            st.markdown(
                f"""
                <div class="guided-card">
                    <div class="phrasal-word">Q{i}. {item['phrasal_verb']}</div>
                    <div class="example-text">예문: {item['example_sentence']}</div>
                    <div class="tip-text">💡 Hint: {item['learning_tip']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            answer = st.radio(
                "💡 뜻을 고르세요.",
                item["options"],
                index=None,
                key=f"phrasal2_guided_{st.session_state.get('phrasal2_guided_round', 0)}_{i}"
            )

            answers.append((item, answer))
            
        if st.button("Guided Practice 확인"):

            score = 0

            for item, answer in answers:

                if answer == item["korean_meaning"]:
                    score += 1
                    st.success(
                        f"정답입니다: {item['phrasal_verb']} = {item['korean_meaning']}"
                    )
                else:
                    st.warning(
                        f"다시 확인해 보세요. {item['phrasal_verb']}의 뜻은 '{item['korean_meaning']}'입니다."
                    )

            if score == len(answers):
                st.success("🎉 Perfect Score!")
                st.balloons()
        
# ==========================================
# 3. Practice Check
# ==========================================
elif mode == "✅ Practice Check":

    st.subheader("✅ Practice Check")
    st.info("목표: 힌트 없이 스스로 구동사의 의미를 확인합니다.")

    if filtered_df.empty:
        st.warning("선택한 조건에 해당하는 표현이 없습니다.")
        st.stop()

    quiz_size = st.selectbox(
        "문항 수",
        [5, 10, 15, 20],
        index=1
    )

    if st.button("새 Practice Check 시작"):

        quiz_items = filtered_df.sample(
            min(quiz_size, len(filtered_df)),
            random_state=random.randint(1, 100000)
        ).to_dict("records")

        for item in quiz_items:

            correct = item["korean_meaning"]

            other_pool = df[
                df["korean_meaning"] != correct
            ]["korean_meaning"].dropna().unique().tolist()

            other_options = random.sample(
                other_pool,
                min(3, len(other_pool))
            )

            options = other_options + [correct]
            random.shuffle(options)

            item["options"] = options

        st.session_state.phrasal2_quiz_items = quiz_items
        st.session_state.phrasal2_check_round = st.session_state.get("phrasal2_check_round", 0) + 1

    if st.session_state.phrasal2_quiz_items:

        answers = []

        for i, item in enumerate(st.session_state.phrasal2_quiz_items, start=1):

            st.markdown(f"### Q{i}. {item['phrasal_verb']}")
            st.caption(
                f"{item['section']} / {item['textbook']} / Lesson {int(float(item['lesson']))}"
            )

            answer = st.radio(
                "💡 뜻을 고르세요.",
                item["options"],
                index=None,
                key=f"phrasal2_check_{st.session_state.get('phrasal2_check_round', 0)}_{i}"
            )

            answers.append((item, answer))

        if st.button("Practice Check 제출"):

            score = 0

            for item, answer in answers:

                correct = item["korean_meaning"]

                if answer == correct:
                    score += 1
                    st.success(f"정답: {item['phrasal_verb']} = {correct}")
                else:
                    st.error(f"오답: {item['phrasal_verb']} = {correct}")
                    st.write(f"예문: {item['example_sentence']}")
                    st.write(f"학습 팁: {item['learning_tip']}")

                    if item not in st.session_state.phrasal2_wrong_items:
                        st.session_state.phrasal2_wrong_items.append(item)

            st.subheader(f"점수: {score} / {len(answers)}")
            
            if score == len(answers):
                st.success("🎉 Perfect Score!")
                st.balloons() 

# ==========================================
# 4. Review
# ==========================================
else:

    st.subheader("🔁 Review")
    st.info("목표: Practice Check에서 틀린 표현을 다시 보고 장기 기억으로 연결합니다.")

    if not st.session_state.phrasal2_wrong_items:

        st.success("아직 오답이 없습니다. Practice Check를 먼저 풀어 보세요.")

    else:

        st.write(
            f"현재 오답 표현 수: **{len(st.session_state.phrasal2_wrong_items)}개**"
        )

        for item in st.session_state.phrasal2_wrong_items:

            st.markdown(
                f"""
                <div class="review-card">
                    <div class="phrasal-word">{item['phrasal_verb']}</div>
                    <div class="meaning-text">뜻: {item['korean_meaning']}</div>
                    <div class="example-text">예문: {item['example_sentence']}</div>
                    <div class="tip-text">💡 학습 팁: {item['learning_tip']}</div>
                </div>
                """,
