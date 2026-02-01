import streamlit as st
import google.generativeai as genai
import random

# API設定
genai.configure(api_key=st.secrets["api_key"])
model = genai.GenerativeModel('models/gemini-flash-latest')

# 日本語ラベルを変数に退避（1行を短くするため）
L_TITLE = "💃 武勇伝デデン"
L_STEP1 = "① キーワード入力"
L_STEP2 = "② 慎吾のオチを選択"
L_STEP3 = "③ あっちゃんの振りを選択"
L_GEN_O = "オチを20案出す"
L_GEN_F = "振りを20案出す"
L_FINISH = "完成！"
L_RETRY = "新しく作る"
L_BACK = "戻る"

st.set_page_config(page_title="武勇伝", page_icon="💃")

# CSS
st.markdown("<style>div[data-testid='stColumn'] > div > div > div > button {margin-top: 28px !important;} .ochi-box {background-color: #f0f2f6; padding: 15px; border-radius: 10px; border-left: 5px solid #ff4b4b; margin-bottom: 20px;}</style>", unsafe_allow_html=True)

st.title(L_TITLE)

if 'step' not in st.session_state:
    st.session_state.step = 1
if 'ochi_list' not in st.session_state:
    st.session_state.ochi_list = []
if 'furi_list' not in st.session_state:
    st.session_state.furi_list = []
if 'kw_value' not in st.session_state:
    st.session_state.kw_value = "空手"

# ランダムキーワード増量版
kws = ["空手", "浮気", "寝坊", "テスト", "料理", "合コン", "筋トレ", "サウナ", "遅刻", "婚活", "美容外科", "残業", "職質", "忘れ物", "推し活", "AI", "メタバース", "自撮り", "確定申告"]

# --- STEP 1 ---
if st.session_state.step == 1:
    st.subheader(L_STEP1)
    c1, c2 = st.columns([3, 1])
    with c1:
        kw = st.text_input("", value=st.session_state.kw_value)
    with c2:
        if st.button("ランダム"):
            st.session_state.kw_value = random.choice(kws)
            st.rerun()
    
    if st.button(L_GEN_O, use_container_width=True, type="primary"):
        with st.spinner("思考中..."):
            p = f"慎吾として「{kw}」のオチを20案。ひらがな、4/4/5、スラッシュ区切り。解説不要、データのみ。"
            try:
                res = model.generate_content(p)
                st.session_state.ochi_list = [l.strip() for l in res.text.split('\n') if '/' in l][:20]
                st.session_state.step = 2
                st.rerun()
            except Exception as e:
                st.error(f"ERR: {e}")

# --- STEP 2 ---
elif st.session_state.step == 2:
    st.subheader(L_STEP2)
    if st.session_state.ochi_list:
        sel_o = st.selectbox("案", st.session_state.ochi_list)
        st.session_state.final_ochi = st.text_input("修正", value=sel_o)
        c1, c2 = st.columns(2)
        with c1:
            if st.button(L_GEN_F, use_container_width=True, type="primary"):
                with st.spinner("思考中..."):
                    fp = f"中田として「{st.session_state.final_ochi}」への振りを20案。ひらがな、4/4/5、スラッシュ区切り。"
                    try:
                        res_f = model.generate_content(fp)
                        st.session_state.furi_list = [l.strip() for l in res_f.text.split('\n') if '/' in l][:20]
                        st.session_state.step = 3
                        st.rerun()
