import streamlit as st
import google.generativeai as genai
import random

# API設定
genai.configure(api_key=st.secrets["api_key"])
model = genai.GenerativeModel('models/gemini-flash-latest')

st.set_page_config(page_title="武勇伝", page_icon="💃")

# CSS
st.markdown("<style>div[data-testid='stColumn'] > div > div > div > button {margin-top: 28px !important;} .ochi-box {background-color: #f0f2f6; padding: 15px; border-radius: 10px; border-left: 5px solid #ff4b4b; margin-bottom: 20px;}</style>", unsafe_allow_html=True)

st.title("💃 武勇伝デデン")

# 初期化
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'ochi_list' not in st.session_state:
    st.session_state.ochi_list = []
if 'furi_list' not in st.session_state:
    st.session_state.furi_list = []
if 'kw_value' not in st.session_state:
    st.session_state.kw_value = "空手"

# ランダムキーワードを大幅増量（日常・ビジネス・珍事）
kws = [
    "空手", "浮気", "寝坊", "テスト", "料理", "合コン", "筋トレ", "サウナ", "遅刻",
    "ダイエット", "二日酔い", "二度寝", "自撮り", "婚活", "美容整外科", "宝くじ",
    "キャンプ", "デバッグ", "プレゼン", "残業", "領収書", "確定申告", "マザコン",
    "ゴミ拾い", "ナンパ", "スカウト", "行列", "ポイ活", "メルカリ", "親知らず",
    "職質", "忘れ物", "タワマン", "格安スマホ", "推し活", "AI", "メタバース"
]

# --- STEP 1: キーワード入力 ---
if st.session_state.step == 1:
    st.subheader("① キーワード入力")
    c1, c2 = st.columns([3, 1])
    with c1:
        # ご要望通りラベルを空（""）にしました
        kw = st.text_input("", value=st.session_state.kw_value)
    with c2:
        if st.button("ランダム"):
            st.session_state.kw_value = random.choice(kws)
            st.rerun()
    
    if st.button("オチを20案出す", use_container_width=True, type="primary"):
        with st.spinner("慎吾がリズムを刻んでいます..."):
            p = f"オリラジ慎吾として、キーワード「{kw}」の情けないオチを20案出せ。"
            p += "【厳守】1.ひらがなのみ 2.4/4/5のリズム 3.スラッシュ区切り "
            p += "4.解説、タイトル、凡例は一切禁止。データのみ20行出力せよ。"
            try:
                res = model.generate_content(p)
                lines = [l.strip() for l in res.text.split('\n') if '/' in l]
                st.session_state.ochi_list = lines[:20]
                st.session_state.step = 2
                st.rerun()
            except Exception as e:
                st.error(f"ERR: {e}")

# --- STEP 2: オチ選択 ---
elif st.session_state.step == 2:
    st.subheader("②
