import streamlit as st
import google.generativeai as genai
import random

# API/Model設定
genai.configure(api_key=st.secrets["api_key"])
model = genai.GenerativeModel('models/gemini-flash-latest')

# --- すべての日本語を変数化（断線防止） ---
L_TITLE = "💃 武勇伝デデン"
L_STEP1 = "① キーワード入力"
L_STEP2 = "② 慎吾のオチを選択"
L_STEP3 = "③ あっちゃんの振りを選択"
L_GEN_O = "オチを20案出す"
L_GEN_F = "振りを20案出す"
L_FINISH = "完成！"
L_RETRY = "新しく作る"
L_BACK = "戻る"
L_MSG = "＼ デデンデンデンデン！ ／"

# AIへの命令文（1行を極限まで短く分割）
P_O_BASE = "慎吾として「"
P_O_RULE = "」のオチ20案。ひらがな、4/4/5、スラッシュ区切り。"
P_F_BASE = "中田として「"
P_F_RULE = "」への振り20案。ひらがな、4/4/5、スラッシュ区切り。"

st.set_page_config(page_title="武勇伝", page_icon="💃")
st.markdown("<style>.ochi-box {background:#f0f2f6; padding:15px; border-radius:10px; border-left:5px solid #ff4b4b; margin-bottom:20px;}</style>", unsafe_allow_html=True)
st.title(L_TITLE)

# セッション初期化
if 'step' not in st.session_state: st.session_state.step = 1
if 'ochi_list' not in st.session_state: st.session_state.ochi_list = []
if 'furi_list' not in st.session_state: st.session_state.furi_list = []
if 'kw' not in st.session_state: st.session_state.kw = "空手"

kws = ["空手", "浮気", "寝坊", "テスト", "料理", "合コン", "筋トレ", "サウナ", "遅刻", "職質", "確定申告", "推し活"]

# --- STEP 1 ---
if st.session_state.step == 1:
    st.subheader(L_STEP1)
    c1, c2 = st.columns([3, 1], vertical_alignment="bottom")
    with c1: val = st.text_input("", value=st.session_state.kw)
    with c2: 
        if st.button("ランダム", use_container_width=True):
            st.session_state.kw = random.choice(kws)
            st.rerun()
    if st.button(L_GEN_O, use_container_width=True, type="primary"):
        prompt = P_O_BASE + val + P_O_RULE
        try:
            r = model.generate_content(prompt)
            st.session_state.ochi_list = [l.strip() for l in r.text.split('\n') if '/' in l][:20]
            st.session_state.step = 2
            st.rerun()
        except Exception as e: st.error(f"ERR: {e}")

# --- STEP 2 ---
elif st.session_state.step == 2:
    st.subheader(L_STEP2)
    if st.session_state.ochi_list:
        sel = st.selectbox("案", st.session_state.ochi_list)
        st.session_state.f_ochi = st.text_input("修正", value=sel)
        if st.button(L_GEN_F, use_container_width=True, type="primary"):
            prompt_f = P_F_BASE + st.session_
