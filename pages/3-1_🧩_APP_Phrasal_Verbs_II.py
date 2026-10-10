import streamlit as st
import pandas as pd
import random
from pathlib import Path

# ==========================================
# Grade 2 MiraeN English II Phrasal Verbs App
# ==========================================

st.set_page_config(
    page_title="Grade 2 Phrasal Verbs",
    page_icon="📘",
    layout="wide"
)

# ---------- Style ----------
st.markdown("""
<style>

/* 전체 기본 글자 */
html, body, [class*="css"] {
    font-size: 17px;
}

/* radio 문제 + 선택지 글자 */
div[data-testid="stRadio"] label p,
div[role="radiogroup"] label p {
    font-size: 18px !important;
    font-weight: 500 !important;
}

/* Sidebar menu text */
section[data-testid="stSidebar"] a,
section[data-testid="stSidebar"] a span,
section[data-testid="stSidebar"] a p {
    font-size: 18px !important;
    font-weight: 500 !important;
}

div[data-testid="stRadio"] > label {
    font-size: 24px !important;
    font-weight: 700 !important;
}

/* 라디오 선택지 글자 */
div[role="radiogroup"] label p {
    font-size: 22px !important;
    font-weight: 500 !important;
}

/* selectbox, slider 라벨 */
label p {
    font-size: 19px !important;
    font-weight: 600 !important;
}

.main-title {
    font-size: 34px;
    font-weight: 800;
    color: #ff6b35;
}

.sub-text {
    font-size: 17px;
    color: #555;
}

.word-card {
    background-color: #fff7f0;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #ffd2b8;
    margin-bottom: 14px;
}

.guided-card {
    background-color: #f3f8ff;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #cfe3ff;
    margin-bottom: 14px;
}

.review-card {
    background-color: #f7fff4;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #cdebc3;
    margin-bottom: 14px;
}

.phrasal-word {
    font-size: 26px;
    font-weight: 800;
    color: #e85d04;
}
