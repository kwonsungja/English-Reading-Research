import streamlit as st
import pandas as pd
import random
from pathlib import Path

# ==========================================
# Grade 2 Collocations App
# ==========================================

# ---------- Page Config ----------
st.set_page_config(
    page_title="Grade 2 Collocations",
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

/* Sidebar menu text */
section[data-testid="stSidebar"] a,
section[data-testid="stSidebar"] a span,
section[data-testid="stSidebar"] a p {
    font-size: 18px !important;
    font-weight: 500 !important;
}

/* 메뉴 선택 라벨 */
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

.collocation-word {
    font-size: 26px;
    font-weight: 800;
    color: #1565c0;
}

.meaning-text {
    font-size: 19px;
    color: #222;
    margin-top: 6px;
}

.example-text {
    font-size: 17px;
    color: #444;
    margin-top: 8px;
}

.tip-text {
    font-size: 16px;
    color: #666;
