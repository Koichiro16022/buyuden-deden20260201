import streamlit as st
import google.generativeai as genai
import random

# API設定
genai.configure(api_key=st.secrets["api_key"])
model = genai.GenerativeModel('models/gemini-flash-latest')

# 定数定義
T1 = "① キーワード入力"
T2 = "② 慎吾のオチを選択"
T3 = "③ あっちゃんの振りを選択"

st.set_page_config(page_title="武勇伝", page_icon="💃")
st.markdown("<style>div[data-testid='stColumn'] > div > div > div > button {margin-top: 28px !important;} .ochi-box {background-color: #f0f2f6; padding: 15px; border-radius: 10px; border-left: 5px solid #ff4b4b; margin-bottom: 20px;}</style>", unsafe_allow_html=True)
st.title("💃 武勇伝デデン")

if 'step' not in st.session_state: st.session_state.step = 1
if 'ochi_list' not in st.session_state: st.session_state.ochi_list = []
if 'furi_list' not in st.session_state: st.session_state.furi_list = []
if 'kw_value' not in st.session_state: st.session_state.kw_value = "空手"

kws = ["空手", "浮気", "寝坊", "テスト", "料理", "合コン", "筋トレ", "サウナ", "遅刻", "職質", "忘れ物", "確定申告"]

# --- STEP 1 ---
if st.session_state.step == 1:
    st.subheader(T1)
    c1, c2 = st.columns([3, 1])
    with c1:
        kw = st.text_input("", value=st.session_state.kw_value)
    with c2:
        if st.button("ランダム"):
            st.session_state.kw_value = random.choice(kws)
            st.rerun()
    
    if st.button("オチを20案出す", use_container_width=True, type="primary"):
        p = f"慎吾として「{kw}」のオチを20案。ひらがな、4/4/5、スラッシュ区切り。解説不要。"
        with st.spinner("思考中..."):
            try:
                res =
