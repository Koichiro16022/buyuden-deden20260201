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

kws = ["空手", "浮気", "寝坊", "テスト", "料理", "合コン", "筋トレ", "サウナ", "遅刻"]

# --- STEP 1 ---
if st.session_state.step == 1:
    st.subheader("① キーワード入力")
    target = st.selectbox("誰向け？", ["エンジニア", "経理", "営業", "品質管理"])
    c1, c2 = st.columns([3, 1])
    with c1:
        kw = st.text_input("ネタの種", value=st.session_state.kw_value)
    with c2:
        if st.button("ランダム"):
            st.session_state.kw_value = random.choice(kws)
            st.rerun()
    
    if st.button("オチを出す", use_container_width=True, type="primary"):
        with st.spinner("思考中..."):
            p = f"{kw}の{target}向けオチを20案。ひらがな、4/4/5、スラッシュ区切り。"
            try:
                res = model.generate_content(p)
                st.session_state.ochi_list = [l.strip() for l in res.text.split('\n') if l.strip()]
                st.session_state.step = 2
                st.rerun()
            except Exception as e:
                st.error(f"ERR: {e}")

# --- STEP 2 ---
elif st.session_state.step == 2:
    st.subheader("② 慎吾のオチを選択")
    if st.session_state.ochi_list:
        sel_o = st.selectbox("案を選択", st.session_state.ochi_list)
        st.session_state.final_ochi = st.text_input("修正", value=sel_o)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("振りを出す", use_container_width=True, type="primary"):
                with st.spinner("思考中..."):
                    fp = f"オチ「{st.session_state.final_ochi}」への強気な振りを20案。ひらがな、4/4/5。"
                    try:
                        res_f = model.generate_content(fp)
                        st.session_state.furi_list = [l.strip() for l in res_f.text.split('\n') if l.strip()]
                        st.session_state.step = 3
                        st.rerun()
                    except Exception as e:
                        st.error(f"ERR: {e}")
        with c2:
            if st.button("戻る", use_container_width=True):
                st.session_state.step = 1
                st.rerun()

# --- STEP 3 ---
elif st.session_state.step == 3:
    st.markdown(f'<div class="ochi-box">し：すごい！ {st.session_state.final_ochi}</div>', unsafe_allow_html=True)
    st.subheader("③ あっちゃんの振りを選択")
