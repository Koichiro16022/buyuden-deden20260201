import streamlit as st
import google.generativeai as genai
import random

# API設定
genai.configure(api_key=st.secrets["api_key"])
model = genai.GenerativeModel('models/gemini-flash-latest')

st.set_page_config(page_title="武勇伝デデン", page_icon="💃")

# CSS
st.markdown("<style>div[data-testid='stColumn'] > div > div > div > button {margin-top: 28px !important;} .ochi-display {background-color: #f0f2f6; padding: 15px; border-radius: 10px; border-left: 5px solid #ff4b4b; margin-bottom: 20px;}</style>", unsafe_allow_html=True)

st.title("💃 武勇伝デデン")

if 'step' not in st.session_state:
    st.session_state.step = 1
if 'ochi_list' not in st.session_state:
    st.session_state.ochi_list = []
if 'furi_list' not in st.session_state:
    st.session_state.furi_list = []
if 'kw_value' not in st.session_state:
    st.session_state.kw_value = "空手"
if 'final_ochi' not in st.session_state:
    st.session_state.final_ochi = ""

random_kws = ["空手", "浮気", "寝坊", "テスト", "料理", "合コン", "筋トレ", "キャンプ", "遅刻", "ダイエット", "プログラミング", "デバッグ", "プレゼン", "飲み会", "二度寝"]

# --- STEP 1 ---
if st.session_state.step == 1:
    st.subheader("① 設定とキーワード")
    target = st.selectbox("誰向けの武勇伝にしますか？", ["一般", "エンジニア", "経理", "営業", "品質管理"])
    col_kw, col_rnd = st.columns([3, 1])
    with col_kw:
        kw = st.text_input("キーワード", value=st.session_state.kw_value)
    with col_rnd:
        if st.button("ランダム", use_container_width=True):
            st.session_state.kw_value = random.choice(random_kws)
            st.rerun()
    
    if st.button("オチを20案出す", use_container_width=True, type="primary"):
        with st.spinner("思考中..."):
            try:
                p = f"キーワード「{kw}」を使って、"
                p += f"{target}向けの情けないオチを20案出せ。"
                p += "ルール：1.ひらがなのみ。2.「4/4/5」のリズム。"
                p += "3.スラッシュで区切り。4.リストのみ出力。"
                res = model.generate_content(p)
                st.session_state.ochi_list = [l.strip() for l in res.text.strip().split('\n') if l.strip()]
                st.session_state.step = 2
                st.rerun()
